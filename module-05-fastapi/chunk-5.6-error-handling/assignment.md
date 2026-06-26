*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.6 — Lab: Harden the API + 🏁 Module Checkpoint

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Polish your Tasks API: add consistent error responses with global exception handlers, pagination on the list endpoint, and a `/api/v1` version prefix. Then complete the **Module 5 Checkpoint** — a full CRUD Tasks API consumed by your React frontend (still in-memory).

## Before you start

- Continue from your Chunk 5.5 backend (`app/` package + CORS) and your React frontend.
- Backend running: `uvicorn app.main:app --reload`; frontend: `npm run dev`.

> **⚠️ Try it yourself first**
>
> The lecture shows each piece. Build it, break it on purpose (request a missing task, send bad data, page past the end), and confirm the error shape stays consistent before checking the solution.

## Part A — Harden the backend

### 1 Create `app/errors.py`

Define a `TaskNotFound` exception and a `register_exception_handlers(app)` function that adds handlers for `TaskNotFound`, `HTTPException`, and `RequestValidationError` — each returning the `{"error": {"code", "message"}}` envelope (validation also includes `details`).

### 2 Use the custom exception

Update `get_task_or_404` in `dependencies.py` to raise `TaskNotFound(task_id)` instead of `HTTPException`. Register the handlers in `main.py`.

### 3 Add pagination

Add a `TaskPage` schema (`items`, `total`, `limit`, `offset`). Change `GET /tasks` to use the `pagination_params` dependency, slice the (optionally filtered) list, and return a `TaskPage`. Cap `limit` sensibly (e.g. `le=100`).

### 4 Version the routes

Include the tasks router under `prefix="/api/v1"` so tasks live at `/api/v1/tasks`. Keep `/health` unversioned.

### 5 Verify the hardening

In `/docs`: confirm tasks are now under `/api/v1`; request a missing id (consistent 404 envelope); send an invalid body (consistent 422 with `details`); list with `?limit=2&offset=0` and check the `total`.

## Part B — Reconnect the frontend

### 6 Update the API base URL

Because routes moved to `/api/v1`, update the frontend `.env` to `VITE_API_URL=http://localhost:8000/api/v1` and restart Vite. (Health checks, if you call them, use the root URL.)

### 7 Read the paginated shape

`GET /tasks` now returns an object. Update `getTasks()` to return `data.items` (and optionally surface `total`). Confirm the list still renders.

### 8 Show real error messages

Update the frontend error handling to read the new envelope (`data.error.message`) when a request fails, and display it. Trigger it by submitting an empty title or deleting a non-existent task.

## 🏁 Module 5 Checkpoint

Tie the whole module together. You should end with a **full CRUD Tasks API** (in-memory) consumed by a working React frontend. Demonstrate the complete loop:

- **Backend:** a structured FastAPI app — `/api/v1/tasks` CRUD with Pydantic schemas, validation, consistent error envelope, pagination, CORS, and an unversioned `/health`.
- **Frontend:** a React + Vite app that lists, creates, toggles, and deletes tasks via the API, using `VITE_API_URL`, handling loading and errors.
- **Proof:** a task created in `/docs` appears in the UI; a task created in the UI appears in `/docs`; restarting the server clears the data (still in-memory).

Write a short `README.md` in `tasks-api` with run instructions for both servers — you'll thank yourself in Module 6.

## ✅ Deliverable — acceptance checklist

- All errors (404, 422, other `HTTPException`s) share the `{"error": {...}}` envelope.
- `TaskNotFound` is raised in logic and translated by a registered handler.
- `GET /api/v1/tasks` returns a `TaskPage` with `items`, `total`, `limit`, `offset`.
- Tasks are served under `/api/v1`; `/health` stays at the root.
- The frontend points at `/api/v1`, reads `data.items`, and shows server error messages.
- Full CRUD works end to end from the React UI (the Module Checkpoint).
- A `README.md` documents how to run backend + frontend.

## 🚀 Stretch goals (optional)

- Add a `409 Conflict` (custom exception) when creating a task whose title already exists.
- Add `next_offset`/`has_more` to `TaskPage` and a "Load more" button in the UI.
- Add a catch-all handler for unexpected `Exception`s returning a generic 500 envelope (don't leak details).
- Add a `sort` query param (e.g. by `created_at` or `title`).
- Write the `requirements.txt` and a one-command dev script; sketch what changes when SQLite arrives in Module 6.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
