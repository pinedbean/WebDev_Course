*Full-Stack Web Dev · Module 8 — Logging & Observability*

# Chunk 8.2 — Error Tracking & Frontend Logging

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How **centralized error handling** turns scary stack traces into clean, logged responses.
- How to log exceptions with full tracebacks using `logger.exception`.
- What **log aggregation** and **error tracking** services do (Sentry, Datadog, ELK, CloudWatch) — conceptually.
- Why apps need **health-check endpoints**, and the difference between **liveness** and **readiness**.
- How a React **error boundary** stops one broken component from white-screening the whole app — and how to **report** frontend crashes back to your server.

In the lab you'll add global error logging, `/health` + `/health/ready`, a React error boundary, and a client-error reporting endpoint.

## 1. The two kinds of failure

In 8.1 you logged the *normal* life of a request. This chunk is about the *abnormal* — failures — on both sides of the stack:

- **Backend errors:** an endpoint raises an exception. Without handling, FastAPI returns a generic `500` and the traceback is lost unless you happened to be watching the terminal.
- **Frontend errors:** a React component throws while rendering. By default React *unmounts the whole tree* — the user gets a blank white page and you never hear about it.

Observability means: when either happens, it's **caught**, **logged with enough detail to debug**, and the user sees something **graceful** instead of a crash. Let's do both.

## 2. Centralized error handling on the backend

You met FastAPI's `HTTPException` in Module 5 — that's for *expected* errors you raise on purpose (404, 401, 400). They're already clean. The danger is the *unexpected* exception: a bug, a `KeyError`, a database hiccup. You want a single place that catches anything unhandled, logs it richly, and returns a tidy JSON body — never a raw traceback to the user (which can leak file paths and internals).

FastAPI gives you an **exception handler**: register one function for a given exception type and it runs whenever that type escapes a route.

```python
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger("app.errors")

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(            # logs the message AND the full traceback
        "unhandled exception",
        extra={"method": request.method, "path": request.url.path},
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

Two things matter here. First, `logger.exception(...)` — call it *inside* an `except` (or an exception handler) and it automatically attaches the current traceback. Your 8.1 JSON formatter already folds that into an `"exception"` field, so the full stack lands in your structured logs, tagged with the request id. Second, the *user* gets only `{"detail": "Internal server error"}` — calm and leak-free.

> **⚠️ Don't swallow `HTTPException`**
>
> A catch-all
>
> Exception
>
> handler should not hijack your intentional
>
> 404
>
> /
>
> 401
>
> responses. FastAPI handles
>
> HTTPException
>
> separately and before this, so your purposeful errors keep their status codes. Only truly unhandled exceptions hit the catch-all.

> **📝 `logger.error` vs `logger.exception`**
>
> logger.exception("msg")
>
> is exactly
>
> logger.error("msg", exc_info=True)
>
> — it logs at ERROR level AND captures the traceback. Use it whenever you're handling a caught exception; use plain
>
> logger.error
>
> when there's no exception object to attach.

## 3. Log aggregation & error tracking (the big picture)

You're emitting structured logs to stdout. In production, where do they go and how do you actually *use* them? That's the job of two related kinds of tooling:

>

| Tool type | What it does | Examples |
| --- | --- | --- |
| **Log aggregation** | Collects logs from every instance into one searchable place; dashboards, filters, retention. | Grafana Loki, ELK/OpenSearch, CloudWatch Logs, Datadog |
| **Error tracking** | Captures exceptions, *groups* duplicates, shows stack traces + context, and **alerts** you. | Sentry, Rollbar, Bugsnag |

You're not wiring these up in this course — but notice that you've *earned the right to*. Because your logs are **structured JSON on stdout with request ids**, pointing them at any of these tools is configuration, not a rewrite. That's the payoff of doing 8.1 properly.

> **💡 The 12-Factor habit**
>
> "Treat logs as event streams" — your app writes to stdout and is done. It never opens log files or talks to Sentry directly in code (well, sometimes a tiny SDK), and definitely never manages rotation. The environment handles delivery. This keeps the app portable across laptop, Docker, and cloud.

## 4. Health-check endpoints

How does a load balancer or orchestrator know your instance is alive and ready for traffic? It periodically calls a **health-check endpoint** and watches the status code. This becomes essential in Module 9, where Nginx and Docker need to route around dead replicas.

There are two distinct questions, and good systems separate them:

| Check | Question | If it fails… |
| --- | --- | --- |
| **Liveness** `/health` | "Is the process up and responding at all?" | Restart the instance. |
| **Readiness** `/health/ready` | "Can it serve real traffic right now?" (e.g. is the DB reachable?) | Stop sending it traffic until it recovers. |

Liveness must be **cheap and dependency-free** — it just proves the web server answers:

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

Readiness checks the things a request actually needs. For the Tasks API that's the database — run a trivial query and report:

```python
from sqlalchemy import text

