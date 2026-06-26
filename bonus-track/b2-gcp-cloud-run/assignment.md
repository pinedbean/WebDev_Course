*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.2 — Lab: TaskFlow Live on Cloud Run

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Get TaskFlow running on Google Cloud. You'll create a project, enable APIs, push both container images to Artifact Registry, deploy the **backend** and **frontend** to Cloud Run, wire up env vars and a JWT secret via Secret Manager, and finish by loading your **live public URL** in a browser.

## Prerequisites

- **Module 9 done:** a containerized TaskFlow with working Dockerfiles for backend (FastAPI, port 8000) and frontend (Vite build served by Nginx).
- A **Google Cloud account with billing enabled**. (New accounts get sign-up credit.)
- **`gcloud` CLI** installed (`gcloud --version`) and **Docker** running.

> **⚠️ This may cost a little — and you must clean up**
>
> Most of this lab fits in the free tier and Cloud Run scales to zero when idle, but Artifact Registry storage and build minutes can incur small charges.
>
> Do the teardown
>
> at the end of the solution to avoid lingering costs, and set a budget alert. Treat your billing account as real money.

## Tasks

### 1 Authenticate & create a project

Run `gcloud auth login` (opens a browser in *your* terminal). Create a new project (e.g. `taskflow-prod-XXXX`), set it as your default, link it to your billing account, and set a default region near you (e.g. `asia-southeast1`). Confirm with `gcloud config list`.

### 2 Enable the APIs you'll use

Enable Cloud Run, Artifact Registry, Secret Manager, and Cloud Build on the project in one command. This is a one-time toggle per service.

### 3 Create an Artifact Registry repo

Create a Docker-format repository named `taskflow` in your region. Configure Docker auth so you can push to `REGION-docker.pkg.dev`.

### 4 Build & push the backend image

Build the backend image **for linux/amd64** (or let Cloud Build build it) and push it to your Artifact Registry repo, tagged `backend:1.0.0`.

> **💡 Easiest path**
>
> gcloud builds submit --tag REGION-docker.pkg.dev/PROJECT/taskflow/backend:1.0.0 .
>
> builds in the cloud and pushes for you — no local arch headaches. The solution shows both this and the local-Docker route.

### 5 Store the JWT secret in Secret Manager

Generate a strong random value and store it as a secret named `jwt-secret` (pipe it in — don't type it as a plain argument). Grant Cloud Run's service account permission to read it.

### 6 Deploy the backend to Cloud Run

Deploy `taskflow-backend` from the pushed image: port 8000, `--allow-unauthenticated`, `ENV=production` as an env var, and `JWT_SECRET` mounted from the `jwt-secret` secret. **Copy the service URL** it prints. Hit `/health` in your browser to confirm it's live.

### 7 Build & deploy the frontend (pointed at the backend URL)

Build the frontend image with `VITE_API_URL` set to the backend's Cloud Run URL (remember: Vite bakes this in at **build time**), push it, and deploy `taskflow-frontend` to Cloud Run (port 80, allow-unauthenticated).

### 8 Fix CORS & open your live app

Update the backend's `CORS_ORIGINS` env var to include the frontend's Cloud Run URL and redeploy. Open the **frontend URL** in your browser, register a user, create a project and a task. You're live on the cloud. 🎉

### 9 Observe the SQLite limitation (then plan the fix)

Note that with SQLite on Cloud Run, data can disappear when the service scales to zero or scales out to a second instance. Write one sentence in your notes about *why* — this is exactly what B.3's Cloud SQL migration fixes.

## ✅ Deliverable — acceptance checklist

- A GCP project exists, is linked to billing, with Run / Artifact Registry / Secret Manager / Cloud Build APIs enabled.
- An Artifact Registry repo `taskflow` contains a `backend` and a `frontend` image.
- A `jwt-secret` exists in Secret Manager and Cloud Run can read it.
- `taskflow-backend` is deployed; `/health` returns OK at its `*.run.app` URL.
- `taskflow-frontend` is deployed and reachable at its own `*.run.app` URL.
- The frontend was built with `VITE_API_URL` = the backend URL, and CORS allows the frontend origin.
- You can register, log in, and create a project/task through the live public URL.
- You can explain why SQLite is a problem here and what fixes it (Cloud SQL).

## 🚀 Stretch goals (optional)

- Set `--min-instances=0 --max-instances=3` and a `--memory`/`--cpu` limit; observe cold starts.
- Set a **budget alert** in Billing so you're emailed if spend crosses a threshold.
- View live logs with `gcloud run services logs read taskflow-backend`.
- Add a second secret (e.g. an API key) and confirm it mounts as an env var.
- Add a custom env var to disable Swagger docs in production.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
