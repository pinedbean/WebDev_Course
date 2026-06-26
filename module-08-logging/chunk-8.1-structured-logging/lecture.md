*Full-Stack Web Dev · Module 8 — Logging & Observability*

# Chunk 8.1 — Structured Logging in FastAPI

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What **observability** means and why `print()` is not logging.
- The five **log levels** and how to choose the right one.
- How Python's `logging` module works: **loggers, handlers, formatters**.
- Why production wants **structured (JSON) logs** instead of free-form text.
- How to write a **request-logging middleware** and attach a **request ID** to every log line so one request is traceable end to end.

In the lab you'll give the Tasks API real, structured logs with request IDs.

## 1. Why logging? (Observability in one minute)

Through Modules 5–7 you mostly debugged by looking at the terminal or hitting `/docs`. That works on your laptop. But once the Tasks API runs on a server — behind Docker and a load balancer (Module 9) — you can't watch it. When a user reports "the app broke at 2pm," you need to *look back in time* and answer: what requests came in? which one failed? why? how long did it take?

That ability to understand what a running system is doing, from the outside, is **observability**. Its three classic pillars are **logs** (events that happened), **metrics** (numbers over time), and **traces** (a request's journey across services). This module focuses on the foundation everyone needs first: **logs**.

> **📝 Logs are your flight recorder**
>
> A log is a timestamped record of "something happened." Good logs turn "it broke and I have no idea why" into "request
>
> a1b2
>
> failed validating the task title at 14:03:11." You're building that flight recorder now, before you need it.

## 2. `print()` vs logging

It's tempting to sprinkle `print("got here")` everywhere. For a one-off script that's fine. For a server, `print()` falls short in every way that matters:

|  | `print()` | `logging` |
| --- | --- | --- |
| Severity | None — everything is equal | Levels (DEBUG…CRITICAL) you can filter |
| Turn off in prod | Edit/delete every line | Raise the level in one place |
| Timestamps / source | You add them by hand | Automatic (time, module, line) |
| Where it goes | Only stdout | stdout, files, JSON, external services |
| Machine-readable | No | Yes (with a JSON formatter) |

The rule of thumb: **`print()` is for humans running a script; `logging` is for programs running in production.** From now on, the Tasks API logs — it never prints.

## 3. Log levels

Every log message has a **level** describing how important/severe it is. Python gives you five, from quietest to loudest:

| Level | Use it for | Example in the Tasks API |
| --- | --- | --- |
| `DEBUG` | Fine-grained detail while developing | "query returned 12 tasks for owner_id=3" |
| `INFO` | Normal, expected events | "request completed 200 in 14ms", "user 5 logged in" |
| `WARNING` | Something odd but handled | "login failed: bad password for a@x.com" |
| `ERROR` | An operation failed | "unhandled exception creating task" |
| `CRITICAL` | The app itself is in danger | "cannot connect to database — shutting down" |

You set a **threshold**, and anything at or above it is emitted. Set the level to `INFO` and you'll see INFO, WARNING, ERROR, CRITICAL — but DEBUG is hidden. This is the superpower `print()` lacks: in development you run at `DEBUG` for maximum detail; in production you run at `INFO` and the noise disappears — **without deleting a single line of code**.

> **💡 A simple heuristic**
>
> If you'd want to be paged at 3am for it →
>
> ERROR
>
> /
>
> CRITICAL
>
> . If it's "huh, that's unusual" →
>
> WARNING
>
> . If it's "the system is working normally" →
>
> INFO
>
> . If only you, mid-debug, care →
>
> DEBUG
>
> .

## 4. How Python's `logging` module is built

Three pieces work together. Understanding them is the whole game:

- **Logger** — what your code talks to. You get one with `logging.getLogger(__name__)` and call `logger.info(...)`. Loggers are named (usually after the module) and organized in a tree.
- **Handler** — decides *where* a record goes: the console (`StreamHandler`), a file (`FileHandler`), etc. A logger can have several handlers.
- **Formatter** — decides *what each line looks like*: plain text, or — what we want — JSON.

>

The minimal setup is one line:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Server started")
logger.warning("Disk almost full")
```

Output:

```
INFO:__main__:Server started
WARNING:__main__:Disk almost full
```

> **📝 Get the logger by `__name__`**
>
> Always do
>
> logger = logging.getLogger(__name__)
>
> at the top of a module. The name becomes the module's path (
>
> app.routers.tasks
>
> ), so every log line tells you exactly where it came from — and you can tune levels per module later.

## 5. Why structured (JSON) logs?

A traditional log line is a sentence built for human eyes:

```
2026-06-26 14:03:11 INFO app.main Request completed: GET /tasks 200 in 14ms
```

That's readable, but a *machine* has to rip it apart with fragile regexes to answer "show me every request slower than 500ms." In production your logs don't get read line-by-line — they get shipped to a tool (CloudWatch, Loki, Datadog, an ELK stack) that **indexes and searches** them. Those tools love **JSON**, where every field is already labelled:

```json
{"timestamp": "2026-06-26T14:03:11Z", "level": "INFO", "logger": "app.main",
 "message": "request completed", "method": "GET", "path": "/tasks",
 "status_code": 200, "duration_ms": 14, "request_id": "a1b2c3d4"}
```

Now "requests slower than 500ms" is a trivial filter on the `duration_ms` field. Same information, but **queryable**. That's the entire point of structured logging: stop writing prose, start emitting data.

We get JSON by writing a custom **formatter** that turns each log record into a JSON object. You'll build a small one in the lab — no extra libraries required (though `structlog` and `python-json-logger` exist if you want batteries included).

> **💡 Best of both worlds**
>
> A common pattern: pretty human-readable text when running locally (
>
> ENVIRONMENT=development
>
> ), JSON when deployed. You choose the formatter based on a setting — same code, two faces.

## 6. Logging extra fields (the "structured" part)

JSON output is only useful if you attach *data* to each event. Python's logging lets you pass an `extra` dict, and your formatter can fold those keys into the JSON:

```
logger.info(
    "request completed",
    extra={"method": "GET", "path": "/tasks", "status_code": 200, "duration_ms": 14},
)
```

The message stays a short, stable label (`"request completed"`) and the variable details live in fields. That's far better than f-stringing everything into the message, because the label is now something you can group and count on.

## 7. Request-logging middleware

You *could* log inside every endpoint, but that's repetitive and easy to forget. FastAPI (via Starlette) lets you register **middleware**: code that wraps every request, running just before the route and just after the response. It's the perfect place to log one tidy line per request.

```python
import time
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)          # run the actual endpoint
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
    return response
