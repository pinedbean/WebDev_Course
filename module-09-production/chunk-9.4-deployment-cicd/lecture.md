*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.4 — Deployment & CI/CD Basics

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The landscape of **deployment options** — VPS, PaaS, container hosts, cloud — and how to choose.
- How to run **database migrations in production** safely (and automatically).
- How **secrets in production** differ from your local `.env`.
- What **CI/CD** is and how to write a first **GitHub Actions** pipeline (lint → test → build).
- The real **limits of SQLite in production** and exactly when/how to move to **PostgreSQL**.

In the lab you'll add a CI workflow and an automated-migration entrypoint, then complete the 🏁 **Module 9 Checkpoint**: a documented, load-balanced, containerized deployment.

## 1. Where can this thing actually run?

You have a containerized, load-balanced stack. "Deploying" means running it on a computer that isn't yours, reachable from the internet. There's a spectrum, trading control for convenience:

| Option | What it is | Good when | Examples |
| --- | --- | --- | --- |
| **VPS** (a rented Linux box) | You SSH in, install Docker, run `docker compose up -d`. | You want full control & lowest cost; happy to manage the server. | DigitalOcean Droplet, Linode, EC2 |
| **Container host** | You hand it an image; it runs & scales containers. | You want managed scaling without babysitting a server. | Cloud Run, ECS/Fargate, Fly.io, Render |
| **PaaS** | You push code; it builds & runs everything. | Fastest path; least ops. | Railway, Render, Heroku-style |
| **Orchestrator** | Declarative clusters of containers. | Many services, large scale, a team. | Kubernetes |

The beautiful thing: because you containerized in 9.2, *all* of these are open to you with little change. A VPS literally runs your existing `docker compose up -d`. A container host wants the same image you already build. You're not locked in.

> **📝 Our path**
>
> For this module we treat a
>
> VPS-style deploy
>
> as the model (Compose on a Linux host) and
>
> simulate it locally
>
> — that's a faithful dry run. The Bonus Track then deploys the very same images to
>
> GCP Cloud Run
>
> (a managed container host) for the cloud-native version.

## 2. Running migrations in production

Your schema lives in Alembic migrations (Module 6). In development you run `alembic upgrade head` by hand. In production that has to happen *reliably*, on the right database, *before* the new code starts serving — and you don't want to SSH in to do it every deploy.

The standard pattern is a **release/entrypoint step**: run migrations as part of starting the container, before launching the server.

```bash
#!/bin/sh
# entrypoint.sh — run migrations, then start the server
set -e
alembic upgrade head
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Point your Dockerfile's `CMD` (or `ENTRYPOINT`) at this script. Now every time the container starts, the DB is brought up to date first, then the app boots. `set -e` means if the migration fails, the container fails loudly instead of serving against a wrong schema.

> **⚠️ With multiple replicas, don't migrate N times at once**
>
> If 3 replicas all start and all run
>
> alembic upgrade head
>
> simultaneously, they race. Alembic is fairly safe (migrations are transactional and it tracks the version), but the clean pattern at scale is a
>
> dedicated one-off migration job
>
> that runs once, then the replicas start. For a single-host Compose deploy, running it in one place (an entrypoint on a single migrating service, or a one-shot
>
> docker compose run api alembic upgrade head
>
> ) is fine. The principle:
>
> migrate once per release, before traffic.

## 3. Secrets in production

Locally, secrets live in a git-ignored `.env`. In production, the principle is the same — **secrets come from the environment, never the image or the repo** — but *where* the environment gets them differs:

| Place | How secrets arrive |
| --- | --- |
| VPS | A root-only `.env` on the server (mode 600), referenced by Compose; never committed. |
| CI/CD | **Encrypted repository secrets** (GitHub → Settings → Secrets), injected as env vars during the run. |
| Cloud / container hosts | A **secret manager** (GCP Secret Manager, AWS Secrets Manager, etc.) mounted as env vars at runtime. |

Rules that never change:

- **Never** bake a secret into a Docker image (anyone who pulls the image can read it) or a `VITE_` var (it ships to the browser).
- The repo holds a `.env.example` with placeholders only — documentation, not values.
- Use a **different, strong `SECRET_KEY` in production** than in dev. If a secret ever leaks (or lands in git history), **rotate it** — deleting the line doesn't undo the exposure.
- Every replica gets the *same* production `SECRET_KEY` (so JWTs verify everywhere — 9.3).

## 4. What is CI/CD?

Two related habits that turn "deploying is scary and manual" into "deploying is boring and automatic":

- **CI — Continuous Integration:** on every push/PR, automatically *check* the code — install deps, lint, run tests, build. Catch breakage before it merges.
- **CD — Continuous Delivery/Deployment:** on merge to `main`, automatically *ship* — build images, run migrations, deploy. Delivery = ready to deploy at the click of a button; Deployment = it happens automatically.

This chunk focuses on **CI** (the universally valuable half) and points at CD. The payoff: a green check on every PR means "this didn't break the build or the tests," and nobody has to remember to run things by hand.

>

## 5. A first GitHub Actions pipeline

**GitHub Actions** runs workflows defined in YAML under `.github/workflows/`. The vocabulary:

- **Workflow** — a YAML file; triggered `on` events (push, pull_request).
- **Job** — a set of steps running on a fresh virtual machine (`runs-on`).
- **Step** — one action (`uses:` a prebuilt action) or shell command (`run:`).

Here's a CI workflow that checks both halves of the Tasks app on every push and PR:

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
      - run: pip install ruff pytest
      - run: ruff check .                 # lint
      - run: pytest                       # tests
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
      - run: npm ci
      - run: npm run build                # building IS a real check
```

