*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.4 — Lab: Refactor into a Package

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Refactor your single-file Tasks API into a clean `app/` package: separate `schemas`, `storage`, `config`, `dependencies`, and `routers`. Behavior stays identical — this is a structure-only change that sets you up for the database and auth modules.

## Before you start

- Work in your existing `tasks-api` project (venv active).
- Install the new dependency: `pip install pydantic-settings`, then refresh `pip freeze > requirements.txt`.
- Target layout:

```text
tasks-api/
└── app/
    ├── __init__.py
    ├── main.py
    ├── config.py
    ├── schemas.py
    ├── storage.py
    ├── dependencies.py
    └── routers/
        ├── __init__.py
        ├── health.py
        └── tasks.py
```

> **⚠️ Don't forget the `__init__.py` files**
>
> You need one in
>
> app/
>
> and one in
>
> app/routers/
>
> (both can be empty) or imports like
>
> from app.routers import tasks
>
> will fail.

## Tasks

### 1 Create the package skeleton

Make the `app/` folder and `app/routers/` subfolder with their `__init__.py` files. Create empty `config.py`, `schemas.py`, `storage.py`, `dependencies.py`, `main.py`, and the two router files.

### 2 Move the schemas

Cut the four Pydantic models (`TaskBase`, `TaskCreate`, `TaskUpdate`, `TaskRead`) into `app/schemas.py`, keeping their imports.

### 3 Build the storage module

In `app/storage.py`, hold the in-memory list and ID counter. Expose functions: `get_all()`, `get_by_id(task_id)`, `add(data)`, `update(task_id, changes)`, and `delete(task_id)`. Routers should call these instead of touching the list.

### 4 Add config

In `app/config.py`, define a `Settings(BaseSettings)` with `app_name` and `cors_origins` (default `["http://localhost:5173"]`), plus a cached `get_settings()`.

### 5 Add a dependency

In `app/dependencies.py`, write `get_task_or_404(task_id)` that looks the task up in storage and raises a 404 if missing. (Optional: add a `pagination_params` dependency too.)

### 6 Write the routers

`app/routers/health.py` holds a router with `GET /health`. `app/routers/tasks.py` holds an `APIRouter(prefix="/tasks", tags=["tasks"])` with all five CRUD routes — using `get_task_or_404` via `Depends` for the single-task routes.

### 7 Wire up `main.py`

In `app/main.py`, create the FastAPI app (title from settings) and `include_router` both routers. `main.py` should contain *no* route definitions of its own.

### 8 Run and verify nothing broke

From the project root run `uvicorn app.main:app --reload`. Open `/docs` — confirm endpoints are grouped under a "tasks" tag and every CRUD operation still behaves exactly as in Chunk 5.3.

## ✅ Deliverable — acceptance checklist

- The `app/` package exists with all the listed files and both `__init__.py` files.
- Schemas live in `schemas.py`; the store lives in `storage.py`.
- Routes are split into `routers/health.py` and `routers/tasks.py` using `APIRouter`.
- `main.py` only creates the app and includes routers (no route bodies).
- Single-task routes use `get_task_or_404` via `Depends`.
- `config.py` provides `Settings` with `cors_origins`, used for the app title.
- `uvicorn app.main:app --reload` runs and all CRUD + `/health` behave as before.

## 🚀 Stretch goals (optional)

- Add a `pagination_params` dependency and apply `limit`/`offset` slicing to `GET /tasks`.
- Create a `.env` file overriding `app_name` and confirm it shows in `/docs`.
- Add a root `GET /` route (in `main.py` or a small router) that redirects/points to `/docs`.
- Add a module-level docstring to each file describing its single responsibility.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
