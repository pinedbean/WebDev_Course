*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.5 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We add observability and a hardening pass across both halves. New/changed files:

```text
backend/app/
├── logging_config.py     (new: JSON formatter + setup)
├── middleware.py         (new: request-id + request log)
├── ratelimit.py          (new: tiny login limiter)
├── main.py               (wire logging, middleware, health/ready, error handler)
├── schemas.py            (tighten validation)
└── routers/auth.py       (apply rate limit)
frontend/src/
├── components/ErrorBoundary.jsx   (new)
├── main.jsx              (wrap App)
└── api/client.js         (surface X-Request-ID)
```

### 1 JSON logging

```python
# app/logging_config.py
import json, logging
from datetime import datetime, timezone

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "level": record.levelname,
            "msg": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "extra_fields"):
            payload.update(record.extra_fields)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def configure_logging(level: str = "INFO"):
    handler = logging.StreamHandler()          # stdout
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    # quiet uvicorn's default access logs (we log requests ourselves)
    logging.getLogger("uvicorn.access").handlers = []
```

### 2 Request-ID + request-log middleware

```python
# app/middleware.py
import time, uuid, logging
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger("taskflow.request")

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start) * 1000, 1)
            log.exception("request_failed", extra={"extra_fields": {
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": duration_ms,
            }})
            raise
        duration_ms = round((time.perf_counter() - start) * 1000, 1)
        log.info("request", extra={"extra_fields": {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
        }})
        response.headers["X-Request-ID"] = request_id
        return response
```

### 3 A tiny login rate limiter

```python
# app/ratelimit.py
import time
from collections import defaultdict
from fastapi import Request, HTTPException

# NOTE: in-memory = per-process. Fine for the MVP; use Redis when you scale
# to multiple replicas (10.6). Documented in the README security notes.
_hits: dict[str, list[float]] = defaultdict(list)
WINDOW_SEC = 60
MAX_ATTEMPTS = 10

def rate_limit_login(request: Request):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    _hits[ip] = [t for t in _hits[ip] if now - t < WINDOW_SEC]
    if len(_hits[ip]) >= MAX_ATTEMPTS:
        raise HTTPException(429, "Too many login attempts, slow down")
    _hits[ip].append(now)
```

Apply it as a dependency on the login route:

```python
# app/routers/auth.py  (add to the login signature)
from app.ratelimit import rate_limit_login

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db),
          _: None = Depends(rate_limit_login)):
    ...
```

### 4 Tighten validation

```python
# app/schemas.py  (changes)
from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=80)

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=2000)

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=4000)
    status: Status = "todo"
    assignee_id: int | None = None
    due_date: date | None = None
```

> **📝 Validate at the edge**
>
> With these constraints, a 1-char password or a 10,000-char title is rejected with a clear 422 before it ever reaches your DB. Cheap, automatic, and it shrinks your attack surface.

### 5 Wire it all in `main.py`

```python
# app/main.py
import os, logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.logging_config import configure_logging
from app.middleware import RequestContextMiddleware
from app.database import get_db
from app.routers import auth, projects, members, tasks

configure_logging(os.getenv("LOG_LEVEL", "INFO"))
log = logging.getLogger("taskflow")

# fail fast if the secret is missing in production
if os.getenv("ENV") == "production" and not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY must be set in production")

app = FastAPI(title="TaskFlow API", version="0.5.0")

# CORS origins from env (comma-separated), default to the dev frontend
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],     # let the browser read it
)
app.add_middleware(RequestContextMiddleware)

app.include_router(auth.router,     prefix="/api/v1/auth",     tags=["auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(members.router,  prefix="/api/v1/projects", tags=["members"])
app.include_router(tasks.router,    prefix="/api/v1/projects", tags=["tasks"])

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/health/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(503, "database unavailable")
    return {"status": "ready"}

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", "-")
    log.error("unhandled_exception",
              extra={"extra_fields": {"request_id": rid,
                                      "path": request.url.path}},
              exc_info=exc)
    return JSONResponse(status_code=500,
        content={"detail": "Internal server error", "request_id": rid})
```

Restart uvicorn and watch the logs — you should see JSON lines like:

