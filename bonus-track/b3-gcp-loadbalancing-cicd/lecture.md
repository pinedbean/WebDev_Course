*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.3 — GCP Load Balancing, Managed Data & CI/CD

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The GCP **HTTP(S) Load Balancer** in front of Cloud Run — global anycast, health checks, autoscaling — and how it relates to the manual Nginx of Chunk 9.3.
- **HTTPS / managed TLS** certificates and mapping a **custom domain**.
- Migrating **SQLite → Cloud SQL (Postgres)** with **connection pooling**.
- Running database **migrations in the cloud**.
- **CI/CD** with Cloud Build (or GitHub Actions): build → test → deploy on every merge to `main` — tied to the Git strategy from B.1.

In the lab you'll make the B.2 deployment durable (Cloud SQL), put a managed-HTTPS load balancer in front, and add an auto-deploy pipeline — finishing the whole Bonus Track.

## 1. Prerequisites

- **B.2 complete:** TaskFlow's backend and frontend already deployed to Cloud Run in a billing-enabled project, with the `gcloud` CLI configured.
- **B.1 complete:** your TaskFlow repo follows GitHub Flow with a protected `main` — the CI/CD pipeline depends on it.
- (Optional) a **domain name** you control, if you want a custom HTTPS domain. You can finish the whole lab on the load balancer's IP without one.

> **⚠️ This chunk has the most cost risk — clean up**
>
> Cloud Run scales to zero, but a
>
> Cloud SQL instance bills continuously while it exists
>
> (even idle), and a global load-balancer forwarding rule has a small hourly cost. Use the smallest Cloud SQL tier, and
>
> delete everything
>
> at the end (the solution has a full teardown). Set a budget alert. The free tier covers most usage, but Cloud SQL is the one to watch.

## 2. The HTTP(S) Load Balancer in front of Cloud Run

In Chunk 9.3 you built load balancing *by hand*: an Nginx container with an `upstream` block round-robining across two FastAPI replicas you started yourself. You owned the Nginx config, the replica count, and the health checks. It taught you exactly what a load balancer *does*.

GCP's **HTTP(S) Load Balancer** is the managed, planet-scale version of that idea. You don't run Nginx or manage replicas — you declare the routing and Google operates the rest:

>

| Concept | Chunk 9.3 Nginx | GCP HTTP(S) LB |
| --- | --- | --- |
| Where it runs | One container you operate | Google's global edge (anycast) |
| Reach | One host/region | **Global** — one IP, served from the nearest edge worldwide |
| Backends | `upstream` list you maintain | A *backend service* pointing at a Cloud Run *serverless NEG* |
| Scaling | You start more replicas | Cloud Run autoscales; LB just routes |
| TLS | You install certs | Google-managed certificate, auto-renewed |

> **📝 Do I even need a load balancer with Cloud Run?**
>
> Cloud Run already gives you an HTTPS URL and autoscaling, so for many apps you don't strictly need a separate LB. You add one when you want a
>
> custom domain with managed TLS
>
> , a
>
> single stable global IP
>
> , path-based routing (e.g.
>
> /api
>
> → backend,
>
> /
>
> → frontend on one domain), a CDN, or Cloud Armor (WAF). That's the production setup we build here.

The LB is assembled from a few pieces: a **serverless NEG** (Network Endpoint Group that targets a Cloud Run service) → a **backend service** → a **URL map** (routing rules) → a **target HTTPS proxy** (holds the certificate) → a **global forwarding rule** (the public IP + port 443). It's verbose to wire up, but each piece maps to something you already understand from Nginx.

## 3. HTTPS, managed TLS & a custom domain

A production app should be served over **HTTPS** on a real domain, not a `*.run.app` URL. The load balancer makes this almost free of effort with a **Google-managed certificate**:

1. Reserve a **global static IP** for the load balancer.
2. In your domain registrar / DNS, point an `A` record (e.g. `app.yourdomain.com`) at that IP.
3. Create a **managed SSL certificate** for that hostname. Google validates domain ownership (via the DNS record) and issues + auto-renews the cert — no manual renewal, no Let's Encrypt cron jobs.

