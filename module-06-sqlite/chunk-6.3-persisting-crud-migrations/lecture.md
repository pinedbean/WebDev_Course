*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.3 — Persisting CRUD & Migrations

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The **repository pattern**: keeping database logic in a `crud.py` layer, separate from your endpoints.
- The core session operations: `add`, `commit`, `refresh`, `get`, `select`/`scalars`, `delete`.
- Converting *every* Tasks endpoint to durable, DB-backed CRUD — including partial `PATCH` updates.
- Why `create_all` isn't enough, and how **Alembic** manages schema changes with versioned migrations.

In the lab you'll replace the in-memory store entirely and create your first Alembic migration.

## 1. The goal: a fully persistent API

After 6.2 your API can *read* from SQLite, but creates/updates/deletes may still touch an in-memory list, and the schema is built with a throwaway `create_all`. Today we finish the job:

1. Move all database access into a clean **CRUD layer** (`crud.py`).
2. Rewrite every endpoint to use that layer through `get_db`.
3. Replace `create_all` with **Alembic** so schema changes are tracked and repeatable.

## 2. The repository pattern

So far, an endpoint mixes two jobs: handling HTTP (status codes, 404s, request bodies) *and* talking to the database. As the app grows that gets messy and hard to test. The **repository pattern** (often just called a "CRUD layer") splits them:

| Layer | Responsibility |
| --- | --- |
| `main.py` / routers | HTTP concerns: parse the request, return the right status, raise 404s. |
| `crud.py` | Database concerns: build queries, add/commit/delete rows. |

Every function in `crud.py` takes a `Session` as its first argument and returns plain ORM objects (or `None`). It knows nothing about HTTP. Benefits: endpoints stay thin, database logic is reusable, and you can test the CRUD layer on its own.

```text
tasks-api/
├── app/
│   ├── main.py        ← endpoints (thin)
│   ├── database.py    ← engine, session, Base, get_db
│   ├── models.py      ← Task ORM model
│   ├── schemas.py     ← Pydantic schemas
│   └── crud.py        ← all DB logic                 (NEW)
├── alembic/           ← migrations                   (NEW)
├── alembic.ini        ← Alembic config               (NEW)
└── tasks.db
```

## 3. The session operations you'll use

Five session methods cover everything in basic CRUD:

| Operation | What it does |
| --- | --- |
| `db.add(obj)` | Stage a new (or modified) object to be saved. |
| `db.commit()` | Write all staged changes to the database (the real `INSERT`/`UPDATE`/`DELETE`). |
| `db.refresh(obj)` | Reload the object from the DB so server-generated fields (`id`, `created_at`) are populated. |
| `db.get(Model, id)` | Fetch one row by primary key; returns the object or `None`. |
| `db.scalars(select(Model))` | Run a query and get back model objects; chain `.all()` or `.first()`. |
| `db.delete(obj)` | Stage an object for deletion (then `commit`). |

## 4. Writing `crud.py`

Here are the five functions for the Tasks API. Read how each maps to a SQL verb from Chunk 6.1:

### Read many / read one

```python
# app/crud.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas

def get_tasks(db: Session) -> list[models.Task]:
    return list(db.scalars(select(models.Task)))

def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)
```

### Create

`add` → `commit` → `refresh` is the standard insert dance. `refresh` fills in the new `id` and `created_at`:

```python
def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
```

### Update (partial / PATCH)

A `PATCH` should change only the fields the client actually sent. Pydantic's `model_dump(exclude_unset=True)` gives just those fields, so untouched columns keep their values:

```python
def update_task(
    db: Session, task: models.Task, data: schemas.TaskUpdate
) -> models.Task:
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task
```

### Delete

```python
def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()
```

> **💡 exclude_unset vs exclude_none**
>
> exclude_unset=True
>
> means "only fields the client included in the JSON" — so a client
>
> can
>
> explicitly set
>
> description
>
> to
>
> null
>
> .
>
> exclude_none=True
>
> would instead drop any field that's
>
> None
>
> , making it impossible to clear a value. For PATCH, you almost always want
>
> exclude_unset
>
> .

## 5. Thin endpoints that use the CRUD layer

Now the endpoints just translate between HTTP and `crud`. Notice how the 404 logic lives here, not in `crud.py`:

```python
# app/main.py (excerpt)
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

app = FastAPI(title="Tasks API")

@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.post("/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, data)

@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.patch("/tasks/{task_id}", response_model=schemas.TaskRead)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, data)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
```

The in-memory `tasks = []` list is now gone entirely. Every operation goes through the database.

## 6. Why `create_all` isn't enough

