*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow · 🎓 FINALE*

# Chunk 10.6 — Lab: Ship Load-Balanced TaskFlow

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Take TaskFlow from "runs on my machine" to a containerized, load-balanced stack that comes up with one command. Dockerize the backend and frontend, put Nginx in front load-balancing across multiple backend replicas, run migrations on startup, add a CI workflow, and polish the README with screenshots. This is the deliverable you put on your résumé.

## Before you start

- Docker Desktop installed and running (`docker --version`, `docker compose version`).
- Your hardened TaskFlow from 10.5 works locally (health/ready routes, env-based config).
- Have your Module 9 notes (Dockerfiles, compose, Nginx upstream) close by.

> **⚠️ Build it yourself first**
>
> You containerized an app in Module 9 — apply the same moves to TaskFlow. Open the solution to compare configs, not to skip the thinking.

## Tasks

### 1 Backend Dockerfile

Write `backend/Dockerfile` (Python slim, cache deps before copying code, expose 8000, a `HEALTHCHECK` hitting `/api/v1/health`). Add a `backend/.dockerignore` (venv, `__pycache__`, `*.db`, `.env`).

### 2 Migrations on startup

Add `backend/entrypoint.sh` that runs `alembic upgrade head` then launches uvicorn, and call it from the Dockerfile. Make sure the DB path points at a mounted volume.

### 3 Frontend Dockerfile (multi-stage)

Write `frontend/Dockerfile`: stage 1 builds with Node (`npm ci` + `npm run build`, with `VITE_API_URL=/api/v1`); stage 2 copies `dist/` into an Nginx image. Add `frontend/.dockerignore` (node_modules, dist).

### 4 Nginx config

Write `frontend/nginx.conf`: an `upstream` pointing at the `backend` service, a `location /api/` that proxies to it (forwarding `X-Request-ID`), and a SPA `location /` with `try_files $uri /index.html`. Add a security header.

### 5 docker-compose with replicas

Write `docker-compose.yml` with a `backend` service (3 replicas, shared DB volume, env from a root `.env`) and a `frontend` service publishing port 80 and depending on the backend. Bring it up with `docker compose up --build`.

### 6 Prove the load balancing

Open `http://localhost` and use the app (register, projects, board) entirely through Nginx. Then demonstrate that requests hit different replicas — e.g. log the hostname per request and watch the request logs cycle, or stop one replica and confirm the app keeps working.

### 7 CI workflow

Add `.github/workflows/ci.yml` that, on push/PR, installs backend deps + runs tests and builds the frontend. Confirm the YAML is valid (it'll run when you push).

### 8 Polish the README + screenshots

Upgrade the root `README.md`: pitch, screenshot/GIF of the board, architecture diagram, `docker compose up` instructions, feature list, security notes, and known limits/next steps. Save 2–3 screenshots under `docs/`.

## ✅ Deliverable — acceptance checklist

- `docker compose up --build` brings up the full stack; the app works at `http://localhost`.
- The frontend is served by Nginx and calls the API same-origin (no CORS errors in prod).
- The backend runs as **multiple replicas**; Nginx load-balances across them (demonstrated).
- Migrations run automatically on container start; data persists in a volume across `down`/`up`.
- Health checks pass; stopping one replica doesn't take the app down.
- A CI workflow builds the frontend and runs backend checks.
- The README has a screenshot, the architecture diagram, run instructions, features, and security/limits notes.

## 🏁 Capstone Checkpoint

Step back and confirm the whole thing: a stranger can clone your repo, run **one command**, and reach a working, load-balanced TaskFlow where users register, collaborate on projects, and manage a task board — observable, hardened, and documented. That is a portfolio-grade, real-world full-stack application.

## 🚀 Stretch goals (optional)

- Deploy to a real host (a small VPS or a container host) and add the live URL to the README.
- Extend CI to build & push the Docker images to a registry.
- Add a `healthcheck` to the compose services and a `restart: unless-stopped` policy.
- Record a 20-second GIF of the board in action for the README.
- **Go to the Bonus Track**: adopt a Git branching strategy (B.1) and deploy TaskFlow to GCP Cloud Run with a managed Postgres + HTTPS load balancer (B.2–B.3).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
