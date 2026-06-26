*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.6 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll add an `errors.py`, paginate the list endpoint, version the routes, then reconnect the frontend and verify the full checkpoint. Final backend layout:

```text
tasks-api/
├── README.md
├── requirements.txt
└── app/
    ├── __init__.py
    ├── main.py          (CORS + exception handlers + /api/v1)
    ├── config.py
    ├── schemas.py       (+ TaskPage)
    ├── storage.py
    ├── dependencies.py  (raises TaskNotFound; pagination)
    ├── errors.py        (new)
    └── routers/
        ├── __init__.py
        ├── health.py
        └── tasks.py     (paginated list)
```

## Part A — Harden the backend

### 1 `app/errors.py`

```python
from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

class TaskNotFound(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task {task_id} does not exist")

def register_exception_handlers(app):
    @app.exception_handler(TaskNotFound)
    async def handle_task_not_found(request: Request, exc: TaskNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": {"code": "task_not_found", "message": str(exc)}},
        )

    @app.exception_handler(StarletteHTTPException)
    async def handle_http_exception(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": "http_error", "message": exc.detail}},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": jsonable_encoder(exc.errors()),
            }},
        )
```

> **📝 Why `StarletteHTTPException`?**
>
> FastAPI's
>
> HTTPException
>
> subclasses Starlette's. Registering the handler on the Starlette base class catches both your
>
> raise HTTPException(...)
>
> calls and framework-raised ones (like 405s).

### 2 Raise the custom exception — `app/dependencies.py`

```python
from fastapi import Query
from app import storage
from app.errors import TaskNotFound

def get_task_or_404(task_id: int) -> dict:
    task = storage.get_by_id(task_id)
    if task is None:
        raise TaskNotFound(task_id)
    return task

def pagination_params(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> dict:
    return {"limit": limit, "offset": offset}
```

`Query(20, ge=1, le=100)` documents and enforces the bounds — a request with `limit=9999` now fails validation (and returns your consistent 422).

### 3 Add `TaskPage` — append to `app/schemas.py`

```
class TaskPage(BaseModel):
    items: list[TaskRead]
    total: int
    limit: int
    offset: int
```

### 4 Paginate the list — `app/routers/tasks.py`

Only `list_tasks` changes; the rest of the router is unchanged from Chunk 5.4.

```python
from fastapi import APIRouter, Depends, status

from app import storage
from app.dependencies import get_task_or_404, pagination_params
from app.schemas import TaskCreate, TaskPage, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=TaskPage)
def list_tasks(
    completed: bool | None = None,
    page: dict = Depends(pagination_params),
):
    items = storage.get_all()
    if completed is not None:
        items = [t for t in items if t["completed"] == completed]

    total = len(items)
    start = page["offset"]
    window = items[start : start + page["limit"]]
    return {
        "items": window,
        "total": total,
        "limit": page["limit"],
        "offset": page["offset"],
    }

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

### 5 Wire it up & version — `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.errors import register_exception_handlers
from app.routers import health, tasks

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(health.router)                    # /health (unversioned)
app.include_router(tasks.router, prefix="/api/v1")   # /api/v1/tasks
```

### 6 Verify in `/docs`

| Request | Expected |
| --- | --- |
| GET `/api/v1/tasks?limit=2&offset=0` | 200, `{items:[...], total, limit:2, offset:0}` |
| GET `/api/v1/tasks/999` | 404, `{"error":{"code":"task_not_found","message":"Task 999 does not exist"}}` |
| POST `/api/v1/tasks` with `{}` | 422, `{"error":{"code":"validation_error","details":[...]}}` |
| GET `/api/v1/tasks?limit=9999` | 422, limit exceeds 100 |
| GET `/health` | 200, `{"status":"ok"}` (still unversioned) |

## Part B — Reconnect the frontend

### 7 Point at `/api/v1` & read `items`

Update the frontend `.env` and restart Vite:

```
VITE_API_URL=http://localhost:8000/api/v1
```

Then update `src/api.js` so `getTasks` returns the array inside the envelope and every call surfaces the server's error message:

```javascript
const BASE_URL = import.meta.env.VITE_API_URL;