```

Now *every* request — to any route, present or future — gets a structured log line with method, path, status, and timing, automatically. In the lab you'll put this in its own module for tidiness.

> **⚠️ Don't log secrets**
>
> Middleware sees everything: headers, bodies, query strings. Never log the
>
> Authorization
>
> header, passwords, or tokens. Log the
>
> shape
>
> of a request (method, path, status, timing), not its sensitive contents.

## 8. Correlation IDs — tracing one request

Here's the problem that ties it together. Under load, dozens of requests are in flight at once, and their log lines interleave:

```
INFO request started  GET /tasks
INFO request started  POST /tasks
WARNING slow query
INFO request completed POST /tasks 201
ERROR task not found
INFO request completed GET /tasks 200
```

Which request hit the slow query? Which one 404'd? You can't tell — the lines are tangled. The fix is a **correlation ID** (a.k.a. **request ID**): a unique id generated when a request arrives and stamped onto *every* log line produced while handling it.

```json
{"request_id": "a1b2", "message": "request started", "path": "/tasks"}
{"request_id": "c3d4", "message": "request started", "path": "/tasks"}
{"request_id": "c3d4", "message": "slow query", "level": "WARNING"}
{"request_id": "a1b2", "message": "request completed", "status_code": 200}
{"request_id": "c3d4", "message": "request completed", "status_code": 201}
```

Now you filter by `request_id = c3d4` and see that one request's whole story in order. In a load-balanced, multi-service world this is indispensable — and you also return the id to the client in an `X-Request-ID` header, so a user reporting a bug can hand you the exact id to search for.

### How do logs deep in your code "know" the request ID?

You don't want to pass `request_id` as an argument through every function. Python's standard library solves this with `contextvars.ContextVar` — a variable that's **isolated per async task**. The middleware sets it at the start of a request; any log record, anywhere in the call stack, can read it back. Because each request runs in its own task, two concurrent requests never see each other's id.

```python
from contextvars import ContextVar

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")

# middleware sets it:
request_id_ctx.set("a1b2c3d4")

# a custom logging.Filter reads it and attaches it to every record:
record.request_id = request_id_ctx.get()
```

You'll wire exactly this in the lab: a `ContextVar`, a small logging `Filter` that copies it onto each record, and middleware that generates the id with `uuid4()`.

> **📝 Why a ContextVar, not a global**
>
> A plain global variable would be shared by
>
> all
>
> requests at once — request A's id would leak into request B's logs. A
>
> ContextVar
>
> gives each async request its own copy. This is the standard Python way to carry "request-scoped" data.

## 9. Where do the logs actually go?

One golden rule for containerized apps (Module 9): **log to standard output (stdout), not to a file.** Your app's only job is to print structured lines to stdout. The platform around it — Docker, the cloud host, a log collector — captures stdout and routes it wherever it needs to go. This keeps your app simple and portable: it doesn't manage log files, rotation, or shipping. We'll lean on this hard in Module 9, but the habit starts now.

## ✅ Recap

- **Observability** = understanding a running system from outside; **logs** are the foundation.
- `logging` beats `print()`: levels, central config, timestamps, destinations, machine-readable output.
- Five levels — **DEBUG, INFO, WARNING, ERROR, CRITICAL** — let you tune verbosity without touching code.
- The module is **Logger → Handler → Formatter**. A custom JSON **formatter** gives you **structured logs** you can query.
- **Middleware** logs one structured line per request; a **request ID** carried in a `ContextVar` ties every line of one request together.
- In containers, **log to stdout** and let the platform ship it.

**Next:** open `assignment.html` and add structured logging + request IDs to the Tasks API.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
