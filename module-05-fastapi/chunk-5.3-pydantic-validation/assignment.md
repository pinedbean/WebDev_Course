*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.3 — Lab: Typed Schemas & Validation

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Upgrade your CRUD API from Chunk 5.2 to use **Pydantic v2 schemas** and real **JSON request bodies**. Define `TaskBase`, `TaskCreate`, `TaskUpdate`, and `TaskRead`, wire them into your routes with `response_model`, and verify automatic validation.

## Before you start

- Continue in `tasks-api` with the venv active and `uvicorn main:app --reload` running.
- You already have Pydantic — it installed with FastAPI in 5.1. Confirm v2 with `pip show pydantic` (Version 2.x).
- Keep storing tasks as dicts in the in-memory list; only the request/response handling changes.

> **⚠️ Try it yourself first**
>
> The lecture shows every piece. Assemble it yourself, run it, and break it on purpose to see the 422s before checking the solution.

## Tasks

### 1 Define the four schemas

Near the top of `main.py` (after the imports), define:

- `TaskBase` — `title` (1–200 chars via `Field`) and `description: str | None = None`.
- `TaskCreate(TaskBase)` — inherits the base fields.
- `TaskUpdate` — `title`, `description`, and `completed`, all optional (default `None`).
- `TaskRead(TaskBase)` — adds `id: int`, `completed: bool`, `created_at: datetime`.

### 2 Convert `POST /tasks` to a body

Change the signature to take a single `payload: TaskCreate`. Build the stored dict from `payload.model_dump()` plus the server-owned fields (`id`, `completed=False`, `created_at`). Add `response_model=TaskRead` and keep status 201.

### 3 Add `response_model` to the read routes

Set `response_model=list[TaskRead]` on `GET /tasks` and `response_model=TaskRead` on `GET /tasks/{task_id}`. Keep the `completed` filter and the 404 behavior.

### 4 Convert `PATCH` to `TaskUpdate`

Take `payload: TaskUpdate`, find the task (404 if missing), and merge with `payload.model_dump(exclude_unset=True)` so only provided fields change. Return with `response_model=TaskRead`.

### 5 Leave DELETE as-is

`DELETE /tasks/{task_id}` still takes only a path param and returns 204 — no body, no schema needed.

### 6 Test the happy path in `/docs`

Notice POST/PATCH now show an editable JSON body with an example. Create a task by sending `{"title": "Read docs"}`, list tasks, and PATCH it with `{"completed": true}`.

### 7 Test validation failures

Deliberately send bad data and confirm you get a **422**:

- `POST /tasks` with `{}` (missing `title`).
- `POST /tasks` with `{"title": ""}` (too short).
- `POST /tasks` with `{"title": 123}` (wrong type) — note Pydantic may coerce; try a list instead to force an error.

Read the `detail` array and find the `loc` that points to the bad field.

## ✅ Deliverable — acceptance checklist

- `TaskBase`, `TaskCreate`, `TaskUpdate`, and `TaskRead` are defined as Pydantic v2 models.
- `POST /tasks` accepts a JSON body (`TaskCreate`) and returns 201 with a `TaskRead`.
- `GET /tasks` uses `response_model=list[TaskRead]`; single GET uses `TaskRead`.
- `PATCH` uses `TaskUpdate` + `exclude_unset=True` for true partial updates.
- Sending an invalid body returns a **422** with a helpful `detail`.
- `title` has a length constraint; an empty title is rejected.
- DELETE still returns 204; `/health` still works.

## 🚀 Stretch goals (optional)

- Add an example to a schema via `model_config = {"json_schema_extra": {"examples": [...]}}` and see it appear in `/docs`.
- Add a custom field validator that strips whitespace from `title` and rejects titles that are only spaces.
- Add a `due_date: datetime | None = None` field to the schemas and confirm ISO date strings validate.
- Return a `409 Conflict` if a task with the exact same title already exists.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
