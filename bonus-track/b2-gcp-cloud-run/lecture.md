*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.2 — Deploy the Capstone to GCP (Cloud Run)

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- GCP fundamentals: **projects**, **billing**, **IAM**, and **regions**.
- The **`gcloud` CLI** — how you drive GCP from the terminal.
- **Artifact Registry** — where your container images live in the cloud.
- **Cloud Run** — serverless containers with autoscaling, scale-to-zero, and request-based billing.
- How to map TaskFlow's **backend** and **frontend** to Cloud Run services.
- **Environment variables** & **Secret Manager** for config and secrets.
- Why **SQLite breaks in the cloud** (ephemeral filesystems) and the path to **Cloud SQL (Postgres)**.

In the lab you'll push TaskFlow's images to Artifact Registry and deploy both services to Cloud Run, ending with a live public URL.

## 1. Prerequisites & honest expectations

This chunk picks up exactly where Module 9 left off: a **containerized TaskFlow** (Dockerfiles for backend + frontend, load-balanced locally behind Nginx). We're going to take those same images and run them on Google Cloud.

**You need:**

- The containerized capstone from **Module 9** (working `docker build` for both services).
- A **Google Cloud account with billing enabled** (a credit card is required to verify, even for the free tier).
- The **`gcloud` CLI** installed locally and **Docker** running.

> **⚠️ Costs & the free tier — read this**
>
> Cloud Run has a generous
>
> free tier
>
> (millions of requests/month) and
>
> scales to zero
>
> , so an idle service costs ~nothing. But Artifact Registry storage, Cloud Build minutes, and (in B.3) Cloud SQL can incur
>
> small charges
>
> . Most of this lab stays within the free tier, but you should treat your billing account as real money.
>
> Always clean up at the end
>
> (the solution has a teardown section) and set a budget alert. New accounts also get a sign-up credit that covers experimentation comfortably.

## 2. GCP fundamentals

Four concepts unlock everything else:

| Concept | What it is | TaskFlow mapping |
| --- | --- | --- |
| **Project** | The top-level container for all your resources, billing, and permissions. Everything lives inside a project, identified by a globally-unique *Project ID*. | One project, e.g. `taskflow-prod`. |
| **Billing account** | The payment method linked to projects. A project must be linked to an active billing account to use most services. | Your personal billing account. |
| **IAM** | Identity & Access Management — *who* (users, service accounts) can do *what* (roles) on *which* resource. Cloud Run uses a *service account* identity to access other services. | Your user is Owner; services run as a service account. |
| **Region** | A geographic location (e.g. `asia-southeast1` = Singapore, `us-central1` = Iowa) where your service runs. Pick one near your users; keep all services + DB in the *same* region. | One region for everything. |

> **💡 Project ID vs project name**
>
> The
>
> Project ID
>
> (e.g.
>
> taskflow-prod-471203
>
> ) is permanent and globally unique — it appears in URLs and commands. The
>
> name
>
> is just a label you can change. GCP often appends random digits to make the ID unique; that's normal.

## 3. The `gcloud` CLI

`gcloud` is Google Cloud's command-line tool — the terminal equivalent of clicking around the web console. You authenticate once, set a default project and region, then drive everything from the shell. The interactive login opens a browser *in your own terminal*:

```javascript
gcloud auth login                       # opens a browser to sign in
gcloud config set project taskflow-prod  # default project for later commands
gcloud config set run/region asia-southeast1
gcloud auth configure-docker asia-southeast1-docker.pkg.dev   # let Docker push to Artifact Registry
```

Each GCP service must be **enabled** on the project before use (this is a one-time toggle per API):

```bash
gcloud services enable run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com
```

> **📝 Two ways to do everything**
>
> Almost anything you do with
>
> gcloud
>
> can also be done in the web Console (console.cloud.google.com). We teach the CLI because it's
>
> reproducible
>
> — you can script it, paste it into a PR, and (in B.3) run it from CI. The Console is great for browsing and debugging.

## 4. Artifact Registry — where images live

Your Docker images currently live on your laptop. The cloud can't run them from there — they need to be in a **container registry** the cloud can pull from. On GCP that's **Artifact Registry**: a private, regional store for your images (the successor to the older Container Registry).

>

You create a **repository** once, then tag your local image with its full registry path and push:

```bash
# create the repo (once)
gcloud artifacts repositories create taskflow \
  --repository-format=docker --location=asia-southeast1

# the full image path pattern:
# REGION-docker.pkg.dev/PROJECT_ID/REPO/IMAGE:TAG
docker tag taskflow-backend \
  asia-southeast1-docker.pkg.dev/taskflow-prod/taskflow/backend:1.0.0
docker push \
  asia-southeast1-docker.pkg.dev/taskflow-prod/taskflow/backend:1.0.0
```

> **⚠️ Build for the right CPU architecture**
>
> If you're on an Apple Silicon Mac (M-series), your local
>
> docker build
>
> produces
>
> arm64
>
> images, but Cloud Run runs
>
> amd64 (x86-64)
>
> . Either build with
>
> docker build --platform linux/amd64 ...
>
> , or skip local building entirely and let Cloud Build build in the cloud (shown in the lab) — it always targets the correct architecture.

## 5. Cloud Run — serverless containers

**Cloud Run** takes a container image and runs it as a fully-managed web service. You don't manage servers, VMs, or clusters — you hand Google an image and a port, and you get back an HTTPS URL. It's the simplest way to put a Dockerized app on the internet.

The key behaviors that make it ideal for TaskFlow:

