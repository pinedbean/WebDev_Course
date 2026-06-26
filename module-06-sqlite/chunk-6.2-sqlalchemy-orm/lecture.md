*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.2 — SQLAlchemy ORM with FastAPI

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What an **ORM** is and why we use one instead of writing SQL by hand.
- The four pieces of SQLAlchemy 2.x: the **engine**, the **session**, the **Base**, and **models**.
- How to map the `Task` entity to a database table with `Mapped` / `mapped_column`.
- How to inject a database session into FastAPI endpoints with a `get_db()` dependency.
- How Pydantic v2's `from_attributes` lets a response model read straight from an ORM object.

In the lab you'll wire your Module 5 Tasks API to a real SQLite file and read tasks from the database.

## 1. Where we are

In Chunk 6.1 you ran SQL by hand. In Module 5 you built a Tasks API whose data lived in a Python list. This chunk connects the two: your Python code will *own* a SQLite database and read/write it — but you'll almost never type SQL yourself. An **ORM** does it for you.

> **📝 The Module 5 starting point**
>
> We assume the Tasks API from Module 5: FastAPI + Pydantic v2, with a
>
> Task
>
> entity (
>
> id
>
> ,
>
> title
>
> ,
>
> description
>
> ,
>
> completed
>
> ,
>
> created_at
>
> ) and schemas
>
> TaskBase
>
> ,
>
> TaskCreate
>
> ,
>
> TaskUpdate
>
> ,
>
> TaskRead
>
> , plus endpoints
>
> GET/POST /tasks
>
> ,
>
> GET/PATCH/DELETE /tasks/{task_id}
>
> , and
>
> GET /health
>
> . Today we add persistence; in 6.3 we convert every endpoint to use it.

## 2. What is an ORM?

An **ORM** (Object–Relational Mapper) is a translator between two worlds:

| Database world | Python world |
| --- | --- |
| A **table** (`tasks`) | A **class** (`Task`) |
| A **column** (`title`) | An **attribute** (`task.title`) |
| A **row** | An **object/instance** |
| A SQL `INSERT` | `db.add(task)` |
| A SQL `SELECT` | `db.get(Task, 1)` |

Instead of building SQL strings, you work with normal Python objects and the ORM generates the SQL. Compare:

```sql
# Raw SQL (what you did in 6.1)
INSERT INTO tasks (title) VALUES ('Buy milk');

# With an ORM (what you'll do now)
task = Task(title="Buy milk")
db.add(task)
db.commit()
```

| Why use an ORM | The trade-off |
| --- | --- |
| Write Python, not SQL strings | Another library to learn |
| Protects against SQL injection automatically | Hides some SQL details (still learn SQL!) |
| Same code works on SQLite, Postgres, MySQL… | Very complex queries can be awkward |
| Type-safe models that match your Pydantic schemas | A little "magic" to get used to |

We'll use **SQLAlchemy 2.x**, the standard Python ORM and the one FastAPI projects reach for most.

## 3. The four pieces of SQLAlchemy

SQLAlchemy has a handful of moving parts. Once you know what each does, the setup file makes total sense:

| Piece | Job |
| --- | --- |
| **Engine** | The connection to the database. Created once, knows *where* the database is (the URL). |
| **Base** | The parent class all your models inherit from. It collects table definitions (its `metadata`). |
| **Model** | A Python class mapped to a table (e.g. `Task` → `tasks`). |
| **Session** | A short-lived workspace for one batch of reads/writes — a "unit of work". You open one per request. |

## 4. The engine & the connection URL

The **engine** is created from a *database URL*. For a SQLite file in the current folder:

```python
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
```

- `sqlite:///./tasks.db` — the `sqlite://` dialect, then the path. `./tasks.db` is a file in the working directory. (Postgres would be `postgresql://user:pass@host/dbname` — same engine, different URL.)
- `check_same_thread=False` — **SQLite-only**. By default SQLite refuses to be used from more than one thread, but FastAPI handles requests across threads. This flag tells SQLite to allow it. (Safe here because each request gets its own session.)

> **⚠️ Only for SQLite**
>
> connect_args={"check_same_thread": False}
>
> is specific to SQLite. If you ever switch to Postgres, drop it.

## 5. The Base & your first model

Every model inherits from a common **Base** class. In SQLAlchemy 2.x you make one by subclassing `DeclarativeBase`:

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

Now define the `Task` model. The 2.x style uses typed attributes: `Mapped[type]` declares the Python type, and `mapped_column(...)` describes the column (constraints, defaults):

