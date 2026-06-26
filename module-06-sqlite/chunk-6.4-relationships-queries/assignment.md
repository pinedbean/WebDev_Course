*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.4 — Lab + 🏁 Module 6 Checkpoint

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Two parts. **Part A**: add a `User` entity related to `Task` (one user → many tasks), with a foreign key, an Alembic migration, and filtering/sorting query params. **Part B (the 🏁 Module 6 Checkpoint)**: connect a React frontend to this API so you have a complete full-stack CRUD app with persistent, *related* data — users, their tasks, create/toggle/delete, and filtering.

## Before you start

- Continue from your Chunk 6.3 project (persistent Tasks API with Alembic), venv active.
- Install the email validator for `EmailStr`: `pip install "pydantic[email]"`
- For the checkpoint you'll reuse a React + Vite app (from Module 4/5). CORS was configured in Module 5 — keep your frontend origin allowed.

> **⚠️ Try it yourself first**
>
> Lean on the lecture's model and query code. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Part A — Add the User relationship

### 1 Add the `User` model & the FK

In `models.py`, add a `User` model (table `users`) with `id`, `email` (`unique=True, index=True`), and `created_at`. Add `owner_id` (a `ForeignKey("users.id")`, `index=True`) to `Task`, and a `relationship()` on each side linked with `back_populates` (`User.tasks` ↔ `Task.owner`).

### 2 Enforce foreign keys in SQLite

Add an event listener so every SQLite connection runs `PRAGMA foreign_keys=ON` (otherwise SQLite ignores the FK). The snippet goes in `database.py` — see the lecture/solution.

### 3 Add schemas for users & owner

Add `UserCreate` (just `email`) and `UserRead` (with nested `tasks`). Add `owner_id` to `TaskRead`, and accept `owner_id` when creating a task (e.g. on `TaskCreate`).

### 4 CRUD & endpoints for users

Add to `crud.py`: `create_user`, `get_user`, `get_users`. Add endpoints: `POST /users`, `GET /users`, `GET /users/{user_id}` (404 if missing). When creating a task, store its `owner_id`.

### 5 Filtering & sorting on `GET /tasks`

Add optional query params to `GET /tasks`: `completed: bool | None`, `owner_id: int | None`, and `sort` (e.g. `created_at` or `title`). Build the `select()` conditionally so each filter is optional.

### 6 Migrate the schema

Generate and apply a migration for the new table, FK, and indexes:

```bash
alembic revision --autogenerate -m "add users and task owner_id"
alembic upgrade head
```

Read the generated file first. Then test in `/docs`: create a user, create tasks with that user's `owner_id`, and fetch `GET /users/{id}` to see tasks nested under the user. Try `GET /tasks?owner_id=1&completed=false`.

## 🏁 Part B — Module 6 Checkpoint: the full-stack app

Wire a **React frontend** to your API so the whole stack runs end-to-end: **React → FastAPI → SQLite**, with persistent, related data. You're not building a new design — reuse your Module 4/5 React app and point it at these endpoints.

### 7 Run both servers

Backend: `uvicorn app.main:app --reload` (port 8000). Frontend: `npm run dev` (port 5173). Confirm CORS allows `http://localhost:5173` (from Module 5).

### 8 Pick / create a user in the UI

Add a small control to create a user (email input → `POST /users`) and a dropdown to select the "current" user from `GET /users`. Store the selected user's id in React state — it becomes the `owner_id` for new tasks.

### 9 Full task CRUD against the database

For the selected user, the UI must:

- **List** their tasks (`GET /tasks?owner_id=…`).
- **Create** a task (`POST /tasks` with the owner's id).
- **Toggle** completed (`PATCH /tasks/{id}`).
- **Delete** a task (`DELETE /tasks/{id}`).

### 10 Filter in the UI

Add an "All / Active / Completed" filter that re-fetches using the `completed` query param (or filters the fetched list). Show each task's owner so the relationship is visible.

### 11 Prove persistence end-to-end

Create users and tasks through the UI, then **restart the backend** and refresh the page. Everything is still there. Switch users and confirm each sees only their own tasks.

## ✅ Deliverable — acceptance checklist

- `User` model with unique, indexed `email`; `Task` has an indexed `owner_id` FK.
- `relationship()` on both sides (`User.tasks` ↔ `Task.owner`) with `back_populates`.
- SQLite foreign-key enforcement is turned on (PRAGMA event listener).
- An Alembic migration adds the `users` table, the FK, and the indexes; `alembic upgrade head` runs cleanly.
- `GET /users/{id}` returns the user with their tasks nested.
- `GET /tasks` supports optional `completed`, `owner_id`, and `sort` query params.
- **Checkpoint:** a React UI creates/selects a user and does full task CRUD for that user against the API.
- **Checkpoint:** data persists across a backend restart and tasks are scoped to the selected user.

## 🚀 Stretch goals (optional)

- Add a many-to-many `tags` table (association table) so a task can have multiple tags.
- Add pagination to `GET /tasks` with `limit` & `offset` query params.
- Use `selectinload` on `GET /users` to avoid the N+1 problem, and confirm fewer queries in the logs.
- Show a per-user task count in the UI (computed from `user.tasks`).
- Verify cascade delete: deleting a user removes their tasks too.

> **📝 Heads-up for Module 7**
>
> Right now the client chooses
>
> owner_id
>
> freely — anyone can act as anyone. That's intentional for learning relationships.
>
> Module 7
>
> adds passwords, login, and JWTs so
>
> owner_id
>
> comes from the authenticated user, and each person sees only their own tasks.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
