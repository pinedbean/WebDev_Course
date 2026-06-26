*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Part A builds the User↔Task relationship and queries on the backend. Part B is the full-stack checkpoint: a React UI driving it all. Every file is shown complete and copy-pasteable.

```text
tasks-api/                       taskflow-ui/ (React, from Module 4/5)
├── app/                         └── src/
│   ├── main.py                      ├── api.js     ← fetch helpers   (NEW)
│   ├── database.py  ← FK pragma     └── App.jsx    ← checkpoint UI
│   ├── models.py    ← User + FK
│   ├── schemas.py   ← user schemas
│   └── crud.py      ← user CRUD
├── alembic/versions/...             (migration)
└── tasks.db
```

## Part A — The User relationship

### 1 `app/database.py` — enforce foreign keys

Same engine/session as before, plus an event listener so every SQLite connection enables FK enforcement:

```python
# app/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# SQLite ignores foreign keys unless we turn them on per connection.
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2 `app/models.py` — User + Task with relationship

```python
# app/models.py
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

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

    owner: Mapped["User"] = relationship(back_populates="tasks")
```

### 3 `app/schemas.py` — user & owner schemas

```python
# app/schemas.py
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False

class TaskCreate(TaskBase):
    owner_id: int                       # which user owns this task

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

class TaskRead(TaskBase):
    id: int
    created_at: datetime
    owner_id: int
    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email: EmailStr

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    tasks: list[TaskRead] = []
    model_config = ConfigDict(from_attributes=True)
```

### 4 `app/crud.py` — add user functions

Keep the task functions from 6.3 and add the user ones. `create_task` now passes `owner_id` through (it's part of `TaskCreate`):

```python
# app/crud.py
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app import models, schemas

# ---- Users ----
def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(email=data.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db: Session, user_id: int) -> models.User | None:
    stmt = (
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.tasks))
    )
    return db.scalars(stmt).first()

def get_users(db: Session) -> list[models.User]:
    return list(db.scalars(select(models.User)))

# ---- Tasks ----
def get_tasks(
    db: Session,
    completed: bool | None = None,
    owner_id: int | None = None,
    sort: str = "created_at",
) -> list[models.Task]:
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

def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)

def create_task(db: Session, data: schemas.TaskCreate) -> models.Task:
    task = models.Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task: models.Task, data: schemas.TaskUpdate) -> models.Task:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()
```

### 5 `app/main.py` — users + filtering

```python
# app/main.py
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

app = FastAPI(title="Tasks API")

# CORS (from Module 5) so the React dev server can call us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

# ---- Users ----
@app.post("/users", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, data)

