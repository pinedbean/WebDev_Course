*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.4 — Relationships & Queries

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why real apps split data across multiple tables — **relationships**.
- **Foreign keys**: how a row in one table points at a row in another.
- Modeling a **one-to-many** relationship (a User has many Tasks) in SQLAlchemy with `relationship()`.
- **Joins**, **filtering**, and **sorting** across tables — and exposing them as query params.
- **Indexes**: why they matter and where to add them.

In the lab you'll add a `User` entity related to `Task`, then assemble the full-stack Module 6 Checkpoint: React + FastAPI + SQLite with persistent, related data.

## 1. Why relationships?

Right now every task is an island. But tasks belong to *someone*. We could cram an owner's name into every task row, but that duplicates data and gets out of sync the moment a name changes. The relational answer is to put users in their **own table** and have each task *point* at its owner:

| users |  |  |
| --- | --- | --- |
| id | email | created_at |
| 1 | jane@example.com | 2026-06-26 09:00 |
| 2 | sam@example.com | 2026-06-26 09:05 |

| tasks |  |  |  |
| --- | --- | --- | --- |
| id | title | completed | owner_id |
| 1 | Buy milk | 0 | 1 |
| 2 | Finish report | 1 | 1 |
| 3 | Call dentist | 0 | 2 |

Tasks 1 and 2 belong to user 1 (Jane); task 3 belongs to user 2 (Sam). The `owner_id` column is the link. This is a **one-to-many** relationship: one user has many tasks; each task has exactly one user.

> **📝 Where this leads**
>
> In
>
> Module 7
>
> the
>
> User
>
> grows a hashed password and login, and tasks get scoped to "the logged-in user" automatically. For now we keep
>
> User
>
> minimal (just
>
> id
>
> ,
>
> email
>
> ,
>
> created_at
>
> ) and pass
>
> owner_id
>
> explicitly so you can focus on the
>
> relationship
>
> mechanics.

## 2. Foreign keys

A **foreign key** (FK) is a column whose value must match a primary key in another table. `tasks.owner_id` is a foreign key referencing `users.id`. The database can *enforce* this — refusing a task whose `owner_id` doesn't exist (referential integrity).

```sql
-- in raw SQL the FK looks like this:
CREATE TABLE tasks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    title     TEXT    NOT NULL,
    owner_id  INTEGER NOT NULL REFERENCES users(id),
    ...
);
```

> **⚠️ SQLite doesn't enforce FKs by default**
>
> For backward compatibility, SQLite only enforces foreign keys if you turn them on per connection with
>
> PRAGMA foreign_keys=ON
>
> . With SQLAlchemy you enable it once via an event listener (shown in the solution). Postgres enforces FKs always.

## 3. Defining the relationship in SQLAlchemy

Two things express a one-to-many in the ORM: a `ForeignKey` column on the "many" side, and a `relationship()` on *both* sides linked by `back_populates`. First the `User` model:

```python
# app/models.py
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    # one user -> many tasks
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
```

Then add the FK and the reverse relationship to `Task`:

```
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, nullable=False
    )
    # many tasks -> one user
    owner: Mapped["User"] = relationship(back_populates="tasks")
```

| Piece | What it gives you in Python |
| --- | --- |
| `ForeignKey("users.id")` | The database link from a task to its user. |
| `User.tasks` | A list of that user's `Task` objects — `jane.tasks`. |
| `Task.owner` | The `User` object that owns a task — `task.owner.email`. |
| `back_populates` | Keeps both sides in sync — appending to `jane.tasks` sets `task.owner`. |
| `cascade="all, delete-orphan"` | Deleting a user also deletes their tasks (no orphaned rows). |

## 4. One-to-many vs many-to-many

Our users↔tasks link is **one-to-many**. The other common shape is **many-to-many**: e.g. a task can have many tags, and a tag can apply to many tasks. That needs a third *association table* holding pairs of ids:

