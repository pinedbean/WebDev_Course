*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.5 — Lab: Connect React to Your API

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Make your React frontend and FastAPI backend talk to each other. You'll enable CORS on the backend, point the frontend at the API via an environment variable, and build a Tasks UI that lists, creates, toggles, and deletes tasks — all through live HTTP calls to your own server.

## Before you start

- Your `tasks-api` backend from Chunk 5.4 (package layout, running with `uvicorn app.main:app --reload`).
- A React + Vite app. **Either** reuse your Module 4 project **or** scaffold a fresh one named `tasks-frontend` with `npm create vite@latest tasks-frontend -- --template react`, then `npm install`.
- You'll run **both** servers at once — backend on `:8000`, frontend on `:5173` — in two terminals.

> **⚠️ Try it yourself first**
>
> Expect a CORS error on your first fetch — that's the lesson. Read the console message, then fix it on the backend.

## Tasks

### 1 Reproduce the CORS error (on purpose)

Before enabling CORS, run both servers and make the frontend fetch `http://localhost:8000/tasks`. Open DevTools → Console and read the CORS error. Confirm in the Network tab that the request was actually *sent*.

### 2 Enable CORS on the backend

In `app/main.py`, add `CORSMiddleware` with `allow_origins=settings.cors_origins` (from your 5.4 config), allowing all methods and headers. Make sure `cors_origins` includes the exact origin your browser shows (`localhost` vs `127.0.0.1`).

### 3 Add the API URL env var

In the frontend root, create `.env` with `VITE_API_URL=http://localhost:8000`. Add `.env` to the frontend's `.gitignore`. Restart `npm run dev` so Vite picks it up.

### 4 Build the API client

Create `src/api.js` with functions `getTasks()`, `createTask(title)`, `toggleTask(id, completed)`, and `deleteTask(id)`. Each reads `import.meta.env.VITE_API_URL`, uses the right method, sets `Content-Type: application/json` for bodies, and throws on a non-OK response.

### 5 Build the Tasks UI

In `App.jsx`, load tasks on mount with `useEffect`. Render a form to add a task, a checkbox per task to toggle `completed`, and a delete button. After each create/toggle/delete, re-fetch the list so the UI stays in sync. Show an error message if a call fails.

### 6 Verify the full round trip

Add a task in the UI → confirm it appears (and persists across a page refresh while the server runs). Check a task → confirm it stays checked after refresh. Delete one → confirm it's gone. In the Network tab, spot the `OPTIONS` preflight before your `POST`/`PATCH`/`DELETE`.

### 7 Prove it's really your backend

Open `/docs` and create a task there. Refresh the React app — it should show up. Then restart Uvicorn and refresh again: the list is empty (in-memory data reset). This makes the frontend↔backend link concrete.

## ✅ Deliverable — acceptance checklist

- Backend has `CORSMiddleware` configured from `settings.cors_origins`.
- Frontend reads the API base URL from `VITE_API_URL` (no hard-coded URL).
- `src/api.js` wraps GET/POST/PATCH/DELETE against the Tasks API.
- The UI lists tasks, adds a task, toggles completion, and deletes a task — all hitting the live API.
- Data created in the React UI also appears in `/docs` (same backend).
- No CORS errors remain in the browser console.

## 🚀 Stretch goals (optional)

- Add loading and empty states ("Loading…", "No tasks yet").
- Show the backend's 422 `detail` message inline when a create fails validation (try an empty title).
- Optimistically update local state instead of re-fetching, then reconcile on error.
- Add an "editing" state to rename a task's title via `PATCH`.
- Extract a `useTasks()` custom hook (callback to Chunk 4.7) that owns loading + the list.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