async function errorMessage(res) {
  try {
    const data = await res.json();
    return data?.error?.message || `Request failed (${res.status})`;
  } catch {
    return `Request failed (${res.status})`;
  }
}

export async function getTasks() {
  const res = await fetch(`${BASE_URL}/tasks`);
  if (!res.ok) throw new Error(await errorMessage(res));
  const data = await res.json();
  return data.items;                 // unwrap the paginated envelope
}

export async function createTask(title) {
  const res = await fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error(await errorMessage(res));
  return res.json();
}

export async function toggleTask(id, completed) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) throw new Error(await errorMessage(res));
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(await errorMessage(res));
}
```

Your `App.jsx` from Chunk 5.5 already shows `err.message`, so it now displays the backend's real messages (e.g. "Task 5 does not exist"). No other frontend changes needed.

### 8 Add a `README.md` in `tasks-api`

```python
# Tasks API

In-memory CRUD API for tasks (FastAPI). Frontend: ../tasks-frontend (React + Vite).

## Run the backend
    python3 -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    uvicorn app.main:app --reload

API docs: http://localhost:8000/docs
Tasks:    http://localhost:8000/api/v1/tasks
Health:   http://localhost:8000/health

## Run the frontend
    cd ../tasks-frontend
    npm install
    npm run dev        # http://localhost:5173

Set tasks-frontend/.env -> VITE_API_URL=http://localhost:8000/api/v1

> Data is in-memory and resets on restart. SQLite persistence comes in Module 6.
```

## 🏁 Module 5 Checkpoint — verify the whole loop

With both servers running, walk the full path one more time:

| Step | Expected |
| --- | --- |
| Add a task in the React UI | Appears in the list (POST → 201) |
| Open `/docs` → GET `/api/v1/tasks` | Same task is there, inside `items` |
| Toggle + delete in the UI | PATCH 200 / DELETE 204; list stays in sync |
| Submit an empty title in the UI | Shows "Request validation failed" from the 422 envelope |
| Restart Uvicorn, refresh the app | Empty list — in-memory data reset (expected) |

If all five pass, your Module 5 deliverable is complete: a clean, documented, versioned, error-tolerant CRUD API driving a real React UI.

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Frontend list is empty / `tasks.map is not a function` | `GET /tasks` now returns an object — return `data.items` from `getTasks()`. |
| All requests 404 after versioning | The frontend base URL must include `/api/v1`; update `.env` and restart Vite. |
| Validation handler not firing | Import `RequestValidationError` from `fastapi.exceptions` and call `register_exception_handlers(app)` in `main.py`. |
| `TypeError: Object of type ... is not JSON serializable` | Wrap `exc.errors()` with `jsonable_encoder(...)` in the validation handler. |
| 404 still returns `{"detail": ...}` | `get_task_or_404` must raise `TaskNotFound`, and its handler must be registered. |
| 422 on `limit` | Expected if it's outside `1..100` — that's the `Query(ge=1, le=100)` guard working. |

## 🎉 Module 5 complete

You built a real backend from scratch: venv + Uvicorn, routes and params, Pydantic validation, a clean package with routers and dependency injection, CORS, consistent error handling, pagination, and versioning — all driving a live React frontend. That's a genuine full-stack slice.

The one thing it still can't do is **remember** anything across restarts. That's exactly what's next.

**Up next → Module 6: Database with SQLite.** You'll replace the in-memory store with SQLite via SQLAlchemy, add migrations, and make your Tasks API persistent — and thanks to your `storage.py` abstraction, your routes barely change. Your Pydantic schemas (with one `from_attributes=True` tweak) come right along.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
