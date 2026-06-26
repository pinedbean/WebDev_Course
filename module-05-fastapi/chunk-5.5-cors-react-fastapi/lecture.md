*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.5 — CORS & Connecting React ↔ FastAPI

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What the browser's **same-origin policy** is and why it blocks your fetch.
- What **CORS** is and how to enable it with FastAPI's `CORSMiddleware`.
- The **preflight** request and which calls trigger one.
- Using an **environment variable** (`VITE_API_URL`) for the API base URL.
- The full request lifecycle: React `fetch` → Uvicorn → FastAPI → JSON → React state.

In the lab you'll connect a React + Vite frontend to your Tasks API and do live CRUD from the UI.

## 1. Two servers, two origins

In development you'll run **two** servers at once:

| Server | URL (origin) | Serves |
| --- | --- | --- |
| FastAPI / Uvicorn | `http://localhost:8000` | The Tasks API (JSON) |
| Vite dev server | `http://localhost:5173` | The React app (UI) |

An **origin** is the combination of *scheme + host + port*. Because the ports differ (5173 vs 8000), these are **different origins**. When your React code calls `fetch("http://localhost:8000/tasks")`, the browser sees a **cross-origin** request — and by default, blocks reading the response.

## 2. The same-origin policy & CORS

Browsers enforce the **same-origin policy**: by default, JavaScript on one origin can't read responses from another origin. It's a security rule that stops a malicious site from quietly calling APIs you're logged into. Without it, any page could read your bank's API using your session.

But legitimate apps *do* need cross-origin calls (your frontend and backend are separate origins). The official escape hatch is **CORS** — *Cross-Origin Resource Sharing*. The **server** sends special response headers that tell the browser "this origin is allowed to read my responses". The key one:

```
Access-Control-Allow-Origin: http://localhost:5173
```

When the browser sees its origin listed, it lets your JS read the response. If the header is missing, the request still *reaches* the server, but the browser **hides the response** from your code and logs a CORS error in the console.

> **⚠️ CORS is a browser thing**
>
> A CORS error means the
>
> browser
>
> blocked you — not that the server failed. The request often succeeded server-side. That's why
>
> curl
>
> and the
>
> /docs
>
> page work fine (no browser origin check) while your React app gets blocked. Fix it on the
>
> server
>
> .

## 3. The preflight request

For "non-simple" requests — anything with a JSON body, a `PATCH`/`DELETE` method, or custom headers — the browser first sends a quiet **preflight**: an `OPTIONS` request asking "am I allowed to do this?" Only if the server's CORS headers approve does the browser send the real request.

```text
React fetch (POST /tasks, JSON)
   │
   ├─ 1. Browser sends  OPTIONS /tasks   (preflight: "may I POST JSON here?")
   │      Server replies with Access-Control-Allow-* headers
   │
   └─ 2. Browser sends  POST /tasks      (the real request)
          Server replies 201 + the new task
```

You don't write preflight handling — `CORSMiddleware` answers `OPTIONS` automatically. Just know that in DevTools' Network tab you'll often see an `OPTIONS` call right before your `POST`. That's normal.

## 4. Enabling CORS in FastAPI

FastAPI ships with `CORSMiddleware` (from Starlette). **Middleware** is code that wraps every request/response — perfect for adding CORS headers globally. Add it in `app/main.py`, reading the allowed origins from the settings you created in Chunk 5.4:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import health, tasks

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,   # ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],                   # GET, POST, PATCH, DELETE, OPTIONS...
    allow_headers=["*"],                   # including Content-Type
)

app.include_router(health.router)
app.include_router(tasks.router)
```

- `allow_origins` — the exact frontend origins permitted. List them precisely; don't use `["*"]` in real apps (especially with credentials).
- `allow_methods` / `allow_headers` — `["*"]` is fine in dev; it permits your JSON `Content-Type` and all CRUD methods.

> **⚠️ localhost ≠ 127.0.0.1 (for CORS)**
>
> To the browser,
>
> http://localhost:5173
>
> and
>
> http://127.0.0.1:5173
>
> are
>
> different
>
> origins. Allow whichever one your browser actually shows in the address bar — or add both to
>
> cors_origins
>
> . Mismatch here is the #1 cause of "I enabled CORS but it still fails".

## 5. The API URL as an environment variable

Hard-coding `http://localhost:8000` in your React code breaks the day you deploy (the API moves to a real domain). Vite exposes env vars prefixed with `VITE_` to your frontend code. Create a `.env` file in the **frontend** project root:

