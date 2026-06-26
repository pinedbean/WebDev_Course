*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll add password hashing to the Tasks API and build `/auth/register` + `/auth/login`. New/changed files:

```text
tasks-api/
└── app/
    ├── models.py              (extend User)
    ├── schemas.py             (UserCreate / UserLogin / UserOut)
    ├── security.py            (new: bcrypt hashing)
    ├── main.py                (include the auth router)
    └── routers/
        └── auth.py            (new: register + login)
```

### 1 Install passlib + bcrypt

```bash
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install "passlib[bcrypt]"
pip freeze > requirements.txt
```

You should see `passlib` and `bcrypt` appear in `requirements.txt`.

### 2 Extend the User model

Add `hashed_password` and `role`. This is SQLAlchemy 2.x typed-mapping style.

```python
# app/models.py
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)   # NEW
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)  # NEW
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    tasks: Mapped[list["Task"]] = relationship(back_populates="owner")
```

Your existing `Task` model keeps its `owner_id` FK and `owner` relationship — no change needed this chunk.

### 3 Migration

```bash
alembic revision --autogenerate -m "add hashed_password and role to users"
alembic upgrade head
```

Open the generated file in `alembic/versions/` and confirm it has `add_column` calls for `hashed_password` and `role` before running `upgrade`.

> **⚠️ "NOT NULL column added" on existing rows**
>
> SQLite can't add a required column to a table that already has rows without a default. In dev the cleanest fix is to wipe old users first:
>
> sqlite3 tasks.db "DELETE FROM tasks; DELETE FROM users;"
>
> then re-run the upgrade, or delete
>
> tasks.db
>
> and run
>
> alembic upgrade head
>
> from scratch.

### 4 `app/security.py`

One module owns all password logic. Everything else imports from here.

```python
# app/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    """Hash a plaintext password for storage (salted bcrypt)."""
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Return True if the plaintext matches the stored hash."""
    return pwd_context.verify(plain, hashed)
```

### 5 Schemas (Pydantic v2)

Separate "in" schemas (carry the password) from the "out" schema (never does).

```python
# app/schemas.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)   # read from ORM objects
```

> **📝 EmailStr**
>
> EmailStr
>
> needs the
>
> email-validator
>
> package. If you hit an import error, run
>
> pip install "pydantic[email]"
>
> and re-freeze.

### 6 The auth router

Create `app/routers/auth.py`. Both endpoints live here.

```python
# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import hash_password, verify_password
from app import models, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut,
             status_code=status.HTTP_201_CREATED)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    email = data.email.lower()
    existing = db.query(models.User).filter(models.User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(email=email, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}   # 7.2: return a JWT here
```

### 7 Register the router

```python
# app/main.py
from fastapi import FastAPI
from app.routers import auth, tasks   # tasks from Module 6

app = FastAPI(title="Tasks API")

app.include_router(auth.router)
app.include_router(tasks.router)
```

### 8 Run & test

```bash
uvicorn app.main:app --reload
```

At `http://localhost:8000/docs`, expand **POST /auth/register** and send:

```json
{ "email": "jane@example.com", "password": "supersecret123" }
```

**Expected (201):** note there is *no* password field in the response.

```json
{
  "id": 1,
  "email": "jane@example.com",
  "role": "user",
  "created_at": "2026-06-26T10:15:00+00:00"
}
```

Confirm the database stored a hash, not plaintext:

```sql
sqlite3 tasks.db "SELECT email, hashed_password FROM users;"
# jane@example.com|$2b$12$Nl2....   <- starts with $2b$ = bcrypt. 
```

Now test **POST /auth/login**:

```json
{ "email": "jane@example.com", "password": "supersecret123" }   -> 200 {"message":"Login successful"}
{ "email": "jane@example.com", "password": "WRONG" }            -> 401 {"detail":"Invalid credentials"}
{ "email": "nobody@example.com", "password": "whatever" }       -> 401 {"detail":"Invalid credentials"}
```

Notice the wrong password and the unknown email give the **exact same** 401 — that's the account-enumeration defense from the lecture.

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: passlib` | venv not active, or you installed globally. Activate it and re-run `pip install "passlib[bcrypt]"`. |
| `AttributeError: module 'bcrypt' has no attribute '__about__'` | A known passlib/bcrypt version mismatch. Pin a compatible bcrypt: `pip install "bcrypt<4.1"` (or upgrade passlib). Hashing still works either way; this is just a noisy warning in some combos. |
| `email-validator is not installed` | `pip install "pydantic[email]"` for `EmailStr`. |
| Migration says "no changes detected" | Alembic can't see your model. Make sure `models.py` is imported in `alembic/env.py` and `target_metadata = Base.metadata`. |
| Response includes the hash | You returned the ORM object without `response_model=schemas.UserOut`, or `UserOut` still lists a password field. Fix the schema. |

## 📄 Complete `app/security.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

## 🎉 You're done

Your Tasks API now stores **salted bcrypt hashes** and verifies logins without ever keeping a readable password. You've built the foundation every login system stands on.

Right now `/auth/login` just says "successful" — the browser still can't stay logged in. In the next chunk you'll issue a **JWT** on login and use it to protect your task routes so each user only touches their own data.

**Up next → Chunk 7.2: JWT Tokens & Protected Routes.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
