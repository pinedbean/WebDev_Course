*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Build the backend file by file. Every file is shown complete and copy-pasteable. Final layout:

```text
backend/
├── .env                    (SECRET_KEY, etc. — gitignored)
├── requirements.txt
├── alembic.ini
├── alembic/
│   ├── env.py              (target_metadata = Base.metadata)
│   └── versions/xxxx_create_tables.py
└── app/
    ├── __init__.py
    ├── main.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── security.py
    ├── deps.py
    └── routers/
        ├── __init__.py
        ├── auth.py
        ├── projects.py
        ├── members.py
        └── tasks.py
```

### 1 Install dependencies & the DB layer

```bash
cd backend && source venv/bin/activate
pip install sqlalchemy alembic "passlib[bcrypt]" "python-jose[cryptography]" \
            "pydantic[email]" python-dotenv
pip freeze > requirements.txt
```

Create `.env` (gitignored) and generate a real secret:

```python
python -c "import secrets; print(secrets.token_hex(32))"
# paste the value below
```

```
# backend/.env
SECRET_KEY=PASTE_YOUR_64_CHAR_HEX_HERE
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./taskflow.db
```

`app/database.py`:

```python
# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

# check_same_thread=False is the standard SQLite + FastAPI setting (Module 6.2)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2 The models

```python
# app/models.py
from datetime import datetime, date
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
    memberships: Mapped[list["Membership"]] = relationship(
        cascade="all, delete-orphan")

class Membership(Base):
    __tablename__ = "memberships"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String, default="member")  # owner|member

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, default="")
    status: Mapped[str] = mapped_column(String, default="todo")
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True)
    due_date: Mapped[date | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    project: Mapped["Project"] = relationship(back_populates="tasks")
```

### 3 Alembic migration

```bash
alembic init alembic
```

Edit `alembic/env.py` — import the models so autogenerate sees them, and set the metadata. Near the top, after the config is loaded:

```python
# alembic/env.py  (key edits)
from app.database import Base, DATABASE_URL
from app import models   # noqa: F401  -- registers all tables on Base.metadata

config.set_main_option("sqlalchemy.url", DATABASE_URL)
target_metadata = Base.metadata
```

So Python can import `app`, run Alembic from the `backend/` folder (where `app/` lives). Then:

```bash
alembic revision --autogenerate -m "create users, projects, memberships, tasks"
alembic upgrade head
```

```
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'projects'
INFO  [alembic.autogenerate.compare] Detected added table 'memberships'
INFO  [alembic.autogenerate.compare] Detected added table 'tasks'
INFO  [alembic.runtime.migration] Running upgrade  -> a1b2c3, create tables
```

> **⚠️ Empty migration?**
>
> If the generated file has empty
>
> upgrade()
>
> /
>
> downgrade()
>
> , Alembic didn't see your models. Confirm the
>
> from app import models
>
> line in
>
> env.py
>
> and that you ran from
>
> backend/
>
> .

### 4 Pydantic schemas

```python
# app/schemas.py
from datetime import datetime, date
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, ConfigDict

Status = Literal["todo", "in_progress", "done"]

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    name: str
    role: str

class ProjectCreate(BaseModel):
    name: str
    description: str = ""

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str
    owner_id: int
    created_at: datetime

class MemberInvite(BaseModel):
    email: EmailStr

class MemberOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    role: str
    name: str
    email: EmailStr

class TaskCreate(BaseModel):
    title: str
    description: str = ""
    status: Status = "todo"
    assignee_id: Optional[int] = None
    due_date: Optional[date] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    assignee_id: Optional[int] = None
    due_date: Optional[date] = None

class TaskOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    title: str
    description: str
    status: Status
    assignee_id: Optional[int]
    due_date: Optional[date]
    created_at: datetime
```

> **📝 Literal = free validation**
>
> Typing
>
> status
>
> as
>
> Literal["todo","in_progress","done"]
>
> makes FastAPI reject any other value with a 422 automatically — no manual checks needed.

### 5 Security helpers

```python
# app/security.py
import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MIN)
    return jwt.encode({"sub": subject, "exp": expire},
                      SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]).get("sub")
    except JWTError:
        return None
