*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We add automated migrations, a CI workflow, a test, and the production docs — then run the 🏁 Checkpoint. New/changed files:

```text
project-root/
├── .github/workflows/ci.yml     (CI: lint + test + build)
├── PRODUCTION.md                (deploy runbook)
├── POSTGRES.md                  (SQLite -> Postgres path)
├── .env.example                 (documented placeholders)
└── tasks-api/
    ├── entrypoint.sh            (migrate, then serve)
    ├── Dockerfile               (uses entrypoint)
    └── tests/test_health.py     (a real test for CI)
```

## Part A — Automated migrations

### 1 `tasks-api/entrypoint.sh`

```bash
#!/bin/sh
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

> **📝 Why `exec`**
>
> exec
>
> replaces the shell with uvicorn so it becomes PID 1 in the container. That means Docker's stop signals reach uvicorn directly for a clean shutdown — without
>
> exec
>
> , signals hit the shell and your server may not stop gracefully.

### 2 Use it in the Dockerfile

```
# tasks-api/Dockerfile  (replace the old CMD)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
CMD ["/entrypoint.sh"]
```

Rebuild and bring it up — migrations now run on start, no manual step:

```bash
docker compose up --build --scale api=3
```

```
api-1  | Running database migrations...
api-1  | INFO  [alembic.runtime.migration] Running upgrade ... -> ..., add auth fields
api-1  | Starting server...
api-1  | {"timestamp":"...","level":"INFO","logger":"uvicorn.error","message":"Uvicorn running on http://0.0.0.0:8000","request_id":"-"}
```

> **⚠️ Avoiding the migration stampede**
>
> With
>
> --scale api=3
>
> every replica runs the entrypoint, so three try to migrate. Alembic tracks the version and migrations are transactional, so this is usually safe (the first wins; the rest see "already at head"). The cleaner pattern for real deploys: a one-shot migrate before scaling —
>
> ```bash
> docker compose run --rm api alembic upgrade head
> docker compose up -d --scale api=3
> ```
>
> Document whichever you choose in the runbook.

## Part B — CI pipeline

### 3 A test for CI to run — `tasks-api/tests/test_health.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
```

```bash
# run locally first
cd tasks-api
pip install pytest httpx
SECRET_KEY=test-secret pytest -q
# 1 passed
```

> **💡 `TestClient` needs `httpx`**
>
> Starlette's
>
> TestClient
>
> is built on
>
> httpx
>
> . If you see an import error,
>
> pip install httpx
>
> (and add it to a dev-requirements list).

### 4 `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: tasks-api
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pip install ruff pytest httpx
      - run: ruff check .
      - run: pytest -q
        env:
          SECRET_KEY: test-secret-not-real

  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: tasks-web
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: tasks-web/package-lock.json
      - run: npm ci
      - run: npm run build
```

> **📝 The throwaway SECRET_KEY**
>
> Your Module 7 settings refuse to start without
>
> SECRET_KEY
>
> (a good thing). CI just needs
>
> a
>
> value to import the app and run tests, so we pass a non-secret literal via the step's
>
> env
>
> . Real secrets in CI come from
>
> ${{ secrets.NAME }}
>
> , never literals — but a test key is fine to hardcode because it protects nothing.

### 5 Simulate the pipeline locally

```bash
cd tasks-api && ruff check . && SECRET_KEY=test pytest -q
cd ../tasks-web && npm ci && npm run build
```

If both pass locally, they'll pass on GitHub. Push to a branch, open a PR, and watch the checks run.

## Part C — Production docs

### 6 `.env.example` + `POSTGRES.md`

```
# .env.example  (root — placeholders only, committed)
SECRET_KEY=
ENVIRONMENT=production
FRONTEND_ORIGIN=http://localhost
LOG_LEVEL=INFO
# Default DB (SQLite). For Postgres, see POSTGRES.md
DATABASE_URL=sqlite:////data/tasks.db
```

```
# POSTGRES.md — moving off SQLite

When: multiple writing replicas, a networked/managed DB, or an
ephemeral filesystem (e.g. Cloud Run).

1. Add a driver:        pip install "psycopg[binary]"
2. Add a db service (compose) or use a managed instance.
3. Set the URL (env only):
   DATABASE_URL=postgresql+psycopg://user:pass@db:5432/tasks
4. Drop SQLite-only bits in database.py:
   - remove connect_args={"check_same_thread": False}
   - remove the WAL / foreign_keys PRAGMA listener
   - (optionally) configure a connection pool
5. Run existing migrations:  alembic upgrade head

Models, schemas, routers, and the load-balanced topology are unchanged.
```

### 7 `PRODUCTION.md` — the runbook

```bash
# PRODUCTION.md — Tasks App Deploy Runbook

## Prerequisites
- Docker + Docker Compose on the host
- A root .env with a STRONG, production-only SECRET_KEY (chmod 600)

## Required env vars (see .env.example)
SECRET_KEY, ENVIRONMENT=production, FRONTEND_ORIGIN, LOG_LEVEL, DATABASE_URL

