*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.2 — Lab: In-Memory CRUD for Tasks

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Extend your `tasks-api` with a complete set of CRUD endpoints over an **in-memory list of tasks**. You'll practice path params, query params, status codes, and 404 handling — testing everything through `/docs`.

## Before you start

- Continue in the same `tasks-api` project from Chunk 5.1.
- Activate the venv (`source .venv/bin/activate`) and run `uvicorn main:app --reload`.
- Keep the `/docs` tab open — you'll send POST/PATCH/DELETE from there.

Each task is a dict with these fields: `id: int`, `title: str`, `description: str | None`, `completed: bool` (default `False`), `created_at` (an ISO timestamp string).

> **⚠️ Try it yourself first**
>
> Use the lecture's worked examples as building blocks, but write the endpoints yourself. Only open the solution to compare.

## Tasks

### 1 Add in-memory storage

At the top of `main.py`, add a module-level `tasks: list[dict] = []` and a `next_id` counter starting at 1. Write a small `find_task(task_id)` helper that returns the matching dict or `None`.

### 2 Create — `POST /tasks`

Accept `title: str` (required) and `description: str | None = None` as query parameters. Build the task dict (auto-assign `id`, set `completed=False` and `created_at`), append it, increment the counter, and return it with status **201**.

### 3 List — `GET /tasks`

Return the full list. Add an optional query param `completed: bool | None = None`: when provided, return only tasks whose `completed` matches; when omitted, return everything.

### 4 Read one — `GET /tasks/{task_id}`

Use a path param `task_id: int`. If the task exists, return it. If not, raise `HTTPException` with status **404** and a clear `detail` message.

### 5 Update — `PATCH /tasks/{task_id}`

Accept optional query params `title`, `description`, and `completed` (all default to `None`). Find the task (404 if missing) and update *only* the fields that were provided. Return the updated task.

### 6 Delete — `DELETE /tasks/{task_id}`

Find the task (404 if missing), remove it from the list, and return nothing with status **204**.

### 7 Exercise the API in `/docs`

Create 3 tasks. List them. Mark one completed via PATCH. Filter with `GET /tasks?completed=true`. Fetch a missing id (e.g. 999) and confirm a 404. Delete one and confirm a 204, then confirm it's gone from the list.

## ✅ Deliverable — acceptance checklist

- `GET /tasks` lists tasks and supports the `completed` filter.
- `GET /tasks/{task_id}` returns one task, or 404 with a `detail` message.
- `POST /tasks` creates a task and responds with status 201.
- `PATCH /tasks/{task_id}` updates only the provided fields; 404 if missing.
- `DELETE /tasks/{task_id}` removes a task and responds with status 204; 404 if missing.
- The `/health` endpoint from 5.1 still works.
- Every endpoint is testable in `/docs` and behaves as described.

## 🚀 Stretch goals (optional)

- Add a `GET /tasks/stats` route returning counts of total/completed/pending. (Remember: define it *before* `/tasks/{task_id}`.)
- Add query params `limit` and `offset` to `GET /tasks` for simple pagination.
- Validate that `title` isn't empty/whitespace; raise a 400 if it is.
- Add a `search: str | None` query param that filters tasks whose title contains the text (case-insensitive).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
