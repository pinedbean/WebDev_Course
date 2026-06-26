*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.5 — Logging, Observability & Hardening

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to emit **structured (JSON) logs** from FastAPI and why they beat `print`.
- How to attach a **request ID** to every request so you can trace one request across logs (and replicas).
- How to build **health checks** (`/health` liveness + a DB-aware readiness check) for load balancers and orchestrators.
- How to add a React **error boundary** so one broken component doesn't blank the whole app.
- How to run a **security & validation hardening pass**: input rules, CORS, secrets, headers, and rate-limiting basics.

The lab delivers an observable, hardened TaskFlow ready to containerize.

## 1. Why structured logging (reprise of Module 8)

In production you don't watch a terminal — you ship logs to a system that *searches* and *filters* them. That only works if each log line is machine-readable. A **structured log** is one JSON object per line:

```json
{"ts":"2026-06-26T09:14:02Z","level":"INFO","msg":"request",
 "request_id":"a1b2c3d4","method":"POST","path":"/api/v1/projects",
 "status":201,"duration_ms":12,"user_id":4}
```

Now you can answer "show me all 5xx responses for user 4 in the last hour" with a query. With `print("created project")` you can't. The rule from Module 8 holds: **log, don't print**, and make every line structured.

| Level | Use for |
| --- | --- |
| `DEBUG` | Verbose developer detail (off in prod) |
| `INFO` | Normal events: requests, startup, a project created |
| `WARNING` | Recoverable oddities: a 404, a failed login attempt |
| `ERROR` | Unhandled exceptions, failed DB writes |

## 2. A JSON log formatter

Python's `logging` module is built-in. We give it a custom formatter that renders the record (plus any extra fields) as JSON:

```python
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
        # merge any structured "extra" fields we attached
        if hasattr(record, "extra_fields"):
            payload.update(record.extra_fields)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def configure_logging():
    handler = logging.StreamHandler()       # stdout -> Docker captures it
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)
```

> **📝 Log to stdout, not a file**
>
> In containers (Module 9), the platform collects whatever you print to stdout/stderr. So don't write log files — write JSON to stdout and let Docker/the host aggregate it. One less thing to manage.

## 3. Request IDs & a logging middleware

A **request ID** is a unique token per request. You log it on every line for that request, return it in a response header, and (in 10.6) it lets you trace a request even when it bounced through one of several backend replicas. We generate or honor an incoming `X-Request-ID` in middleware:

```python
import time, uuid, logging
from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger("taskflow.request")

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        start = time.perf_counter()
        response = await call_next(request)
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

Because `request.state.request_id` is set, any handler or error logger can include the same id — so all the lines for one request share a key.

> **💡 Show the id to the user (carefully)**
>
> Returning
>
> X-Request-ID
>
> in the response lets your frontend display "Error — reference a1b2c3d4" on a failure. A user can quote that id in a bug report and you can find the exact request in your logs.

## 4. Health checks: liveness vs. readiness

Load balancers and orchestrators poll an endpoint to decide whether to send traffic to an instance. Two flavors:

| Check | Question | Implementation |
| --- | --- | --- |
| `/health` (liveness) | "Is the process up?" | Return `{"status":"ok"}` — cheap, no dependencies. |
| `/health/ready` (readiness) | "Can it serve real traffic?" | Try a trivial DB query; 200 if it works, 503 if not. |

```python
from sqlalchemy import text

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/health/ready")
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception:
        raise HTTPException(503, "database unavailable")
```

Nginx (10.6) will hit `/health` to drop dead replicas out of rotation. Keep liveness dependency-free so a slow DB doesn't get a healthy process killed.

## 5. Catching errors centrally

Unhandled exceptions should be *logged with the request id* and returned as a clean 500 — never a stack trace to the user. A global exception handler does both:

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception):
    rid = getattr(request.state, "request_id", "-")
    logging.getLogger("taskflow").error(
        "unhandled_exception",
        extra={"extra_fields": {"request_id": rid, "path": request.url.path}},
        exc_info=exc,
    )
    return JSONResponse(status_code=500,
        content={"detail": "Internal server error", "request_id": rid})
```

> **⚠️ Never leak internals**
>
> A raw traceback in an HTTP response is an information-disclosure vulnerability (it reveals file paths, library versions, sometimes secrets). Log the detail server-side; return a generic message + the request id to the client.

## 6. The React error boundary

A JavaScript error in one component will, by default, unmount your entire React tree — the user sees a blank white page. An **error boundary** (Module 8.2) catches render errors in its subtree and shows a fallback instead. It must be a class component (the one place we still use one):

```python
import { Component } from "react";

export default class ErrorBoundary extends Component {
  state = { error: null };
  static getDerivedStateFromError(error) { return { error }; }
  componentDidCatch(error, info) {
    // send to your logging endpoint / console
    console.error("UI crash:", error, info);
  }
  render() {
    if (this.state.error) {
      return (
        <div className="crash">
          <h1>Something went wrong</h1>
          <button onClick={() => location.reload()}>Reload</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

Wrap the app with it in `main.jsx` so any page crash degrades gracefully instead of going blank.

## 7. The hardening pass

Walk a checklist before shipping. Each item closes a real gap (these echo Module 7.4):

| Area | Hardening |
| --- | --- |
| Input validation | Pydantic field rules: `min_length` on passwords, max lengths on titles/names, the `Literal` status set, `EmailStr`. Reject junk at the edge. |
| Secrets | `SECRET_KEY` from env only; no defaults in prod; `.env` gitignored; fail fast if missing. |
| CORS | Allow only your real frontend origin(s) — not `"*"` — via an env var. |
| Auth | Token expiry enforced; generic "incorrect email or password" (don't reveal which); password length minimum. |
| Headers | Add basic security headers (e.g. `X-Content-Type-Options: nosniff`) — easy via middleware or Nginx in 10.6. |
| XSS | Never use `dangerouslySetInnerHTML`; React escapes by default. Validate/normalize inputs. |
| Rate limiting | At minimum, throttle `/auth/login` to slow brute-force (a simple in-memory limiter for the MVP; a shared store in real prod). |
| Errors | Global handler logs detail, returns generic message + request id (section 5). |

```python
# Example: tighten a password rule in schemas.py
from pydantic import BaseModel, EmailStr, Field

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(min_length=1, max_length=80)
```

> **💡 Hardening is a habit, not a feature**
>
> You won't make TaskFlow unhackable in one session — but a documented checklist you actually ran is exactly what reviewers and interviewers want to see. Note what you did (and what you'd add next) in the README's security section.

## ✅ Recap

- **Structured JSON logs** to stdout make production debuggable; `print` doesn't.
- A **request-ID middleware** tags every line and the response header so you can trace one request anywhere.
- **Liveness** (`/health`) and **readiness** (`/health/ready`) checks serve load balancers; keep liveness dependency-free.
- A **global exception handler** logs the detail + request id and returns a clean 500; a React **error boundary** prevents blank-page crashes.
- The **hardening pass** tightens validation, secrets, CORS, auth messages, headers, and rate limiting — and you document it.

**Next:** open `assignment.html` and make TaskFlow observable and hardened.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
