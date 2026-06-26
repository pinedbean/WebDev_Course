*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.4 — Lab: CI/CD & the Module 9 Checkpoint

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Make the Tasks app **deployable and self-checking**. You'll automate database migrations at container start, write a **GitHub Actions CI pipeline** (lint + test backend, build frontend), document a deploy runbook, and lay out the path off SQLite. Then you'll complete the 🏁 **Module 9 Checkpoint**: a documented, load-balanced, containerized deployment you can demo end to end.

## Before you start

- You finished **9.1–9.3**: production builds, Docker images, Compose, and the Nginx-load-balanced stack with multiple API replicas.
- Your project is in a Git repo (you'll add a workflow under `.github/workflows/`). A GitHub remote helps for the CI stretch goal but isn't required to write the file.
- Docker Desktop running.

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Part A — Automated migrations

### 1 Write an entrypoint that migrates then serves

Create `tasks-api/entrypoint.sh` that runs `alembic upgrade head` and then starts the server (uvicorn/gunicorn, bound to `0.0.0.0`, multiple workers). Use `set -e` so a failed migration aborts startup loudly.

### 2 Wire it into the Dockerfile

Copy `entrypoint.sh` into the image, make it executable, and set it as the container's `CMD`/`ENTRYPOINT`. Rebuild and bring the stack up — confirm migrations now run automatically (you no longer need the manual `alembic upgrade head` from 9.2/9.3).

> **💡 Avoid a migration stampede**
>
> With multiple replicas, don't have all of them migrate at once. Either run the entrypoint migration on a single designated service, or use a one-shot
>
> docker compose run --rm api alembic upgrade head
>
> before scaling up. Note your choice in the runbook.

## Part B — CI pipeline

### 3 Create `.github/workflows/ci.yml`

Add a workflow triggered on push to `main` and on pull requests, with two parallel jobs:

- **backend** — checkout, set up Python 3.11, install requirements + `ruff` + `pytest`, run `ruff check .` and `pytest` (provide a throwaway `SECRET_KEY` via step env).
- **frontend** — checkout, set up Node 20, `npm ci`, `npm run build`.

### 4 Add a tiny backend test

So `pytest` has something to run, add `tasks-api/tests/test_health.py` using FastAPI's `TestClient` to assert `GET /health` returns 200 and `{"status":"ok", ...}`. (Install `httpx` if needed.) Confirm it passes locally with `pytest`.

### 5 Run the checks locally (simulate CI)

Before relying on GitHub, run the same commands locally so you know the pipeline will be green:

```bash
cd tasks-api && ruff check . && pytest
cd ../tasks-web && npm ci && npm run build
```

## Part C — Production readiness

### 6 Secrets & the Postgres path

Confirm no secret is baked into any image or `VITE_` var, and that a root `.env.example` documents required variables with placeholders. Then add a short `POSTGRES.md` (or a section in your runbook) describing the exact change to move from SQLite to Postgres: install a driver, change `DATABASE_URL`, run existing migrations, drop SQLite-only pragmas.

### 7 Write the deploy runbook

Expand your 9.1 `PRODUCTION.md` into a real runbook covering: prerequisites, required env vars, build commands, how migrations run, start/stop (`docker compose up -d` / `down`), how to scale (`--scale api=N`), health-check URLs, where logs go, and how to roll back (redeploy the previous image tag).

## 🏁 Module 9 Checkpoint — Documented, load-balanced, containerized deployment

Tie the whole module together. Bring up the full stack and verify each property. You should be able to demo this start to finish from your runbook alone.

1. **One command up:** `docker compose up -d --build --scale api=3` brings up Nginx + 3 API replicas + the shared DB.
2. **Migrations ran automatically** (or via your documented one-shot step) — the DB schema is current with no manual SQL.
3. **Single origin:** the browser uses `http://localhost` only; the frontend loads and API calls go through `/api/`.
4. **Load balancing is visible:** repeated `/api/health` calls show the `instance` rotating across replicas.
5. **Stateless auth works across replicas:** log in once, use the app — staying logged in despite requests hitting different replicas (shared `SECRET_KEY`).
6. **Resilience:** stop one replica; the app keeps serving (Nginx routes around it).
7. **Observability:** `docker compose logs -f` shows structured JSON logs with request ids; an induced error returns a clean 500 and is logged.
8. **CI is green:** the GitHub Actions workflow (or the local simulation) passes lint, tests, and the frontend build.
9. **Documented:** the runbook lets someone else reproduce all of the above, and the Postgres-migration path is written down.

## ✅ Deliverable — acceptance checklist

- `entrypoint.sh` runs `alembic upgrade head` then starts the server; the Dockerfile uses it.
- `.github/workflows/ci.yml` runs backend lint+test and frontend build on push/PR.
- A passing backend test exists (at least `GET /health`), and the CI steps pass when simulated locally.
- No secrets in images or `VITE_` vars; `.env.example` documents required vars; a Postgres-migration note exists.
- A deploy runbook documents build, env, migrations, start/stop, scaling, health, logs, and rollback.
- 🏁 The full stack comes up load-balanced and containerized, and you can demo every checkpoint item from the runbook.

## 🚀 Stretch goals (optional)

- Add a CD job (`on: push: branches:[main]`) that builds and pushes the Docker images to a registry (GHCR), using `${{ secrets.* }}` for credentials.
- Actually deploy: spin up a cheap VPS, install Docker, copy your repo + a server-side `.env`, and run `docker compose up -d` behind the host's firewall.
- Add a real Postgres service to a `docker-compose.prod.yml` and point `DATABASE_URL` at it; run your migrations against it and confirm the app is unchanged.
- Cache CI dependencies (`actions/setup-node` cache, pip cache) to speed up runs.
- Add a CI status badge to your README.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