| Relationship | Example | How it's modeled |
| --- | --- | --- |
| One-to-many | User → Tasks | FK column on the "many" side (what we're building) |
| Many-to-many | Tasks ↔ Tags | A separate `task_tags` association table |
| One-to-one | User → Profile | FK with a `unique` constraint |

We'll implement one-to-many here; many-to-many tags are a stretch goal in the lab.

## 5. Querying across tables

### Accessing related objects

Once the relationship exists, you traverse it like normal Python attributes — the ORM fetches the related rows for you:

```
user = db.get(models.User, 1)
print(user.email)                 # jane@example.com
print(len(user.tasks))            # 2
for t in user.tasks:
    print(t.title)                # Buy milk, Finish report

task = db.get(models.Task, 3)
print(task.owner.email)           # sam@example.com
```

### Joins & filtering by the related table

To filter tasks by something on the user, use a `join`. To filter by the FK directly, just add a `where`:

```python
from sqlalchemy import select

# all tasks belonging to user 1 (filter on the FK — no join needed)
stmt = select(models.Task).where(models.Task.owner_id == 1)
tasks = db.scalars(stmt).all()

# all tasks owned by a given email (join to users)
stmt = (
    select(models.Task)
    .join(models.User)
    .where(models.User.email == "jane@example.com")
)
tasks = db.scalars(stmt).all()
```

### Filtering & sorting

Chain `where`, `order_by`, and `limit` to build exactly the query you need:

```
stmt = (
    select(models.Task)
    .where(models.Task.completed == False)   # only unfinished
    .order_by(models.Task.created_at.desc()) # newest first
    .limit(20)
)
```

These map directly onto the SQL clauses you learned in 6.1 — `WHERE`, `ORDER BY`, `LIMIT`. The ORM is just generating that SQL.

## 6. Exposing filters as query params

A great API lets the client choose what to fetch via query parameters. Build the query conditionally:

```python
@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(
    completed: bool | None = None,
    owner_id: int | None = None,
    sort: str = "created_at",
    db: Session = Depends(get_db),
):
    stmt = select(models.Task)
    if completed is not None:
        stmt = stmt.where(models.Task.completed == completed)
    if owner_id is not None:
        stmt = stmt.where(models.Task.owner_id == owner_id)
    if sort == "title":
        stmt = stmt.order_by(models.Task.title)
    else:
        stmt = stmt.order_by(models.Task.created_at.desc())
    return list(db.scalars(stmt))
```

Now `GET /tasks?completed=false&owner_id=1&sort=title` returns user 1's unfinished tasks, sorted by title. Each filter is optional.

## 7. The N+1 problem & eager loading (intro)

By default SQLAlchemy loads related objects **lazily** — it runs an extra query the first time you touch `task.owner`. Loop over 100 tasks and read each owner, and you fire 1 query for the tasks plus 100 more for owners: the infamous **N+1 problem**.

When you know you'll need the related data, load it *eagerly* in one go with `selectinload`:

```python
from sqlalchemy.orm import selectinload

# fetch users AND all their tasks in just two queries total
stmt = select(models.User).options(selectinload(models.User.tasks))
users = db.scalars(stmt).all()
```

You don't need this for small datasets, but it's the first optimization to reach for when listing related data gets slow.

## 8. Indexes (intro)

An **index** is a lookup structure the database keeps so it can find rows by a column *without scanning the whole table* — like the index at the back of a book. Without one, `WHERE owner_id = 1` reads every row; with one, it jumps straight to the matches.

| Add an index when… | How |
| --- | --- |
| You filter/sort by a column often | `mapped_column(..., index=True)` |
| A column must be unique (like `email`) | `mapped_column(..., unique=True, index=True)` |
| It's a foreign key you filter by | `mapped_column(ForeignKey(...), index=True)` |

That's why our `User.email` is `unique=True, index=True` and `Task.owner_id` is `index=True`. Indexes speed up reads but slightly slow writes and use disk — so index the columns you actually query, not every column.

> **💡 Migrations carry indexes too**
>
> Because indexes and FKs are part of the schema, adding them is just another Alembic migration: change the model,
>
> alembic revision --autogenerate -m "add users and owner_id"
>
> , then
>
> alembic upgrade head
>
> .

## 9. Schemas for related data

Expose the relationship in your API by adding schemas for `User` and including `owner_id` on tasks. You can even nest a user's tasks in the read schema:

```python
# app/schemas.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class UserCreate(BaseModel):
    email: EmailStr

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    tasks: list[TaskRead] = []          # nested!
    model_config = ConfigDict(from_attributes=True)
```

With `from_attributes=True`, returning a `User` ORM object yields JSON with the user *and* their tasks embedded. (`EmailStr` needs `pip install "pydantic[email]"`.)

## ✅ Recap

- Relationships split data across tables; a **foreign key** (`tasks.owner_id → users.id`) is the link.
- Model a one-to-many with a `ForeignKey` column plus `relationship(back_populates=...)` on both sides; `User.tasks` and `Task.owner` become Python attributes.
- Query across tables with `.where()` on the FK, or `.join()` for conditions on the other table; combine with `order_by`/`limit`.
- Expose filters as optional query params by building the `select()` conditionally.
- Watch for the **N+1 problem**; reach for `selectinload` when listing related data.
- Add **indexes** to columns you filter/sort by (and unique ones like `email`); ship schema changes as Alembic migrations.

**Next:** open `assignment.html` — add the User relationship and build the full-stack Module 6 Checkpoint.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
