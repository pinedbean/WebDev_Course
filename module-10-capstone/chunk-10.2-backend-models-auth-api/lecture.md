*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.2 — Backend: Models, Auth & Core API

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to translate the ERD into **SQLAlchemy 2.x models** with relationships and a many-to-many join.
- How to manage schema changes with an **Alembic migration** (vs. quick `create_all`).
- How to wire **JWT auth** — register, login, `get_current_user` — reusing Module 7.
- The key new idea: an **ownership/authorization dependency** so users only touch projects they own or belong to.
- How to structure the API into routers (`auth`, `projects`, `members`, `tasks`) that scale.

This is the data + auth foundation. The lab delivers a secured API with persistent data.

## 1. From ERD to SQLAlchemy models

Each entity from 10.1 becomes a class that inherits from a shared `Base`. SQLAlchemy 2.x uses typed `Mapped[...]` columns. Here's `User` and `Project` with their relationship:

```python
from datetime import datetime
from sqlalchemy import String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="user")
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    projects: Mapped[list["Project"]] = relationship(back_populates="owner")

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, default="")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    owner: Mapped["User"] = relationship(back_populates="projects")
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project", cascade="all, delete-orphan")
```

The `relationship()` calls give you Python-side navigation: `project.owner`, `user.projects`, `project.tasks`. The `ForeignKey` is the actual DB column; the relationship is the convenient accessor.

> **📝 cascade="all, delete-orphan"**
>
> Deleting a project should delete its tasks too (an orphan task with no project is meaningless). This cascade does that automatically so you don't leave dangling rows.

## 2. Modeling the many-to-many: Membership

Users and Projects are many-to-many. Because our join row carries extra data (`role`), we model it as a **full entity** (an "association object"), not a bare table:

```
class Membership(Base):
    __tablename__ = "memberships"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String, default="member")  # owner|member
```

When a user creates a project, we create *both* the `Project` (with `owner_id`) and a `Membership` row with `role="owner"`. Now every access check can ask one simple question: *"is there a membership row for this user + project?"*

> **💡 Why both owner_id AND a membership?**
>
> owner_id
>
> answers "who can delete/rename the project?" fast. The membership answers "who can see it and its tasks?" Keeping both is a small redundancy that makes authorization checks clean and uniform.

## 3. The Task model & nullable columns

```python
from datetime import date

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, default="")
    status: Mapped[str] = mapped_column(String, default="todo")  # todo|in_progress|done
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True)
    due_date: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    project: Mapped["Project"] = relationship(back_populates="tasks")
```

Note `Mapped[int | None]` and `nullable=True` for the optional assignee and due date — an unassigned task or one without a deadline is valid. We *validate* the status string in Pydantic (next), not in the DB.

## 4. Migrations: Alembic vs. create_all

You have two ways to create the tables. Know both:

| Approach | When |
| --- | --- |
| `Base.metadata.create_all(engine)` | Fast for first-time setup / demos. Creates tables that don't exist — but never *alters* existing ones. |
| **Alembic migration** | The professional choice. Each schema change is a versioned, reviewable, reversible script — exactly what you need once data is real (and in the Bonus Track's cloud DB). |

We initialize Alembic, point it at our models' `Base.metadata`, autogenerate the first migration, and run it:

```bash
alembic init alembic
# edit alembic/env.py: target_metadata = Base.metadata
alembic revision --autogenerate -m "create users, projects, memberships, tasks"
alembic upgrade head
```

> **⚠️ Autogenerate needs to "see" your models**
>
> In
>
> alembic/env.py
>
> you must import the models module so all four classes are registered on
>
> Base.metadata
>
> before autogenerate runs — otherwise it produces an empty migration.

## 5. Auth, reused from Module 7

The auth layer is exactly the pattern you built in Module 7, just applied to TaskFlow's `User`. Three pieces:

- **`security.py`** — `hash_password`/`verify_password` (passlib bcrypt) and `create_access_token`/`decode_access_token` (python-jose).
- **`routers/auth.py`** — `/register` (hash, insert, return token), `/login` (verify, return token), `/me` (return current user).
- **`deps.py`** — `get_current_user` reads the `Authorization: Bearer` token, decodes it, loads the user.

```python
# the heart of register
@router.post("/register", status_code=201, response_model=schemas.Token)
def register(body: schemas.RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == body.email)):
        raise HTTPException(409, "Email already registered")
    user = User(email=body.email, name=body.name,
                hashed_password=hash_password(body.password))
    db.add(user); db.commit(); db.refresh(user)
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}
```

> **📝 Token subject = user id**
>
> We put the user's
>
> id
>
> in the JWT
>
> sub
>
> claim.
>
> get_current_user
>
> decodes it and loads that user from the DB on every protected request — stateless auth that scales across the load-balanced replicas in 10.6.

## 6. The big new idea: ownership & access dependencies

Module 7 taught "only see your own data" for a single owner. TaskFlow adds *collaboration*: a project is visible to its owner **and** its members. We express that as small dependencies that each route reuses.

```python
# app/deps.py
def get_project_for_member(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    membership = db.scalar(
        select(Membership).where(
            Membership.project_id == project_id,
            Membership.user_id == user.id))
    if not membership:
        raise HTTPException(403, "You do not have access to this project")
    return project

def get_project_for_owner(
    project: Project = Depends(get_project_for_member),
    user: User = Depends(get_current_user),
) -> Project:
    if project.owner_id != user.id:
        raise HTTPException(403, "Only the project owner can do this")
    return project
```

Now a route just declares what it needs and the rules are enforced automatically:

```python
@router.get("/{project_id}/tasks")
def list_tasks(project: Project = Depends(get_project_for_member), ...):
    # if we got here, the caller is a member — safe to return tasks
    ...

@router.delete("/{project_id}")
def delete_project(project: Project = Depends(get_project_for_owner), ...):
    # only the owner reaches this line
    ...
```

> **💡 Authorization as composition**
>
> get_project_for_owner
>
> depends on
>
> get_project_for_member
>
> , which depends on
>
> get_current_user
>
> . Each layer adds one check. This is dependency injection (Module 5.4) doing real security work — no copy-pasted
>
> if
>
> blocks scattered across routes.

## 7. Project structure

We split the API into routers, mirroring the contract. Everything mounts under `/api/v1` in `main.py`:

```text
backend/app/
├── main.py            (create app, CORS, include routers under /api/v1)
├── database.py        (engine, SessionLocal, Base, get_db)
├── models.py          (User, Project, Membership, Task)
├── schemas.py         (Pydantic: RegisterIn, ProjectOut, TaskCreate, ...)
├── security.py        (hashing + JWT)
├── deps.py            (get_db, get_current_user, get_project_for_member/owner)
└── routers/
    ├── auth.py        (/auth/register, /login, /me)
    ├── projects.py    (/projects CRUD)
    ├── members.py     (/projects/{id}/members)
    └── tasks.py       (/projects/{id}/tasks CRUD + filters)
```

```
# main.py — mounting routers with the version prefix
app.include_router(auth.router,     prefix="/api/v1/auth",     tags=["auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(members.router,  prefix="/api/v1/projects", tags=["members"])
app.include_router(tasks.router,    prefix="/api/v1/projects", tags=["tasks"])
```

## ✅ Recap

- ERD entities become typed SQLAlchemy 2.x models; relationships give Python-side navigation, foreign keys store the link.
- Many-to-many with extra data → an association entity (`Membership` with a `role`).
- **Alembic** versions every schema change; `create_all` is a quick demo shortcut.
- Auth reuses Module 7: bcrypt hashing, JWT with the user id as subject, `get_current_user`.
- The headline pattern: **ownership dependencies** (`get_project_for_member` / `get_project_for_owner`) enforce access uniformly via composition.

**Next:** open `assignment.html` and build the secured TaskFlow API with persistent data.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
