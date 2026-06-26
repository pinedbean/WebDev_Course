*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.4 — Authorization, Refresh & Security Hardening

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- **Authorization** with roles & permissions (RBAC), and a reusable `require_role` dependency.
- **Token expiry** and the **refresh token** pattern (short access + long refresh).
- The big web vulnerabilities — **XSS, CSRF, SQL injection** — and how your stack already mitigates them (plus what you must still do).
- **Secrets management**: `.env`, `pydantic-settings`, keeping keys out of Git.
- A practical **hardening checklist** for the Tasks API before the Module Checkpoint.

In the lab you'll add an admin role, a refresh endpoint, move secrets to `.env`, and complete the 🏁 **Module 7 Checkpoint**: a secure full-stack app where users only see their own data.

## 1. Authorization: roles & permissions

Authentication answered "who are you?". **Authorization** answers "what may you do?". The simplest model that scales is **Role-Based Access Control (RBAC)**: every user has a `role` (you added `"user"` / `"admin"` in 7.1), and endpoints check the role before acting.

You already do *ownership* authorization (users only touch their own tasks). Roles add a second axis: an **admin** may do things a normal user can't — like list all users. The clean way to express this in FastAPI is a **dependency factory** that produces a guard for a given role:

```python
# app/deps.py  (additions)
from fastapi import Depends, HTTPException, status

def require_role(*allowed_roles: str):
    """Build a dependency that allows only the given roles."""
    def checker(current_user: models.User = Depends(get_current_user)) -> models.User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    return checker

# Handy alias
get_current_admin = require_role("admin")
```

Now an admin-only route is one line of declaration:

```python
# app/routers/admin.py
from app.deps import get_current_admin

@router.get("/users", response_model=list[schemas.UserOut])
def list_all_users(db: Session = Depends(get_db),
                   admin: models.User = Depends(get_current_admin)):
    return db.query(models.User).all()
```

> **📝 401 vs 403**
>
> 401 Unauthorized
>
> = "I don't know who you are" (no/invalid token).
>
> 403 Forbidden
>
> = "I know who you are, but you're not allowed." A logged-in normal user hitting an admin route gets
>
> 403
>
> , not 401.

## 2. Token expiry & refresh tokens

In 7.2 your access token expires (good — a stolen token dies quickly). But a short expiry means users would get logged out mid-session. The standard fix is **two tokens**:

| Token | Lifetime | Job |
| --- | --- | --- |
| **Access token** | Short (e.g. 15–30 min) | Sent on every API request to prove identity. |
| **Refresh token** | Long (e.g. 7–30 days) | Sent only to `/auth/refresh` to get a fresh access token. |

>

You distinguish the two by a `type` claim in the payload, and give them different expiries:

```python
# app/security.py  (additions)
REFRESH_TOKEN_EXPIRE_DAYS = 7

def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    payload = {
        "sub": subject,
        "type": token_type,                       # "access" or "refresh"
        "exp": datetime.now(timezone.utc) + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_access_token(subject: str) -> str:
    return create_token(subject, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

def create_refresh_token(subject: str) -> str:
    return create_token(subject, "refresh", timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
```

The `/auth/refresh` endpoint verifies the refresh token (and that its `type` is `"refresh"`), then issues a brand-new access token.

> **⚠️ Refresh tokens are powerful — protect them**
>
> A refresh token is a long-lived key to the account. Never accept an
>
> access
>
> token at the refresh endpoint (check the
>
> type
>
> claim). In production, refresh tokens are often stored in an
>
> httpOnly
>
> cookie and can be
>
> revoked
>
> server-side (a denylist) so a logout truly ends the session. Plain stateless JWTs can't be revoked before they expire — a real trade-off to be honest about.

## 3. The big three vulnerabilities

### XSS — Cross-Site Scripting

An attacker injects JavaScript that runs in *other users'* browsers (e.g. a task title containing a `<script>` tag that, when rendered, runs). That script can read your `localStorage` token and impersonate the user.

- **React mitigates this by default**: it escapes any value you put in JSX (`{userInput}` renders as text, not HTML).
- **Your job:** never use `dangerouslySetInnerHTML` with untrusted data; sanitize any HTML you must render; set a Content-Security-Policy header in production.

### CSRF — Cross-Site Request Forgery

