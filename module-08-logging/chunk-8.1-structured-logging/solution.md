*Full-Stack Web Dev · Module 8 — Logging & Observability*

# Chunk 8.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll add a logging module, a request-logging middleware, and wire both into the app. New/changed files:

```text
tasks-api/
└── app/
    ├── logging_config.py     (new: ContextVar, JSON formatter, filter, setup_logging)
    ├── middleware.py         (new: request-ID + request-logging middleware)
    ├── main.py               (call setup_logging, register middleware)
    ├── routers/
    │   ├── auth.py           (log failed logins)
    │   └── tasks.py          (log task creation)
```

### 1 `app/logging_config.py` — the whole logging brain

One file owns the context variable, the JSON formatter, the request-ID filter, and the setup function.

```python
# app/logging_config.py
import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone

# Request-scoped id. Each async request gets its own value; default "-".
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

# The attributes every LogRecord already has; anything else is our `extra`.
_STANDARD = set(logging.LogRecord(
    "", 0, "", 0, "", None, None
).__dict__.keys()) | {"message", "asctime", "taskName"}

class RequestIdFilter(logging.Filter):
    """Copy the current request id onto every record."""
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True

class JsonFormatter(logging.Formatter):
    """Render each record as a single-line JSON object."""
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        # Fold in any extra={...} keys the caller passed.
        for key, value in record.__dict__.items():
            if key not in _STANDARD and key not in payload:
                payload[key] = value
        # Include exception info when present.
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)

def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger once: JSON to stdout, with request ids."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.handlers.clear()          # idempotent: avoid duplicate handlers on --reload
    root.addHandler(handler)
    root.setLevel(level)

    # Let our middleware be the single per-request line; mute uvicorn's access log.
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
```

> **📝 Why build `_STANDARD` from a throwaway record**
>
> A fresh
>
> LogRecord
>
> already carries all the built-in attributes (
>
> levelname
>
> ,
>
> pathname
>
> ,
>
> lineno
>
> …). Anything NOT in that set is something
>
> you
>
> added via
>
> extra=
>
> — exactly the fields we want in the JSON. We add
>
> message
>
> /
>
> asctime
>
> /
>
> taskName
>
> because they appear only after formatting.

### 2 `app/middleware.py` — one structured line per request

```python
# app/middleware.py
import logging
import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logging_config import request_id_ctx

logger = logging.getLogger("app.request")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Reuse an incoming id (e.g. from a load balancer) or make a new one.
        request_id = request.headers.get("X-Request-ID") or uuid4().hex[:8]
        token = request_id_ctx.set(request_id)

        start = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            request_id_ctx.reset(token)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "request completed",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
            },
        )
        response.headers["X-Request-ID"] = request_id
        return response
```

> **💡 Why `BaseHTTPMiddleware` instead of `@app.middleware("http")`**
>
> Both work. A class is tidier to keep in its own file and is the same style you'll reuse for error handling in 8.2. The
>
> reset(token)
>
> in the
>
> finally
>
> block restores the previous context value cleanly even if the route raises.

### 3 Wire it into `app/main.py`

Call `setup_logging()` **before** creating the app, and register the middleware. (Driving the level from settings is a nice touch — add `log_level: str = "INFO"` to `Settings` if you like.)

```python
# app/main.py  (additions)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.logging_config import setup_logging
from app.middleware import RequestLoggingMiddleware
from app.routers import auth, tasks, admin

setup_logging(getattr(settings, "log_level", "INFO"))

app = FastAPI(title="Tasks API")

app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(admin.router)
```

> **⚠️ Middleware order**
>
> Middleware runs in the reverse order it's added for the response. Adding
>
> RequestLoggingMiddleware
>
> first means it's the
>
> outermost
>
> wrapper, so it times the full request (including CORS handling) and always sets the request id before anything else runs.

### 4 Add real logs in the routers