```python
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

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

| Line | Meaning |
| --- | --- |
| `__tablename__ = "tasks"` | Maps this class to the `tasks` table. |
| `Mapped[int]` + `primary_key=True` | The `id` column; SQLite auto-increments it. |
| `Mapped[str \| None]` | An optional column — `None` in Python = `NULL` in SQL. |
| `default=False` | Python-side default for `completed`. |
| `server_default=func.now()` | The *database* stamps the time on insert. |

Notice how closely this mirrors your Pydantic `Task`. The ORM model is the database-facing twin of the Pydantic schema.

## 6. The session: a unit of work

You never use the engine directly in your endpoints. Instead you open a **session** — a temporary workspace that batches your changes and commits them together. You build a session factory once with `sessionmaker`:

```python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

Calling `SessionLocal()` gives you a fresh session bound to the engine. The lifecycle is always: **open → use → commit (or rollback) → close**.

## 7. Creating the tables

The database file has no tables until you make them. The quick way (we'll replace this with Alembic migrations in 6.3) is to ask the Base to create every known table:

```
Base.metadata.create_all(bind=engine)
```

This looks at every model that inherits from `Base` and runs the matching `CREATE TABLE … IF NOT EXISTS`. Run it once at startup.

> **⚠️ create_all can't change existing tables**
>
> create_all
>
> only creates tables that don't exist yet. If you later add a column to a model, it will
>
> not
>
> alter the existing table. That's the exact problem
>
> Alembic migrations
>
> solve in Chunk 6.3 — for now,
>
> create_all
>
> is fine to get started.

## 8. Dependency injection: `get_db()`

Each request needs its own session, and that session must always be closed afterward — even if the request errors. FastAPI's **dependency injection** handles this perfectly with a generator function:

```python
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

The magic is in `yield`: FastAPI runs the code up to `yield` (opening the session), hands the session to your endpoint, and then runs the `finally` block (closing it) after the response is sent. You declare you want one with `Depends`:

```python
from fastapi import Depends

@app.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()   # 2.x style shown in 6.3
    return tasks
```

Now `db` is a ready-to-use session, automatically cleaned up. This is the single most important pattern in this module — every database endpoint takes `db: Session = Depends(get_db)`.

## 9. Pydantic v2 meets the ORM

Your endpoints return ORM `Task` objects, but FastAPI serializes responses through Pydantic schemas like `TaskRead`. By default Pydantic reads from dictionaries, not arbitrary objects. To let it read attributes off an ORM object, enable `from_attributes` in Pydantic v2:

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

With `from_attributes=True`, FastAPI can take the ORM `Task` object your endpoint returns and build a `TaskRead` from `task.id`, `task.title`, etc. — no manual conversion needed.

> **💡 ORM model vs Pydantic schema — keep both**
>
> They look similar but do different jobs. The
>
> SQLAlchemy model
>
> (
>
> models.Task
>
> ) defines the database table. The
>
> Pydantic schema
>
> (
>
> schemas.TaskRead
>
> ) defines the JSON shape going in/out of the API. Keeping them separate means your database and your API contract can evolve independently.

## 10. Putting it together: the file layout

We split the database wiring into its own module so it can be imported anywhere:

```text
tasks-api/
├── app/
│   ├── __init__.py
│   ├── main.py          ← FastAPI app + endpoints
│   ├── database.py      ← engine, SessionLocal, Base, get_db   (NEW)
│   ├── models.py        ← SQLAlchemy models (Task)            (NEW)
│   └── schemas.py       ← Pydantic schemas (TaskRead, …)
└── tasks.db             ← created on first run
```

A minimal `database.py` brings the pieces from sections 4–8 together:

```python
# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

You'll build all of this for real in the lab, then read one task back out of SQLite.

## ✅ Recap

- An **ORM** maps tables↔classes, rows↔objects, columns↔attributes — you write Python, it writes SQL.
- SQLAlchemy's four pieces: the **engine** (connection), **Base** (model registry), **models** (tables), and the **session** (unit of work).
- SQLite needs `connect_args={"check_same_thread": False}` with FastAPI.
- Models use `Mapped[...]` + `mapped_column(...)`; `Base.metadata.create_all()` builds the tables (temporarily, until Alembic).
- Inject a session per request with a `get_db()` generator and `Depends(get_db)`.
- Pydantic v2's `ConfigDict(from_attributes=True)` lets `TaskRead` serialize an ORM object directly.

**Next:** open `assignment.html` and connect your Tasks API to SQLite.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
