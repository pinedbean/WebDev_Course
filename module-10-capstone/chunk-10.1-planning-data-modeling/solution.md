*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll create the monorepo, write a complete `SPEC.md`, and scaffold a runnable FastAPI backend and React frontend. Target layout:

```text
capstone-taskflow/
├── .gitignore
├── README.md
├── SPEC.md
├── backend/
│   ├── venv/                 (not committed)
│   ├── requirements.txt
│   ├── .env.example
│   └── app/
│       └── main.py           (GET /api/v1/health)
└── frontend/                 (Vite React app)
    ├── .env                  (VITE_API_URL=...)
    └── src/ ...
```

### 1 Create the monorepo & Git

```bash
# macOS / zsh
cd ~/Desktop/webdev-course
mkdir -p capstone-taskflow/backend capstone-taskflow/frontend
cd capstone-taskflow
git init
```

Create `.gitignore` at the repo root:

```
# .gitignore
# Python
venv/
__pycache__/
*.pyc
*.db
.env

# Node / Vite
node_modules/
dist/
.DS_Store
```

> **⚠️ Keep secrets out of Git**
>
> .env
>
> is in
>
> .gitignore
>
> on purpose. We commit a
>
> .env.example
>
> (no real secrets) so teammates know which variables exist. This habit pays off in the Bonus Track.

### 2 Write `SPEC.md`

Create `SPEC.md` at the repo root. Here's a complete reference version — adjust the wording, but keep all the sections.

```
# TaskFlow — Specification

TaskFlow is a team task & project tracker. A user registers, creates
projects, invites teammates, and manages tasks on a board (To Do /
In Progress / Done) with assignees and due dates.

## MVP Scope

| In scope                                   | Out of scope (v2)             |
|--------------------------------------------|-------------------------------|
| Register / login / logout (JWT)            | Password reset, OAuth         |
| Create & list projects (owned + member)    | Archiving, templates          |
| Invite a member by email                   | Notifications, comments       |
| Create / edit / delete tasks               | Subtasks, attachments, labels |
| Task status, assignee, due date            | Drag-and-drop reordering      |
| Filter board by status / assignee          | Full-text search              |

## User Stories

1. As a visitor, I want to register with email + password, so that I have an account.
   - Unique email -> account created and I'm logged in.
   - Duplicate email -> clear "email already registered" error.
2. As a user, I want to log in, so that I can access my projects.
   - Correct credentials -> receive a JWT and land on /projects.
3. As a user, I want to create a project, so that I can organize work.
   - New project appears immediately; I am its "owner".
4. As an owner, I want to invite a teammate by email, so that we collaborate.
   - Existing user becomes a "member"; unknown email -> 404.
5. As a member, I want to create tasks with status/assignee/due date.
   - Task appears in the correct column and persists across reloads.
6. As a member, I want to move a task between columns, so the board is accurate.
   - Status change persists (PATCH) and survives a reload.
7. As a member, I want to filter the board by status and assignee.

## Data Model (Entities)

User(id, email UNIQUE, hashed_password, name, role[user|admin], created_at)
Project(id, name, description, owner_id -> User, created_at)
Membership(id, project_id -> Project, user_id -> User, role[owner|member])
Task(id, project_id -> Project, title, description,
     status[todo|in_progress|done], assignee_id -> User NULLABLE,
     due_date NULLABLE, created_at)

Relationships:
- User 1 --- * Project          (Project.owner_id)
- Project 1 --- * Task           (Task.project_id)
- User 1 --- * Task (assignee)   (Task.assignee_id, nullable)
- User * --- * Project           (via Membership join table)

## API Contract (prefix /api/v1)

| Method | Path                              | Purpose                  | Auth        |
|--------|-----------------------------------|--------------------------|-------------|
| POST   | /auth/register                    | Create account + token   | no          |
| POST   | /auth/login                       | Log in + token           | no          |
| GET    | /auth/me                          | Current user             | yes         |
| GET    | /projects                         | List my projects         | yes         |
| POST   | /projects                         | Create project           | yes         |
| GET    | /projects/{id}                    | Get one project          | member      |
| PATCH  | /projects/{id}                    | Update project           | owner       |
| DELETE | /projects/{id}                    | Delete project           | owner       |
| GET    | /projects/{id}/members            | List members             | member      |
| POST   | /projects/{id}/members            | Invite member by email   | owner       |
| GET    | /projects/{id}/tasks              | List tasks (+filters)    | member      |
| POST   | /projects/{id}/tasks              | Create task              | member      |
| PATCH  | /projects/{id}/tasks/{taskId}     | Edit / move / assign     | member      |
| DELETE | /projects/{id}/tasks/{taskId}     | Delete task              | member      |
| GET    | /health                           | Liveness check           | no          |

### Sample payloads

POST /auth/register
  req:  { "email": "ana@x.com", "password": "secret123", "name": "Ana" }
  201:  { "access_token": "eyJ...", "token_type": "bearer" }

POST /projects/{id}/tasks
  req:  { "title": "Hero copy", "description": "", "status": "todo",
          "assignee_id": 4, "due_date": "2026-07-10" }
  201:  { "id": 17, "project_id": 3, "title": "Hero copy", "status": "todo",
          "assignee_id": 4, "due_date": "2026-07-10",
          "created_at": "2026-06-26T09:14:00Z" }

### Status codes
200 OK · 201 Created · 204 No Content · 401 Unauthorized ·
403 Forbidden · 404 Not Found · 422 Unprocessable Entity
```

