*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.2 — Lab: Build the Secured TaskFlow API

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Turn the ERD and API contract into a working, secured backend. Implement the four SQLAlchemy models with a migration, JWT register/login/me, and CRUD for projects, members, and tasks — all guarded by ownership/membership rules. By the end, a user can only touch projects they own or belong to, and data survives a restart.

## Before you start

- You finished 10.1: `capstone-taskflow/backend/` exists with a venv and a `/api/v1/health` route.
- Activate the venv: `cd backend && source venv/bin/activate`.
- Keep your `SPEC.md` API contract open — you're implementing it exactly.

> **⚠️ Build it yourself first**
>
> Lean on your Module 6 (models/migrations) and Module 7 (auth) muscle memory. Open the solution to compare file shapes or when stuck — not before you've attempted each route.

## Tasks

### 1 Install deps & set up the DB layer

Install `sqlalchemy`, `alembic`, `"passlib[bcrypt]"`, `"python-jose[cryptography]"`, `"pydantic[email]"`, and `python-dotenv`. Re-freeze `requirements.txt`. Create `app/database.py` with the engine, `SessionLocal`, `Base`, and a `get_db` dependency (Module 6.2).

### 2 Write the models

In `app/models.py`, define `User`, `Project`, `Membership`, and `Task` exactly per the ERD (fields, types, foreign keys, nullable assignee/due date, relationships, and the delete cascade from project → tasks).

### 3 Create & run a migration

Initialize Alembic, point `env.py` at `Base.metadata` (importing your models), autogenerate the first migration ("create tables"), and run `alembic upgrade head`. Confirm `taskflow.db` now has four tables.

### 4 Pydantic schemas

In `app/schemas.py` define request/response models: `RegisterIn`, `LoginIn`, `UserOut`, `Token`, `ProjectCreate`/`ProjectOut`, `MemberInvite`/`MemberOut`, `TaskCreate`/`TaskUpdate`/`TaskOut`. Validate `status` against the allowed set and use `EmailStr` for emails.

### 5 Auth: security + router

Add `app/security.py` (hash/verify + JWT) and `app/routers/auth.py` with `POST /register`, `POST /login`, and `GET /me`. Registering must reject a duplicate email (409). Store `SECRET_KEY` in `.env` (loaded via `python-dotenv`).

### 6 Dependencies for access control

In `app/deps.py` add `get_current_user`, plus `get_project_for_member` and `get_project_for_owner` that 404 on missing projects and 403 when the caller isn't a member/owner.

### 7 Projects + members routers

In `routers/projects.py`: list (only mine), create (also create an owner Membership), get, patch (owner), delete (owner). In `routers/members.py`: list members, and invite by email (owner only; 404 if the email isn't a registered user; avoid duplicate memberships).

### 8 Tasks router with filtering

In `routers/tasks.py`: list tasks for a project (members only) with optional `?status=` and `?assignee_id=` filters; create; patch (move status / edit / assign); delete. Mount all routers under `/api/v1` in `main.py`.

### 9 Test the whole flow in `/docs`

Using Swagger UI: register two users, log in, create a project as user A, invite user B, create tasks, filter them, and confirm user B can see them but a stranger (user C) gets a 403/404. Restart the server and confirm data persists.

## ✅ Deliverable — acceptance checklist

- Four tables created via an Alembic migration; `taskflow.db` persists data across restarts.
- `POST /auth/register` + `/login` return a JWT; duplicate email returns 409; `/auth/me` returns the current user.
- Creating a project also creates an owner `Membership` row.
- `GET /projects` returns only projects the caller owns or is a member of.
- Owner-only actions (update/delete project, invite member) return 403 for non-owners.
- Inviting a non-existent email returns 404; inviting an existing user adds a member.
- Tasks CRUD works and is restricted to members; `?status=` and `?assignee_id=` filters work.
- A stranger cannot read another team's project or tasks (403/404).

## 🚀 Stretch goals (optional)

- Add `pytest` tests with FastAPI's `TestClient` covering register/login and one access-denied case.
- Seed script: create a demo user + project + a few tasks so the frontend has data in 10.3.
- Add pagination to `GET /projects/{id}/tasks` (`?limit=&offset=`), per Module 5.6.
- Return `UserOut` (id + name) for a task's assignee so the board can show names without a second request.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
