*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.3 — Lab: Durable, Load-Balanced, Auto-Deploying TaskFlow

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Take the B.2 deployment to production grade. You'll provision a **Cloud SQL Postgres** instance and point TaskFlow at it (so data survives), run migrations in the cloud, put a **global HTTPS load balancer** in front, and add a **CI/CD pipeline** that auto-deploys on every merge to `main` — tied to the Git strategy you set up in B.1. This finishes the Bonus Track.

## Prerequisites

- **B.2 complete:** TaskFlow backend + frontend live on Cloud Run; `gcloud` configured with your project + region.
- **B.1 complete:** TaskFlow repo on GitHub using GitHub Flow with a protected `main`.
- **Alembic migrations** exist for your schema (from Module 6 / Module 10).
- (Optional) a domain you control, for the custom-domain + managed-TLS step.

> **⚠️ Cost watch — Cloud SQL bills while it exists**
>
> Unlike Cloud Run, a Cloud SQL instance and a load-balancer forwarding rule cost money
>
> continuously
>
> , even idle. Use the smallest tier, and run the
>
> full teardown
>
> in the solution the moment you've demoed it. Set a budget alert first.

## Tasks

### 1 Provision Cloud SQL (Postgres)

Enable the Cloud SQL Admin API. Create the smallest Postgres instance in your region, create a `taskflow` database and a `taskflow` user with a strong password, and store that password in **Secret Manager**.

### 2 Point the backend at Postgres + add pooling

Update the backend to read a Postgres `DATABASE_URL` (driver `postgresql+psycopg`) and configure a small SQLAlchemy **connection pool** (`pool_size`, `max_overflow`, `pool_pre_ping`). Commit on a feature branch via your B.1 workflow.

### 3 Run migrations against the cloud DB

Use the **Cloud SQL Auth Proxy** to tunnel to the instance from your machine and run `alembic upgrade head` so the tables exist in Postgres.

### 4 Redeploy the backend connected to Cloud SQL

Redeploy `taskflow-backend` with `--add-cloudsql-instances`, the Postgres `DATABASE_URL` env var, and the DB password mounted from Secret Manager. Verify data now **persists** across a redeploy / scale-to-zero (the thing that failed in B.2).

### 5 Put an HTTP(S) Load Balancer in front

Reserve a global static IP, create a **serverless NEG** targeting your Cloud Run service, then a backend service → URL map → target proxy → forwarding rule. Confirm traffic reaches TaskFlow through the load balancer's IP.

### 6 Add HTTPS + a custom domain (optional if you have one)

Point a DNS `A` record at the static IP, create a **Google-managed SSL certificate** for that hostname, attach it to an HTTPS target proxy, and add an HTTP→HTTPS redirect. Wait for the cert to go `ACTIVE`, then load `https://your-domain`.

### 7 Wire up CI/CD (auto-deploy on merge to `main`)

Add either a `cloudbuild.yaml` + Cloud Build trigger **or** a `.github/workflows/deploy.yml` GitHub Actions workflow that builds, tests, and deploys to Cloud Run on every push to `main`. Use keyless auth (Workload Identity Federation) if using GitHub Actions.

### 8 Prove the loop: PR → merge → auto-deploy

Make a small visible change (e.g. a footer version string) on a **feature branch**, open a PR, get it through your B.1 review/branch-protection, squash-merge to `main`, and watch the pipeline deploy it automatically. Confirm the change is live.

### 9 Tear down (after you've demoed)

Run the full cleanup in the solution: delete the load-balancer pieces, the Cloud SQL instance, the Cloud Run services, and secrets — or delete the whole project. Confirm in Billing that nothing is still running.

## ✅ Deliverable — acceptance checklist

- A Cloud SQL Postgres instance + `taskflow` DB and user exist; the password is in Secret Manager.
- The backend connects via `postgresql+psycopg` with a configured connection pool.
- Alembic migrations ran against Cloud SQL; tables exist.
- The redeployed backend uses Cloud SQL and data **persists** across redeploys / scale-to-zero.
- A global HTTP(S) Load Balancer routes public traffic to the Cloud Run service.
- (If domain) A managed TLS cert is `ACTIVE` and the app loads over `https://your-domain` with HTTP→HTTPS redirect.
- A CI/CD pipeline (Cloud Build or GitHub Actions) builds, tests, and deploys on merge to `main`.
- A PR merged to `main` auto-deployed and the change is visibly live.
- Resources were cleaned up (or the project deleted) to stop charges.

## 🚀 Stretch goals (optional)

- Add a **migration step** to the pipeline so `alembic upgrade head` runs automatically before each deploy (via a Cloud Run Job).
- Enable **Cloud SQL automated backups** + point-in-time recovery and note the retention window.
- Put the **frontend behind the same load balancer** with path routing: `/api/*` → backend, `/*` → frontend, one domain.
- Add **Cloud Armor** (a basic WAF rule) or Cloud CDN to the backend service.
- Add a deploy **rollback** note: how to shift traffic back to the previous Cloud Run revision.

## 🏁 Bonus Track Complete

When the checklist is green you've built a **cloud-native deployment story you can demo and defend in interviews**: an auto-deploying, load-balanced TaskFlow on GCP with a managed Postgres database and HTTPS. You took it from "runs on my machine" (Module 9) to "ships like a real team does":

- **B.1** — a professional Git strategy: branches, PRs, review, protected `main`, SemVer releases.
- **B.2** — containers on Cloud Run with Artifact Registry + Secret Manager.
- **B.3** — managed data (Cloud SQL), global HTTPS load balancing, and CI/CD where *every reviewed merge to `main` auto-ships*.

The solution page has the exact commands, config files, and the all-important teardown. Go finish it. 🚀

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