| Feature | What it means |
| --- | --- |
| **Autoscaling** | Cloud Run spins up more container instances as traffic rises and removes them as it falls — automatically. This is the managed equivalent of the manual Nginx replicas you ran in Chunk 9.3. |
| **Scale to zero** | With no traffic, it scales down to *zero* instances — you pay nothing while idle. The first request after idle incurs a "cold start" (a second or two to boot a container). |
| **Request-based billing** | You're billed for CPU/memory only *while a request is being handled*, rounded to the nearest 100 ms — not for idle time. |
| **Stateless & HTTPS by default** | Each instance is ephemeral and gets no guaranteed disk; every service gets a free HTTPS `*.run.app` URL. |

Because TaskFlow uses **stateless JWT auth** (no server-side sessions), it scales horizontally cleanly — any instance can serve any request, exactly the property that made Nginx round-robin work in Module 9. Cloud Run just automates the scaling.

```bash
gcloud run deploy taskflow-backend \
  --image asia-southeast1-docker.pkg.dev/taskflow-prod/taskflow/backend:1.0.0 \
  --region asia-southeast1 \
  --port 8000 \
  --allow-unauthenticated      # public web service (vs internal-only)
```

That command returns a URL like `https://taskflow-backend-abc123-as.a.run.app`. Done — your API is on the internet, behind Google's HTTPS, autoscaling.

## 6. Mapping TaskFlow to Cloud Run

TaskFlow is two containers, so it becomes **two Cloud Run services**:

>

- **Backend** — the FastAPI image listening on `:8000`, exposing `/api/v1/*` and `/health`. Deploy first so you know its URL.
- **Frontend** — the Vite build served by Nginx. It needs to know the backend's URL. Vite bakes `VITE_*` variables in *at build time*, so the backend URL must be passed as a build arg/env when the frontend image is built — not at deploy time.

> **💡 The build-time gotcha**
>
> Frontend env vars (
>
> VITE_API_URL
>
> ) are compiled into the static JS during
>
> npm run build
>
> . Backend env vars are read at
>
> runtime
>
> . So: build the backend → deploy it → grab its URL → build the frontend with that URL → deploy the frontend.

## 7. Environment variables & Secret Manager

Your backend needs config: the JWT signing secret, the database URL, allowed CORS origins. Two kinds:

- **Non-secret config** (e.g. `ENV=production`, `CORS_ORIGINS=https://...`) → plain Cloud Run env vars via `--set-env-vars`.
- **Secrets** (JWT secret, DB password) → **Secret Manager**, a dedicated, access-controlled vault. You store the value once, then mount it into Cloud Run by reference — the secret value never appears in your deploy command, your shell history, or your repo.

```bash
# store a secret (value piped in, not typed as an argument)
printf '%s' "$(openssl rand -hex 32)" | \
  gcloud secrets create jwt-secret --data-file=-

# reference it from Cloud Run as an env var
gcloud run deploy taskflow-backend \
  --image ... \
  --set-env-vars ENV=production \
  --set-secrets JWT_SECRET=jwt-secret:latest
```

The service account that Cloud Run runs as needs the *Secret Manager Secret Accessor* role to read it — an IAM grant you do once. This is the production-grade way to handle the secrets you've been keeping in a local `.env` file.

> **⚠️ Never put secrets in the image or in Git**
>
> Don't bake secrets into a Dockerfile or commit them. Anyone who pulls the image or clones the repo would get them. Secret Manager keeps the value out of both — exactly the "keep secrets out of history" rule from B.1, applied in the cloud.

## 8. The SQLite-in-the-cloud problem

TaskFlow uses SQLite — a single file on disk. That's perfect locally, but it collides with two facts about Cloud Run:

1. **The filesystem is ephemeral.** Each instance gets a fresh, in-memory scratch disk that *vanishes* when the instance scales down. Any data SQLite wrote disappears — your users' tasks would evaporate the moment the service idles.
2. **Instances don't share a disk.** Autoscaling runs multiple instances; each would have its own separate SQLite file, so two users could hit two different "databases". SQLite's single-writer model also fights concurrent instances.

>

The fix is a **managed database** that lives *outside* the containers and is shared by all instances. On GCP that's **Cloud SQL (Postgres)**: durable storage, real concurrent writes, automated backups. The application code barely changes — SQLAlchemy 2.x just needs a Postgres connection URL instead of a SQLite one.

> **📝 For this chunk: ship it, then fix it properly**
>
> To get a
>
> live URL today
>
> , B.2 deploys with SQLite so you see the full pipeline end-to-end (and you'll observe the data-loss limitation first-hand).
>
> Chunk B.3 migrates to Cloud SQL Postgres
>
> for durable, shared data. This mirrors how real projects evolve: ship the thin slice, then harden it.

## ✅ Recap

- GCP organizes everything under a **project** with a **billing account**, governed by **IAM**, running in a **region**.
- `gcloud` drives GCP from the terminal; you enable each API once and set a default project + region.
- **Artifact Registry** stores your images; build for **amd64** so Cloud Run can run them.
- **Cloud Run** runs a container as an autoscaling, scale-to-zero, HTTPS web service billed per request.
- TaskFlow = two services; the frontend bakes `VITE_API_URL` at *build* time, the backend reads env vars at *runtime*.
- **Secret Manager** holds secrets; non-secret config goes in env vars.
- **SQLite breaks** on Cloud Run's ephemeral, unshared disks → B.3 moves to **Cloud SQL Postgres**.

**Next:** open `assignment.html` and deploy TaskFlow to Cloud Run.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
