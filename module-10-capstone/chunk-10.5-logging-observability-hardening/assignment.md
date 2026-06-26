*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.5 — Lab: Observability & Hardening

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Make TaskFlow production-trustworthy. Add structured JSON logging with per-request IDs, liveness + readiness health checks, a global exception handler, a React error boundary, tightened input validation, and a documented security-hardening pass. By the end, every request is traceable and the app fails safely.

## Before you start

- Your full-stack TaskFlow from 10.2–10.4 runs and works end to end.
- Have your Module 8 notes (structured logging, request IDs, error boundary) and 7.4 (hardening) handy.
- Activate the backend venv; keep both servers runnable.

> **⚠️ Build it yourself first**
>
> Most of this you've done in Modules 7.4 and 8 — apply it to TaskFlow. Reach for the solution to compare, not to copy blind.

## Tasks

### 1 Structured JSON logging

Add `app/logging_config.py` with a JSON formatter and a `configure_logging()` that logs to stdout. Call it at startup in `main.py`. Confirm log lines are single-line JSON with `ts`, `level`, `msg`.

### 2 Request-ID middleware

Add middleware that generates (or honors an incoming `X-Request-ID`) per request, stores it on `request.state`, logs one structured line per request (method, path, status, duration), and returns the id in the `X-Request-ID` response header.

### 3 Health checks

Keep `/api/v1/health` as a dependency-free liveness check. Add `/api/v1/health/ready` that runs `SELECT 1` and returns 200/503. Verify both with `curl`.

### 4 Global exception handler

Add a handler for unhandled exceptions that logs the error (with request id and `exc_info`) and returns a generic 500 with the request id — no stack trace to the client. Test it by temporarily raising an error in a route.

### 5 React error boundary

Add `src/components/ErrorBoundary.jsx` and wrap `<App/>` with it in `main.jsx`. Verify that a deliberately thrown render error shows the fallback UI (with a reload button) instead of a blank page.

### 6 Surface the request id in the client

Update the API client to read the `X-Request-ID` response header on errors and include it in the thrown `Error` (e.g. "… (ref a1b2c3d4)") so failures are traceable from the UI.

### 7 Validation tightening

Add Pydantic field constraints: password `min_length=8`, name/title max lengths, ensure status uses the `Literal` set. Confirm bad input returns 422 with a helpful message.

### 8 Security pass + document it

Move `CORS` origins and `SECRET_KEY` to env (fail fast if the secret is missing in prod). Add a simple rate limit on `/auth/login`. Add a "Security notes" section to the README listing what you hardened and what you'd add next.

## ✅ Deliverable — acceptance checklist

- Backend emits one-line JSON logs to stdout, one per request, including a request id, method, path, status, and duration.
- Responses carry an `X-Request-ID` header; an incoming one is honored.
- `/health` (liveness) and `/health/ready` (DB-aware) both work and return correct codes.
- Unhandled errors return a generic 500 + request id; the full detail is logged, not exposed.
- A React error boundary shows a fallback instead of a blank page on a render crash.
- The client includes the request id in error messages it surfaces.
- Input validation rejects weak/oversized input with 422.
- CORS + secret come from env; login is rate-limited; README has a "Security notes" section.

## 🚀 Stretch goals (optional)

- Add a frontend error-reporting POST endpoint (`/api/v1/client-errors`) that the error boundary calls.
- Add response time as a `Server-Timing` header for DevTools.
- Add security headers via middleware (`X-Content-Type-Options`, `Referrer-Policy`).
- Add a `/metrics`-style counter (requests by status) you can eyeball.
- Write a test that asserts a 500 response never contains a traceback.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