```

### 6 Dependencies (auth + access control)

```python
# app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import decode_access_token
from app.models import User, Project, Membership

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    cred_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    sub = decode_access_token(token)
    if sub is None:
        raise cred_err
    user = db.get(User, int(sub))
    if user is None:
        raise cred_err
    return user

def get_project_for_member(
    project_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(404, "Project not found")
    is_member = db.scalar(
        select(Membership).where(
            Membership.project_id == project_id,
            Membership.user_id == user.id))
    if is_member is None:
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

> **💡 404 vs 403**
>
> We 404 a missing project and 403 an existing one you can't access. Some apps deliberately 404 both (so attackers can't probe which IDs exist). Either is defensible — be consistent and document it in
>
> SPEC.md
>
> .

### 7 Auth router

```python
# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import User
from app import schemas
from app.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/register", status_code=201, response_model=schemas.Token)
def register(body: schemas.RegisterIn, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == body.email)):
        raise HTTPException(409, "Email already registered")
    user = User(email=body.email, name=body.name,
                hashed_password=hash_password(body.password))
    db.add(user); db.commit(); db.refresh(user)
    return {"access_token": create_access_token(str(user.id)),
            "token_type": "bearer"}

# Form login so Swagger's "Authorize" button works (OAuth2 password flow).
# username = email.
@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Incorrect email or password")
    return {"access_token": create_access_token(str(user.id)),
            "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def me(user: User = Depends(get_current_user)):
    return user
```

> **📝 Why a form for login?**
>
> Using
>
> OAuth2PasswordRequestForm
>
> makes the Swagger "Authorize" button work out of the box (it posts
>
> username
>
> /
>
> password
>
> as form data). Your React frontend will send the same form fields in 10.3.

### 8 Projects router

```python
# app/routers/projects.py
from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, get_project_for_member, get_project_for_owner
from app.models import User, Project, Membership
from app import schemas

router = APIRouter()

@router.get("", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    # projects where the user has a membership row
    ids = db.scalars(
        select(Membership.project_id).where(Membership.user_id == user.id)
    ).all()
    if not ids:
        return []
    return db.scalars(select(Project).where(Project.id.in_(ids))).all()

@router.post("", status_code=201, response_model=schemas.ProjectOut)
def create_project(body: schemas.ProjectCreate,
                   db: Session = Depends(get_db),
                   user: User = Depends(get_current_user)):
    project = Project(name=body.name, description=body.description,
                      owner_id=user.id)
    db.add(project); db.flush()                 # get project.id before commit
    db.add(Membership(project_id=project.id, user_id=user.id, role="owner"))
    db.commit(); db.refresh(project)
    return project

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project: Project = Depends(get_project_for_member)):
    return project

@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(body: schemas.ProjectUpdate,
                   project: Project = Depends(get_project_for_owner),
                   db: Session = Depends(get_db)):
    data = body.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(project, key, value)
    db.commit(); db.refresh(project)
    return project

@router.delete("/{project_id}", status_code=204)
def delete_project(project: Project = Depends(get_project_for_owner),
                   db: Session = Depends(get_db)):
    db.delete(project); db.commit()
    return Response(status_code=204)
```

### 9 Members router

```python
# app/routers/members.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_project_for_member, get_project_for_owner
from app.models import User, Project, Membership
from app import schemas

router = APIRouter()

@router.get("/{project_id}/members", response_model=list[schemas.MemberOut])
def list_members(project: Project = Depends(get_project_for_member),
                 db: Session = Depends(get_db)):
    rows = db.execute(
        select(Membership, User)
        .join(User, User.id == Membership.user_id)
        .where(Membership.project_id == project.id)
    ).all()
    return [schemas.MemberOut(user_id=u.id, role=m.role, name=u.name,
                              email=u.email) for m, u in rows]

@router.post("/{project_id}/members", status_code=201,
             response_model=schemas.MemberOut)
def invite_member(body: schemas.MemberInvite,
                  project: Project = Depends(get_project_for_owner),
                  db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == body.email))
    if user is None:
        raise HTTPException(404, "No user with that email")
    existing = db.scalar(select(Membership).where(
        Membership.project_id == project.id, Membership.user_id == user.id))
    if existing:
        raise HTTPException(409, "User is already a member")
    db.add(Membership(project_id=project.id, user_id=user.id, role="member"))
    db.commit()
    return schemas.MemberOut(user_id=user.id, role="member",
                             name=user.name, email=user.email)
```

