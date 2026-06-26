*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.3 — Lab: A Persistent CRUD API

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Turn your Tasks API into a fully persistent CRUD service. You'll build a `crud.py` repository layer, rewire every endpoint (`GET`/`POST`/`PATCH`/`DELETE`) to use it, delete the in-memory list for good, and replace `create_all` with a real **Alembic** migration. When you're done, data created through the API survives a server restart.

## Before you start

- Continue from your Chunk 6.2 project (the Tasks API connected to SQLite), venv active.
- Install Alembic into the venv: `pip install alembic`
- This lab changes how the schema is created. To avoid mixing the old `create_all` table with Alembic, plan to start from a fresh `tasks.db` (delete it before your first migration — instructions in the solution).

> **⚠️ Try it yourself first**
>
> Work from the lecture's
>
> crud.py
>
> and Alembic steps. Only open
>
> solution.html
>
> when stuck or to compare.

## Part A — Repository & DB-backed CRUD

### 1 Create `app/crud.py`

Write five functions, each taking a `Session` first: `get_tasks(db)`, `get_task(db, task_id)`, `create_task(db, data)`, `update_task(db, task, data)`, and `delete_task(db, task)`. Use `add`/`commit`/`refresh` for create, attribute assignment + `commit` for update, and `delete` + `commit` for delete. These functions must contain **no HTTP logic**.

### 2 Rewrite every endpoint to use `crud`

Update all five task endpoints to take `db: Session = Depends(get_db)` and delegate to `crud`:

- `GET /tasks` → `crud.get_tasks`
- `POST /tasks` → `crud.create_task` (return `201 Created`)
- `GET /tasks/{task_id}` → `crud.get_task` (404 if missing)
- `PATCH /tasks/{task_id}` → look up, 404 if missing, then `crud.update_task`
- `DELETE /tasks/{task_id}` → look up, 404 if missing, then `crud.delete_task` (return `204 No Content`)

### 3 Make PATCH partial

Ensure your update only changes the fields the client actually sent, using `data.model_dump(exclude_unset=True)`. Sending only `{"completed": true}` must not wipe the title or description.

### 4 Delete the in-memory store

Remove the old `tasks: list = []` and any code that used it. The database is now the only source of truth.

## Part B — Alembic migrations

### 5 Initialize Alembic

From the project root, run `alembic init alembic`. This creates the `alembic/` folder and `alembic.ini`.

### 6 Wire Alembic to your project

- In `alembic.ini`, set `sqlalchemy.url = sqlite:///./tasks.db`.
- In `alembic/env.py`, import your `Base` and your `models`, and set `target_metadata = Base.metadata`.
- Remove (or comment out) `Base.metadata.create_all(bind=engine)` from `main.py` — Alembic owns the schema now.

### 7 Generate & apply the first migration

Start from a clean database (delete any old `tasks.db`), then:

```bash
alembic revision --autogenerate -m "create tasks table"
alembic upgrade head
```

Open the generated file in `alembic/versions/` and read its `upgrade()` — it should create the `tasks` table with your five columns.

### 8 Test the full cycle & persistence

Run the server and use `/docs` to: create a task (POST), list tasks (GET), fetch one (GET by id), toggle it (PATCH `{"completed": true}`), and delete one (DELETE). Confirm a missing id returns 404. Then **restart the server** and verify your created tasks are still there.

## ✅ Deliverable — acceptance checklist

- `app/crud.py` exists with the five DB functions and no HTTP logic.
- All five task endpoints use `Depends(get_db)` and call into `crud`; the in-memory list is gone.
- `POST` returns 201, `DELETE` returns 204, missing ids return 404.
- PATCH only updates the fields sent (partial update via `exclude_unset`).
- An Alembic migration file exists under `alembic/versions/` that creates the `tasks` table.
- `alembic upgrade head` runs cleanly and `create_all` is no longer used.
- Tasks created via the API survive a full server restart.

## 🚀 Stretch goals (optional)

- Roll back and re-apply: `alembic downgrade -1` then `alembic upgrade head`. Watch the `tasks` table disappear and come back.
- Add a `priority` column (integer, default 0) to the `Task` model, then generate & apply a *second* migration for it. Confirm the schema changed without losing data.
- Check the current revision with `alembic current` and the history with `alembic history`.
- Add a simple unit test that calls `crud.create_task` against a temporary session.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