> **💡 Mermaid bonus**
>
> Add a fenced
>
> ```mermaid
>
> block with an
>
> erDiagram
>
> and GitHub renders the ERD automatically. The text ERD above is fine for grading.

### 3 Scaffold the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install fastapi "uvicorn[standard]"
pip freeze > requirements.txt
mkdir -p app
touch app/__init__.py
```

Create `backend/app/main.py`:

```python
# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="TaskFlow API", version="0.1.0")

# Allow the Vite dev server to call us during development (Module 5.5).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
```

Run it:

```bash
uvicorn app.main:app --reload
```

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

Visit `http://localhost:8000/api/v1/health` → you should see `{"status":"ok"}`, and `http://localhost:8000/docs` shows the interactive Swagger UI.

Also add `backend/.env.example` so future chunks know which variables exist:

```
# backend/.env.example
SECRET_KEY=change-me-to-a-64-char-hex-string
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./taskflow.db
```

### 4 Scaffold the frontend

From the repo root, create the Vite app *into* the existing `frontend/` folder, then install Router:

```bash
cd ~/Desktop/webdev-course/capstone-taskflow
npm create vite@latest frontend -- --template react
cd frontend
npm install
npm install react-router-dom
npm run dev
```

```
  VITE v5.x  ready in 312 ms
  ➜  Local:   http://localhost:5173/
```

Open that URL — the default Vite + React page renders. Now add `frontend/.env` (Vite reads `VITE_`-prefixed vars, per Module 4.7):

```
# frontend/.env
VITE_API_URL=http://localhost:8000/api/v1
```

> **📝 Two terminals**
>
> Keep
>
> uvicorn
>
> running in one terminal and
>
> npm run dev
>
> in another. You'll work with both servers up for the rest of the module.

### 5 README & first commit

Create `README.md` at the repo root:

```python
# TaskFlow

A team task & project tracker (capstone for the Full-Stack Web Dev course).
Stack: React + Vite frontend, FastAPI + SQLite backend, JWT auth.

## Run locally
### Backend
    cd backend
    python3 -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload     # http://localhost:8000

### Frontend
    cd frontend
    npm install
    npm run dev                        # http://localhost:5173

See SPEC.md for scope, data model, and the API contract.
```

```bash
cd ~/Desktop/webdev-course/capstone-taskflow
git add .
git commit -m "chore: scaffold TaskFlow monorepo + spec"
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `uvicorn: command not found` | Your venv isn't active. Re-run `source venv/bin/activate` (prompt shows `(venv)`). |
| `npm create vite` refuses — folder not empty | The `frontend/` folder must be empty. Remove stray files, or scaffold into a temp name and move the contents in. |
| Health route 404 | You ran `uvicorn` from the wrong directory. Run it from `backend/` so `app.main:app` resolves. |
| Frontend can't reach API later | That's CORS — handled by the middleware in `main.py`. Confirm the origin matches your Vite port (5173). |
| `node_modules` got committed | It's huge. Confirm `node_modules/` is in `.gitignore`, then `git rm -r --cached node_modules`. |

## 🎉 Done — what's next

You've turned an idea into a plan and stood up both halves of TaskFlow. You now have a spec you can defend, an ERD that maps to real tables, an API contract both sides agree on, and two running servers.

- ✅ `SPEC.md` with scope, stories, ERD, API contract.
- ✅ Backend answering `/api/v1/health`; `/docs` live.
- ✅ Frontend dev server running with `VITE_API_URL` set.

**Up next → Chunk 10.2: Backend — Models, Auth & Core API.** You'll turn the ERD into SQLAlchemy models with a migration, add JWT register/login, and build Projects/Tasks CRUD with ownership rules.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
