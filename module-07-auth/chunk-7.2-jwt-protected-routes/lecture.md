*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.2 — JWT Tokens & Protected Routes

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What a **JWT** is: its three parts (header, payload, signature) and what each does.
- How signing/verifying makes a token **tamper-proof** — and why it is *not* encrypted.
- Access tokens, **expiry**, and a `SECRET_KEY`.
- Creating and decoding JWTs in FastAPI with **python-jose**.
- Wiring `OAuth2PasswordBearer` and a **`get_current_user`** dependency to protect routes.
- Scoping the Tasks API so each user only sees their **own** tasks.

In the lab you'll issue a JWT on login, add a `get_current_user` dependency, build `GET /auth/me`, and lock down every task route.

## 1. The problem JWTs solve

In 7.1 login ended with "Login successful" — but the very next request the server has no idea who you are again (HTTP is stateless). We need the browser to carry *proof of identity* on every request. That proof is a **token**.

A **JWT** (JSON Web Token, pronounced "jot") is a compact, signed string the server issues at login. The browser stores it and sends it back on each request in an `Authorization` header. Because the token is *signed*, the server can trust it without looking anything up in a session store — that's **stateless** auth, and it's what makes the load-balanced setup in Module 9 simple.

>

## 2. Anatomy of a JWT

A JWT is three Base64url chunks joined by dots: `header.payload.signature`.

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzE4OTk5OTk5fQ.3a8f...signature...
```

| Part | Contains | Example (decoded) |
| --- | --- | --- |
| **Header** | The algorithm & token type | `{"alg":"HS256","typ":"JWT"}` |
| **Payload** | The *claims*: who the user is + metadata | `{"sub":"1","exp":1718999999}` |
| **Signature** | A cryptographic seal over header+payload using your `SECRET_KEY` | `HMACSHA256(...)` |

Common **claims** in the payload:

- `sub` ("subject") — who the token is about. We put the **user id** here (as a string).
- `exp` ("expiration") — a Unix timestamp after which the token is invalid.
- `iat` ("issued at") — when it was created (optional but useful).

> **⚠️ The payload is readable by anyone**
>
> A JWT is
>
> signed, not encrypted
>
> . Anyone holding the token can Base64-decode the payload and read every claim (try pasting one into
>
> jwt.io
>
> ).
>
> Never put secrets in a JWT
>
> — no passwords, no credit cards. Put only an identifier (the user id) and non-sensitive metadata.

## 3. Signing & verifying — what the signature buys you

The signature is computed from the header, the payload, and your server's `SECRET_KEY`. If anyone changes a single character of the payload (say, to impersonate another user), the signature no longer matches and verification fails.

- **Only your server** knows the `SECRET_KEY`, so only your server can mint valid tokens.
- Anyone can *read* a token, but nobody can *forge* or *tamper with* one without the key.
- So if a token verifies, you can trust its claims came from your server.

> **⚠️ Protect the SECRET_KEY like a password**
>
> If your
>
> SECRET_KEY
>
> leaks, attackers can mint tokens for
>
> any
>
> user. Keep it in an environment variable /
>
> .env
>
> file —
>
> never hard-code it in source or commit it to Git
>
> . Generate a strong one:
>
> python -c "import secrets; print(secrets.token_hex(32))"
>
> . (We harden secrets management properly in 7.4.)

## 4. Access tokens & expiry

The token you issue at login is an **access token** — it grants access to protected routes. It must **expire** (the `exp` claim) so a stolen token isn't useful forever. A common access-token lifetime is short, e.g. **15–60 minutes**.

"But then users get logged out constantly?" That's what **refresh tokens** solve — a longer-lived token used only to get a fresh access token. We add those in 7.4. For now, a single access token with a sensible expiry is exactly right.

## 5. JWTs in FastAPI with python-jose

Install the library (the `cryptography` extra provides the signing backend):

```bash
pip install "python-jose[cryptography]"
```

Add token functions to `security.py` next to your password helpers:

```python
# app/security.py  (additions)
import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")   # 7.4: load from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(subject: str) -> str:
    """Sign a JWT whose 'sub' claim is the user id (a string)."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str | None:
    """Return the user id from a valid token, or None if invalid/expired."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
```

`jwt.decode` automatically rejects an expired or tampered token by raising `JWTError`, which we turn into `None`. Now update login to return a token instead of a message:

```python
# app/routers/auth.py  (updated login)
from app.security import verify_password, create_access_token

@router.post("/login", response_model=schemas.Token)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email.lower()).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
```

With a tiny `Token` schema:

```
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

## 6. OAuth2PasswordBearer — telling FastAPI where the token comes from

FastAPI ships an OAuth2 helper that reads the token out of the `Authorization: Bearer ...` header and powers the green "Authorize" button in `/docs`. Point it at your login URL:

```python
# app/deps.py
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
```

When a route depends on `oauth2_scheme`, FastAPI will: (a) extract the bearer token from the header, and (b) automatically return `401` if it's missing.

> **📝 The OAuth2 "password flow" expects form fields**
>
> The standard token endpoint receives
>
> form-encoded
>
> username
>
> &
>
> password
>
> (not JSON), via FastAPI's
>
> OAuth2PasswordRequestForm
>
> . That's what makes the
>
> /docs
>
> Authorize button work. In the lab you'll switch login to this form so the docs UI and your future frontend both work cleanly. (Our "username" field will just hold the email.)

## 7. The get_current_user dependency

This is the keystone. One dependency that: reads the token → decodes it → loads the user from the DB → hands it to your route. Any route that wants "the logged-in user" just declares it as a parameter.

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

Now a protected route is trivially:

```python
# app/routers/auth.py
from app.deps import get_current_user

@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(get_current_user)):
    return current_user
```

Hit `GET /auth/me` with no token → `401`. With a valid token → your user. The dependency is reusable across every protected endpoint in your app.

## 8. Scoping tasks to the current user

Authentication isn't useful until your data respects it. Add the same dependency to your task routes and filter by `owner_id` so users only see and touch their own tasks.

```python
# app/routers/tasks.py  (key changes)
from app.deps import get_current_user

@router.get("", response_model=list[schemas.TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()

@router.post("", response_model=schemas.TaskOut, status_code=201)
def create_task(
    data: schemas.TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task = models.Task(**data.model_dump(), owner_id=current_user.id)  # owner = you
    db.add(task); db.commit(); db.refresh(task)
    return task
```

For **get one / update / delete**, fetch the task *and* require it belongs to the current user — otherwise `404` (not `403`, so you don't even reveal that someone else's task exists):

```python
def get_owned_task(task_id: int, db, current_user) -> models.Task:
    task = db.get(models.Task, task_id)
    if task is None or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

> **💡 This is authorization sneaking in**
>
> Filtering by
>
> owner_id
>
> is your first taste of
>
> authorization
>
> (the "what can you do?" question). In 7.4 you'll formalize it with roles so an admin can override ownership.

## ✅ Recap

- A **JWT** is `header.payload.signature` — signed (tamper-proof), **not encrypted** (readable), so never put secrets in it.
- Sign with a secret `SECRET_KEY` + an `exp` expiry; `create_access_token` on login, `decode_access_token` to verify.
- `OAuth2PasswordBearer(tokenUrl="auth/login")` reads the `Authorization: Bearer` header and powers the docs Authorize button.
- `get_current_user` decodes the token, loads the user, and is reused by every protected route.
- Scope task routes by `owner_id` so users only see their own data (return `404` for others' tasks).

**Next:** open `assignment.html` and turn login into a real token-based system.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
