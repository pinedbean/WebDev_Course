*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll add JWT issuing, a `get_current_user` dependency, `/auth/me`, and owner-scoped task routes. New/changed files:

```text
tasks-api/
└── app/
    ├── security.py            (add JWT functions)
    ├── schemas.py             (add Token)
    ├── deps.py                (new: oauth2_scheme + get_current_user)
    ├── routers/
    │   ├── auth.py            (token login + /me)
    │   └── tasks.py           (scope to owner_id)
```

### 1 Install & set the secret

```python
pip install "python-jose[cryptography]"
pip freeze > requirements.txt

python -c "import secrets; print(secrets.token_hex(32))"
export SECRET_KEY="paste-the-64-char-value"   # PowerShell: $env:SECRET_KEY="..."
```

> **📝 Same terminal**
>
> export
>
> only lives in the current shell. Start
>
> uvicorn
>
> in that
>
> same
>
> terminal so it sees
>
> SECRET_KEY
>
> . (7.4 makes this permanent with a
>
> .env
>
> file.)

### 2 JWT functions in `security.py`

```python
# app/security.py  (full file)
import os
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
```

### 3 Token schema

```
# app/schemas.py  (add)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

### 4 `app/deps.py` — the dependency

```python
# app/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import decode_access_token
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_error
    user = db.get(models.User, int(user_id))
    if user is None:
        raise credentials_error
    return user
```

### 5 Login (form) + `/auth/me`

```python
# app/routers/auth.py  (full file)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import hash_password, verify_password, create_access_token
from app.deps import get_current_user
from app import models, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut,
             status_code=status.HTTP_201_CREATED)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    email = data.email.lower()
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=email, hashed_password=hash_password(data.password))
    db.add(user); db.commit(); db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # OAuth2 form sends "username" + "password"; we use the email as username.
    user = db.query(models.User).filter(
        models.User.email == form_data.username.lower()
    ).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user
```

> **📝 Why login no longer takes JSON**
>
> Switching to
>
> OAuth2PasswordRequestForm
>
> means login expects form fields (
>
> username
>
> ,
>
> password
>
> ). That's what the docs Authorize button and the
>
> OAuth2PasswordBearer
>
> spec expect, and what your React app will send in 7.3 (as
>
> application/x-www-form-urlencoded
>
> ).

### 6 Scope the task routes

```python
# app/routers/tasks.py  (full file)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app import models, schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_owned_task(task_id: int, db: Session, current_user: models.User) -> models.Task:
    task = db.get(models.Task, task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db),
               current_user: models.User = Depends(get_current_user)):
    return (db.query(models.Task)
              .filter(models.Task.owner_id == current_user.id)
              .all())

@router.post("", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    task = models.Task(**data.model_dump(), owner_id=current_user.id)
    db.add(task); db.commit(); db.refresh(task)
    return task

@router.get("/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db),
             current_user: models.User = Depends(get_current_user)):
    return get_owned_task(task_id, db, current_user)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, data: schemas.TaskUpdate, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    task = get_owned_task(task_id, db, current_user)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit(); db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db),
                current_user: models.User = Depends(get_current_user)):
    task = get_owned_task(task_id, db, current_user)
    db.delete(task); db.commit()
```

### 7 Run & verify the flow

```bash
uvicorn app.main:app --reload
```

At `/docs`: register `a@x.com` and `b@x.com`, click **Authorize**, log in as A (username = email).

**Login response (200):**

```json
{ "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", "token_type": "bearer" }
```

Create a task as A, then list — only A's tasks come back. Authorize as B and list — empty. Try B fetching A's task id:

```
GET /tasks/1   (as B)   ->  404 {"detail":"Task not found"}
GET /tasks     (no auth) -> 401 {"detail":"Not authenticated"}
GET /auth/me   (as A)    -> 200 {"id":1,"email":"a@x.com","role":"user",...}
```

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Every protected call is `401` even after login | You logged in but didn't click **Authorize** in docs, or your client isn't sending `Authorization: Bearer <token>`. |
| `Signature verification failed` / random 401s | The `SECRET_KEY` changed between issuing and verifying (you restarted uvicorn in a shell without the env var). Use the same key consistently. |
| `422 Unprocessable Entity` on login | You're sending JSON to the form endpoint. Use form fields `username`/`password` (the docs form does this automatically). |
| `ImportError: cannot import name 'jwt'` | Install the right package: `pip install "python-jose[cryptography]"` (not `jose`). |
| Circular import between `deps.py` and `auth.py` | Keep `oauth2_scheme` + `get_current_user` in `deps.py`, import it into routers — never the reverse. |
| `sub` must be a string | python-jose is strict: pass `str(user.id)` to `create_access_token` and `int(user_id)` when loading. |

## 📄 Complete `app/deps.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import decode_access_token
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = decode_access_token(token)
    if user_id is None:
        raise credentials_error
    user = db.get(models.User, int(user_id))
    if user is None:
        raise credentials_error
    return user
```

## 🎉 You're done

The Tasks API is now a real authenticated backend: login mints a signed JWT, `get_current_user` guards every protected route, and each user's data is isolated by `owner_id`. You proved it by confirming user B can't see or fetch user A's tasks.

So far you've tested through `/docs`. Next you'll put a friendly face on it: a React login/register UI that stores the token, attaches it to every request, and protects pages behind a real auth flow.

**Up next → Chunk 7.3: Frontend Auth Flow in React.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
