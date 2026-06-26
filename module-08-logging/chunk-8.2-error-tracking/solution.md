*Full-Stack Web Dev · Module 8 — Logging & Observability*

# Chunk 8.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Part A hardens the backend (error handler, health checks, client-log sink). Part B catches frontend crashes. New/changed files:

```text
tasks-api/                          tasks-web/
└── app/                             └── src/
    ├── main.py    (handler + health)    ├── api.js        (reportClientError)
    ├── schemas.py (ClientErrorReport)   ├── main.jsx      (wrap with boundary)
    └── routers/                         └── components/
        └── meta.py (/client-logs)           └── ErrorBoundary.jsx  (new)
```

## Part A — Backend

### 1 Catch-all exception handler in `app/main.py`

```python
# app/main.py  (additions — keep your 8.1 setup_logging + middleware)
import logging
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

logger = logging.getLogger("app.errors")

app = FastAPI(title="Tasks API")
# ... add_middleware(...) and include_router(...) as before ...

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "unhandled exception",
        extra={"method": request.method, "path": request.url.path},
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
```

> **📝 Your purposeful errors are safe**
>
> FastAPI handles
>
> HTTPException
>
> (and
>
> RequestValidationError
>
> ) with its own built-in handlers, which run before this catch-all. A
>
> raise HTTPException(404, ...)
>
> still returns a real 404 — only genuinely unhandled exceptions reach this function.

### 2 Health checks (liveness + readiness)

```python
# app/main.py  (additions)

@app.get("/health", tags=["health"])
def health():
    """Liveness: is the process up? Cheap, no dependencies."""
    return {"status": "ok"}

@app.get("/health/ready", tags=["health"])
def readiness(db: Session = Depends(get_db)):
    """Readiness: can we actually serve? Check the database."""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception:
        logger.exception("readiness check failed")
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "database": "down"},
        )
```

### 3 The client-log sink

Schema first:

```python
# app/schemas.py  (add)
from pydantic import BaseModel

class ClientErrorReport(BaseModel):
    message: str
    stack: str = ""
    url: str = ""
```

