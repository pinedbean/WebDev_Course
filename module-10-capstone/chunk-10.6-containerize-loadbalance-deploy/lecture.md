*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow · 🎓 FINALE*

# Chunk 10.6 — Containerize, Load-Balance & Deploy

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to write a **backend Dockerfile** for FastAPI and a **multi-stage frontend Dockerfile** (build with Node, serve with Nginx).
- How **docker-compose** runs the whole stack and scales the backend to **multiple replicas**.
- How **Nginx load-balances** across those replicas and reverse-proxies the API + serves the SPA.
- Why **stateless JWT** makes scaling out easy — and where SQLite hits its limit.
- How to add a **CI workflow** and a **polished README** with screenshots for your portfolio.

This is the 🎓 course finale. The lab delivers a deployed, load-balanced TaskFlow you can put on your résumé.

## 1. The target architecture

Everything you containerized in Module 9 now wraps your real app. One Nginx in front; it serves the built frontend and proxies `/api` to a pool of identical backend replicas; all backends share one SQLite volume.

```text
                      ┌─────────────────────────┐
browser ──────────►   │   nginx  (port 80)       │
                      │  - serves built SPA      │
                      │  - /api -> upstream pool │
                      └───────────┬──────────────┘
                    round-robin   │
           ┌────────────────┬─────┴───────┬────────────────┐
           ▼                ▼              ▼
    ┌────────────┐  ┌────────────┐  ┌────────────┐
    │ backend #1 │  │ backend #2 │  │ backend #3 │   (FastAPI + uvicorn)
    └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
          └───────────────┴───────────────┘
                          ▼
                 ┌──────────────────┐
                 │  SQLite volume   │   (shared file)
                 └──────────────────┘
```

This is exactly the Module 9.3 pattern, now hosting TaskFlow. Because your auth is stateless (the JWT carries the user id), any replica can serve any request — no sticky sessions needed.

## 2. The backend Dockerfile

A small Python base, install deps, copy code, run uvicorn. We add a `HEALTHCHECK` that hits the liveness route from 10.5.

```dockerfile
# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# install deps first so this layer is cached when only code changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request as u; u.urlopen('http://localhost:8000/api/v1/health')"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

> **📝 Order layers by change frequency**
>
> Copy
>
> requirements.txt
>
> and install
>
> before
>
> copying your source. Docker caches layers; since deps change rarely, rebuilds after a code edit skip the slow
>
> pip install
>
> .

## 3. The frontend Dockerfile (multi-stage)

The frontend has two phases: **build** the static bundle with Node, then **serve** it with a tiny Nginx image. A multi-stage build throws away Node and `node_modules` from the final image — it ships only the built `dist/`.

```dockerfile
# frontend/Dockerfile
# ---- stage 1: build ----
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
# bake the API path the SPA will call (relative -> same origin via nginx)
ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# ---- stage 2: serve ----
FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
```

> **💡 Same-origin in production**
>
> In dev, the SPA called
>
> http://localhost:8000/api/v1
>
> . In production it calls
>
> /api/v1
>
> (no host) — the same Nginx that served the page proxies it to the backend. That removes CORS entirely in prod and is the standard SPA deployment shape.

## 4. Nginx: serve the SPA + load-balance the API

One Nginx config does both jobs. An `upstream` block names the backend pool; `location /api/` proxies to it (round-robin by default); everything else serves the SPA with a fallback to `index.html` (so client-side routes like `/projects/3` work on refresh).

```
# frontend/nginx.conf
upstream taskflow_api {
    server backend:8000;     # docker-compose load-balances replicas of "backend"
}

server {
    listen 80;

    # API -> backend pool
    location /api/ {
        proxy_pass http://taskflow_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Request-ID $request_id;   # trace id flows through
    }

    # SPA: serve files, fall back to index.html for client routes
    location / {
        root /usr/share/nginx/html;
        try_files $uri /index.html;
    }

    # basic hardening header (from the 10.5 pass)
    add_header X-Content-Type-Options nosniff;
}
```

The magic is `server backend:8000`: in Compose, `backend` is a service name. When you run multiple replicas, Docker's internal DNS round-robins the name across them — Nginx load-balances for free. (For explicit control you can list each replica, as you did in Module 9.3.)

## 5. docker-compose: the whole stack

Compose defines the services, the shared DB volume, env, and how many backend replicas to run.

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
    deploy:
      replicas: 3            # three identical backends
    expose:
      - "8000"              # internal only; not published to the host

  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"             # the only public entrypoint
    depends_on:
      - backend

volumes:
  taskflow_data:
```

Bring it up and scale:

```python
echo "SECRET_KEY=$(python -c 'import secrets;print(secrets.token_hex(32))')" > .env
docker compose up --build
# the app is at http://localhost
```

> **⚠️ SQLite + replicas: the honest caveat**
>
> Multiple replicas writing one SQLite file works for a demo (they share a volume), but SQLite serializes writes and isn't built for concurrent multi-process writers at scale. It's perfect for showing the architecture; the README should note "swap SQLite for Postgres to scale writes" — which is exactly what Bonus Track B.3 does.

## 6. Running migrations in containers

Tables must exist before the app serves traffic. The clean pattern is a one-shot command that runs `alembic upgrade head` on startup. A simple approach for the capstone is an entrypoint that migrates then launches uvicorn:

```bash
# backend/entrypoint.sh
#!/bin/sh
set -e
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
```

With three replicas all running this, Alembic is safe to run repeatedly — it no-ops if already at head. (In bigger systems you run migrations as a separate job; for the capstone, on-start is fine and documented.)

## 7. A CI workflow

Continuous Integration runs checks on every push. A minimal GitHub Actions workflow installs deps, runs backend tests, and builds the frontend — proving the project still builds before you merge (ties into Bonus Track B.1's GitHub Flow).

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
```

> **💡 CI is your safety net**
>
> Even this small workflow catches "it builds on my machine but not clean" — a missing dependency, a syntax error, a broken import. Green checks on a PR are what reviewers (and you, in six months) trust.

## 8. The README — your portfolio front door

A recruiter spends 30 seconds on your repo. The README is the demo. Make it sell the work:

- One-line pitch + a **screenshot or GIF** of the board near the top.
- Tech stack badges/list; the architecture diagram (section 1).
- **Run it**: `docker compose up` in three commands.
- Feature list mapped to the user stories from 10.1.
- The **Security notes** from 10.5 and the "known limits / next steps" (SQLite, refresh tokens).
- A link to the live deployment (or the Bonus Track GCP one).

> **📝 Screenshots**
>
> Take 2–3 clean screenshots (login, projects, board) and drop them in
>
> docs/
>
> ; reference them with
>
> ![Board](docs/board.png)
>
> . A picture of the working board is worth more than a paragraph.

## ✅ Recap

- A **backend Dockerfile** (cache deps first, healthcheck) and a **multi-stage frontend Dockerfile** (Node builds, Nginx serves).
- **Nginx** serves the SPA (with `try_files` fallback) and reverse-proxies `/api` to a backend **upstream pool**, load-balancing across replicas.
- **docker-compose** runs the stack, scales the backend, and shares one DB volume; **stateless JWT** makes scaling out trivial.
- Migrations run on container start; a small **CI workflow** builds/tests on every push.
- A **polished README** with screenshots turns the project into a portfolio piece.

**Next:** open `assignment.html` and ship the deployed, load-balanced TaskFlow.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
