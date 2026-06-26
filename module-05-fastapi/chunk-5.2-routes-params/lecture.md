*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.2 — Routes, Path & Query Params

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The HTTP methods — **GET, POST, PUT, PATCH, DELETE** — and what each means.
- **Path parameters** (part of the URL) vs **query parameters** (after the `?`).
- How FastAPI converts and validates params from type hints.
- **Status codes** and how to return the right one (201, 204, 404…).
- How to design a set of CRUD endpoints around a resource.

In the lab you'll build full in-memory CRUD for tasks: list, get one, create, update, delete.

## 1. HTTP methods = verbs

Every request has a **method** (a verb) describing the *intent*, and a **path** (a noun) naming the *resource*. Together they form an endpoint. For a "tasks" resource the standard set is:

| Method | Endpoint | Meaning | FastAPI decorator |
| --- | --- | --- | --- |
| GET | `/tasks` | List all tasks | `@app.get` |
| GET | `/tasks/{id}` | Get one task | `@app.get` |
| POST | `/tasks` | Create a task | `@app.post` |
| PATCH | `/tasks/{id}` | Partially update a task | `@app.patch` |
| PUT | `/tasks/{id}` | Replace a task entirely | `@app.put` |
| DELETE | `/tasks/{id}` | Delete a task | `@app.delete` |

This pattern is **REST**: the path names *what* (the resource), the method says *what to do* with it. We'll use **PATCH** for updates in this course because we usually change *some* fields, not replace the whole task.

> **📝 GET vs the rest**
>
> A browser address bar only sends
>
> GET
>
> . To send POST/PATCH/DELETE you need a tool — that's exactly what the
>
> /docs
>
> page is for. Later, your React app's
>
> fetch
>
> will send them.

## 2. Path parameters

A **path parameter** is a placeholder inside the URL itself, written in `{braces}`. It identifies *which* resource. Declare a function argument with the same name and a type hint; FastAPI extracts and converts it.

```python
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    return {"task_id": task_id}
```

Because of `task_id: int`, FastAPI converts the text from the URL into an integer. Request `/tasks/7` → `task_id == 7` (an int). Request `/tasks/abc` → FastAPI auto-returns a **422** error explaining the value isn't a valid integer. You wrote zero validation code.

> **💡 Order matters**
>
> Put fixed paths
>
> before
>
> parameterized ones. Define
>
> /tasks/stats
>
> before
>
> /tasks/{task_id}
>
> , or "stats" would be read as an id and fail conversion.

## 3. Query parameters

A **query parameter** comes after the `?` in a URL, as `key=value` pairs joined by `&`. Use them to filter, sort, paginate, or search — optional tweaks to a request. In FastAPI, any function argument that is *not* in the path automatically becomes a query parameter.

```python
@app.get("/tasks")
def list_tasks(completed: bool | None = None, limit: int = 10):
    return {"completed": completed, "limit": limit}
```

- `limit: int = 10` — has a default, so it's **optional**; `/tasks` uses 10.
- `completed: bool | None = None` — optional, defaults to "not provided".
- Request `/tasks?completed=true&limit=5` → `completed=True`, `limit=5`.

|  | Path param | Query param |
| --- | --- | --- |
| Where | In the URL path: `/tasks/7` | After `?`: `/tasks?limit=5` |
| Required? | Always required | Optional if it has a default |
| Use for | Identifying one resource | Filtering / options |

## 4. Status codes

Every response carries a 3-digit **status code** telling the client what happened. By default FastAPI returns **200 OK**. You set a different default per route with `status_code=`, and signal errors by raising `HTTPException`.

| Code | Name | Use when |
| --- | --- | --- |
| 200 | OK | A successful GET / PATCH (default). |
| 201 | Created | A POST that created a new resource. |
| 204 | No Content | A successful DELETE — nothing to return. |
| 400 | Bad Request | The client sent something invalid. |
| 404 | Not Found | The requested resource doesn't exist. |
| 422 | Unprocessable Entity | FastAPI's auto validation failed. |
| 500 | Server Error | Your code crashed (a bug). |

Roughly: **2xx** = success, **4xx** = the client's fault, **5xx** = the server's fault.

### Setting the success code

```python
from fastapi import status

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(...):
    ...

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    ...   # return nothing for 204
```

### Raising errors with `HTTPException`

When a task id doesn't exist, you should return **404**, not crash. Raise `HTTPException` and FastAPI turns it into a proper JSON error response:

```python
from fastapi import HTTPException, status

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task
```

The client receives `{"detail": "Task not found"}` with status 404.

## 5. In-memory storage for tasks

We need somewhere to keep tasks while the server runs. For now that's a plain Python `list` of dicts living in `main.py` — **in-memory storage**. It resets every time the server restarts; that's fine for learning. Module 6 replaces it with a real SQLite database.

```
# in-memory "database"
tasks: list[dict] = []
next_id: int = 1     # we hand out ids ourselves
```

A small helper to find a task by id keeps routes tidy:

```python
def find_task(task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None
```

> **⚠️ It's volatile on purpose**
>
> Restart Uvicorn and your tasks vanish. With
>
> --reload
>
> , saving a file restarts the server too. That's expected in Module 5 — persistence arrives with SQLite in Module 6.

## 6. A worked CRUD route

Here's a create endpoint. There's one wrinkle: **request bodies** (sending JSON in a POST) need Pydantic models, which is Chunk 5.3's whole topic. For *this* chunk we'll accept the task's fields as **query parameters** so we can focus on routing and status codes:

```python
from datetime import datetime
from fastapi import status

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(title: str, description: str | None = None):
    global next_id
    task = {
        "id": next_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }
    tasks.append(task)
    next_id += 1
    return task
```

Calling `POST /tasks?title=Buy%20milk` returns the new task with status 201. (`%20` is just a URL-encoded space.)

> **💡 This feels clunky — and it should**
>
> Cramming a task's data into the URL works, but it's awkward and won't scale to nested data. That's the motivation for
>
> request bodies + Pydantic
>
> in Chunk 5.3, where
>
> POST /tasks
>
> will accept a clean JSON body instead.

## ✅ Recap

- HTTP **methods** are verbs (GET/POST/PATCH/DELETE) on resource **paths** — that's REST.
- **Path params** (`/tasks/{id}`) identify a resource; **query params** (`?limit=5`) are optional filters.
- Type hints make FastAPI **convert and validate** params automatically (bad input → 422).
- Return the right **status code**: 201 on create, 204 on delete, 404 (via `HTTPException`) when not found.
- Store tasks in an in-memory `list[dict]` for now; SQLite comes in Module 6.

**Next:** open `assignment.html` and build the full in-memory CRUD API for tasks.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
