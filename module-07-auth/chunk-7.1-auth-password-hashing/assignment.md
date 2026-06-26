*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.1 — Lab: Secure Register & Login Endpoints

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Add a password layer to the **Tasks API**. You'll extend the `User` model with a `hashed_password` and a `role`, create a reusable `security.py` with bcrypt hashing, and build two endpoints: `POST /auth/register` (hashes the password) and `POST /auth/login` (verifies it). No JWTs yet — that's 7.2. The goal here is that **plaintext passwords never touch your database**.

## Before you start

- Your **Tasks API** from Module 6 should run: FastAPI + SQLAlchemy 2.x + SQLite (`tasks.db`), with a `get_db()` dependency and Alembic configured.
- You already have a `Task` model and a minimal `User` model (`id`, `email` unique, `created_at`) with User → Tasks.
- Activate your virtual environment (macOS/zsh): `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
- The server runs with `uvicorn app.main:app --reload` and docs live at `http://localhost:8000/docs`.

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when you're stuck or to compare at the end.

## Tasks

### 1 Install passlib + bcrypt

With your venv active, install the password library and pin it to your requirements.

```bash
pip install "passlib[bcrypt]"
pip freeze > requirements.txt
```

### 2 Extend the User model

In your SQLAlchemy `User` model add two columns:

- `hashed_password` — a non-nullable string.
- `role` — a string with a default of `"user"` (you'll use `"admin"` in 7.4).

Keep the existing `id`, `email` (unique), `created_at`, and the relationship to tasks.

### 3 Create an Alembic migration

Your DB schema changed, so generate and apply a migration so `tasks.db` gets the new columns.

```bash
alembic revision --autogenerate -m "add hashed_password and role to users"
alembic upgrade head
```

> **💡 Existing rows**
>
> If you already have users without a password, it's simplest to delete the dev DB rows (or the file) and start fresh, since
>
> hashed_password
>
> is required.

### 4 Build `app/security.py`

Create a single module that owns password hashing. It should export a `pwd_context` (a `CryptContext` using bcrypt) plus `hash_password(plain)` and `verify_password(plain, hashed)` helpers.

### 5 Add Pydantic schemas

In your schemas module add:

- `UserCreate` — incoming: `email` (use `EmailStr`) + `password`.
- `UserLogin` — incoming: `email` + `password`.
- `UserOut` — outgoing: `id`, `email`, `role`, `created_at`. **Never** include the password or the hash. Set `model_config = ConfigDict(from_attributes=True)` (Pydantic v2).

### 6 Build the auth router — `POST /auth/register`

Create `app/routers/auth.py` with an `APIRouter(prefix="/auth", tags=["auth"])`. The register endpoint should:

- Reject a duplicate email with `400`.
- Hash the incoming password with `hash_password` and store the user.
- Return `UserOut` with status `201`.

Remember to include the router in `app/main.py` with `app.include_router(auth.router)`.

### 7 Add `POST /auth/login`

Look up the user by email and call `verify_password`. If the user is missing *or* the password is wrong, raise `401` with the **same** vague message (`"Invalid credentials"`). On success, return `{"message": "Login successful"}` for now — you'll swap this for a JWT in 7.2.

### 8 Test in the docs

Run the server and open `/docs`. Register a user, then check the DB to confirm the stored value is a bcrypt hash, not plaintext:

```sql
sqlite3 tasks.db "SELECT email, hashed_password, role FROM users;"
```

Then hit `/auth/login` with the right password (expect success) and a wrong one (expect `401`).

## ✅ Deliverable — acceptance checklist

- `passlib[bcrypt]` is installed and in `requirements.txt`.
- The `User` model has `hashed_password` and `role` (default `"user"`), applied via an Alembic migration.
- `app/security.py` exposes `pwd_context`, `hash_password`, and `verify_password`.
- `POST /auth/register` hashes the password, rejects duplicate emails (400), and returns `UserOut` (201) with no password field.
- `POST /auth/login` returns success for correct credentials and `401 "Invalid credentials"` for a wrong password *or* unknown email.
- Inspecting `tasks.db` shows a bcrypt hash (starts with `$2b$`) — never plaintext.

## 🚀 Stretch goals (optional)

- Add a minimum password length to `UserCreate` with Pydantic: `password: str = Field(min_length=8)`.
- Normalize emails to lowercase before storing and comparing, so `Jane@x.com` and `jane@x.com` are the same account.
- Print two hashes of the *same* password in a Python shell and confirm they differ (the salt at work).
- Read the bcrypt cost factor in your stored hash (the number after `$2b$`) and try bumping it via the `CryptContext` (e.g. `bcrypt__rounds=13`); notice login gets slower.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
