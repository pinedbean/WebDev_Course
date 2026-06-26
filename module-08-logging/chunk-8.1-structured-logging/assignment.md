*Full-Stack Web Dev · Module 8 — Logging & Observability*

# Chunk 8.1 — Lab: Structured Logs with Request IDs

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Give the **Tasks API** production-grade logging. You'll add a logging configuration that emits **JSON log lines**, a **request-logging middleware** that times every request, and a **request ID** (correlation ID) carried in a `ContextVar` and attached to every log line plus an `X-Request-ID` response header. By the end, every request the API handles produces one structured, traceable JSON log entry.

## Before you start

- Your **Tasks API** from Module 7 runs: FastAPI + SQLAlchemy + SQLite, JWT auth, an `app/` package, routes under `/auth` and `/tasks`, settings via `app/config.py`.
- Activate your virtual environment (macOS/zsh): `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
- The server runs with `uvicorn app.main:app --reload`; docs at `http://localhost:8000/docs`.

> **📝 No new dependencies required**
>
> Everything here uses the Python standard library (
>
> logging
>
> ,
>
> json
>
> ,
>
> uuid
>
> ,
>
> contextvars
>
> ,
>
> time
>
> ). You don't need to
>
> pip install
>
> anything for the core tasks.

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Tasks

### 1 Create the request-ID context

Decide where request-scoped state lives. Create a `ContextVar` named `request_id_ctx` (default `"-"`) — you can keep it in a new `app/logging_config.py`. The middleware will `.set()` it; the log filter will `.get()` it.

### 2 Write a JSON formatter

In `app/logging_config.py`, write a `logging.Formatter` subclass whose `format()` returns a JSON string. It must always include: `timestamp` (UTC ISO-8601), `level`, `logger` (the record name), `message`, and `request_id`. It should also fold in any custom keys you pass via `extra=` (e.g. `method`, `path`, `status_code`, `duration_ms`), and include exception text when one is present.

> **💡 How to find the "extra" keys**
>
> Custom
>
> extra
>
> values become attributes on the record. Compare each record's
>
> __dict__
>
> against a set of the standard
>
> LogRecord
>
> attributes, and include whatever is left over.

### 3 Write a filter that injects the request ID

Add a tiny `logging.Filter` subclass whose `filter()` reads `request_id_ctx.get()` and sets `record.request_id` on the record (then returns `True`). Attaching it to the handler means *every* log line — even ones deep inside your routers — carries the current request's id.

### 4 A `setup_logging()` function

Add `setup_logging(level: str = "INFO")` that configures the **root logger**: one `StreamHandler` (to stdout) using your JSON formatter and your request-ID filter, at the given level. Call it once when the app starts. Make it idempotent (clear existing handlers first) so `--reload` doesn't stack duplicate handlers.

### 5 Add the request-logging middleware

Register an HTTP middleware (in `app/main.py`, or a small `app/middleware.py`) that for every request:

- Generates a request id with `uuid4().hex[:8]` (or reuses an incoming `X-Request-ID` header if present) and stores it via `request_id_ctx.set(...)`.
- Times the request with `time.perf_counter()`.
- Calls the route, then logs **one** `INFO` line `"request completed"` with `extra` = `method`, `path`, `status_code`, `duration_ms`.
- Adds the id to the response as an `X-Request-ID` header.

### 6 Replace prints & add a couple of real logs

Grep your project for `print(` and convert any to `logger.*` calls. Then add at least two meaningful logs: a `WARNING` on a failed login (in `auth.py`) and an `INFO` when a task is created (in `tasks.py`), e.g. `logger.info("task created", extra={"task_id": task.id, "owner_id": current_user.id})`. Use `logger = logging.getLogger(__name__)` at the top of each module.

> **⚠️ Never log secrets**
>
> Do not log the
>
> Authorization
>
> header, passwords, tokens, or full request bodies. Log identifiers and shapes, not sensitive values.

### 7 Run it and read your logs

Start the server and make a few requests (via `/docs` or `curl`). Confirm each request prints one JSON line with a `request_id`, and that the same id comes back in the `X-Request-ID` response header.

```bash
uvicorn app.main:app --reload
# in another terminal:
curl -i http://localhost:8000/health     # look for the X-Request-ID header
```

### 8 Prove correlation works

Hit a protected route without a token and create a task with a token. Confirm the failed-login warning and the "task created" info each carry their own request id, and that a single request's lines all share one id.

## ✅ Deliverable — acceptance checklist

- `app/logging_config.py` exists with a JSON formatter, a request-ID filter, and `setup_logging()`.
- Logs print as **one JSON object per line** to stdout, each with `timestamp`, `level`, `logger`, `message`, and `request_id`.
- A request-logging middleware emits one `"request completed"` line per request with `method`, `path`, `status_code`, and `duration_ms`.
- Each response includes an `X-Request-ID` header equal to the `request_id` in that request's logs.
- No `print()` calls remain; at least one `WARNING` (failed login) and one `INFO` (task created) are logged.
- Two concurrent/separate requests have *different* request ids, and all log lines from one request share *the same* id.

## 🚀 Stretch goals (optional)

- Add an `ENVIRONMENT` setting to `config.py`: use pretty text logs in `development` and JSON in `production`.
- Also log a `"request started"` line (handy for spotting requests that hang and never complete).
- Log the authenticated `user_id` on each request when a token is present (without logging the token itself).
- Quiet the noisy `uvicorn.access` logger (set its level to `WARNING`) so your structured line is the single source of truth per request.
- Pretty-print one log line: `curl -s localhost:8000/tasks | head` — then pipe a captured JSON log through `python -m json.tool`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
