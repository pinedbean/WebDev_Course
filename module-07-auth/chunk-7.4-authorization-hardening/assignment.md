*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.4 — Lab: Roles, Refresh & Hardening + 🏁 Checkpoint

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Lock the Tasks API down properly. You'll add a **role-based admin endpoint**, a **refresh-token** flow, move the `SECRET_KEY` into a git-ignored `.env` loaded by `pydantic-settings`, and tighten CORS. Then you'll complete the 🏁 **Module 7 Checkpoint**: prove that, end to end, users only ever see their own data and an admin can see everyone's.

## Before you start

- Chunks 7.1–7.3 complete: hashing, JWT login + `get_current_user`, owner-scoped tasks, and the React auth frontend.
- Backend venv active; React app from 7.3 available.
- The `User` model already has a `role` column (default `"user"`).

> **⚠️ Try it yourself first**
>
> Work from the lecture. Only open
>
> solution.html
>
> when stuck or to compare.

## Part A — Authorization (roles)

### 1 Add a `require_role` dependency

In `deps.py` write a `require_role(*roles)` dependency factory that returns the current user if their role is allowed, else raises `403`. Add a `get_current_admin = require_role("admin")` alias.

### 2 Add an admin-only endpoint

Create `app/routers/admin.py` with `GET /admin/users` that returns all users (`list[UserOut]`), guarded by `get_current_admin`. Include the router in `main.py`.

### 3 Make an admin user

Register a user, then promote them in the DB (no self-service admin signup!):

```sql
sqlite3 tasks.db "UPDATE users SET role='admin' WHERE email='admin@x.com';"
```

## Part B — Refresh tokens & expiry

### 4 Issue access + refresh on login

Add `create_refresh_token` (longer expiry, `type="refresh"`) and a `type="access"` claim to access tokens. Return both from `/auth/login` (extend the `Token` schema with `refresh_token`).

### 5 Add `POST /auth/refresh`

Accept a refresh token, verify it *and* confirm its `type` is `"refresh"` (reject access tokens here), then return a fresh access token. Reject expired/invalid tokens with `401`.

## Part C — Secrets & hardening

### 6 Move secrets to `.env`

Install `pydantic-settings`, create `app/config.py` with a `Settings` class reading `SECRET_KEY` + token expiries from `.env`, and use `settings.secret_key` in `security.py`. Add `.env`, `*.db`, and `.venv/` to `.gitignore`, and commit a `.env.example` with empty placeholders.

### 7 Tighten CORS & validation

Set `CORSMiddleware` `allow_origins` to your exact frontend origin (`http://localhost:5173`), not `"*"`. Confirm `UserCreate.password` has a server-side `min_length`. Confirm auth errors stay vague ("Invalid credentials").

## Part D — Frontend touch-ups (optional but recommended)

### 8 Store the refresh token & auto-refresh

Save the refresh token at login, and in `apiFetch`, when a call returns `401`, try `POST /auth/refresh` once; if it succeeds, save the new access token and retry the original request before giving up and logging out.

## 🏁 Module 7 Checkpoint — Secure full-stack app

Tie the whole module together and **prove** the security properties. Run the backend and the React app, then verify each statement below by actually doing it:

1. **Auth required:** Logged out, the dashboard redirects to `/login`; `GET /tasks` with no token returns `401`.
2. **Data isolation:** Register users A and B. A creates tasks; logged in as B the dashboard shows none of A's tasks, and `GET /tasks/{A-task-id}` returns `404`.
3. **Passwords safe:** `sqlite3 tasks.db "SELECT email, hashed_password FROM users;"` shows only bcrypt hashes (`$2b$…`).
4. **Roles:** A normal user calling `GET /admin/users` gets `403`; the admin gets the full list.
5. **Refresh:** An expired access token is rejected (`401`), and `/auth/refresh` issues a working new one without re-login.
6. **Secrets:** `git status` shows `.env` and `*.db` are *ignored*; the `SECRET_KEY` is nowhere in source.

When all six hold, the module deliverable — a secure full-stack app where users only see their own data — is complete.

## ✅ Deliverable — acceptance checklist

- `require_role` / `get_current_admin` dependency; `GET /admin/users` returns `403` for normal users, data for admins.
- Login returns access + refresh tokens; `POST /auth/refresh` issues a new access token and rejects non-refresh tokens.
- `SECRET_KEY` and expiries load from a git-ignored `.env` via `pydantic-settings`; `.env.example` committed.
- CORS allowlists the real frontend origin; password length validated server-side; auth errors stay vague.
- All six 🏁 Checkpoint statements verified by hand.

## 🚀 Stretch goals (optional)

- Add an admin-only `DELETE /admin/users/{id}` and an endpoint to change a user's role.
- Implement token **revocation**: keep a denylist of refresh-token IDs (`jti` claim) so logout truly ends a session.
- Add basic **login rate limiting** (e.g. `slowapi`) to slow brute-force attempts.
- Move the refresh token into an `httpOnly` cookie and add the matching backend handling — then note what CSRF protection you'd now need.
- Hide admin-only UI in React based on `user.role` (defense in depth — the server still enforces it).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
