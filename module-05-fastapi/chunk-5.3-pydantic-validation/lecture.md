*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.3 — Request Bodies & Pydantic Validation

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What a **request body** is and why JSON beats query params for sending data.
- **Pydantic v2** models: `BaseModel`, typed fields, defaults, and `Field` constraints.
- The schema pattern: **TaskBase / TaskCreate / TaskUpdate / TaskRead**.
- How `response_model` shapes and filters what you send back.
- How FastAPI turns validation failures into clean **422** errors — automatically.

In the lab you'll replace the query-param CRUD from 5.2 with typed schemas and real JSON bodies.

## 1. The request body

A **request body** is data sent *inside* the request (not in the URL), almost always as JSON. It's how clients send structured data on POST/PATCH/PUT. Compare the two styles for creating a task:

```
# Chunk 5.2 (clunky): data crammed into the URL
POST /tasks?title=Buy%20milk&description=2%25%20fat

# This chunk (clean): data in a JSON body
POST /tasks
Content-Type: application/json

{
  "title": "Buy milk",
  "description": "2% fat"
}
```

Bodies handle nested data, are easier to read, and don't leak into server logs the way URLs do. To accept one in FastAPI, you describe its *shape* with a **Pydantic model**.

## 2. Pydantic models

**Pydantic** (installed automatically with FastAPI — it's Pydantic **v2**) lets you declare data shapes as Python classes. You subclass `BaseModel` and list fields with type hints:

```python
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
```

That tiny class gives you a lot:

- **Validation** — incoming JSON must match the types, or you get an error.
- **Coercion** — e.g. the string `"true"` becomes the bool `True` where appropriate.
- **Editor help** — autocomplete and type checking on `task.title`.
- **Docs** — the model's shape appears in `/docs` with an example.

Fields with a default (like `description: str | None = None`) are optional; fields without one (like `title: str`) are required.

### Adding constraints with `Field`

Want rules beyond the type? Use `Field`. Here `title` must be 1–200 characters:

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
```

Now an empty title is rejected before your route code ever runs. Other handy constraints: `ge`/`le` (number ranges), `pattern` (regex). You describe the rule once; Pydantic enforces it everywhere.

## 3. Using a model as a request body

Add a parameter typed as your model. FastAPI sees it's a Pydantic model and reads it from the JSON body (not the query string):

```python
@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate):
    # payload is a validated TaskCreate object
    print(payload.title)          # dot access, fully typed
    data = payload.model_dump()   # -> a plain dict
    ...
```

If the client sends invalid JSON (missing `title`, wrong type, empty string), FastAPI never calls your function — it returns a **422** automatically. Your route body can assume the data is already valid. That's the big win.

> **📝 `model_dump()`**
>
> In Pydantic v2,
>
> model_dump()
>
> converts a model to a plain
>
> dict
>
> (the v1 name was
>
> .dict()
>
> ). Use it when you need to merge model data into your in-memory store.

## 4. The four-schema pattern

One model rarely fits every situation. The data a client *sends to create* differs from what you *send back* (the response has an `id` and `created_at` the client can't know). The clean, reusable pattern — which you'll carry into Modules 6, 7, and the capstone — is four small schemas:

| Schema | Purpose | Fields |
| --- | --- | --- |
| `TaskBase` | Shared fields, inherited by others | `title`, `description` |
| `TaskCreate` | Body for `POST /tasks` | (inherits base) |
| `TaskUpdate` | Body for `PATCH` — all optional | `title?`, `description?`, `completed?` |
| `TaskRead` | The response shape | base + `id`, `completed`, `created_at` |

```python
from datetime import datetime
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)

class TaskCreate(TaskBase):
    pass                       # creating uses exactly the base fields

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    completed: bool | None = None

class TaskRead(TaskBase):
    id: int
    completed: bool
    created_at: datetime
```

Inheritance (`class TaskCreate(TaskBase)`) means shared fields are declared once. The server owns `id`, `completed`, and `created_at`, so they live only on `TaskRead` — clients can't set them.

## 5. `response_model` — shaping the output

Tell a route what it returns with `response_model=`. FastAPI validates your return value against it, drops any extra keys, and documents the response in `/docs`:

```python
@app.post("/tasks", response_model=TaskRead, status_code=201)
def create_task(payload: TaskCreate):
    ...
    return task   # a dict; FastAPI coerces it to TaskRead

@app.get("/tasks", response_model=list[TaskRead])
def list_tasks():
    return tasks
```

Why bother when we control the dict? Because `response_model` is a **contract**: it guarantees the response shape, hides fields you didn't list (great later for not leaking password hashes), and keeps your docs honest. `list[TaskRead]` says "a JSON array of tasks".

## 6. PATCH with `exclude_unset`

For partial updates, `TaskUpdate` makes every field optional. The trick is telling apart "field not sent" from "field set to null". Pydantic v2 does this with `model_dump(exclude_unset=True)` — it returns only the fields the client actually included:

```python
@app.patch("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, payload: TaskUpdate):
    task = find_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)   # only provided fields
    task.update(updates)                               # merge into stored dict
    return task
```

Send `{"completed": true}` and only `completed` changes — title and description are untouched. Much cleaner than the manual `if x is not None` checks from 5.2.

## 7. Automatic validation errors (422)

You don't write validation handling — FastAPI returns a structured **422 Unprocessable Entity** whenever a body fails its schema. Send `POST /tasks` with `{"title": ""}` and you get:

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

The `loc` array pinpoints exactly which field failed and where. Your React app (Chunk 5.5) can read this to show inline form errors. Consistent, machine-readable errors for free.

> **💡 Looking ahead to the database**
>
> In Module 6 your tasks become SQLAlchemy ORM
>
> objects
>
> instead of dicts. To let
>
> TaskRead
>
> read attributes off an object, you'll add
>
> model_config = ConfigDict(from_attributes=True)
>
> . Same schemas, one extra line — that's why this pattern pays off.

## ✅ Recap

- Send structured data in a **JSON request body**, described by a **Pydantic `BaseModel`**.
- Use **four schemas**: `TaskBase` (shared), `TaskCreate`, `TaskUpdate` (all optional), `TaskRead` (response).
- `Field(...)` adds constraints like `min_length`; invalid input becomes an automatic **422**.
- `response_model=` guarantees and documents the output shape; `list[TaskRead]` for collections.
- PATCH uses `model_dump(exclude_unset=True)` to update only the fields that were sent.

**Next:** open `assignment.html` and convert your CRUD API to typed schemas and real JSON bodies.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
