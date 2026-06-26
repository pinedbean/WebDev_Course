*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll create each file in the `app/` package. The code is the same logic from Chunk 5.3, just reorganized. End state:

```text
tasks-api/
├── requirements.txt
└── app/
    ├── __init__.py        (empty)
    ├── main.py
    ├── config.py
    ├── schemas.py
    ├── storage.py
    ├── dependencies.py
    └── routers/
        ├── __init__.py    (empty)
        ├── health.py
        └── tasks.py
```

### 1 Create the folders & install the dep

```bash
# from the tasks-api project root, with the venv active
pip install pydantic-settings
pip freeze > requirements.txt

mkdir -p app/routers
touch app/__init__.py app/routers/__init__.py
```

(You can also delete the old top-level `main.py` once the new package works.)

### 2 `app/schemas.py`

```python
from datetime import datetime
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None

class TaskRead(TaskBase):
    id: int
    completed: bool
    created_at: datetime
```

### 3 `app/storage.py`

The store and its access functions. Routers will only call these.

```python
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
        **data,                      # title, description
    }
    _tasks.append(task)
    _next_id += 1
    return task

def update(task_id: int, changes: dict) -> dict | None:
    task = get_by_id(task_id)
    if task is None:
        return None
    task.update(changes)
    return task

def delete(task_id: int) -> bool:
    task = get_by_id(task_id)
    if task is None:
        return False
    _tasks.remove(task)
    return True
```

### 4 `app/config.py`

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Tasks API"
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### 5 `app/dependencies.py`

```python
from fastapi import HTTPException, status
from app import storage

def get_task_or_404(task_id: int) -> dict:
    task = storage.get_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task

def pagination_params(limit: int = 20, offset: int = 0) -> dict:
    return {"limit": limit, "offset": offset}
```

### 6 `app/routers/health.py`

```python
from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
def health_check():
    return {"status": "ok"}
```

### 7 `app/routers/tasks.py`

All routes use the `/tasks` prefix. The single-task routes inject `get_task_or_404`, so the 404 logic lives in exactly one place.

```python
from fastapi import APIRouter, Depends, status

from app import storage
from app.dependencies import get_task_or_404
from app.schemas import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskRead])
def list_tasks(completed: bool | None = None):
    tasks = storage.get_all()
    if completed is None:
        return tasks
    return [t for t in tasks if t["completed"] == completed]

@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    return storage.add(payload.model_dump())

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task: dict = Depends(get_task_or_404)):
    return task

@router.patch("/{task_id}", response_model=TaskRead)
def update_task(payload: TaskUpdate, task: dict = Depends(get_task_or_404)):
    task.update(payload.model_dump(exclude_unset=True))
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task: dict = Depends(get_task_or_404)):
    storage.delete(task["id"])
    return None
```

> **📝 Empty path with a prefix**
>
> Because the router has
>
> prefix="/tasks"
>
> , the list/create routes use
>
> ""
>
> — the full path becomes
>
> /tasks
>
> . The single-item routes use
>
> "/{task_id}"
>
> .

### 8 `app/main.py`

The app just wires routers together — no route bodies here.

```python
from fastapi import FastAPI

from app.config import get_settings
from app.routers import health, tasks

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.include_router(health.router)
app.include_router(tasks.router)
```

### 9 Run from the project root

```bash
uvicorn app.main:app --reload
```

Open `/docs`. Endpoints are now grouped under **tasks** and **health** tags. Re-run your CRUD checks from Chunk 5.3 — identical behavior, cleaner code.

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: No module named 'app'` | Run Uvicorn from the `tasks-api` root (the parent of `app/`), and ensure `app/__init__.py` exists. |
| `ModuleNotFoundError: No module named 'app.routers'` | Add the empty `app/routers/__init__.py`. |
| `ImportError: cannot import name 'BaseSettings' from 'pydantic'` | In Pydantic v2 it moved — import from `pydantic_settings`, and run `pip install pydantic-settings`. |
| GET `/tasks` 404s but `/tasks/` works (or vice-versa) | Use `@router.get("")` with the prefix; don't add an extra slash. |
| Circular import between `storage` and `dependencies` | Keep `storage.py` free of FastAPI imports; only `dependencies.py` imports `storage`, never the reverse. |
| Old `main.py` still runs | You're launching `main:app` instead of `app.main:app`. Update the Uvicorn command. |

## 🎉 You're done

Your API is now a real project: routers per feature, schemas and storage isolated, shared logic injected with `Depends`, and config driven by settings. This is the exact skeleton Modules 6 and 7 build on.

**Up next → Chunk 5.5: CORS & Connecting React ↔ FastAPI** — you'll add CORS middleware (using the `cors_origins` you just set up) and call this API from your React + Vite frontend.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