A malicious site tricks a logged-in user's browser into making a request to *your* API using their ambient credentials. CSRF specifically targets **cookies**, which browsers send automatically.

- **If you use the `Authorization: Bearer` header** (as we do), you're largely immune — browsers don't auto-attach that header to cross-site requests, so the attacker's page can't add your token.
- **If you switch to cookie-stored tokens**, you must add CSRF defenses (SameSite cookies, CSRF tokens). This is the flip side of the storage trade-off from 7.3.

### SQL Injection

An attacker puts SQL into an input (`'; DROP TABLE users; --`) hoping you concatenate it into a query.

- **SQLAlchemy mitigates this by default**: the ORM uses parameterized queries, so values are never treated as SQL.
- **Your job:** never build queries with f-strings/string concatenation of user input; stick to the ORM or bound parameters.

> **💡 The reassuring pattern**
>
> Modern frameworks make the secure path the default path: React escapes output, SQLAlchemy parameterizes queries, bearer headers sidestep CSRF. Security is mostly about
>
> not opting out
>
> of these defaults — and validating everything on the server.

## 4. Validate on the server — always

Frontend validation (the `required` attribute, min length) is a *UX nicety*, not security — anyone can call your API directly with `curl` or Postman, bypassing the browser entirely. **The server is the only place you can trust.** Good news: Pydantic already enforces your schemas on every request. Lean on it: required fields, types, `EmailStr`, length/range constraints with `Field`.

```
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
```

## 5. Secrets management

Your `SECRET_KEY` (and database URLs, API keys) must never be hard-coded or committed. The standard approach is a `.env` file that stays out of Git, loaded into typed settings.

```
# .env  (NEVER commit this)
SECRET_KEY=3f9a...64-hex-chars...
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./tasks.db
```

Load it with **pydantic-settings** (the Pydantic v2 way) so config is typed and validated at startup:

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    secret_key: str
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite:///./tasks.db"
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()   # reads .env + real env vars
```

And make sure Git ignores it:

```
# .gitignore
.env
*.db
.venv/
```

> **⚠️ If a secret ever lands in Git**
>
> It's compromised — even if you delete it in a later commit, it lives in history.
>
> Rotate it immediately
>
> (generate a new
>
> SECRET_KEY
>
> ; all old tokens become invalid, which is exactly what you want). Commit a
>
> .env.example
>
> with empty placeholders so teammates know what to set, but never the real values.

## 6. Hardening checklist

Before you call an auth system "done," walk this list. You'll apply the relevant items in the lab.

| Area | Do this |
| --- | --- |
| Passwords | bcrypt/argon2 hashing (done), minimum length, never logged or returned. |
| Tokens | Short access expiry, refresh flow, secret from env, `type` claim checked. |
| Errors | Vague auth messages ("Invalid credentials") to prevent account enumeration. |
| CORS | Allowlist specific origins (your frontend), not `"*"`, in production. |
| Validation | Server-side Pydantic on every input; don't trust the client. |
| Transport | HTTPS in production (tokens in plaintext over HTTP can be sniffed) — you'll add this in Module 9. |
| Rate limiting | Throttle `/auth/login` to slow brute-force attempts (a reverse-proxy or middleware concern; Module 9). |
| Secrets | `.env` ignored by Git, rotate if leaked, separate dev/prod keys. |

> **📝 Lock down CORS**
>
> During development
>
> allow_origins=["http://localhost:5173"]
>
> is fine. In production set it to your real frontend domain. A wide-open
>
> allow_origins=["*"]
>
> combined with credentials is a common, dangerous misconfiguration.

## ✅ Recap

- **RBAC**: a `role` per user + a `require_role` dependency; normal user hitting an admin route gets **403**.
- **Refresh tokens** (long-lived) mint fresh **access tokens** (short-lived) so sessions persist without re-login; check the `type` claim and protect refresh tokens.
- React escaping beats **XSS**, bearer headers sidestep **CSRF**, SQLAlchemy parameterization beats **SQL injection** — don't opt out of these defaults.
- Always **validate on the server**; client checks are UX only.
- Keep secrets in `.env` (git-ignored), load via `pydantic-settings`, rotate if leaked. Allowlist CORS.

**Next:** open `assignment.html`, harden the app, and complete the 🏁 Module 7 Checkpoint.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