```json
{"ts":"2026-06-26T09:14:02+00:00","level":"INFO","msg":"request",
 "logger":"taskflow.request","request_id":"7f3a9c1b22e1","method":"GET",
 "path":"/api/v1/projects","status":200,"duration_ms":3.2}
```

Sanity-check the health routes:

```bash
curl -i http://localhost:8000/api/v1/health        # 200 {"status":"ok"} + X-Request-ID header
curl http://localhost:8000/api/v1/health/ready     # {"status":"ready"}
```

### 6 React error boundary

```python
// src/components/ErrorBoundary.jsx
import { Component } from "react";

export default class ErrorBoundary extends Component {
  state = { error: null };
  static getDerivedStateFromError(error) { return { error }; }
  componentDidCatch(error, info) {
    console.error("UI crash:", error, info);
    // stretch: POST to /api/v1/client-errors here
  }
  render() {
    if (this.state.error) {
      return (
        <div style={{ padding: 40, textAlign: "center" }}>
          <h1>Something went wrong</h1>
          <p>Please reload the page. If it keeps happening, contact support.</p>
          <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

```python
// src/main.jsx  (wrap App)
import ErrorBoundary from "./components/ErrorBoundary";
// ...
<React.StrictMode>
  <ErrorBoundary>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </ErrorBoundary>
</React.StrictMode>
```

### 7 Surface the request id in the client

```javascript
// src/api/client.js  (update the error branch)
const res = await fetch(`${BASE}${path}`, { method, headers, body: payload });
const requestId = res.headers.get("X-Request-ID");
if (res.status === 204) return null;
const data = await res.json().catch(() => ({}));
if (!res.ok) {
  const ref = requestId ? ` (ref ${requestId})` : "";
  throw new Error((data.detail || `Request failed (${res.status})`) + ref);
}
return data;
```

Now a failure shows e.g. `You do not have access to this project (ref 7f3a9c1b22e1)`, and that id appears in your backend logs.

### 8 Test the failure paths & document

Temporarily add a route that raises, hit it, and confirm: the response is `{"detail":"Internal server error","request_id":"..."}` (no traceback), and the logs contain an `"unhandled_exception"` line with the same id and the full `exc`. Then remove the test route. To test the boundary, throw inside a component's render and confirm the fallback shows.

Add a **Security notes** section to the README:

```
## Security notes
- Passwords bcrypt-hashed (passlib); never stored or logged in plaintext.
- JWT access tokens, 30-min expiry; SECRET_KEY from env (required in prod).
- CORS restricted to known origins via CORS_ORIGINS env var.
- Input validated by Pydantic (lengths, email, status enum).
- Login rate-limited (per-IP, in-memory MVP -> move to Redis when scaling).
- Errors return a generic message + request id; details logged server-side only.
- Token in localStorage (XSS trade-off): no dangerouslySetInnerHTML; React escapes output.
- Next steps: refresh tokens, httpOnly-cookie option, security headers via Nginx,
  per-user rate limits, audit logging.
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Logs still plain text | Call `configure_logging()` *before* creating the app, and clear `uvicorn.access` handlers. |
| Frontend can't read `X-Request-ID` | Add it to `expose_headers` in the CORS middleware. |
| 500 handler not firing | FastAPI handles `HTTPException` separately; the `Exception` handler only catches *unhandled* errors. Raise a plain `ValueError` to test. |
| Error boundary doesn't catch | Boundaries catch render errors, not event-handler/async errors. Throw in render to test. |
| 429 during normal use | You set the login limit too low or are hammering it. Adjust `MAX_ATTEMPTS`/`WINDOW_SEC`. |

## 🎉 Done — what's next

TaskFlow is now observable and hardened: every request is logged as JSON with a traceable id, health checks are ready for a load balancer, errors fail safely on both ends, and you've run (and documented) a real security pass.

- ✅ Structured logs + request IDs + health/ready.
- ✅ Global exception handler + React error boundary.
- ✅ Validation + CORS/secrets/rate-limit hardening, documented.

**Up next → Chunk 10.6: Containerize, Load-Balance & Deploy.** The finale — Docker for both halves, Nginx load balancing across replicas, a CI workflow, and a polished README. Your health checks and stateless JWT are exactly what makes that scale.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
