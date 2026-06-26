*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.1 — Capstone Planning & Data Modeling

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How professionals turn a fuzzy idea into a **buildable plan**: MVP scope, user stories, and acceptance criteria.
- How to design an **entity-relationship model** (ERD) for TaskFlow's four tables and draw the relationships.
- How to write an **API contract** — the exact endpoints, request bodies, responses, and status codes — *before* writing code.
- How to wireframe the screens so the frontend and backend agree on what data each page needs.
- How to scaffold the two repos (`backend/` + `frontend/`) you'll grow over the next five chunks.

This is the start of the capstone. By the end of the lab you'll have a written spec, an ERD, an API contract, and two running "hello world" projects.

## 1. Meet TaskFlow — and why we plan first

**TaskFlow** is a team task & project tracker. A user signs up, creates *projects*, invites teammates, and tracks *tasks* on a board with columns: *To Do → In Progress → Done*. Think a stripped-down Trello/Jira you could actually put on a résumé.

You already know every ingredient — this module just assembles them. Here's the map of what you reuse:

| From module | Skill you'll reuse in TaskFlow |
| --- | --- |
| 1–2 (HTML/CSS) | Semantic markup & responsive layout for the board and forms. |
| 3 (JavaScript) | `fetch`, `async/await`, array methods to shape API data. |
| 4 (React + Vite) | Components, hooks, React Router, Context, a `useFetch`-style data layer. |
| 5 (FastAPI) | Routers, Pydantic schemas, dependency injection, error handling. |
| 6 (SQLite + SQLAlchemy) | Models, relationships, sessions, Alembic migrations. |
| 7 (Auth) | Password hashing, JWT, `get_current_user`, protected routes, roles. |
| 8 (Logging) | Structured logs, request IDs, `/health`. |
| 9 (Production) | Docker, Nginx load balancing, CI/CD. |

> **📝 Why plan at all?**
>
> Writing code is cheap to
>
> start
>
> and expensive to
>
> redo
>
> . A half-page of planning (scope + data model + API contract) prevents the classic capstone trap: building the frontend and backend in two different shapes that don't fit together. Plan once, build calmly.

## 2. Define the MVP scope

An **MVP** (Minimum Viable Product) is the smallest version that delivers the core value. The skill is saying *no* to good ideas so you can ship the essential ones. Draw a hard line:

| ✅ In scope (build it) | 🚫 Out of scope (write it down, skip it) |
| --- | --- |
| Register / login / logout (JWT) | Password reset emails, OAuth/Google login |
| Create & list projects you own or belong to | Project archiving, project templates |
| Invite a member to a project by email | Notifications, activity feeds, comments |
| Create / edit / delete tasks | Subtasks, attachments, labels/tags |
| Task status (todo / in_progress / done), assignee, due date | Drag-and-drop reordering, Gantt charts |
| Filter the board (by status / assignee) | Full-text search, saved filters |

> **💡 The "out" list is a feature, not a failure**
>
> Recording what you deliberately left out shows judgment. In an interview, "I scoped these out to ship a working MVP, and here's how I'd add them" is a strong answer.

## 3. User stories & acceptance criteria

A **user story** captures a requirement from the user's point of view in one sentence: *"As a <role>, I want <goal>, so that <benefit>."* It keeps you focused on value, not on technology. Each story gets **acceptance criteria** — the checklist that proves it's done.

```
As a visitor, I want to register with email + password,
  so that I can have my own account.
  ✓ Given a unique email, when I submit, then an account is created and I'm logged in.
  ✓ Given an email already in use, then I see a clear "email taken" error.

As a user, I want to create a project,
  so that I can organize my team's work.
  ✓ The new project appears in my project list immediately.
  ✓ I am set as the project "owner".

As a project owner, I want to invite a teammate by email,
  so that we can collaborate.
  ✓ An existing user is added as a "member".
  ✓ Members can see the project's tasks but cannot delete the project.

As a member, I want to move a task between To Do / In Progress / Done,
  so that the board reflects reality.
  ✓ Changing status persists and survives a page reload.
```

Notice each story maps cleanly to an API endpoint and a screen. That's the point — stories become your build checklist.

## 4. Entity-Relationship (ER) modeling

Now the heart of planning: the **data model**. An entity becomes a database table; relationships become foreign keys. TaskFlow has four entities. Read each as "a row in this table is one ___":

### The four entities