`Base.metadata.create_all()` creates tables that don't exist — and stops there. The moment your schema *changes*, it can't help you:

- You add an `owner_id` column to `tasks` (you will, in 6.4). `create_all` won't add it to the existing table.
- You have a production database with real data — you can't just drop and recreate it.
- A teammate clones the repo and needs the exact same schema as you.

What you need is a **version-controlled history of schema changes** that can be applied step by step to any database. That's a **migration tool**.

## 7. Alembic: migrations for SQLAlchemy

**Alembic** is SQLAlchemy's official migration tool. Each schema change becomes a **migration file** (a versioned script with an `upgrade()` and a `downgrade()`). Think of it as *git for your database schema*.

| Concept | Meaning |
| --- | --- |
| **Migration / revision** | One versioned change, e.g. "create tasks table". Has a unique id. |
| `upgrade()` | Apply the change (create the table, add the column). |
| `downgrade()` | Undo it (drop the table/column) — your safety net. |
| **autogenerate** | Alembic compares your models to the DB and writes the migration for you. |
| `alembic_version` table | A tiny table Alembic adds to track which revision the DB is on. |

### Setting up Alembic

```bash
pip install alembic
alembic init alembic
```

This creates an `alembic/` folder and an `alembic.ini` file. Two edits connect Alembic to your project:

**1. Point it at your database** — in `alembic.ini`, set the URL to match `database.py`:

```bash
# alembic.ini
sqlalchemy.url = sqlite:///./tasks.db
```

**2. Give it your models' metadata** — in `alembic/env.py`, import your `Base` and every model, then set `target_metadata`. This is how autogenerate "sees" your tables:

```python
# alembic/env.py (near the top, after the default imports)
from app.database import Base
from app import models  # noqa: F401  -- import so models register on Base

target_metadata = Base.metadata
```

> **⚠️ Import the models, or autogenerate sees nothing**
>
> If you set
>
> target_metadata = Base.metadata
>
> but never import
>
> models
>
> , the
>
> Task
>
> class never registers on
>
> Base
>
> , and autogenerate produces an
>
> empty
>
> migration. Always import your models in
>
> env.py
>
> .

## 8. Creating & running your first migration

With the model registered, autogenerate the initial migration. The `-m` message is a human-readable label:

```bash
alembic revision --autogenerate -m "create tasks table"
```

Alembic writes a file under `alembic/versions/` containing the generated `upgrade()`/`downgrade()`. **Always open and read it** before applying — autogenerate is good but not infallible. Then apply it:

```bash
alembic upgrade head
```

`head` means "the latest revision". Your database now has the `tasks` table *and* an `alembic_version` row recording the migration. To roll back the last step:

```bash
alembic downgrade -1
```

> **📝 Remove the create_all call**
>
> Once Alembic manages your schema, delete (or comment out)
>
> Base.metadata.create_all(bind=engine)
>
> from
>
> main.py
>
> . Migrations are now the single source of truth for the schema. (If your DB already had tables from 6.2, start from a fresh
>
> tasks.db
>
> so the first migration applies cleanly — see the solution.)

## 9. The everyday migration workflow

From now on, whenever you change a model, you do the same two steps. You'll use this constantly in 6.4 and beyond:

```bash
# 1. Change a model in models.py (add a column, a table, an index…)
# 2. Generate a migration from the change:
alembic revision --autogenerate -m "add priority to tasks"
# 3. Read the generated file, then apply it:
alembic upgrade head
```

> **⚠️ SQLite has limited ALTER TABLE**
>
> SQLite can't drop or heavily alter columns the way Postgres can. Alembic works around this with "batch mode" (it rebuilds the table). For simple additions you usually won't notice; if a migration fails on SQLite, look up Alembic's
>
> render_as_batch=True
>
> option. We'll flag this again if it bites in 6.4.

## ✅ Recap

- The **repository pattern** puts all DB logic in `crud.py`; endpoints stay thin and handle only HTTP (including 404s).
- Core session ops: `add` → `commit` → `refresh` to create; `db.get` / `db.scalars(select(...))` to read; mutate attributes + `commit` to update; `db.delete` + `commit` to delete.
- `PATCH` uses `model_dump(exclude_unset=True)` so only sent fields change.
- `create_all` can't evolve a schema; **Alembic** tracks changes as versioned migrations (`upgrade`/`downgrade`).
- Wire Alembic by setting `sqlalchemy.url` in `alembic.ini` and importing `Base` + models in `env.py` for `target_metadata`.
- Daily loop: change model → `alembic revision --autogenerate` → read it → `alembic upgrade head`.

**Next:** open `assignment.html` and make the whole Tasks API persistent with a migration.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