Add an HTTP→HTTPS redirect so visitors on `http://` are bumped to `https://`. Provisioning the certificate can take 10–60 minutes the first time (it waits for DNS to propagate and validate) — that's normal.

> **💡 No domain? You can still finish**
>
> A managed cert
>
> requires
>
> a domain you control. If you don't have one, the lab's core deliverable (LB → Cloud Run, Cloud SQL, CI/CD) is fully reachable over the LB's IP on HTTP, and you keep the per-service Cloud Run HTTPS URLs. The custom-domain + managed-TLS part is then an optional stretch.

## 4. Migrating SQLite → Cloud SQL (Postgres)

This is the fix for the problem you watched happen in B.2: SQLite's file died with the ephemeral instance. **Cloud SQL** is GCP's managed relational database — you get a real Postgres server with durable disks, automated backups, and the ability for *all* your Cloud Run instances to share *one* database.

>

### Why SQLAlchemy 2.x makes this easy

Because TaskFlow uses SQLAlchemy as its ORM, the application code barely changes — you swap the **connection URL** and the right driver:

```
# before (local SQLite)
DATABASE_URL = "sqlite:///./taskflow.db"

# after (Cloud SQL Postgres)
DATABASE_URL = "postgresql+psycopg://taskflow:PASSWORD@/taskflow?host=/cloudsql/PROJECT:REGION:INSTANCE"
```

Cloud Run connects to Cloud SQL over a secure **Unix socket** at `/cloudsql/INSTANCE_CONNECTION_NAME` (mounted when you deploy with `--add-cloudsql-instances`). No public IP, no firewall rules — the connection stays inside Google's network.

### Connection pooling — important for serverless

Postgres has a hard cap on simultaneous connections (often ~100 on small tiers). Cloud Run autoscaling can spin up many instances, and each one opening many DB connections will exhaust that cap fast. The fix is a **connection pool** with sane limits, configured in SQLAlchemy's engine:

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=5,         # connections kept open per instance
    max_overflow=2,      # extra burst connections
    pool_pre_ping=True,  # check a connection is alive before using it
    pool_recycle=1800,   # recycle conns every 30 min (avoid stale ones)
)
```

Keep `pool_size` small *per instance*: many small pools across many instances add up. `pool_pre_ping` avoids the classic "server closed the connection unexpectedly" error when an idle connection was dropped.

## 5. Running migrations in the cloud

A fresh Cloud SQL database is empty — it has no tables. Your schema lives in **Alembic migrations** (from Module 6). You must run them against the cloud database *before* the app serves traffic. The safe options:

| Approach | How | When |
| --- | --- | --- |
| **Cloud SQL Auth Proxy** from your laptop | Run the proxy locally, point `alembic upgrade head` at `127.0.0.1`. | One-off / manual migrations. Simplest to start. |
| **A migration step in CI/CD** | A Cloud Build step (or a one-shot Cloud Run Job) runs `alembic upgrade head` on each deploy, before routing traffic. | Automated, repeatable. The production pattern. |

> **⚠️ Don't auto-create tables in app startup for prod**
>
> It's tempting to call
>
> Base.metadata.create_all()
>
> on startup. That works once but can't evolve a schema safely and races across multiple instances. Use
>
> Alembic migrations
>
> run as a deliberate, single step — never let N autoscaled instances all try to migrate at once.

The **Cloud SQL Auth Proxy** is a small binary that opens an authenticated local tunnel to your instance, so tools that expect a normal `host:port` (like Alembic) just work:

```bash
# terminal 1: start the proxy (uses your gcloud credentials)
cloud-sql-proxy PROJECT:REGION:INSTANCE --port 5432