| Entity | Fields |
| --- | --- |
| **User** | `id`, `email` (unique), `hashed_password`, `name`, `role` ("user"/"admin"), `created_at` |
| **Project** | `id`, `name`, `description`, `owner_id` → User, `created_at` |
| **Membership** | `id`, `project_id` → Project, `user_id` → User, `role` ("owner"/"member") |
| **Task** | `id`, `project_id` → Project, `title`, `description`, `status` ("todo"/"in_progress"/"done"), `assignee_id` → User (nullable), `due_date` (nullable), `created_at` |

### The relationships

- A **User** owns many **Projects** (one-to-many via `Project.owner_id`).
- A **Project** has many **Tasks** (one-to-many via `Task.project_id`).
- A **Task** may be assigned to one **User** (many-to-one via `Task.assignee_id`, nullable = unassigned).
- **Users ↔ Projects** is *many-to-many* (a user can be in many projects; a project has many users). We model that with the **Membership** join table — the same many-to-many pattern from Module 6.

### The ERD (text form)

You don't need fancy tools — a crisp text/ASCII diagram is perfectly professional. Each box is a table; arrows point from the foreign key to what it references.

```text
┌────────────────────┐          ┌────────────────────┐
│        User        │          │      Project       │
├────────────────────┤          ├────────────────────┤
│ id            (PK) │◄──────┐  │ id            (PK)  │
│ email   (unique)   │       └──┤ owner_id      (FK)  │
│ hashed_password    │          │ name               │
│ name               │          │ description        │
│ role               │          │ created_at         │
│ created_at         │          └─────────┬──────────┘
└─────────┬──────────┘                    │ 1
          │ 1                              │
          │            ┌──────────────────┴───────┐
          │            │        Membership         │   (join: User ↔ Project)
          │            ├───────────────────────────┤
          └───────────►│ user_id        (FK)       │◄──┐
                       │ project_id     (FK)       │   │
                       │ role  (owner|member)      │   │
                       └───────────────────────────┘   │
          ┌────────────────────┐                       │
          │        Task        │                       │
          ├────────────────────┤                       │
          │ id            (PK)  │      * many           │
          │ project_id    (FK) ─┼──► Project.id         │
          │ assignee_id   (FK) ─┼──► User.id (nullable) ┘
          │ title / description │
          │ status              │
          │ due_date (nullable) │
          │ created_at          │
          └─────────────────────┘
```

> **📝 Why a Membership table (not a column)?**
>
> You can't store "many users" in a single column. The join table is the standard relational way to model many-to-many, and it gives us a natural home for a per-project
>
> role
>
> (owner vs. member). The project's
>
> owner_id
>
> is a convenient shortcut; the owner also gets a Membership row with
>
> role="owner"
>
> so all access checks can go through one place.

## 5. Designing the API contract

The **API contract** is the agreement between frontend and backend: every URL, method, what you send, what you get back, and the status code. Designing it now means both halves can be built in parallel and they'll fit. We follow REST conventions from Module 5 and version the API under `/api/v1`.

### Endpoint summary

| Method & path | Purpose | Auth? |
| --- | --- | --- |
| `POST /api/v1/auth/register` | Create account, return token | No |
| `POST /api/v1/auth/login` | Log in, return token | No |
| `GET /api/v1/auth/me` | Current user profile | Yes |
| `GET /api/v1/projects` | List projects I own or belong to | Yes |
| `POST /api/v1/projects` | Create a project (I become owner) | Yes |
| `GET /api/v1/projects/{id}` | Get one project | Yes (member) |
| `PATCH /api/v1/projects/{id}` | Update project | Yes (owner) |
| `DELETE /api/v1/projects/{id}` | Delete project | Yes (owner) |
| `GET /api/v1/projects/{id}/members` | List members | Yes (member) |
| `POST /api/v1/projects/{id}/members` | Invite a member by email | Yes (owner) |
| `GET /api/v1/projects/{id}/tasks` | List tasks (with filters) | Yes (member) |
| `POST /api/v1/projects/{id}/tasks` | Create a task | Yes (member) |
| `PATCH /api/v1/projects/{id}/tasks/{taskId}` | Edit / move / assign a task | Yes (member) |
| `DELETE /api/v1/projects/{id}/tasks/{taskId}` | Delete a task | Yes (member) |
| `GET /api/v1/health` | Liveness check (no auth) | No |

### Worked example — the shape of one request/response

Pin down exact JSON. Here's `POST /api/v1/projects/{id}/tasks`:

```
// Request body (what the frontend sends)
{
  "title": "Design the board UI",
  "description": "Three columns, drag later",
  "status": "todo",
  "assignee_id": 4,        // or null = unassigned
  "due_date": "2026-07-10" // ISO date, or null
}

// 201 Created response (what the backend returns)
{
  "id": 17,
  "project_id": 3,
  "title": "Design the board UI",
  "description": "Three columns, drag later",
  "status": "todo",
  "assignee_id": 4,
  "due_date": "2026-07-10",
  "created_at": "2026-06-26T09:14:00Z"
}
```

