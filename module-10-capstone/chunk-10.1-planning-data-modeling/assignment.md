*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.1 — Lab: Spec, ERD & Scaffolded Repos

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Produce the planning artifacts and skeletons for TaskFlow: a written `SPEC.md` (scope, user stories, ERD, API contract), and two scaffolded projects — a FastAPI `backend/` that answers `/health`, and a React + Vite `frontend/` that runs. No feature code yet; you're laying the foundation you build on for the rest of the module.

## Before you start

- You've completed Modules 0–9 (or are following along with the stack). You need **Node.js LTS**, **Python 3.11+**, and **Git** installed (check with `node -v`, `python3 --version`, `git --version`).
- Pick a home for the project, e.g. `~/Desktop/webdev-course/capstone-taskflow/`.
- Have the lecture's ERD and API contract open for reference.

> **⚠️ Try it yourself first**
>
> Write the spec in your own words and scaffold from memory of Modules 4 and 5. Only open
>
> solution.html
>
> to compare or when truly stuck.

## Tasks

### 1 Create the monorepo & initialize Git

Make the top-level `capstone-taskflow/` folder with `backend/` and `frontend/` subfolders. Run `git init` at the top level and add a sensible `.gitignore` (ignore `venv/`, `__pycache__/`, `node_modules/`, `*.db`, `.env`, `dist/`).

### 2 Write `SPEC.md` — scope & user stories

At the repo root, create `SPEC.md`. Include: a one-paragraph product summary; an **In scope / Out of scope** table; and at least **six user stories** ("As a… I want… so that…") each with 1–2 acceptance criteria. Cover register/login, projects, invites, and tasks.

### 3 Add the ERD to the spec

In `SPEC.md`, document the four entities (User, Project, Membership, Task) with their fields and types, and describe each relationship in words (e.g. "User 1—* Project via `owner_id`"). Include a text/ASCII ERD diagram, or link an image you drew.

### 4 Add the API contract to the spec

Add an endpoint table (method, path, purpose, auth) for all routes under `/api/v1`. Then write the exact JSON request/response for at least **two** endpoints (pick `POST /auth/register` and `POST /projects/{id}/tasks`). List the status codes you'll use.

### 5 Scaffold the backend

In `backend/`: create a virtual environment, install `fastapi` + `uvicorn`, freeze `requirements.txt`, and create `app/main.py` with a FastAPI app that exposes `GET /api/v1/health` returning `{"status":"ok"}`. Run it and confirm the route works and `/docs` loads.

### 6 Scaffold the frontend

In the repo root, create the Vite React app into `frontend/`, install dependencies plus `react-router-dom`, and run the dev server. Confirm the default app renders at the printed localhost URL. Add an `.env` with `VITE_API_URL=http://localhost:8000/api/v1`.

### 7 Write the README & commit

Add a short root `README.md` (what TaskFlow is, how to run backend + frontend). Make your first commit, e.g. `git commit -m "chore: scaffold TaskFlow monorepo + spec"`.

## ✅ Deliverable — acceptance checklist

- `capstone-taskflow/` exists with `backend/` and `frontend/` and a Git repo (with `.gitignore`).
- `SPEC.md` contains product summary, in/out scope table, and 6+ user stories with acceptance criteria.
- `SPEC.md` documents the 4 entities + fields and describes every relationship.
- `SPEC.md` has the full endpoint table plus exact JSON for 2 endpoints and the status-code list.
- Backend runs: `GET http://localhost:8000/api/v1/health` returns `{"status":"ok"}` and `/docs` loads.
- Frontend runs: the Vite dev server renders the default React app; `.env` defines `VITE_API_URL`.
- A root `README.md` exists and you've made at least one commit.

## 🚀 Stretch goals (optional)

- Draw the ERD in a visual tool (dbdiagram.io, Excalidraw, or Mermaid) and export a PNG into the repo.
- Add a Mermaid `erDiagram` code block to `SPEC.md` so GitHub renders it automatically.
- Write a tiny `Makefile` or `npm` scripts so `make dev` starts both servers.
- Create the empty router files (`app/routers/auth.py`, `projects.py`, `tasks.py`) so 10.2 has a head start.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
