*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Build the repository layer first, rewire the endpoints, then set up Alembic and run the first migration. Every file is shown complete. Final layout:

```text
tasks-api/
├── app/
│   ├── __init__.py
│   ├── main.py        ← thin endpoints
│   ├── database.py    ← (from 6.2)
│   ├── models.py      ← (from 6.2)
│   ├── schemas.py     ← (from 6.2)
│   └── crud.py        ← repository layer            (NEW)
├── alembic/
│   ├── env.py         ← edited
│   └── versions/
│       └── xxxx_create_tasks_table.py               (generated)
├── alembic.ini        ← edited
└── tasks.db
```

## Part A — Repository & DB-backed CRUD

### 1 `app/crud.py`

```python
# app/crud.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas

def get_tasks(db: Session) -> list[models.Task]:
    return list(db.scalars(select(models.Task)))

def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(
    db: Session, task: models.Task, data: schemas.TaskUpdate
) -> models.Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()
```

### 2 `app/main.py` — thin endpoints

No more in-memory list, no more `create_all`. Every endpoint goes through `crud`:

```python
# app/main.py
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

app = FastAPI(title="Tasks API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.post(
    "/tasks",
    response_model=schemas.TaskRead,
    status_code=status.HTTP_201_CREATED,
)
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

> **📝 models.py, database.py, schemas.py**
>
> These are unchanged from Chunk 6.2.
>
> TaskUpdate
>
> already has all-optional fields, which is what makes the partial PATCH work.

## Part B — Alembic migrations

### 3 Start clean & initialize Alembic

Because 6.2 created the table with `create_all`, delete that file so the first migration owns the schema from scratch:

```bash
rm tasks.db          # Windows: del tasks.db
alembic init alembic
```

```
Creating directory '.../alembic' ...  done
Generating .../alembic.ini ...  done
Generating .../alembic/env.py ...  done
Please edit configuration/connection/logging settings in 'alembic.ini' ...
```

### 4 Edit `alembic.ini`

Find the `sqlalchemy.url` line and set it to your SQLite file:

```bash
# alembic.ini
sqlalchemy.url = sqlite:///./tasks.db
```

### 5 Edit `alembic/env.py`

Near the top, after the existing imports, point Alembic at your models' metadata. The `import models` line is essential — it registers `Task` on `Base` so autogenerate can see it:

```python
# alembic/env.py
import os, sys

# make the app package importable when Alembic runs
sys.path.append(os.getcwd())

from app.database import Base
from app import models  # noqa: F401  (imported so the table registers)

# ... existing Alembic config code ...

target_metadata = Base.metadata
```

> **⚠️ Replace the default `target_metadata = None`**
>
> The generated
>
> env.py
>
> ships with
>
> target_metadata = None
>
> . Change it to
>
> Base.metadata
>
> , or autogenerate will detect no tables.

### 6 Make sure `create_all` is gone

In `main.py`, confirm there is no `Base.metadata.create_all(bind=engine)` left (the thin `main.py` above already omits it). Migrations are now the only thing that builds the schema.

### 7 Autogenerate & apply

```bash
alembic revision --autogenerate -m "create tasks table"
```

```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.autogenerate.compare] Detected added table 'tasks'
  Generating .../alembic/versions/a1b2c3d4e5f6_create_tasks_table.py ...  done
```

Open that generated file and confirm its `upgrade()` creates the table:

```python
# alembic/versions/a1b2c3d4e5f6_create_tasks_table.py
def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("completed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    op.drop_table("tasks")
```

Now apply it:

```bash
alembic upgrade head
```

```
INFO  [alembic.runtime.migration] Running upgrade  -> a1b2c3d4e5f6, create tasks table
```

A fresh `tasks.db` now contains both `tasks` and `alembic_version`:

```
sqlite3 tasks.db ".tables"
# alembic_version  tasks
```

### 8 Exercise the full CRUD cycle

```bash
uvicorn app.main:app --reload
```

At `http://127.0.0.1:8000/docs`:

- **POST /tasks** with `{"title": "Buy milk", "description": "2% organic"}` → `201` and a task with `id: 1`.
- **GET /tasks** → a list containing your task.
- **PATCH /tasks/1** with `{"completed": true}` → title/description unchanged, `completed` now `true`.
- **GET /tasks/999** → `404 {"detail": "Task not found"}`.
- **DELETE /tasks/1** → `204 No Content`.

Create a couple of tasks, then **stop and restart** the server. `GET /tasks` still returns them — the data is in `tasks.db`, not memory. The API is now genuinely persistent.

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Autogenerated migration is empty ("no changes detected") | You didn't import models in `env.py`, or `target_metadata` is still `None`. Import `app.models` and set `target_metadata = Base.metadata`. |
| `ModuleNotFoundError: No module named 'app'` when running alembic | Run alembic from the project root, and add `sys.path.append(os.getcwd())` at the top of `env.py`. |
| `Target database is not up to date` | You generated a new revision without applying the previous one. Run `alembic upgrade head` first. |
| `table tasks already exists` on upgrade | The table was left over from 6.2's `create_all`. Delete `tasks.db` and re-run `alembic upgrade head`. |
| PATCH wipes other fields | Use `data.model_dump(exclude_unset=True)`, not `model_dump()`. |
| `sqlite3.OperationalError` when altering a column later | SQLite's limited `ALTER TABLE`. Enable batch mode in `env.py`'s `context.configure(..., render_as_batch=True)`. |

## 🎉 You're done

Your Tasks API is now fully persistent: a clean repository layer drives every endpoint, and Alembic owns the schema with a versioned, repeatable migration. You can clone this project anywhere, run `alembic upgrade head`, and get the exact same database.

**Next chunk** you'll model *connected* data: add a `User` entity, give each task an owner, and query across the two tables with joins, filtering, and sorting — then assemble the full-stack Module 6 checkpoint.

**Up next → Chunk 6.4: Relationships & Queries.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