# terminal 2: run migrations against the tunnel
export DATABASE_URL="postgresql+psycopg://taskflow:PASSWORD@127.0.0.1:5432/taskflow"
alembic upgrade head
```

## 6. CI/CD: build → test → deploy on every merge

Right now you deploy by typing `gcloud run deploy` by hand. **CI/CD** automates that: when code is merged to `main`, a pipeline automatically builds the image, runs tests, and (if green) deploys it. This is where B.1 pays off — **only reviewed, protected `main` ever deploys**.

>

Two common ways to do this on GCP:

### Option A — Cloud Build (GCP-native)

A `cloudbuild.yaml` in your repo defines steps; a Cloud Build **trigger** watches your GitHub repo and runs it on every push to `main`. Everything stays inside GCP.

```yaml
# cloudbuild.yaml
steps:
  # 1. build the backend image
  - name: gcr.io/cloud-builders/docker
    args: ['build', '-t',
           '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA',
           './backend']

  # 2. run tests inside the image
  - name: '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA'
    entrypoint: pytest
    args: ['-q']

  # 3. push the image
  - name: gcr.io/cloud-builders/docker
    args: ['push',
           '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA']

  # 4. run DB migrations, then deploy
  - name: gcr.io/google.com/cloudsdktool/cloud-sdk
    entrypoint: gcloud
    args: ['run', 'deploy', 'taskflow-backend',
           '--image', '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA',
           '--region', '$_REGION', '--quiet']

substitutions:
  _REGION: asia-southeast1
images:
  - '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA'
```

`$SHORT_SHA` and `$PROJECT_ID` are built-in substitutions Cloud Build fills in; tagging images by commit SHA gives you an exact, rollback-able record of what's deployed.

### Option B — GitHub Actions (deploys to GCP)

If your team lives in GitHub, a workflow file does the same job and keeps CI next to your PRs. It authenticates to GCP (ideally via **Workload Identity Federation** — keyless — rather than a downloaded service-account JSON), then builds and deploys.

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]          # only main — protected by B.1 rules

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write          # for keyless auth to GCP
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.DEPLOY_SA }}
      - uses: google-github-actions/setup-gcloud@v2
      - run: |
          gcloud builds submit --tag \
            "$REGION-docker.pkg.dev/$PROJECT/taskflow/backend:$GITHUB_SHA" ./backend
          gcloud run deploy taskflow-backend \
            --image "$REGION-docker.pkg.dev/$PROJECT/taskflow/backend:$GITHUB_SHA" \
            --region "$REGION" --quiet
        env:
          PROJECT: ${{ secrets.GCP_PROJECT }}
          REGION: asia-southeast1
```

> **⚠️ Don't commit a service-account key**
>
> The old way — downloading a JSON key and storing it as a secret — is a liability (it's a long-lived credential that can leak, exactly the B.1 "secrets in history" risk). Prefer
>
> Workload Identity Federation
>
> , which lets GitHub mint short-lived tokens with no stored key. If you must use a key, store it in GitHub Encrypted Secrets, never in the repo.

Either option, the principle is the same and it closes the loop with B.1: a developer opens a PR, it's reviewed and CI-checked, it squash-merges into a protected `main`, and *that merge* is the only thing that ships to production. No more manual deploys, no "works on my machine".

## ✅ Recap

- The GCP **HTTP(S) Load Balancer** is the managed, global version of Chunk 9.3's Nginx: serverless NEG → backend service → URL map → HTTPS proxy → forwarding rule.
- A **Google-managed TLS certificate** + a DNS `A` record gives you HTTPS on a custom domain, auto-renewed.
- **Cloud SQL Postgres** replaces SQLite for durable, shared data; SQLAlchemy just needs a new URL + a small **connection pool**.
- Run **Alembic migrations** deliberately (via the Cloud SQL Auth Proxy or a pipeline step) — never auto-create on startup in prod.
- **CI/CD** (Cloud Build or GitHub Actions) builds, tests, and deploys on every merge to `main` — and B.1's branch protection ensures only reviewed, green `main` ships.

**Next:** open `assignment.html` and assemble the full cloud-native deployment — then finish the Bonus Track. 🏁

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
