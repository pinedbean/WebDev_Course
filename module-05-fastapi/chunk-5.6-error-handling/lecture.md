*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.6 — Error Handling & API Best Practices

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to return **consistent, predictable error responses** across the whole API.
- **Custom exceptions** and global **exception handlers**.
- **Pagination** with a proper response envelope (`items`, `total`, `limit`, `offset`).
- **API versioning** basics with a `/api/v1` prefix.
- A checklist of REST best practices to carry into every future API.

In the lab you'll harden the Tasks API, then assemble the 🏁 **Module 5 Checkpoint**: a full CRUD API consumed by your React frontend.

## 1. Why consistent errors matter

Right now your errors come in two shapes: `HTTPException` gives `{"detail": "..."}`, and validation gives a `detail` array. A frontend has to handle each differently. A **good API uses one error shape everywhere**, so clients write error handling once. We'll standardize on:

```json
{
  "error": {
    "code": "task_not_found",
    "message": "Task 99 does not exist"
  }
}
```

A machine-readable `code` (for logic/i18n) plus a human-readable `message` (for display). Validation errors add a `details` array.

## 2. Custom exceptions

Instead of constructing an `HTTPException` at every call site, define a small **domain exception** that describes *what went wrong* in business terms. Put it in `app/errors.py`:

```python
class TaskNotFound(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task {task_id} does not exist")
```

Now your dependency just raises it — no status codes mixed into business logic:

```python
from app.errors import TaskNotFound

def get_task_or_404(task_id: int) -> dict:
    task = storage.get_by_id(task_id)
    if task is None:
        raise TaskNotFound(task_id)
    return task
```

The HTTP concern (which status code, what JSON) is decided in *one* place — the handler — keeping routes clean.

## 3. Global exception handlers

An **exception handler** catches a given exception type anywhere in the app and turns it into a response. Register handlers with `@app.exception_handler(...)`. We'll translate our custom error, normal `HTTPException`s, and validation errors into the same shape:

```python
# app/errors.py
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

Then in `app/main.py`, after creating `app`:

```python
from app.errors import register_exception_handlers
register_exception_handlers(app)
```

- `jsonable_encoder` safely converts Pydantic's error objects to JSON-friendly data.
- Every error — yours, FastAPI's, validation — now arrives in the same envelope.

> **📝 Don't leak internals**
>
> Never return raw exception text or stack traces to clients (it can expose how your system works). Return a friendly message; log the details server-side. Real logging is Module 8's topic.

## 4. Pagination

Returning *every* task in one response is fine for 10 tasks, disastrous for 10,000. **Pagination** returns a slice plus the metadata clients need to fetch more. The two common knobs are `limit` (page size) and `offset` (how many to skip).

Wrap the results in an **envelope** so the client knows the total. Define a response schema:

```
# app/schemas.py
class TaskPage(BaseModel):
    items: list[TaskRead]
    total: int
    limit: int
    offset: int
```

And use the pagination dependency from Chunk 5.4 to slice:

```python
@router.get("", response_model=TaskPage)
def list_tasks(
    completed: bool | None = None,
    page: dict = Depends(pagination_params),   # {"limit": ..., "offset": ...}
):
    items = storage.get_all()
    if completed is not None:
        items = [t for t in items if t["completed"] == completed]

    total = len(items)
    start = page["offset"]
    window = items[start : start + page["limit"]]
    return {"items": window, "total": total,
            "limit": page["limit"], "offset": page["offset"]}
```

A request to `/tasks?limit=2&offset=2` returns:

```json
{
  "items": [ ... 2 tasks ... ],
  "total": 7,
  "limit": 2,
  "offset": 2
}
```

> **⚠️ This changes the response shape**
>
> GET /tasks
>
> now returns an object, not a bare array. Your React client must read
>
> data.items
>
> (you'll update it in the checkpoint). Add sensible bounds too — e.g. cap
>
> limit
>
> with
>
> Field(le=100)
>
> so a client can't request a million rows.

## 5. API versioning

Once a frontend (or other teams) depend on your API, you can't freely change response shapes — you'd break them. **Versioning** lets you ship a new, incompatible version while the old one keeps working. The simplest, most common approach is a **URL prefix**:

```
/api/v1/tasks      ← today's contract
/api/v2/tasks      ← a future, breaking redesign (when needed)
```

You already structure routes with routers, so versioning is one line — add a prefix when including the tasks router:

```
# app/main.py
app.include_router(health.router)                     # /health  (unversioned)
app.include_router(tasks.router, prefix="/api/v1")    # /api/v1/tasks
```

Health checks usually stay *unversioned* at `/health` so monitoring tools have a stable URL. Everything functional lives under `/api/v1`.

> **📝 Other versioning styles**
>
> Some APIs version via a header (
>
> Accept: application/vnd.api+json;version=1
>
> ) or a query param. URL-prefix versioning is the easiest to read, test, and cache — a great default. You won't need
>
> v2
>
> for a long time; the point is leaving room for it.

## 6. REST best-practices checklist

Pulling the module together, a solid REST API:

| Practice | What it looks like |
| --- | --- |
| Resource-based URLs | Nouns, plural: `/tasks`, `/tasks/{id}` — not `/getTask`. |
| Correct methods | GET (read), POST (create), PATCH (update), DELETE (remove). |
| Meaningful status codes | 201 create, 204 delete, 404 missing, 422 invalid. |
| Validated input | Pydantic schemas on every body. |
| Consistent errors | One JSON error envelope everywhere. |
| Pagination | Limit/offset + total on list endpoints. |
| Versioning | A stable `/api/v1` prefix. |
| Self-documenting | Tags, schemas, and examples in `/docs`. |
| Health check | A stable, unversioned `/health`. |

> **💡 Looking ahead**
>
> Your API is polished but still forgets everything on restart.
>
> Module 6
>
> swaps the in-memory store for
>
> SQLite + SQLAlchemy
>
> so data persists — and because your routes only call
>
> storage.*
>
> functions, that swap touches almost nothing else. The structure you built is paying off.

## ✅ Recap

- Return **one consistent error envelope** (`code` + `message`) for all failures.
- Raise **custom exceptions** in business logic; translate them in **global exception handlers**.
- **Paginate** list endpoints with `limit`/`offset` and a `TaskPage` envelope (`items` + `total`).
- **Version** functional routes under `/api/v1`; keep `/health` unversioned.
- Follow the REST checklist: nouns, right methods, right codes, validation, docs, health.

**Next:** open `assignment.html` — harden the API and complete the 🏁 Module 5 Checkpoint.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
