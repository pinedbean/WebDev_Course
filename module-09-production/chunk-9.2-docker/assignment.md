*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.2 — Lab: The Whole App via Docker Compose

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Containerize the Tasks app so it runs anywhere. You'll write a **backend Dockerfile**, a **multi-stage frontend Dockerfile** (Node build → Nginx serve), `.dockerignore` files, and a **`docker-compose.yml`** that runs both — with the SQLite database stored in a **named volume** so data survives. The deliverable is the full app coming up with one command: `docker compose up --build`.

## Before you start

- You finished **9.1**: the frontend builds (`npm run build` → `dist/`) and the backend reads config from env vars.
- **Install Docker Desktop** (macOS) and confirm it's running: `docker --version` and `docker compose version` both work.
- Suggested top-level layout: a project root containing `tasks-api/` and `tasks-web/` (put `docker-compose.yml` at the root).

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Tasks

### 1 Backend Dockerfile

In `tasks-api/`, create a `Dockerfile` based on `python:3.11-slim`. Copy `requirements.txt` and install *before* copying the code (layer caching), expose 8000, and set the start command to run uvicorn bound to `0.0.0.0`. Add a `tasks-api/.dockerignore` excluding `__pycache__/`, `.venv/`, `tasks.db`, `.env`, and `.git/`.

### 2 Make the DB path configurable

Your container will store SQLite in a mounted volume (e.g. `/data`), not the source folder. Confirm `DATABASE_URL` drives the path in `app/database.py` (it should read `settings.database_url`). You'll pass `sqlite:////data/tasks.db` from Compose.

> **💡 Four slashes for an absolute path**
>
> SQLite URLs use
>
> sqlite:///relative.db
>
> (three slashes = relative) vs
>
> sqlite:////data/tasks.db
>
> (four = absolute
>
> /data/tasks.db
>
> ). The volume mounts at an absolute path, so you need four.

### 3 Frontend multi-stage Dockerfile

In `tasks-web/`, create a **multi-stage** `Dockerfile`: stage 1 uses `node:20-alpine` to `npm ci` and `npm run build`; stage 2 uses `nginx:alpine` and copies `--from=build` the `dist/` into Nginx's web root. Add a `tasks-web/.dockerignore` (ignore `node_modules/`, `dist/`).

### 4 Frontend `nginx.conf` with SPA fallback

Create `tasks-web/nginx.conf` that serves the static files and falls back to `index.html` (`try_files $uri $uri/ /index.html;`) so refreshing on `/dashboard` works. Have the Dockerfile copy it into `/etc/nginx/conf.d/default.conf`.

### 5 `docker-compose.yml`

At the project root, define two services:

- `api` — builds `./tasks-api`; sets `SECRET_KEY`, `DATABASE_URL=sqlite:////data/tasks.db`, `ENVIRONMENT=production`, `FRONTEND_ORIGIN`; mounts a named volume `tasks-data` at `/data`; maps `8000:8000`.
- `web` — builds `./tasks-web`; maps `5173:80`; `depends_on: [api]`.

Declare the `tasks-data` named volume. Put your real `SECRET_KEY` in a root `.env` (git-ignored) and reference it as `${SECRET_KEY}` in Compose.

### 6 Bring it up

```bash
docker compose up --build
```

Watch both images build and the containers start. Then in your browser open `http://localhost:5173` (frontend) and confirm the backend answers at `http://localhost:8000/health`.

### 7 Run migrations inside the container

Your fresh volume has an empty DB. Apply the schema by running Alembic in the running api container:

```bash
docker compose exec api alembic upgrade head
```

(In 9.4 you'll automate this at startup. For now, run it once.) Then register/log in and create a task through the UI.

### 8 Prove persistence

Create some tasks, then stop and restart the stack and confirm your data is still there:

```bash
docker compose down       # stops & removes containers (NOT the named volume)
docker compose up         # bring it back
# log in again — your tasks are still present (they live in tasks-data)
```

## ✅ Deliverable — acceptance checklist

- `tasks-api/Dockerfile` builds a working backend image (deps installed before code; binds `0.0.0.0:8000`).
- `tasks-web/Dockerfile` is multi-stage (Node build → Nginx serve) and the final image contains only `dist/` on Nginx.
- Both folders have a `.dockerignore`; the frontend has an `nginx.conf` with an SPA fallback to `index.html`.
- `docker-compose.yml` defines `api` + `web`, a named volume for the SQLite file, port maps, and env vars (secret from a git-ignored `.env`).
- `docker compose up --build` serves the frontend at `:5173` and the backend at `:8000`; `/health` returns ok.
- Data survives `docker compose down` + `up` (the volume persisted it); no secrets or `tasks.db` are baked into any image.

## 🚀 Stretch goals (optional)

- Add a `healthcheck` to the `api` service in Compose that curls `/health`, and make `web` wait for it with `depends_on: condition: service_healthy`.
- Shrink the backend image: add a non-root user and use `--no-cache-dir`; compare `docker images` sizes before/after.
- Run the backend with multiple workers in the container `CMD` (from 9.1) and watch the logs show several worker PIDs.
- Use `docker compose logs -f` and confirm your 8.1 JSON logs stream to stdout from inside the container.
- Add a `.env.example` at the root documenting the Compose variables.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