@app.get("/health/ready")
def readiness(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception:
        logger.exception("readiness check failed")
        return JSONResponse(status_code=503,
                            content={"status": "not ready", "database": "down"})
```

> **⚠️ Keep liveness dumb**
>
> Don't check the database in
>
> /health
>
> . If liveness touches the DB and the DB blips, the orchestrator will
>
> restart
>
> healthy app instances — making an outage worse. Liveness = "am I running"; readiness = "can I serve". Status
>
> 503
>
> on readiness tells the balancer "skip me for now," which is exactly right.

## 5. The frontend problem: React unmounts on a crash

If any component throws during render, React 18's default is to unmount the entire component tree — the user is left staring at a blank page, and you have no idea it happened. The fix is a **React error boundary**: a component that "catches" render errors in its children, shows a fallback UI, and lets you report the error.

Error boundaries must (still) be **class components**, because they rely on two lifecycle methods that have no hook equivalent:

- `static getDerivedStateFromError(error)` — runs during render after a child throws; returns new state so you can show a fallback.
- `componentDidCatch(error, info)` — runs after; the place to **log/report** the error (it also gives you a component stack).

```python
import { Component } from "react";
import { reportClientError } from "./api";

export class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(error) {
    return { hasError: true };          // flip to the fallback UI
  }

  componentDidCatch(error, info) {
    // Send it somewhere we can actually see it.
    reportClientError(error, info.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div role="alert">
          <h1>Something went wrong.</h1>
          <button onClick={() => location.reload()}>Reload</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

You wrap your app with it once, at the top:

```html
<ErrorBoundary>
  <App />
</ErrorBoundary>
```

> **📝 What boundaries do and don't catch**
>
> They catch errors thrown
>
> during rendering
>
> of their child tree. They do
>
> not
>
> catch errors in event handlers, async code (
>
> fetch
>
> /
>
> setTimeout
>
> ), or the boundary itself. For those, use ordinary
>
> try/catch
>
> and the
>
> window.onerror
>
> /
>
> unhandledrejection
>
> handlers (a stretch goal in the lab).

## 6. Reporting frontend errors to the backend

A crash that only appears in the user's browser console is invisible to you. So the error boundary should **report** the error to your server, where it joins your structured logs. A minimal pattern: a frontend helper POSTs the message + stack to a small endpoint; the backend logs it.

```javascript
// frontend: src/api.js
export async function reportClientError(error, componentStack) {
  try {
    await fetch(`${BASE}/client-logs`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: String(error?.message || error),
        stack: componentStack || error?.stack || "",
        url: window.location.href,
      }),
    });
  } catch {
    // Never let the reporter itself crash the app.
  }
}
```

```python
# backend: a public router
@router.post("/client-logs", status_code=202)
def client_logs(report: ClientErrorReport):
    logger.error("client error", extra={
        "client_message": report.message,
        "client_url": report.url,
        "client_stack": report.stack[:2000],   # cap it
    })
    return {"received": True}
```

Now a React crash on a user's machine shows up in *your* JSON logs (with a request id), right next to your backend errors. That's true full-stack observability.

> **⚠️ Treat client input as hostile**
>
> Anyone can POST to
>
> /client-logs
>
> . Cap the stack length, don't log it at a level that pages you, and never
>
> eval
>
> or trust it. In a real app you'd also rate-limit this endpoint. Logging it at
>
> ERROR
>
> is fine; just know it's user-supplied.

## ✅ Recap

- A catch-all **exception handler** + `logger.exception` logs full tracebacks (tagged with the request id) while returning a clean, leak-free 500 to users.
- Your structured stdout logs are ready for **log aggregation** (Loki/ELK/CloudWatch) and **error tracking** (Sentry) — wiring them up is config, not a rewrite.
- **Liveness** (`/health`) proves the process is up; **readiness** (`/health/ready`) proves it can serve (DB reachable). Keep liveness dependency-free.
- A React **error boundary** (a class component) catches render crashes, shows a fallback, and **reports** the error to your backend so it lands in your logs.
- Boundaries don't catch event-handler/async errors — use `try/catch` and global handlers for those.

**Next:** open `assignment.html` and make the Tasks app observable end to end.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
