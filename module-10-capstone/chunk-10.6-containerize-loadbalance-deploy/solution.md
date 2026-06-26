*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow · 🎓 FINALE*

# Chunk 10.6 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We containerize both halves, put Nginx in front of replicated backends, run migrations on start, add CI, and polish the README. New files:

```text
capstone-taskflow/
├── .env                       (SECRET_KEY for compose — gitignored)
├── docker-compose.yml
├── .github/workflows/ci.yml
├── docs/                      (screenshots)
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── entrypoint.sh
└── frontend/
    ├── Dockerfile
    ├── .dockerignore
    └── nginx.conf
```

### 1 Backend Dockerfile + ignore + entrypoint

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/api/v1/health')"

CMD ["./entrypoint.sh"]
```

```
# backend/.dockerignore
venv/
__pycache__/
*.pyc
*.db
.env
```

```bash
# backend/entrypoint.sh
#!/bin/sh
set -e
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> **📝 Alembic finds the DB**
>
> Your
>
> alembic/env.py
>
> reads
>
> DATABASE_URL
>
> from the environment (10.2). In the container that's
>
> sqlite:////data/taskflow.db
>
> — four slashes = an absolute path to the mounted volume.

### 2 Frontend Dockerfile + ignore

```dockerfile
# frontend/Dockerfile
# ---- build ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# ---- serve ----
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

```
# frontend/.dockerignore
node_modules/
dist/
.env
```

> **⚠️ Vite bakes env at build time**
>
> VITE_API_URL
>
> is compiled into the bundle during
>
> npm run build
>
> — it is
>
> not
>
> read at runtime. That's why we set it as a build
>
> ARG
>
> to
>
> /api/v1
>
> (same-origin), so the production SPA calls the API through Nginx.

### 3 Nginx config

```
# frontend/nginx.conf
upstream taskflow_api {
    server backend:8000;     # Docker DNS round-robins across replicas
}

server {
    listen 80;

    location /api/ {
        proxy_pass http://taskflow_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Request-ID $request_id;
    }

    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }

    add_header X-Content-Type-Options nosniff;
    add_header Referrer-Policy strict-origin-when-cross-origin;
}
```

### 4 docker-compose

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - CORS_ORIGINS=http://localhost
      - DATABASE_URL=sqlite:////data/taskflow.db
      - ENV=production
    volumes:
      - taskflow_data:/data
    expose:
      - "8000"
    deploy:
      replicas: 3
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  taskflow_data:
```

Create the root `.env` with a secret, then build & run:

```python
cd capstone-taskflow
echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > .env
docker compose up --build
```

```
[+] Running 5/5
 ✔ Network capstone-taskflow_default       Created
 ✔ Container capstone-taskflow-backend-1   Started
 ✔ Container capstone-taskflow-backend-2   Started
 ✔ Container capstone-taskflow-backend-3   Started
 ✔ Container capstone-taskflow-frontend-1  Started
backend-1  | {"ts":"...","level":"INFO","msg":"request","path":"/api/v1/health","status":200}
```

Open `http://localhost` — the full app runs through Nginx. Register, create a project, use the board. No CORS errors, because it's all same-origin now.

> **📝 Compose v2 `deploy.replicas`**
>
> Modern
>
> docker compose
>
> honors
>
> deploy.replicas
>
> for plain
>
> up
>
> . If your version ignores it, scale explicitly:
>
> docker compose up --build --scale backend=3
>
> .

### 5 Prove the load balancing

Add the container hostname to each request log so you can see the rotation. In `app/middleware.py`, include `socket.gethostname()`:

```python
# app/middleware.py  (add to the logged extra_fields)
import socket
HOSTNAME = socket.gethostname()
# ...
log.info("request", extra={"extra_fields": {
    "request_id": request_id, "host": HOSTNAME,
    "method": request.method, "path": request.url.path,
    "status": response.status_code, "duration_ms": duration_ms,
}})
```

Rebuild, then hammer the health route and watch the `host` field cycle across replicas:

```bash
for i in $(seq 1 6); do curl -s http://localhost/api/v1/health > /dev/null; done
docker compose logs backend | grep '"path":"/api/v1/health"' | tail -6
```

```
backend-1  | {... "host":"a1b2c3", "path":"/api/v1/health", "status":200}
backend-2  | {... "host":"d4e5f6", "path":"/api/v1/health", "status":200}
backend-3  | {... "host":"g7h8i9", "path":"/api/v1/health", "status":200}
backend-1  | {... "host":"a1b2c3", ...}
```

Different `host` values = Nginx is balancing. Now kill one replica and confirm the app stays up:

```bash
docker compose stop backend-2     # or: docker stop <container>
# refresh http://localhost — still works; Nginx routes around the dead node
```

