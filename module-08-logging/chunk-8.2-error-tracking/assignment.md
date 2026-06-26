*Full-Stack Web Dev · Module 8 — Logging & Observability*

# Chunk 8.2 — Lab: Health Checks & Error Capture

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Make the Tasks app **observable when things go wrong**. On the backend you'll add a catch-all **exception handler** that logs full tracebacks and returns a clean 500, plus **liveness** (`/health`) and **readiness** (`/health/ready`) endpoints, and a `/client-logs` endpoint. On the frontend you'll add a React **error boundary** that shows a fallback UI instead of a white screen and **reports** the crash to your backend — so a browser-side error ends up in your server logs.

## Before you start

- You finished **Chunk 8.1**: the Tasks API has `app/logging_config.py` (JSON logs + request ids) and a request-logging middleware.
- Your React frontend (`tasks-web/` from Module 7) runs with `npm run dev` and has `src/api.js`, `src/main.jsx`, and pages.
- Activate the backend venv and have both servers runnable (`uvicorn app.main:app --reload` and `npm run dev`).

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Part A — Backend

### 1 Add a catch-all exception handler

Register an `@app.exception_handler(Exception)` in `app/main.py` (or a small `app/errors.py`). It must log with `logger.exception("unhandled exception", extra={...})` (include `method` and `path`) and return a `JSONResponse` with status `500` and body `{"detail": "Internal server error"}`. Confirm your intentional `HTTPException`s (401/404) are unaffected.

### 2 Add a temporary "boom" route to test it

So you can trigger an unhandled error on demand, add a throwaway route that raises (you'll delete it after testing):

```python
@app.get("/boom")
def boom():
    raise ValueError("kaboom for testing")
```

Hitting `/boom` should return a clean `500 {"detail":"Internal server error"}` while your terminal shows a JSON log line with the full traceback in an `exception` field and the request id.

### 3 Liveness: `GET /health`

Add a dependency-free liveness check that returns `{"status": "ok"}` with a `200`. It must **not** touch the database. (If you already have `/health` from earlier modules, keep it — just confirm it's dependency-free.)

### 4 Readiness: `GET /health/ready`

Add a readiness check that runs a trivial query (`SELECT 1`) through the `get_db` dependency. Return `{"status":"ready","database":"ok"}` on success; on failure, log it and return status `503` with `{"status":"not ready","database":"down"}`.

> **💡 Running raw SQL via SQLAlchemy**
>
> Wrap the string:
>
> db.execute(text("SELECT 1"))
>
> , importing
>
> from sqlalchemy import text
>
> .

### 5 Client-error endpoint: `POST /client-logs`

Add a Pydantic schema `ClientErrorReport` (`message: str`, `stack: str = ""`, `url: str = ""`) and a public endpoint (status `202`) that logs the report at `ERROR` with `extra` fields. Cap the stack length (e.g. `report.stack[:2000]`) before logging.

## Part B — Frontend

### 6 Add a `reportClientError` helper

In `src/api.js`, add a function that POSTs `{ message, stack, url }` to `/client-logs`. Wrap the whole thing in `try/catch` so the reporter can never itself throw and worsen the crash.

### 7 Build the error boundary

Create `src/components/ErrorBoundary.jsx` as a **class component** with `getDerivedStateFromError` (flip to a fallback) and `componentDidCatch` (call `reportClientError(error, info.componentStack)`). The fallback UI should be a friendly message and a "Reload" button — not a blank screen.

### 8 Wrap your app

In `src/main.jsx`, wrap `<App />` (inside your providers/router) with `<ErrorBoundary>…</ErrorBoundary>` so a crash anywhere in the tree is caught.

### 9 Add a way to trigger a crash, then verify

Temporarily add a component/button that throws during render (e.g. a "Crash" button that sets state causing a child to throw, or a component that does `throw new Error("boom")`). Trigger it and confirm: (a) you see your fallback UI, not a white page; (b) a `POST /client-logs` fires (Network tab); (c) your backend terminal shows a JSON `"client error"` log line. Remove the crash trigger and `/boom` afterwards.

## ✅ Deliverable — acceptance checklist

- An unhandled backend exception returns `500 {"detail":"Internal server error"}` and is logged with a full traceback + request id.
- Intentional `HTTPException`s (401/404) still return their own status codes (the catch-all didn't swallow them).
- `GET /health` returns `200 {"status":"ok"}` and does not touch the DB.
- `GET /health/ready` returns `200` when the DB query succeeds, and `503` when it can't reach the DB.
- `POST /client-logs` accepts a report and logs it (stack capped), returning `202`.
- A React render crash shows a graceful fallback (no white screen) and POSTs to `/client-logs`, which appears in the backend logs.

## 🚀 Stretch goals (optional)

- Catch *async/global* errors too: add `window.addEventListener("error", …)` and `"unhandledrejection"` handlers in `main.jsx` that call `reportClientError`.
- Include the current `request_id` idea on the client: read the `X-Request-ID` header from failed API responses and include it in the report.
- Add a custom handler for `RequestValidationError` that logs which fields failed (without logging the values).
- Have `/health/ready` also report app version and uptime.
- Rate-limit `/client-logs` (even a tiny in-memory counter) so a crash loop can't flood your logs.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