### 10 Tasks router (with filters)

```python
# app/routers/tasks.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Response, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_project_for_member
from app.models import Project, Task
from app import schemas

router = APIRouter()

@router.get("/{project_id}/tasks", response_model=list[schemas.TaskOut])
def list_tasks(
    project: Project = Depends(get_project_for_member),
    db: Session = Depends(get_db),
    status: Optional[str] = Query(None),
    assignee_id: Optional[int] = Query(None),
):
    stmt = select(Task).where(Task.project_id == project.id)
    if status:
        stmt = stmt.where(Task.status == status)
    if assignee_id is not None:
        stmt = stmt.where(Task.assignee_id == assignee_id)
    return db.scalars(stmt.order_by(Task.created_at)).all()

@router.post("/{project_id}/tasks", status_code=201,
             response_model=schemas.TaskOut)
def create_task(body: schemas.TaskCreate,
                project: Project = Depends(get_project_for_member),
                db: Session = Depends(get_db)):
    task = Task(project_id=project.id, **body.model_dump())
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.patch("/{project_id}/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, body: schemas.TaskUpdate,
                project: Project = Depends(get_project_for_member),
                db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None or task.project_id != project.id:
        raise HTTPException(404, "Task not found")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit(); db.refresh(task)
    return task

@router.delete("/{project_id}/tasks/{task_id}", status_code=204)
def delete_task(task_id: int,
                project: Project = Depends(get_project_for_member),
                db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if task is None or task.project_id != project.id:
        raise HTTPException(404, "Task not found")
    db.delete(task); db.commit()
    return Response(status_code=204)
```

> **⚠️ Always re-check the project_id**
>
> Even though the member dependency confirmed access to
>
> project_id
>
> , we still verify
>
> task.project_id == project.id
>
> . Otherwise a member of project 3 could edit task 99 belonging to project 7 by guessing the id. Defense in depth.

### 11 Wire it all up in `main.py`

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, projects, members, tasks

app = FastAPI(title="TaskFlow API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,     prefix="/api/v1/auth",     tags=["auth"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(members.router,  prefix="/api/v1/projects", tags=["members"])
app.include_router(tasks.router,    prefix="/api/v1/projects", tags=["tasks"])

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
```

Create empty `app/routers/__init__.py` so it's a package. Run it:

```bash
uvicorn app.main:app --reload
```

### 12 Test the full flow in `/docs`

Open `http://localhost:8000/docs` and walk the happy path, then the denied path:

1. POST `/auth/register` for Ana and for Ben (two accounts). Copy Ana's token.
2. Click **Authorize**, log in as Ana (username = her email).
3. POST `/projects` → "Website". GET `/projects` returns it.
4. POST `/projects/1/members` with Ben's email → 201.
5. POST `/projects/1/tasks` a couple of times; GET with `?status=todo`.
6. Re-authorize as Ben → he sees the project & tasks. Register Cara, authorize as her → GET `/projects/1` returns **403**.

A quick `curl` sanity check (no auth) still works:

```bash
curl http://localhost:8000/api/v1/health
{"status":"ok"}
```

Stop and restart `uvicorn` — your data is still there because it lives in `taskflow.db`.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: app` in Alembic | Run `alembic` from the `backend/` directory, or add the project root to `sys.path` in `env.py`. |
| Login returns 422 | Use the form fields `username`/`password` (Swagger's Authorize box), not JSON. |
| `401` on every protected route | You didn't click Authorize, or the token expired. Re-login. |
| bcrypt error on install | Reinstall: `pip install --upgrade "passlib[bcrypt]"`. On Apple Silicon ensure recent `pip`. |
| Created project not in `GET /projects` | You forgot to also insert the owner `Membership` row in `create_project`. |

## 🎉 Done — what's next

You now have a real, secured backend: four persisted tables, JWT auth, collaboration via memberships, and access rules enforced by composable dependencies. This is the engine the rest of TaskFlow plugs into.

- ✅ Models + Alembic migration; data persists.
- ✅ Register / login / me with JWT.
- ✅ Projects, members, tasks CRUD scoped by ownership/membership.

**Up next → Chunk 10.3: Frontend — Auth, Layout & Project Views.** You'll build login/register pages, an app shell, protected routing, and the projects list wired to this API.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