@app.get("/users", response_model=list[schemas.UserRead])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.get("/users/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ---- Tasks ----
@app.get("/tasks", response_model=list[schemas.TaskRead])
def list_tasks(
    completed: bool | None = None,
    owner_id: int | None = None,
    sort: str = "created_at",
    db: Session = Depends(get_db),
):
    return crud.get_tasks(db, completed=completed, owner_id=owner_id, sort=sort)

@app.post("/tasks", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    if crud.get_user(db, data.owner_id) is None:
        raise HTTPException(status_code=400, detail="owner_id does not exist")
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

### 6 Migrate & verify

```bash
alembic revision --autogenerate -m "add users and task owner_id"
```

```
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added column 'tasks.owner_id'
INFO  [alembic.autogenerate.compare] Detected added index ...
  Generating .../versions/b2c3d4e5f6a7_add_users_and_task_owner_id.py ...  done
```

```bash
alembic upgrade head
```

> **⚠️ Existing rows + a NOT NULL FK**
>
> If your
>
> tasks.db
>
> already has tasks (with no owner), adding a
>
> NOT NULL owner_id
>
> will fail. Easiest for the lab: start fresh —
>
> rm tasks.db
>
> , then
>
> alembic upgrade head
>
> . (In production you'd add the column nullable, backfill owners, then tighten it.)

Test in `/docs`: **POST /users** `{"email": "jane@example.com"}` → user 1. **POST /tasks** `{"title": "Buy milk", "owner_id": 1}`. Then **GET /users/1**:

```json
{
  "id": 1,
  "email": "jane@example.com",
  "created_at": "2026-06-26T09:00:00",
  "tasks": [
    { "title": "Buy milk", "description": null, "completed": false,
      "id": 1, "created_at": "2026-06-26T09:01:00", "owner_id": 1 }
  ]
}
```

The user comes back with their tasks nested — the relationship works. Try `GET /tasks?owner_id=1&completed=false&sort=title` to see filtering + sorting.

## 🏁 Part B — Module 6 Checkpoint: React + FastAPI + SQLite

Now the frontend. These two files turn your API into a working full-stack app. Drop them into your Module 4/5 React project's `src/`.

### 7 `src/api.js` — fetch helpers

```javascript
// src/api.js
const BASE = "http://127.0.0.1:8000";

export async function getUsers() {
  const res = await fetch(`${BASE}/users`);
  return res.json();
}

export async function createUser(email) {
  const res = await fetch(`${BASE}/users`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email }),
  });
  return res.json();
}

export async function getTasks(ownerId, completed) {
  const params = new URLSearchParams({ owner_id: ownerId });
  if (completed !== null) params.set("completed", completed);
  const res = await fetch(`${BASE}/tasks?${params}`);
  return res.json();
}

export async function createTask(title, ownerId) {
  const res = await fetch(`${BASE}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, owner_id: ownerId }),
  });
  return res.json();
}