```python
# app/routers/auth.py  (top of file + inside login)
import logging
logger = logging.getLogger(__name__)

# ... inside login(), when credentials fail:
if not user or not verify_password(form_data.password, user.hashed_password):
    logger.warning("login failed", extra={"email": form_data.username.lower()})
    raise HTTPException(status_code=401, detail="Invalid credentials")
logger.info("login succeeded", extra={"user_id": user.id})
```

```python
# app/routers/tasks.py  (top of file + inside create_task)
import logging
logger = logging.getLogger(__name__)

# ... after db.refresh(task):
logger.info("task created", extra={"task_id": task.id, "owner_id": current_user.id})
return task
```

> **📝 Log the email, never the password**
>
> Logging the attempted email on a failed login is useful for spotting attacks. The password must never appear — note we only pass
>
> email
>
> in
>
> extra
>
> .

### 5 Run & read the logs

```bash
uvicorn app.main:app --reload
```

Hit a few endpoints. Each request now prints one JSON line to your terminal:

```json
{"timestamp": "2026-06-26T14:03:11.482Z", "level": "INFO", "logger": "app.request", "message": "request completed", "request_id": "9f2c1a7b", "method": "GET", "path": "/health", "status_code": 200, "duration_ms": 1.74}
{"timestamp": "2026-06-26T14:03:20.119Z", "level": "WARNING", "logger": "app.routers.auth", "message": "login failed", "request_id": "3b8e0d52", "email": "a@x.com"}
{"timestamp": "2026-06-26T14:03:20.121Z", "level": "INFO", "logger": "app.request", "message": "request completed", "request_id": "3b8e0d52", "method": "POST", "path": "/auth/login", "status_code": 401, "duration_ms": 88.3}
```

Notice the failed-login WARNING and its "request completed" line share `request_id: 3b8e0d52` — that's correlation working.

### 6 Confirm the response header

```bash
curl -i http://localhost:8000/health
```

```
HTTP/1.1 200 OK
x-request-id: 9f2c1a7b
content-type: application/json

{"status":"ok"}
```

The `x-request-id` matches the `request_id` in the log for that call — a user can quote it and you can find their exact request instantly.

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Each request prints the log line *twice* | `--reload` re-imported the module and stacked handlers. Keep `root.handlers.clear()` in `setup_logging()`. |
| Logs are still plain text, not JSON | You're seeing uvicorn's own startup/access logs. Your app logs are JSON; mute `uvicorn.access` (set it to WARNING) and look for your lines. |
| `request_id` is always `"-"` | The filter isn't attached to the handler, or the middleware isn't setting the ContextVar. Confirm `handler.addFilter(RequestIdFilter())` and that the request-logging middleware runs. |
| All requests share one request id | You used a module-level global instead of a `ContextVar`, or set it once at import. It must be `.set()` per request inside the middleware. |
| `TypeError: Object of type ... is not JSON serializable` | An `extra` value isn't JSON-native (e.g. a datetime). `json.dumps(..., default=str)` (as shown) handles it. |
| `X-Request-ID` header missing | Make sure you set it on the `response` object the middleware returns, after `call_next`. |

## 📄 Complete `app/logging_config.py`

```python
import json
import logging
import sys
from contextvars import ContextVar
from datetime import datetime, timezone

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

_STANDARD = set(logging.LogRecord(
    "", 0, "", 0, "", None, None
).__dict__.keys()) | {"message", "asctime", "taskName"}

class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        for key, value in record.__dict__.items():
            if key not in _STANDARD and key not in payload:
                payload[key] = value
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)

def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
```

## 🎉 You're done

The Tasks API is now observable from the outside: every request produces one structured JSON line with timing and status, every line carries a **request id** that ties a single request's events together, and that id rides back to the client in `X-Request-ID`. This is the exact foundation log-aggregation tools expect — and the habit (log to stdout, structured, with correlation) you'll rely on in Docker and behind a load balancer.

Logging tells you what *happened*. Next you'll make failures loud and catchable: centralized error handling, health checks, and a React error boundary that reports crashes instead of showing a blank screen.

**Up next → Chunk 8.2: Error Tracking & Frontend Logging.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