```
# tasks-frontend/.env
VITE_API_URL=http://localhost:8000
```

Read it anywhere in your React code via `import.meta.env`:

```javascript
const BASE_URL = import.meta.env.VITE_API_URL;
// later: fetch(`${BASE_URL}/tasks`)
```

> **📝 Restart Vite after editing `.env`**
>
> Vite only reads
>
> .env
>
> at startup. Change it? Stop and re-run
>
> npm run dev
>
> . Also add
>
> .env
>
> to
>
> .gitignore
>
> — env files don't belong in Git.

## 6. A tiny API client

Keep all fetch calls in one module (`src/api.js`) so components stay clean. Each function returns parsed JSON or throws on a non-OK status. Note the JSON body needs `Content-Type: application/json` and `JSON.stringify`:

```javascript
const BASE_URL = import.meta.env.VITE_API_URL;

export async function getTasks() {
  const res = await fetch(`${BASE_URL}/tasks`);
  if (!res.ok) throw new Error(`Failed to load tasks (${res.status})`);
  return res.json();
}

export async function createTask(title) {
  const res = await fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error(`Failed to create task (${res.status})`);
  return res.json();
}

export async function toggleTask(id, completed) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) throw new Error(`Failed to update task (${res.status})`);
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Failed to delete task (${res.status})`);
}
```

This mirrors your backend exactly: `getTasks` → `GET /tasks`, `createTask` → `POST /tasks`, and so on. Same skills as the public-API fetch from Chunk 4.4 — now pointed at *your* server.

## 7. Wiring it into a component

Using `useState` and `useEffect` (Chunks 4.3–4.4), load tasks on mount and re-fetch after each change. Here's the shape — note the escaped JSX:

```python
import { useEffect, useState } from "react";
import { getTasks, createTask, toggleTask, deleteTask } from "./api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);

  async function load() {
    try {
      setTasks(await getTasks());
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => { load(); }, []);

  async function handleAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;
    await createTask(title.trim());
    setTitle("");
    load();                       // refresh from the server
  }

  return (
    <main>
      <h1>✅ Tasks</h1>
      {error && <p className="error">{error}</p>}

      <form onSubmit={handleAdd}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task…"
        />
        <button type="submit">Add</button>
      </form>

      <ul>
        {tasks.map((t) => (
          <li key={t.id}>
            <input
              type="checkbox"
              checked={t.completed}
              onChange={() => toggleTask(t.id, !t.completed).then(load)}
            />
            {t.title}
            <button onClick={() => deleteTask(t.id).then(load)}>🗑</button>
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;
```

The pattern: call the API, then `load()` to re-sync state with the server. (You could update local state directly for snappier UX; re-fetching keeps it simple and always correct.)

## 8. The full lifecycle

When you check a task's box, here's the round trip:

1. React calls `toggleTask(id, true)` → `fetch` a `PATCH` with a JSON body.
2. The browser sends a CORS **preflight** (`OPTIONS`); `CORSMiddleware` approves it.
3. The browser sends the real `PATCH /tasks/3`; **Uvicorn** hands it to **FastAPI**.
4. FastAPI validates the body (`TaskUpdate`), updates the in-memory store, returns `TaskRead` JSON (200).
5. CORS headers let the browser expose the response; `load()` re-fetches and React re-renders.

That's a full-stack write — from a click in the browser to your Python code and back. Everything you've built across Modules 4 and 5 working together.

## ✅ Recap

- Frontend (`:5173`) and backend (`:8000`) are **different origins**; the browser's same-origin policy blocks cross-origin reads.
- **CORS** is the server opting in via response headers; enable it with `CORSMiddleware` and your `cors_origins` setting.
- JSON/PATCH/DELETE calls trigger an automatic **preflight** `OPTIONS` — the middleware handles it.
- Store the API base in `VITE_API_URL` and read it with `import.meta.env`; restart Vite after edits.
- A small `api.js` wraps `fetch` for each endpoint; components call it and re-sync state.
- Watch the `localhost` vs `127.0.0.1` trap — they're different origins to the browser.

**Next:** open `assignment.html` and connect a React frontend to your Tasks API end to end.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
