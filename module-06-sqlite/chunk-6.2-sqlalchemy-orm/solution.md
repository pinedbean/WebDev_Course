*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Follow each step to connect your Tasks API to SQLite. Every file is shown complete and copy-pasteable. The target layout:

```text
tasks-api/
├── app/
│   ├── __init__.py
│   ├── main.py          ← endpoints + create_all
│   ├── database.py      ← engine, SessionLocal, Base, get_db   (NEW)
│   ├── models.py        ← Task ORM model                       (NEW)
│   └── schemas.py       ← Pydantic schemas
├── .venv/
└── tasks.db             ← created on first run
```

### 1 Install SQLAlchemy

With your virtual environment active:

```bash
pip install "sqlalchemy>=2.0"
```

Optionally freeze it: `pip freeze > requirements.txt`.

### 2 `app/database.py`

All the database wiring in one place — the four pieces from the lecture plus the `get_db` dependency:

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# check_same_thread is SQLite-specific; required because FastAPI
# may use the connection across threads.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# FastAPI dependency: one session per request, always closed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3 `app/models.py`

The `Task` ORM model. It inherits the `Base` from `database.py` so `create_all` can find it:

```python
# app/models.py
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
```

### 4 `app/schemas.py`

The Pydantic v2 schemas. The key change is `ConfigDict(from_attributes=True)` on the *read* schema so it can serialize an ORM object. (`TaskCreate` / `TaskUpdate` are shown for completeness — you'll use them fully in 6.3.)

```python
# app/schemas.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TaskRead(TaskBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

### 5 `app/main.py`

Create the tables on startup, then read tasks from the database via `Depends(get_db)`. We also seed one row the first time so there's data to see. SQLAlchemy 2.x reads with `select()` + `db.scalars(...)`:

```python
# app/main.py
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db, SessionLocal
from app import models, schemas

# Create tables (temporary — replaced by Alembic in 6.3).
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tasks API")

# One-time seed so GET /tasks returns something on a fresh DB.
def seed_if_empty() -> None:
    db = SessionLocal()
    try:
        existing = db.scalars(select(models.Task)).first()
        if existing is None:
            db.add(models.Task(title="Buy milk", description="2% organic"))
            db.add(models.Task(title="Finish report", completed=True))
            db.commit()
    finally:
        db.close()

seed_if_empty()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.scalars(select(models.Task)).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

> **📝 Why `db.scalars(...)`?**
>
> In SQLAlchemy 2.x,
>
> db.scalars(select(Task))
>
> returns the
>
> Task
>
> objects themselves;
>
> .all()
>
> gives a list,
>
> .first()
>
> gives one or
>
> None
>
> . For a lookup by primary key,
>
> db.get(Task, id)
>
> is the shortcut.

### 6 Run it

```bash
uvicorn app.main:app --reload
```

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

A `tasks.db` file now sits in your project root. Open `http://127.0.0.1:8000/docs`, run **GET /tasks**, and you'll get:

```
[
  {
    "title": "Buy milk",
    "description": "2% organic",
    "completed": false,
    "id": 1,
    "created_at": "2026-06-26T09:00:00"
  },
  {
    "title": "Finish report",
    "description": null,
    "completed": true,
    "id": 2,
    "created_at": "2026-06-26T09:00:00"
  }
]
```

### 7 Prove persistence

Stop the server (`Ctrl`+`C`) and start it again. Because `seed_if_empty()` only inserts when the table is empty, no duplicates are added — and **GET /tasks** still returns your two rows. The data lives in `tasks.db`, not in memory.

Confirm directly with the CLI from Chunk 6.1:

```
sqlite3 tasks.db ".schema tasks"
```

```sql
CREATE TABLE tasks (
    id INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    completed BOOLEAN NOT NULL,
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL,
    PRIMARY KEY (id)
);
```

That's the table SQLAlchemy generated from your model. You never wrote that SQL — the ORM did.

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `tasks.db` never appears / no `tasks` table | Make sure `models` is imported in `main.py` *before* `create_all`, and that the model inherits the same `Base` from `database.py`. |
| `sqlite3.OperationalError: ... another thread` | You forgot `connect_args={"check_same_thread": False}` on `create_engine`. |
| `ResponseValidationError` on GET /tasks | Add `model_config = ConfigDict(from_attributes=True)` to `TaskRead`, and set `response_model` on the endpoint. |
| `ImportError: cannot import name 'Base'` | Circular import. Keep `Base` only in `database.py`; `models.py` imports from `database`, not the other way around. |
| Duplicate seed rows on every restart | The empty-check (`db.scalars(...).first() is None`) prevents this. If you removed it, delete `tasks.db` and restart. |
| `ModuleNotFoundError: No module named 'app'` | Run uvicorn from the project root (the folder that *contains* `app/`), and make sure `app/__init__.py` exists. |

## 🎉 You're done

Your Tasks API now owns a real SQLite database. You defined an ORM model, opened sessions through dependency injection, and read live data from disk — all without writing SQL by hand.

Right now only the read endpoints touch the database, and there's a leftover in-memory list. **Next chunk** you'll convert *every* endpoint to durable, DB-backed CRUD using a clean repository layer, and replace `create_all` with proper **Alembic migrations**.

**Up next → Chunk 6.3: Persisting CRUD & Migrations.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