## Build & start (load-balanced)
docker compose run --rm api alembic upgrade head     # migrate once
docker compose up -d --build --scale api=3           # Nginx + 3 replicas

## Stop
docker compose down            # keeps the data volume
docker compose down -v         # DANGER: also deletes the database volume

## Migrations
Run automatically via entrypoint.sh, OR once via the command above.

## Health
- Liveness:  GET http://HOST/api/health
- Readiness: GET http://HOST/api/health/ready

## Logs
docker compose logs -f         # structured JSON, with request ids

## Scale
docker compose up -d --scale api=N

## Rollback
Redeploy the previous image tag (git revert + rebuild, or pull prior tag),
then re-run migrations only if the schema changed.
```

## 🏁 Module 9 Checkpoint — verification walkthrough

Bring the whole thing up and confirm each property. This is the demo you can give from the runbook alone.

```bash
# 0. Up: load-balanced + containerized, migrations automatic
docker compose up -d --build --scale api=3

# 1. Single origin + frontend served
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/        # 200

# 2. Load balancing visible (instance rotates)
for i in $(seq 1 6); do curl -s http://localhost/api/health; echo; done
# {"status":"ok","instance":"...a..."}
# {"status":"ok","instance":"...b..."}
# {"status":"ok","instance":"...c..."}  (cycles)

# 3. Readiness (DB reachable)
curl -s http://localhost/api/health/ready
# {"status":"ready","database":"ok"}

# 4. Stateless auth across replicas (browser): register, log in,
#    create tasks, refresh -> still logged in though requests hit
#    different replicas (shared SECRET_KEY).
docker compose exec api printenv SECRET_KEY   # same on every replica

# 5. Resilience: kill a replica, app keeps serving
docker compose ps                              # find an api container id
docker compose stop <one-api-container>
for i in $(seq 1 6); do curl -s http://localhost/api/health; echo; done
# still answers (from the surviving replicas)

# 6. Observability: structured logs + clean errors
docker compose logs -f api                     # JSON lines w/ request_id

# 7. CI green (locally or on GitHub)
cd tasks-api && ruff check . && SECRET_KEY=test pytest -q
cd ../tasks-web && npm ci && npm run build
```

When all seven pass and your `PRODUCTION.md` lets someone else reproduce them, the checkpoint is complete: a **documented, load-balanced, containerized deployment**. 🏁

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `entrypoint.sh: permission denied` | You didn't `chmod +x`. Add `RUN chmod +x /entrypoint.sh` in the Dockerfile (line endings must be LF, not CRLF). |
| Migrations run but app doesn't start | You forgot `exec` (or the uvicorn line). The script should end with `exec uvicorn ...`. |
| CI fails: `field required: secret_key` | Add `env: SECRET_KEY: test-...` to the step that imports the app / runs pytest. |
| CI fails on `ruff` style nits | Run `ruff check . --fix` locally, commit, push. Or relax rules in `pyproject.toml`. |
| `npm ci` fails in CI | Commit your `package-lock.json` — `ci` requires it and installs exactly from it. |
| All replicas migrate and one errors | Use the one-shot `docker compose run --rm api alembic upgrade head` before scaling, as documented. |
| `database is locked` under real write load | SQLite's ceiling. Follow `POSTGRES.md` — it's mostly a `DATABASE_URL` change. |

## 📄 Complete `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  backend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: tasks-api
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pip install ruff pytest httpx
      - run: ruff check .
      - run: pytest -q
        env:
          SECRET_KEY: test-secret-not-real

  frontend:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: tasks-web
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: npm
          cache-dependency-path: tasks-web/package-lock.json
      - run: npm ci
      - run: npm run build
```

## 🎉 Module 9 complete

You took the Tasks app from "runs on my laptop" to a production-shaped system:

- **9.1** — production builds, env (build-time vs runtime), secrets hygiene, prod run config.
- **9.2** — Dockerfiles (incl. a multi-stage frontend), `.dockerignore`, and the whole app via `docker compose up` with a durable volume.
- **9.3** — Nginx reverse proxy + load balancing across multiple FastAPI replicas; stateless JWT means no sticky sessions; the honest SQLite single-writer limit.
- **9.4** — automated migrations, a GitHub Actions CI pipeline, a documented deploy runbook, the path to Postgres — and the 🏁 Checkpoint.

Combined with Module 8's observability, you now have an app that's **built, containerized, load-balanced, observable, deployable, and documented**. That's a genuinely production-grade story you can defend in an interview.

> **📝 Where this goes next**
>
> You've practiced every production skill on the Tasks API. In
>
> Module 10 (Capstone: TaskFlow)
>
> you'll apply all of it — auth, logging, Docker, load balancing, CI — to build and ship a real, portfolio-grade app from scratch. And the optional
>
> Bonus Track
>
> takes this exact containerized stack to the cloud on GCP (Cloud Run, a managed HTTPS load balancer, Cloud SQL/Postgres, and CI/CD).

**Up next → Module 10, Chunk 10.1: Capstone Planning & Data Modeling.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