Then a tiny router (kept separate so it's clearly public):

```python
# app/routers/meta.py  (new)
import logging
from fastapi import APIRouter, status

from app import schemas

logger = logging.getLogger("app.client")
router = APIRouter(tags=["meta"])

@router.post("/client-logs", status_code=status.HTTP_202_ACCEPTED)
def client_logs(report: schemas.ClientErrorReport):
    logger.error(
        "client error",
        extra={
            "client_message": report.message[:500],
            "client_url": report.url[:300],
            "client_stack": report.stack[:2000],   # cap untrusted input
        },
    )
    return {"received": True}
```

```python
# app/main.py
from app.routers import auth, tasks, admin, meta
app.include_router(meta.router)
```

### 4 Test the backend

Add a throwaway `/boom` route (`raise ValueError("kaboom")`) and exercise everything:

```bash
curl -i localhost:8000/health
# HTTP/1.1 200 OK   {"status":"ok"}

curl -s localhost:8000/health/ready
# {"status":"ready","database":"ok"}

curl -i localhost:8000/boom
# HTTP/1.1 500 Internal Server Error   {"detail":"Internal server error"}
```

The `/boom` call leaves a structured error log in your terminal — note the traceback in `exception` and the matching request id:

```json
{"timestamp": "2026-06-26T14:20:02.551Z", "level": "ERROR", "logger": "app.errors", "message": "unhandled exception", "request_id": "7c1a9e02", "method": "GET", "path": "/boom", "exception": "Traceback (most recent call last):\n  ...\nValueError: kaboom"}
```

Delete `/boom` once you're satisfied.

## Part B — Frontend

### 5 `reportClientError` in `src/api.js`

```javascript
// src/api.js  (add; BASE already defined at top)
export async function reportClientError(error, componentStack = "") {
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
    // Swallow: the reporter must never crash the app.
  }
}
```

### 6 `src/components/ErrorBoundary.jsx`

```python
import { Component } from "react";
import { reportClientError } from "../api";

export default class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(_error) {
    return { hasError: true };          // render the fallback next
  }

  componentDidCatch(error, info) {
    // info.componentStack tells us which component tree threw.
    reportClientError(error, info?.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div role="alert" style={{ maxWidth: 480, margin: "60px auto", textAlign: "center" }}>
          <h1>Something went wrong.</h1>
          <p>The error has been reported. Try reloading the page.</p>
          <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

> **📝 Why this is still a class**
>
> There is no hook equivalent for
>
> getDerivedStateFromError
>
> /
>
> componentDidCatch
>
> yet, so error boundaries remain class components. You write it once and never touch it again — everything inside can be modern function components.

### 7 Wrap the app in `src/main.jsx`

```python
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ErrorBoundary from "./components/ErrorBoundary";
import App from "./App";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
);
```

> **💡 Where to place the boundary**
>
> At the very top it catches everything (shown above). You can
>
> also
>
> wrap smaller sections (e.g. just the dashboard) with their own boundaries so a crash in one widget doesn't blank the whole app. Start with one at the root.

### 8 Trigger a crash and verify end to end

Add a temporary component that throws during render and drop it into a page:

```html
function Boom() {
  throw new Error("frontend boom for testing");
}
// render <Boom /> somewhere, e.g. on the Dashboard, to test.
```

Run both servers, load the page that renders `<Boom />`, and confirm:

- You see the **fallback UI** ("Something went wrong." + Reload), not a blank white page.
- DevTools → Network shows a `POST /client-logs` returning `202`.
- Your backend terminal prints a JSON `"client error"` line:

```json
{"timestamp": "2026-06-26T14:25:40.880Z", "level": "ERROR", "logger": "app.client", "message": "client error", "request_id": "b4d9f1a0", "client_message": "frontend boom for testing", "client_url": "http://localhost:5173/dashboard", "client_stack": "\n    at Boom ...\n    at Dashboard ..."}
```

Remove the `<Boom />` component when done.

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| The catch-all 500 hides a real 404/401 | You're catching `HTTPException`. Only register `@app.exception_handler(Exception)`; let FastAPI keep handling `HTTPException` itself. |
| `/health/ready` always 200 even with no DB | You didn't actually execute a query. Use `db.execute(text("SELECT 1"))` and wrap it in `try/except`. |
| Error boundary doesn't catch the crash | The error is in an event handler or async code (boundaries only catch render errors), or the throwing component isn't inside the boundary. Test by throwing during render. |
| In dev, React shows its own error overlay first | That's Vite's dev overlay — dismiss it (or press Esc). Your fallback still rendered underneath; the overlay doesn't appear in a production build. |
| `POST /client-logs` fails with CORS | Add it under your existing CORS config; it's a normal POST so the Module 7 allowlist covers it (match the frontend origin). |
| Reporter throws and re-crashes the page | Keep the whole `fetch` inside `try/catch` in `reportClientError` — never let it raise. |

## 📄 Complete `src/components/ErrorBoundary.jsx`

```python
import { Component } from "react";
import { reportClientError } from "../api";

export default class ErrorBoundary extends Component {
  state = { hasError: false };

  static getDerivedStateFromError(_error) {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    reportClientError(error, info?.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div role="alert" style={{ maxWidth: 480, margin: "60px auto", textAlign: "center" }}>
          <h1>Something went wrong.</h1>
          <p>The error has been reported. Try reloading the page.</p>
          <button onClick={() => window.location.reload()}>Reload</button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

## 🎉 Module 8 complete

Your Tasks app is now **observable end to end**:

- **8.1** — structured JSON logs to stdout, a request-logging middleware, and a request id on every line + `X-Request-ID` header.
- **8.2** — a catch-all exception handler that logs tracebacks and returns clean 500s, `/health` + `/health/ready`, a `/client-logs` sink, and a React error boundary that turns crashes into a graceful fallback you actually hear about.

When something goes wrong now — backend or frontend — it's caught, logged with context, and traceable by id. That's exactly what you need before exposing the app to the world. Next you'll take it to production: real builds, containers, and a load balancer.

> **📝 You just earned health checks for free**
>
> Those
>
> /health
>
> and
>
> /health/ready
>
> endpoints aren't just nice to have — Nginx and Docker will
>
> call
>
> them in Module 9 to route around dead replicas. You built them at exactly the right time.

**Up next → Module 9, Chunk 9.1: Production Builds & Environments.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