export async function toggleTask(id, completed) {
  const res = await fetch(`${BASE}/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  return res.json();
}

export async function deleteTask(id) {
  await fetch(`${BASE}/tasks/${id}`, { method: "DELETE" });
}
```

### 8 `src/App.jsx` — the checkpoint UI

User picker + create, task list scoped to the user, create/toggle/delete, and an All/Active/Completed filter:

```python
// src/App.jsx
import { useEffect, useState } from "react";
import * as api from "./api";

export default function App() {
  const [users, setUsers] = useState([]);
  const [currentUserId, setCurrentUserId] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("all");   // all | active | completed
  const [newEmail, setNewEmail] = useState("");
  const [newTitle, setNewTitle] = useState("");

  // load users once
  useEffect(() => {
    api.getUsers().then((data) => {
      setUsers(data);
      if (data.length && currentUserId === null) setCurrentUserId(data[0].id);
    });
  }, []);

  // (re)load tasks whenever the user or filter changes
  useEffect(() => {
    if (currentUserId === null) return;
    const completed = filter === "all" ? null : filter === "completed";
    api.getTasks(currentUserId, completed).then(setTasks);
  }, [currentUserId, filter]);

  async function addUser(e) {
    e.preventDefault();
    if (!newEmail.trim()) return;
    const user = await api.createUser(newEmail.trim());
    setUsers([...users, user]);
    setCurrentUserId(user.id);
    setNewEmail("");
  }

  async function addTask(e) {
    e.preventDefault();
    if (!newTitle.trim() || currentUserId === null) return;
    await api.createTask(newTitle.trim(), currentUserId);
    setNewTitle("");
    reload();
  }

  function reload() {
    const completed = filter === "all" ? null : filter === "completed";
    api.getTasks(currentUserId, completed).then(setTasks);
  }

  async function onToggle(t) {
    await api.toggleTask(t.id, !t.completed);
    reload();
  }

  async function onDelete(id) {
    await api.deleteTask(id);
    reload();
  }

  return (
    <main style={{ maxWidth: 560, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>TaskFlow (Module 6)</h1>

      <section>
        <h2>User</h2>
        <select
          value={currentUserId ?? ""}
          onChange={(e) => setCurrentUserId(Number(e.target.value))}
        >
          {users.map((u) => (
            <option key={u.id} value={u.id}>{u.email}</option>
          ))}
        </select>
        <form onSubmit={addUser}>
          <input
            placeholder="new user email"
            value={newEmail}
            onChange={(e) => setNewEmail(e.target.value)}
          />
          <button>Add user</button>
        </form>
      </section>

      <section>
        <h2>Tasks</h2>
        <form onSubmit={addTask}>
          <input
            placeholder="new task title"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
          />
          <button>Add task</button>
        </form>

        <div>
          {["all", "active", "completed"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{ fontWeight: filter === f ? "bold" : "normal" }}
            >{f}</button>
          ))}
        </div>

        <ul>
          {tasks.map((t) => (
            <li key={t.id}>
              <input
                type="checkbox"
                checked={t.completed}
                onChange={() => onToggle(t)}
              />
              <span style={{ textDecoration: t.completed ? "line-through" : "none" }}>
                {t.title}
              </span>
              <button onClick={() => onDelete(t.id)}>✕</button>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
```

### 9 Run the full stack

```bash
# terminal 1 — backend
uvicorn app.main:app --reload

# terminal 2 — frontend
npm run dev
```

Open `http://localhost:5173`. Add a user, select them, add tasks, check them off, delete one, and flip the All/Active/Completed filter. Every action hits FastAPI, which reads/writes `tasks.db`.

### 10 Prove it end-to-end

- **Persistence:** create tasks, stop the backend (`Ctrl`+`C`), restart it, refresh the page — your data is still there.
- **Relationship/scoping:** add a second user, switch the dropdown — each user sees only their own tasks.
- **Ground truth:** `sqlite3 tasks.db "SELECT t.title, u.email FROM tasks t JOIN users u ON u.id = t.owner_id;"` shows each task next to its owner.

That's a complete full-stack CRUD app with persistent, related data: **React → FastAPI → SQLite**. 🏁

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Migration fails: `NOT NULL constraint failed: tasks.owner_id` | Existing tasks have no owner. For the lab, `rm tasks.db` and re-run `alembic upgrade head`. |
| You can create a task with a bogus `owner_id` | Enable the FK pragma (step 1) and keep the `owner_id` existence check in `POST /tasks`. |
| Autogenerate didn't detect `users` | Import `app.models` in `alembic/env.py` and set `target_metadata = Base.metadata` (from 6.3). |
| Browser console: CORS error | Add the `CORSMiddleware` with `allow_origins=["http://localhost:5173"]`; match your actual frontend URL/port. |
| `ImportError: email-validator is not installed` | `pip install "pydantic[email]"` for `EmailStr`. |
| Listing users runs one query per user's tasks (N+1) | Use `selectinload(models.User.tasks)` as in `get_user`; apply it to `get_users` too. |
| UI shows no tasks after switching users | Make sure the tasks `useEffect` depends on `currentUserId` and `filter`, and that `getTasks` passes `owner_id`. |

## 🎉 Module 6 complete

You took the Tasks API from volatile in-memory data to a real, persistent, *relational* database — and wired it to a React frontend for a complete full-stack app. Along the way you learned:

- **6.1** raw SQL & SQLite fundamentals.
- **6.2** the SQLAlchemy ORM, sessions, and dependency-injected DB access.
- **6.3** a repository layer, DB-backed CRUD, and Alembic migrations.
- **6.4** relationships, foreign keys, joins, filtering/sorting, and indexes.

> **📝 The honest gap → Module 7**
>
> Right now the client picks any
>
> owner_id
>
> it wants — there's no real security. That's deliberate: you focused on data modeling.
>
> Module 7 (Authentication & Security)
>
> adds password hashing, login, and JWT tokens so the server knows
>
> who
>
> is calling, derives
>
> owner_id
>
> from the authenticated user, and ensures each person sees only their own tasks.

**Up next → Module 7, Chunk 7.1: Auth Concepts & Password Hashing.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
