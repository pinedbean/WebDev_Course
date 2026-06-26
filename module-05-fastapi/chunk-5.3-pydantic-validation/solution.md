*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll refactor `main.py` to use Pydantic v2 schemas and JSON bodies. The storage stays as in-memory dicts; the request/response layer becomes typed and validated. Full file at the bottom.

### 1 Imports & the four schemas

Add Pydantic imports and define the schema classes under your imports.

```python
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Tasks API", description="Backend for the WebDev course")

# ---- Schemas -------------------------------------------------------------
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

### 2 Storage & helper (unchanged)

```python
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

### 3 Create — body in, `TaskRead` out

`payload.model_dump()` turns the validated body into a dict; we spread it and add the server-owned fields with `**`.

```python
@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_id
    task = {
        "id": next_id,
        **payload.model_dump(),       # title, description
        "completed": False,
        "created_at": datetime.now(),
    }
    tasks.append(task)
    next_id += 1
    return task
```

> **📝 `created_at` as a real datetime**
>
> We store a
>
> datetime
>
> object (not a string now).
>
> response_model=TaskRead
>
> serializes it to an ISO string in the JSON automatically — one less manual
>
> .isoformat()
>
> .

### 4 Read routes with response models

```python
@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(completed: bool | None = None):
    if completed is None:
        return tasks
    return [t for t in tasks if t["completed"] == completed]

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

### 5 PATCH with `exclude_unset`

```python
@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)
    task.update(updates)
    return task
```

### 6 DELETE (unchanged)

```python
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(task)
    return None
```

### 7 Verify in `/docs`

| Request | Expected |
| --- | --- |
| POST `{"title": "Read docs"}` | 201, body includes `id`, `completed:false`, `created_at` |
| PATCH 1 `{"completed": true}` | 200, only `completed` changed |
| POST `{}` | 422, `loc` points to `["body","title"]` |
| POST `{"title": ""}` | 422, "String should have at least 1 character" |
| POST `{"title": ["x"]}` | 422, wrong type for `title` |

## 📄 Complete `main.py`

```python
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Tasks API", description="Backend for the WebDev course")

# ---- Schemas -------------------------------------------------------------
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

# ---- In-memory store -----------------------------------------------------
tasks: list[dict] = []
next_id: int = 1

def find_task(task_id: int) -> dict | None:
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None

# ---- Routes --------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(completed: bool | None = None):
    if completed is None:
        return tasks
    return [t for t in tasks if t["completed"] == completed]

@app.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate):
    global next_id
    task = {
        "id": next_id,
        **payload.model_dump(),
        "completed": False,
        "created_at": datetime.now(),
    }
    tasks.append(task)
    next_id += 1
    return task

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    updates = payload.model_dump(exclude_unset=True)
    task.update(updates)
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
| POST still asks for query params, not a body | The parameter must be typed as a Pydantic model (`payload: TaskCreate`). Plain types like `str` become query params. |
| `AttributeError: 'TaskUpdate' object has no attribute 'dict'` | That's Pydantic v1. In v2 use `model_dump()`, not `.dict()`. |
| PATCH wipes fields you didn't send | You forgot `exclude_unset=True` in `model_dump()`. |
| Response shows extra/odd fields | Add the right `response_model` so FastAPI filters the output to `TaskRead`. |
| `created_at` serialization error | Make sure `TaskRead.created_at` is typed `datetime` and you stored a `datetime` (or an ISO string). |
| 422 on every POST even with good data | Check your JSON keys match field names exactly (`title`, not `Title`). |

## 🎉 You're done

Your API now speaks clean JSON, validates every request automatically, and documents its exact shapes. The four-schema pattern you built here is the same one you'll reuse in Module 6 (with the database) and the capstone.

**Up next → Chunk 5.4: Project Structure & Routers** — your `main.py` is getting long; you'll split it into an `app/` package with routers, schemas, storage, and config.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