Two jobs run in parallel on fresh Ubuntu VMs. The backend job installs, lints with `ruff`, and runs `pytest` (note the throwaway `SECRET_KEY` from a step env — a non-secret value just to satisfy settings validation in CI). The frontend job installs and builds — and because the build is strict (9.1), a build failure catches real problems.

> **💡 The build itself is a test**
>
> Even before you have many unit tests,
>
> npm run build
>
> succeeding and the backend importing cleanly catch a surprising number of mistakes. Start there; grow the test suite over time.

> **📝 Toward CD (the next step you're ready for)**
>
> Add a job that runs only
>
> on: push: branches:[main]
>
> , builds your Docker images, pushes them to a registry, and triggers a deploy — pulling secrets from
>
> GitHub repository secrets
>
> via
>
> ${{ secrets.SECRET_KEY }}
>
> . The Bonus Track wires exactly this to GCP. The mental model is the same workflow file with one more job.

## 6. SQLite in production: the honest limits

SQLite carried you all the way here, and it's genuinely great — zero-config, fast, a single file, perfect for development and many small single-instance apps. But you hit its wall in 9.3, and it's worth naming the limits precisely:

| Limit | Why it bites in production |
| --- | --- |
| **Single writer** | Only one write at a time across the whole DB. Multiple replicas under write load → `database is locked`. |
| **It's a file, not a server** | It must live on a disk the process can open. It can't be reached over the network, so replicas on different machines can't share it. |
| **Ephemeral filesystems** | On container hosts (Cloud Run, etc.) the local disk is wiped on restart — your data would vanish without an external store. |
| **Limited concurrency tooling** | No connection pooling over a network, no role-based access at the DB layer, fewer ops features. |

### When to move to PostgreSQL

Move when any of these is true: you run **multiple instances that write**, you need the DB on a **separate/managed host**, you're on an **ephemeral filesystem**, or you have meaningful **write concurrency**. Postgres is a real client/server database built for exactly this — many concurrent writers over the network, pooling, robust tooling.

### The good news: the migration is small

Because you used **SQLAlchemy + Alembic**, the switch is mostly configuration, not a rewrite:

```bash
# 1. Install a driver
pip install "psycopg[binary]"

# 2. Change the URL (SQLite -> Postgres) via env var only
DATABASE_URL=postgresql+psycopg://user:pass@db-host:5432/tasks

# 3. Run your existing migrations against the new DB
alembic upgrade head
```

Your models, queries, routers, and the load-balanced topology are unchanged. A few SQLite-specific bits go away (the `check_same_thread` connect-arg, the WAL/foreign-key pragmas) and you'd add a real connection pool — but the shape of the app is identical. *This* is the reward for building on an ORM and migrations from the start.

> **💡 You already designed for this**
>
> Stateless JWT (replicas don't need shared session state) + an ORM + migrations + env-driven config means "scale the data tier" is a contained change. The Bonus Track does it for real with
>
> Cloud SQL (Postgres)
>
> on GCP.

## 7. The deploy runbook

Production isn't just code — it's a **documented, repeatable process**. A good runbook (you started one in 9.1) answers: how to build, what env vars are required, how to run migrations, how to start/stop, how to check health, and how to roll back. The 🏁 Checkpoint asks you to write this down, because "it only deploys when I'm at the keyboard remembering the steps" isn't a deployment — it's a liability.

## ✅ Recap

- Deployment options run from **VPS** (you manage it) to **container hosts/PaaS** (managed) — your image runs on all of them.
- Run **migrations as a release step** (entrypoint), once per release, before traffic; `set -e` so failures are loud.
- **Secrets come from the environment** — server `.env`, CI repo secrets, or a secret manager — never the image, repo, or frontend. Rotate on leak.
- **CI** checks every push (install/lint/test/build) via **GitHub Actions**; **CD** adds build-image + deploy on merge to `main`.
- **SQLite** is single-writer and file-bound; move to **Postgres** when you scale writes or need a networked/managed DB — and thanks to SQLAlchemy + Alembic, that's mostly a URL change.

**Next:** open `assignment.html`, add CI + automated migrations, and complete the 🏁 Module 9 Checkpoint.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