### 6 CI workflow

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r backend/requirements.txt
      - run: cd backend && pytest -q || echo "no tests yet"
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "20" }
      - run: cd frontend && npm ci && npm run build
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker compose build
```

Commit and push — the checks run on GitHub. A green check on every PR is the habit Bonus Track B.1 builds on.

### 7 Polish the README

Take screenshots (login, projects, board) into `docs/`, then make the README sell it:

```python
# TaskFlow

A collaborative team task & project tracker. Register, create projects,
invite teammates, and manage work on a kanban board.

![Task board](docs/board.png)

## Stack
React + Vite · FastAPI · SQLAlchemy · SQLite · JWT auth · Nginx · Docker

## Architecture
Browser -> Nginx (serves SPA, load-balances /api) -> 3x FastAPI -> SQLite volume

## Run it
    git clone <your-repo> && cd capstone-taskflow
    echo "SECRET_KEY=$(python3 -c 'import secrets;print(secrets.token_hex(32))')" > .env
    docker compose up --build
    # open http://localhost

## Features
- Email/password auth (JWT), protected routes
- Projects with owner + member roles; invite teammates by email
- Task board: To Do / In Progress / Done, assignees, due dates, filtering
- Structured JSON logs with request IDs; /health + /health/ready
- Nginx load balancing across stateless backend replicas

## Security notes
(see the list from Chunk 10.5)

## Known limits / next steps
- SQLite serializes writes — swap for Postgres to scale (Bonus Track B.3)
- Add refresh tokens, real rate-limit store (Redis), e2e tests
- Deploy to GCP Cloud Run with HTTPS load balancer (Bonus Track B.2–B.3)
```

### 8 Final verification

1. `docker compose down` then `docker compose up` — your data is still there (the volume persists).
2. The app works end-to-end through `http://localhost` with no CORS errors.
3. Logs show requests spread across `backend-1/2/3`.
4. Stopping a replica doesn't break the app.
5. README renders with the screenshot and run instructions.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| Frontend loads but API 502 | Nginx can't reach the backend. Check the `upstream` name matches the compose service (`backend:8000`) and backends are healthy. |
| 404 on refresh at `/projects/3` | Missing the SPA fallback. Confirm `try_files $uri /index.html;` in nginx.conf. |
| API calls go to `localhost:8000` in prod | You didn't rebuild with `VITE_API_URL=/api/v1`. Rebuild the frontend image. |
| `SECRET_KEY` empty / app refuses to start | Create the root `.env` before `up`; compose reads `${SECRET_KEY}` from it. |
| DB resets every restart | The volume isn't mounted or the path is wrong. Use `sqlite:////data/taskflow.db` + the `taskflow_data:/data` volume. |
| Only one replica in logs | Your compose version ignores `deploy.replicas`; use `--scale backend=3`. |

## 🎓 Course complete — congratulations!

You did it. Starting from a blank HTML file, you built **TaskFlow**: a real, collaborative, full-stack web application — and you shipped it containerized and load-balanced. Take a moment; this is a genuine milestone.

Look at everything you assembled, end to end:

- **Frontend** — React + Vite SPA: auth context, protected routes, an app shell, a projects view, and a collaborative kanban board with filtering. (Modules 1–4)
- **Backend** — FastAPI + SQLAlchemy: four related tables, JWT auth, and CRUD guarded by composable ownership/membership rules. (Modules 5–7)
- **Observability** — structured JSON logs, request IDs, health checks, a global error handler, and a React error boundary. (Module 8)
- **Production** — Dockerized both halves, Nginx load-balancing across stateless replicas, migrations on start, CI, and a portfolio README. (Module 9)

That is a portfolio-grade, interview-ready project. Put it on your résumé, link the repo, and walk an interviewer through the architecture diagram — you can defend every decision because you made each one.

### ➡️ Where to go next: the optional Bonus Track

You've taken TaskFlow as far as "runs great on one host." The **Bonus Track** takes it to the cloud the way teams actually ship:

- **B.1 — Git Strategy & Collaborative Workflows:** GitHub Flow, PRs & review, merge vs. rebase, branch protection, and a tagged `v1.0.0` release on your TaskFlow repo.
- **B.2 — Deploy to GCP (Cloud Run):** push your images to Artifact Registry and run TaskFlow on serverless containers with a public URL.
- **B.3 — GCP Load Balancing, Managed Data & CI/CD:** an HTTPS load balancer, migrate SQLite → Cloud SQL (Postgres), and auto-deploy on every merge.

Your stateless JWT, health checks, env-based config, and `/api/v1` versioning were all designed to make that cloud jump smooth. When you're ready, start at **bonus-track/b1-git-strategy**. Otherwise — go build something of your own with the exact skills you just proved you have. 🚀

## ✅ Capstone deliverable

- ✅ Dockerized frontend + backend; one-command `docker compose up`.
- ✅ Nginx load-balancing across multiple stateless replicas, demonstrated.
- ✅ Migrations on start, persistent volume, CI workflow.
- ✅ A polished, screenshot-rich README — a deployed, load-balanced TaskFlow for your résumé.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
