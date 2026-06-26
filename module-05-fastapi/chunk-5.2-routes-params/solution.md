*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll grow `main.py` into a full in-memory CRUD API. Each step shows the route and explains the design choice. The complete file is at the bottom.

### 1 Imports & in-memory storage

At the top of `main.py`, import the pieces we need and set up the store and helper.

```python
from datetime import datetime
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Tasks API", description="Backend for the WebDev course")

# In-memory "database" (resets on restart)
tasks: list[dict] = []
next_id: int = 1

def find_task(task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### 2 Create — `POST /tasks`

Fields arrive as query params for now. We assign the id ourselves, default `completed` to `False`, and stamp `created_at`. `global next_id` lets us reassign the module-level counter.

```python
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

### 3 List — `GET /tasks`

The optional `completed` query param filters the list. When it's `None`, we return everything.

```python
@app.get("/tasks")
def list_tasks(completed: bool | None = None):
    if completed is None:
        return tasks
    return [t for t in tasks if t["completed"] == completed]
```

### 4 Read one — `GET /tasks/{task_id}`

The path param is typed `int`, so `/tasks/abc` auto-fails with 422. A missing id is a 404 we raise ourselves.

```python
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

### 5 Update — `PATCH /tasks/{task_id}`

Every field is optional. We only overwrite a field if the caller actually sent it (i.e. it isn't `None`). This is what makes it a *partial* update.

```python
@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    completed: bool | None = None,
):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if completed is not None:
        task["completed"] = completed
    return task
```

> **📝 Why check `is not None`?**
>
> If we blindly assigned every argument, omitting
>
> description
>
> would wipe it to
>
> None
>
> . Checking
>
> is not None
>
> means "only change what was provided" — true PATCH behavior.

### 6 Delete — `DELETE /tasks/{task_id}`

204 means "success, no body" — so we return nothing.

```python
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return None
```

### 7 Exercise it in `/docs`

With the server running, open `/docs` and walk through:

| Action | Expected |
| --- | --- |
| POST `/tasks?title=Buy milk` ×3 (vary titles) | 201, each returns a task with a new `id` |
| GET `/tasks` | 200, all three tasks |
| PATCH `/tasks/1?completed=true` | 200, task 1 now `"completed": true` |
| GET `/tasks?completed=true` | 200, just task 1 |
| GET `/tasks/999` | 404, `{"detail":"Task not found"}` |
| DELETE `/tasks/2` | 204, empty body; it's gone from the list |

## 📄 Complete `main.py`

```python
from datetime import datetime
from fastapi import FastAPI, HTTPException, status

app = FastAPI(title="Tasks API", description="Backend for the WebDev course")

# In-memory "database" (resets on restart)
tasks: list[dict] = []
next_id: int = 1

def find_task(task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks(completed: bool | None = None):
    if completed is None:
        return tasks
    return [t for t in tasks if t["completed"] == completed]

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

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: str | None = None,
    description: str | None = None,
    completed: bool | None = None,
):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if completed is not None:
        task["completed"] = completed
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return None
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `name 'next_id' is not defined` on create | Add `global next_id` as the first line of `create_task` before you reassign it. |
| `/docs` shows POST fields as query params, not a body | Expected for this chunk — request bodies (JSON) need Pydantic, which is Chunk 5.3. |
| Filtering by `completed` returns nothing | Send `true`/`false` (lowercase). FastAPI parses these into Python `True`/`False`. |
| `/tasks/stats` gives a 422 | A literal route must be declared *before* `/tasks/{task_id}`, or "stats" is parsed as an id. |
| All tasks gone after editing code | Normal — `--reload` restarts the server and in-memory data resets. Persistence comes in Module 6. |
| DELETE returns 200 with a body | Add `status_code=204` to the decorator and `return None`. |

## 🎉 You're done

You built a working in-memory CRUD API with proper methods, params, and status codes — and you handled the "not found" case correctly. That's the backbone of every REST service.

You also felt the pain of stuffing data into query strings. Next we fix it properly.

**Up next → Chunk 5.3: Request Bodies & Pydantic Validation** — clean JSON bodies, typed schemas (`TaskCreate`, `TaskRead`…), and automatic validation.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
