*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll add roles, refresh tokens, env-based secrets, and run the 🏁 Module 7 Checkpoint. New/changed files:

```text
tasks-api/
├── .env                       (new: secrets, git-ignored)
├── .env.example               (new: placeholders, committed)
├── .gitignore                 (ignore .env, *.db, .venv)
└── app/
    ├── config.py              (new: pydantic-settings)
    ├── security.py            (refresh + type claim, settings)
    ├── schemas.py             (Token gains refresh_token)
    ├── deps.py                (require_role / get_current_admin)
    ├── main.py                (CORS allowlist, admin router)
    └── routers/
        ├── auth.py            (return refresh, /auth/refresh)
        └── admin.py           (new: GET /admin/users)
```

## Part A — Authorization (roles)

### 1 `require_role` in `deps.py`

```python
# app/deps.py  (add to the existing file)
def require_role(*allowed_roles: str):
    def checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    return checker

get_current_admin = require_role("admin")
```

### 2 The admin router

```python
# app/routers/admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_admin
from app import models, schemas

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[schemas.UserOut])
def list_all_users(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_current_admin),
):
    return db.query(models.User).all()
```

```python
# app/main.py  (add)
from app.routers import auth, tasks, admin
app.include_router(admin.router)
```

### 3 Promote an admin

```sql
sqlite3 tasks.db "UPDATE users SET role='admin' WHERE email='admin@x.com';"
sqlite3 tasks.db "SELECT email, role FROM users;"
# admin@x.com|admin
```

## Part B — Refresh tokens

### 4 Token helpers with a `type` claim

```python
# app/security.py  (token section, using settings from Part C)
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings

ALGORITHM = "HS256"

def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    payload = {
        "sub": subject,
        "type": token_type,
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)

def create_access_token(subject: str) -> str:
    return create_token(subject, "access",
                        timedelta(minutes=settings.access_token_expire_minutes))

def create_refresh_token(subject: str) -> str:
    return create_token(subject, "refresh",
                        timedelta(days=settings.refresh_token_expire_days))

def decode_token(token: str, expected_type: str) -> str | None:
    """Return the subject if valid AND of the expected type, else None."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
    except JWTError:
        return None
    if payload.get("type") != expected_type:
        return None
    return payload.get("sub")
```

> **📝 Update get_current_user**
>
> Point your existing dependency at the new decoder:
>
> user_id = decode_token(token, "access")
>
> . Now an access token is required for protected routes, and a refresh token won't be accepted there.

### 5 Return both tokens + a refresh endpoint

```
# app/schemas.py
class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str
```

```python
# app/routers/auth.py  (updated login + new refresh)
from app.security import (hash_password, verify_password,
                          create_access_token, create_refresh_token, decode_token)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == form_data.username.lower()).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": create_refresh_token(str(user.id)),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=schemas.Token)
def refresh(data: schemas.RefreshRequest, db: Session = Depends(get_db)):
    user_id = decode_token(data.refresh_token, expected_type="refresh")
    if user_id is None or db.get(models.User, int(user_id)) is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return {"access_token": create_access_token(user_id), "token_type": "bearer"}
```

## Part C — Secrets & hardening

### 6 Env-based settings

```bash
pip install pydantic-settings
pip freeze > requirements.txt
```

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str = "sqlite:///./tasks.db"
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

```
# .env   (NEVER commit)
SECRET_KEY=3f9a...paste-64-hex-chars...
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_ORIGIN=http://localhost:5173
```

```
# .env.example   (commit this — placeholders only)
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
FRONTEND_ORIGIN=http://localhost:5173
```

```
# .gitignore
.env
*.db
.venv/
__pycache__/
```

> **⚠️ Generate a real key**
>
> python -c "import secrets; print(secrets.token_hex(32))"
>
> and paste it into
>
> .env
>
> . Settings validation will fail at startup if
>
> SECRET_KEY
>
> is missing — that's a feature: no silent insecure default.

### 7 CORS allowlist

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],   # exact origin, not "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Password length is already enforced server-side via `UserCreate.password = Field(min_length=8)`, and login still returns the vague `"Invalid credentials"` — both confirmed from earlier chunks.

## Part D — Frontend auto-refresh (optional)

### 8 Store refresh token & retry on 401