And the standard error shape (FastAPI's default), so the frontend always knows where to read the message:

```
// 403 Forbidden — you're not a member of this project
{ "detail": "You do not have access to this project" }
```

### Status codes we commit to

| Code | When |
| --- | --- |
| `200 OK` | Successful GET / PATCH |
| `201 Created` | Successful POST that creates a resource |
| `204 No Content` | Successful DELETE |
| `400 / 422` | Bad input / validation failure (Pydantic returns 422) |
| `401 Unauthorized` | Missing/expired token |
| `403 Forbidden` | Logged in, but not allowed (not a member/owner) |
| `404 Not Found` | Resource doesn't exist (or you can't see it) |

## 6. Wireframing the screens

A **wireframe** is a rough sketch of a screen's layout — boxes and labels, no colors. It forces you to ask "what data does this page need?", which feeds the API contract. TaskFlow's MVP has five screens:

```text
┌─────────────────────────────┐   ┌─────────────────────────────────────────┐
│        /login  /register    │   │   /projects   (after login)               │
│  ┌───────────────────────┐  │   │  TaskFlow            [user ▾] [Logout]    │
│  │ email   [__________]  │  │   │ ───────────────────────────────────────  │
│  │ password[__________]  │  │   │  My Projects            [ + New Project ] │
│  │     [   Log in    ]   │  │   │  ┌────────┐ ┌────────┐ ┌────────┐        │
│  │  no account? Register │  │   │  │Website │ │Mobile  │ │Backlog │ ...    │
│  └───────────────────────┘  │   │  └────────┘ └────────┘ └────────┘        │
└─────────────────────────────┘   └─────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  /projects/3   "Website Redesign"        Filter: [status ▾][assignee ▾]    │
│  ──────────────────────────────────────────────────────────────────────   │
│   Members: Ana(owner) Ben Cara   [ + Invite ]            [ + New Task ]     │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐                       │
│  │  TO DO      │   │ IN PROGRESS │   │   DONE       │                       │
│  ├─────────────┤   ├─────────────┤   ├─────────────┤                       │
│  │ ▢ Hero copy │   │ ▢ Nav bar   │   │ ▣ Set up CI  │                       │
│  │   @Ben 7/10 │   │   @Ana 7/02 │   │   @Cara      │                       │
│  │ ▢ Footer    │   │             │   │              │                       │
│  └─────────────┘   └─────────────┘   └─────────────┘                       │
└──────────────────────────────────────────────────────────────────────────┘
```

Each card shows the fields your API returns: title, assignee, due date. The columns *are* the `status` values. This is why we modeled status as a fixed set of strings — it maps 1:1 to UI columns.

## 7. Scaffolding the two repos

Finally, set up the folders you'll grow over the next five chunks. TaskFlow is a **monorepo**: one top-level folder with a backend and a frontend side-by-side. That keeps the whole app in one Git repo (handy for Module 9's Docker Compose and the Bonus Track).

```text
capstone-taskflow/
├── README.md
├── SPEC.md                 ← scope, user stories, ERD, API contract
├── backend/                ← FastAPI + SQLAlchemy (Modules 5–8)
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── deps.py
│   │   └── routers/
│   ├── requirements.txt
│   └── .env.example
└── frontend/               ← React + Vite (Module 4)
    ├── src/
    │   ├── api/
    │   ├── context/
    │   ├── components/
    │   ├── pages/
    │   └── App.jsx
    ├── index.html
    └── package.json
```

The lab walks you through creating this exact structure and getting a "hello" route plus a Vite dev server running. You won't write feature code yet — that starts in 10.2.

> **💡 Plan-as-code**
>
> Your
>
> SPEC.md
>
> lives
>
> in the repo
>
> . When the spec changes, you edit the file and commit it — the plan and the code evolve together, and reviewers can see both.

## ✅ Recap

- An **MVP scope** with an explicit "out" list keeps the capstone shippable.
- **User stories** (As a… I want… so that…) + acceptance criteria become your build checklist.
- The **ERD** has four entities — User, Project, Membership (join), Task — with foreign keys for every relationship and a join table for the User↔Project many-to-many.
- The **API contract** nails down every endpoint, body, response, and status code under `/api/v1` before any code is written.
- **Wireframes** connect screens to the data they need; the repo is a monorepo with `backend/` + `frontend/`.

**Next:** open `assignment.html` and produce your `SPEC.md`, ERD, API contract, and two scaffolded projects.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
