*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.4 — Project Structure & Routers

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why a single `main.py` stops scaling, and how to split into an `app/` package.
- **APIRouter** — grouping related routes and mounting them with `include_router`.
- **Dependency injection** with `Depends` — reusing logic like "find this task or 404".
- **Settings/config** with `pydantic-settings` and environment variables.
- How the new layout runs: `uvicorn app.main:app --reload`.

In the lab you'll refactor your one-file API into a clean, growable package — no behavior change, much better organization.

## 1. Why split the file?

Your `main.py` now holds imports, schemas, storage, and every route. It works, but it's heading toward hundreds of lines where everything touches everything. As soon as Module 6 adds a database and Module 7 adds users, a single file becomes painful to navigate and risky to change.

The fix is **separation of concerns**: each file has one job. Here's the layout we'll build — the same shape real FastAPI projects use, and the one Module 6/7/capstone extend:

```text
tasks-api/
├── .venv/
├── .gitignore
├── requirements.txt
└── app/
    ├── __init__.py        # marks "app" as a Python package
    ├── main.py            # creates the FastAPI app, includes routers
    ├── config.py          # settings (app name, CORS origins, ...)
    ├── schemas.py         # Pydantic models (TaskBase/Create/Update/Read)
    ├── storage.py         # the in-memory store + access functions
    ├── dependencies.py    # shared dependencies (get_task_or_404, pagination)
    └── routers/
        ├── __init__.py
        ├── health.py      # GET /health
        └── tasks.py       # the /tasks CRUD routes
```

> **📝 What's `__init__.py`?**
>
> An (often empty) file that tells Python "this folder is a package", so you can do
>
> from app.routers import tasks
>
> . One per package folder (
>
> app/
>
> and
>
> app/routers/
>
> ).

## 2. APIRouter — routes in their own file

An **APIRouter** is a mini-FastAPI you can attach routes to, then mount onto the main app. It works exactly like `app`, but lives in its own module. In `app/routers/tasks.py`:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("")          # full path becomes  GET /tasks
def list_tasks():
    ...

@router.get("/{task_id}")  # full path becomes  GET /tasks/{task_id}
def get_task(task_id: int):
    ...
```

- `prefix="/tasks"` — every route here is automatically under `/tasks`, so you write `""` and `"/{task_id}"`.
- `tags=["tasks"]` — groups these endpoints together in `/docs` under a "tasks" heading.

Then in `app/main.py` you create the app and **include** the routers:

```python
from fastapi import FastAPI
from app.routers import health, tasks

app = FastAPI(title="Tasks API")

app.include_router(health.router)
app.include_router(tasks.router)
```

The app no longer defines routes itself — it just wires routers together. New feature later? Add a file under `routers/` and one `include_router` line.

## 3. A storage module

Move the in-memory list and its access functions into `app/storage.py`. Routers stop touching the list directly and call named functions instead — this is the seed of the **repository pattern** you'll formalize in Module 6 when these functions start hitting SQLite.

```python
# app/storage.py
from datetime import datetime

_tasks: list[dict] = []
_next_id: int = 1

def get_all() -> list[dict]:
    return _tasks

def get_by_id(task_id: int) -> dict | None:
    return next((t for t in _tasks if t["id"] == task_id), None)

def add(data: dict) -> dict:
    global _next_id
    task = {
        "id": _next_id,
        "completed": False,
        "created_at": datetime.now(),
        **data,                      # title, description from the request
    }
    _tasks.append(task)
    _next_id += 1
    return task
```

Why does the swap to SQLite later become easy? Because routers only know `storage.get_all()`, `storage.add(...)`, etc. Change *how* storage works without changing a single route. That's the payoff of separation.

## 4. Dependency injection with `Depends`

Notice every "single task" route repeats the same lines: look up the task, raise 404 if missing. FastAPI's **dependency injection** lets you write that logic once as a function and "inject" its result into any route.

A dependency is just a function. Declare a parameter as `= Depends(that_function)` and FastAPI runs it first, passing the result in. In `app/dependencies.py`:

```python
from fastapi import HTTPException
from app import storage

def get_task_or_404(task_id: int) -> dict:
    task = storage.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

Now routes that need an existing task just ask for one:

```python
from fastapi import Depends
from app.dependencies import get_task_or_404

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task: dict = Depends(get_task_or_404)):
    return task                # already guaranteed to exist
```

FastAPI sees the dependency needs `task_id`, pulls it from the path, runs `get_task_or_404`, and hands the route a ready task (or already returned a 404). No repeated lookup-and-check in every route.

> **💡 Dependencies are everywhere**
>
> This same mechanism powers a
>
> huge
>
> amount of FastAPI: in Module 6 you'll inject a database session, and in Module 7 a "current logged-in user". Get comfortable with
>
> Depends
>
> now — it's one of FastAPI's most important ideas.

### A reusable params dependency

Dependencies can also bundle query params. A pagination dependency keeps `limit`/`offset` consistent across endpoints:

```python
def pagination_params(limit: int = 20, offset: int = 0) -> dict:
    return {"limit": limit, "offset": offset}

@router.get("", response_model=list[TaskRead])
def list_tasks(page: dict = Depends(pagination_params)):
    items = storage.get_all()
    return items[page["offset"] : page["offset"] + page["limit"]]
```

(Chunk 5.6 turns this into a proper paginated response envelope — for now it just slices the list.)

## 5. Settings & config

Hard-coding things like the app name or which frontend URLs may call your API is fragile — those differ between your laptop and production. `pydantic-settings` (a companion to Pydantic) reads **environment variables** into a typed `Settings` object, with sensible defaults.

```bash
pip install pydantic-settings
```

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Tasks API"
    cors_origins: list[str] = ["http://localhost:5173"]   # the Vite dev server

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

- Each field has a **default**, so it works with no setup.
- `env_file=".env"` lets you override values via a `.env` file (already git-ignored from 5.1).
- `@lru_cache` means `get_settings()` builds the object once and reuses it.

Use it where needed:

```python
from app.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)
```

> **📝 Why `cors_origins` already?**
>
> You'll need it in the very next chunk. Chunk 5.5 connects your React app, and CORS decides which origins are allowed to call the API. Defining it in settings now means 5.5 just reads it.

## 6. Running the restructured app

The app object now lives at `app/main.py`, so the import path changes. Run from the **project root** (the `tasks-api` folder, the parent of `app/`):

```bash
uvicorn app.main:app --reload
```

Read it as "from the `app.main` module, use the `app` object". Everything else — `/docs`, your endpoints, behavior — is identical. You only reorganized.

> **⚠️ Run from the right folder**
>
> Run Uvicorn from
>
> tasks-api/
>
> , not from inside
>
> app/
>
> . If you see
>
> ModuleNotFoundError: No module named 'app'
>
> , you're in the wrong directory or missing an
>
> __init__.py
>
> .

## ✅ Recap

- Split the monolith into an `app/` package: `main`, `config`, `schemas`, `storage`, `dependencies`, and `routers/`.
- **APIRouter** groups routes (with `prefix` + `tags`); `app.include_router(...)` mounts them.
- A **storage module** hides the data details — easy to swap for SQLite later.
- **`Depends`** injects shared logic (like `get_task_or_404`) so routes stay DRY.
- **`pydantic-settings`** gives typed config from env vars, including `cors_origins` for the next chunk.
- Run it with `uvicorn app.main:app --reload` from the project root.

**Next:** open `assignment.html` and refactor your Tasks API into the package layout.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