```javascript
// src/api.js  (enhanced apiFetch)
export async function apiFetch(path, options = {}, _retry = true) {
  const headers = { ...(options.headers || {}) };
  const token = localStorage.getItem("token");
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, { ...options, headers });

  if (res.status === 401 && _retry) {
    const refreshed = await tryRefresh();           // attempt once
    if (refreshed) return apiFetch(path, options, false);  // retry original
    localStorage.removeItem("token");
    localStorage.removeItem("refresh");
    throw new Error("Unauthorized");
  }
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Request failed");
  }
  return res.status === 204 ? null : res.json();
}

async function tryRefresh() {
  const refresh_token = localStorage.getItem("refresh");
  if (!refresh_token) return false;
  const res = await fetch(`${BASE}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token }),
  });
  if (!res.ok) return false;
  const { access_token } = await res.json();
  localStorage.setItem("token", access_token);
  return true;
}
```

In `AuthContext.login`, also save the refresh token: `localStorage.setItem("refresh", refresh_token)`, and clear it in `logout`.

## 🏁 Module 7 Checkpoint — verification walkthrough

Run the backend (in the shell where `.env` is read) and the React app, then confirm each:

```sql
# 1. Auth required
curl -i http://localhost:8000/tasks
# -> HTTP/1.1 401 Unauthorized

# 2. Data isolation  (log in as B, try A's task)
curl -s -X POST localhost:8000/auth/login -d "username=b@x.com&password=secret12345" \
  -H "Content-Type: application/x-www-form-urlencoded"   # grab B's access_token
curl -i localhost:8000/tasks/1 -H "Authorization: Bearer <B_TOKEN>"
# -> 404 {"detail":"Task not found"}   (task 1 belongs to A)

# 3. Passwords safe
sqlite3 tasks.db "SELECT email, hashed_password FROM users;"
# -> every value starts with $2b$ ...

# 4. Roles
curl -i localhost:8000/admin/users -H "Authorization: Bearer <NORMAL_USER_TOKEN>"
# -> 403 {"detail":"Not enough permissions"}
curl -s localhost:8000/admin/users -H "Authorization: Bearer <ADMIN_TOKEN>"
# -> [ {...}, {...} ]   full user list

# 5. Refresh
curl -s -X POST localhost:8000/auth/refresh \
  -H "Content-Type: application/json" -d '{"refresh_token":"<REFRESH>"}'
# -> { "access_token": "eyJ...", "token_type": "bearer" }

# 6. Secrets
git status   # .env and tasks.db should NOT appear (they're ignored)
grep -r "SECRET_KEY" app/   # only reads settings.secret_key — no literal key
```

In the browser: logged out → dashboard redirects to `/login`; log in as A and B in turn → each sees only their own tasks; refresh the page → still logged in; log out → blocked again. When all six pass, your **secure full-stack app where users only see their own data** is complete.

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| App won't start: `field required: secret_key` | Good — settings is doing its job. Create `.env` with `SECRET_KEY=...` in the project root and run uvicorn from there. |
| Admin route returns `403` for your admin | The DB role wasn't updated, or you're using an *old* token minted before promotion. Log in again to get a fresh token. |
| `/auth/refresh` accepts an access token | You skipped the `type` check. Use `decode_token(token, "refresh")` and return `None` when the type doesn't match. |
| CORS breaks after the allowlist change | `allow_origins` must match the browser origin exactly, including scheme and port (no trailing slash). |
| Old tokens all invalid after editing `.env` | Expected — changing `SECRET_KEY` invalidates every existing token. Log in again. |

## 📄 Complete `app/config.py`

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str = "sqlite:///./tasks.db"
    frontend_origin: str = "http://localhost:5173"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
```

## 🎉 Module 7 complete

You built a real authentication & authorization system on the Tasks API and proved its security properties end to end:

- **7.1** — bcrypt password hashing; secure register/login.
- **7.2** — JWT issuing, `get_current_user`, owner-scoped routes.
- **7.3** — React login experience: token storage, auth context, protected routes, logout.
- **7.4** — roles & admin access, refresh tokens, env-based secrets, hardened CORS — and the 🏁 Checkpoint.

Your app now knows *who* every request is and enforces *what* they may do. The natural next question in production is: when something goes wrong (a failed login, a 500, a slow request), **how would you even know?** That's observability.

**Up next → Module 8: Logging & Observability** — structured logs, request IDs, and error tracking so you can see what your app is doing in production.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
