*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Continue from your B.2 deployment. Reuse (or re-export) these shell variables; add the new ones for this chunk:

```bash
export PROJECT=$(gcloud config get-value project)
export REGION=asia-southeast1
export REG=$REGION-docker.pkg.dev/$PROJECT/taskflow
export INSTANCE=taskflow-db                 # Cloud SQL instance name
export CONNNAME=$PROJECT:$REGION:$INSTANCE   # Cloud SQL "connection name"
```

> **⚠️ Cloud SQL is billing now — set a budget & plan to delete**
>
> The instance you create in step 1 costs money continuously until you delete it. Use the smallest tier, set a budget alert, and run the teardown (bottom of page) as soon as you've demoed.

### 1 Provision Cloud SQL (Postgres)

```javascript
gcloud services enable sqladmin.googleapis.com

# smallest tier, smallest disk; pick a strong root password
gcloud sql instances create $INSTANCE \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=$REGION \
  --storage-size=10GB

gcloud sql databases create taskflow --instance=$INSTANCE

# app user + password stored in Secret Manager (not typed in plain commands)
export DBPASS=$(openssl rand -base64 24)
gcloud sql users create taskflow --instance=$INSTANCE --password="$DBPASS"
printf '%s' "$DBPASS" | gcloud secrets create db-password --data-file=-

# let Cloud Run's service account read it
export PROJNUM=$(gcloud projects describe $PROJECT --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding db-password \
  --member="serviceAccount:$PROJNUM-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

Find the connection name to confirm `$CONNNAME`:

```bash
gcloud sql instances describe $INSTANCE --format='value(connectionName)'
# taskflow-prod-12345:asia-southeast1:taskflow-db
```

### 2 Point the backend at Postgres + add pooling

On a feature branch (B.1 workflow), make sure the Postgres driver is a dependency and the engine reads `DATABASE_URL` with a small pool. In `requirements.txt`:

```
sqlalchemy>=2.0
psycopg[binary]>=3.1
```

In your DB setup module:

```python
import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ["DATABASE_URL"]   # set per-environment

connect_args = {}
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=2,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args=connect_args,
)
```

The Cloud Run connection string uses the Unix socket (no host/port):

```
postgresql+psycopg://taskflow:PASSWORD@/taskflow?host=/cloudsql/PROJECT:REGION:INSTANCE
```

```bash
git switch -c feature/postgres-support
git add backend/requirements.txt backend/app/db.py
git commit -m "feat(db): support postgres via DATABASE_URL with connection pooling"
git push -u origin feature/postgres-support
gh pr create --base main --fill
```

### 3 Run migrations against the cloud DB

Download the **Cloud SQL Auth Proxy** (one binary), start the tunnel, and run Alembic against it:

```bash
# terminal 1 — start the proxy (uses your gcloud creds)
cloud-sql-proxy $CONNNAME --port 5432

# terminal 2 — run migrations through the tunnel
cd backend
export DATABASE_URL="postgresql+psycopg://taskflow:$DBPASS@127.0.0.1:5432/taskflow"
alembic upgrade head
```

Expected: Alembic prints each revision applied, ending at `head`. Verify the tables:

```bash
gcloud sql connect $INSTANCE --user=taskflow --database=taskflow
# at the psql prompt:
\dt
# users | projects | memberships | tasks ...
```

> **📝 macOS install of the proxy**
>
> brew install cloud-sql-proxy
>
> (or download the release binary). On Linux/Windows grab the matching binary from the Cloud SQL Auth Proxy releases. Authentication uses your existing
>
> gcloud auth
>
> — the tunnel opens in your own terminal.

### 4 Redeploy the backend connected to Cloud SQL

```bash
gcloud run deploy taskflow-backend \
  --image $REG/backend:1.0.0 \
  --region $REGION \
  --port 8000 \
  --allow-unauthenticated \
  --add-cloudsql-instances $CONNNAME \
  --set-env-vars ENV=production \
  --set-env-vars "DATABASE_URL=postgresql+psycopg://taskflow:PLACEHOLDER@/taskflow?host=/cloudsql/$CONNNAME" \
  --set-secrets JWT_SECRET=jwt-secret:latest \
  --update-secrets DB_PASSWORD=db-password:latest
```

> **💡 Keep the password out of the URL**
>
> Cleanest pattern: mount the password as the
>
> DB_PASSWORD
>
> secret and have the app assemble
>
> DATABASE_URL
>
> from
>
> DB_PASSWORD
>
> + the socket path at startup, so no secret ever sits in an env var string. If you inline it in
>
> DATABASE_URL
>
> instead, build that value from the mounted secret — never paste the literal password into the command.

**Prove persistence:** create a task, then force a new revision and reload:

```bash
gcloud run services update taskflow-backend --region $REGION \
  --update-env-vars TOUCH=$RANDOM
# log back in — your task is STILL THERE. Cloud SQL fixed the B.2 data loss. ✅
```

### 5 Put an HTTP(S) Load Balancer in front of Cloud Run

Build the LB from its pieces. Each maps to a Chunk 9.3 Nginx concept (NEG≈upstream, backend service≈the proxy block, URL map≈location routing).

```bash
gcloud services enable compute.googleapis.com

# 1. global static IP
gcloud compute addresses create taskflow-ip --global
export LB_IP=$(gcloud compute addresses describe taskflow-ip --global --format='value(address)')
echo $LB_IP

# 2. serverless NEG targeting the Cloud Run service
gcloud compute network-endpoint-groups create taskflow-neg \
  --region=$REGION \
  --network-endpoint-type=serverless \
  --cloud-run-service=taskflow-backend

# 3. backend service + attach the NEG
gcloud compute backend-services create taskflow-bes --global
gcloud compute backend-services add-backend taskflow-bes \
  --global \
  --network-endpoint-group=taskflow-neg \
  --network-endpoint-group-region=$REGION

# 4. URL map → backend service
gcloud compute url-maps create taskflow-urlmap --default-service=taskflow-bes
```

For a quick HTTP check before adding TLS:

```bash
gcloud compute target-http-proxies create taskflow-http-proxy --url-map=taskflow-urlmap
gcloud compute forwarding-rules create taskflow-http-rule \
  --global --target-http-proxy=taskflow-http-proxy \
  --address=taskflow-ip --ports=80
# wait a few minutes, then:
curl http://$LB_IP/health      # routed through the global LB to Cloud Run
```

### 6 Add HTTPS + a custom domain

Requires a domain you control. Point DNS, then attach a Google-managed cert:

```bash
# in your DNS provider: create an A record
#   app.yourdomain.com  ->  $LB_IP

gcloud compute ssl-certificates create taskflow-cert \
  --domains=app.yourdomain.com --global

gcloud compute target-https-proxies create taskflow-https-proxy \
  --url-map=taskflow-urlmap \
  --ssl-certificates=taskflow-cert

gcloud compute forwarding-rules create taskflow-https-rule \
  --global --target-https-proxy=taskflow-https-proxy \
  --address=taskflow-ip --ports=443
```

Watch the cert until it's `ACTIVE` (can take 10–60 min while DNS validates):

```bash
gcloud compute ssl-certificates describe taskflow-cert --global \
  --format='value(managed.status)'
# PROVISIONING ... then ACTIVE
```

Add an HTTP→HTTPS redirect so port 80 bumps users to 443 (create a tiny redirect URL map and point the existing HTTP proxy at it). Once `ACTIVE`, open `https://app.yourdomain.com`. 🔒

> **📝 No domain?**
>
> Skip step 6. Your deliverable is still met by the LB IP over HTTP (step 5) plus the Cloud Run HTTPS URLs. The managed-cert path is the only part that needs a real domain.

### 7 Wire up CI/CD

Pick one. **Option A — Cloud Build**. Commit `cloudbuild.yaml` at the repo root:

```yaml
steps:
  - name: gcr.io/cloud-builders/docker
    args: ['build','-t','$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA','./backend']
  - name: '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA'
    entrypoint: pytest
    args: ['-q']
  - name: gcr.io/cloud-builders/docker
    args: ['push','$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA']
  - name: gcr.io/google.com/cloudsdktool/cloud-sdk
    entrypoint: gcloud
    args: ['run','deploy','taskflow-backend',
           '--image','$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA',
           '--region','$_REGION','--quiet']
substitutions:
  _REGION: asia-southeast1
images:
  - '$_REGION-docker.pkg.dev/$PROJECT_ID/taskflow/backend:$SHORT_SHA'
```

Create a trigger that runs it on pushes to `main` (connect your GitHub repo first when prompted, in your browser):

```bash
gcloud builds triggers create github \
  --name=taskflow-deploy \
  --repo-name=taskflow --repo-owner=YOUR-USER \
  --branch-pattern='^main$' \
  --build-config=cloudbuild.yaml
```

**Option B — GitHub Actions**. Commit `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
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

> **⚠️ Use keyless auth**
>
> For GitHub Actions, set up
>
> Workload Identity Federation
>
> and reference it via
>
> secrets.WIF_PROVIDER
>
> /
>
> secrets.DEPLOY_SA
>
> — don't download and commit a service-account JSON key. That's the B.1 "no secrets in the repo" rule enforced in CI.

### 8 Prove the loop: PR → merge → auto-deploy

```bash
git switch main && git pull origin main
git switch -c feature/footer-version
# edit the frontend footer to show e.g. "TaskFlow v1.1"
git commit -am "feat(ui): show version in footer"
git push -u origin feature/footer-version
gh pr create --base main --fill
# review (B.1), then:
gh pr merge --squash --delete-branch
```

The merge to protected `main` triggers the pipeline. Watch it:

```bash
# Cloud Build:
gcloud builds list --limit=1
# or GitHub Actions: the "Actions" tab on your repo
```

When it finishes, reload the app — your footer change is live, deployed entirely by the pipeline. **That's the whole point: a reviewed merge to `main` shipped to production with zero manual steps.**

## 📄 Quick reference — what you built

```
Cloud SQL Postgres   →  durable, shared DB (alembic upgrade head)
       ▲
Cloud Run backend    →  --add-cloudsql-instances, pooled SQLAlchemy
       ▲  serverless NEG
HTTP(S) Load Balancer →  global IP, managed TLS, custom domain
       ▲
Users (https)

CI/CD:  PR → review → squash-merge to protected main → build → test → deploy
```

## 🛠️ Troubleshooting

| Symptom | Fix |
| --- | --- |
| Backend logs: `could not connect to server` / socket error | Missing `--add-cloudsql-instances $CONNNAME` on deploy, or `DATABASE_URL` host isn't `/cloudsql/$CONNNAME`. Both must match the instance connection name. |
| `remaining connection slots are reserved` / too many connections | Pool too large × many instances. Lower `pool_size`/`max_overflow`, or cap `--max-instances` on Cloud Run. |
| `server closed the connection unexpectedly` | Stale pooled connection. Ensure `pool_pre_ping=True` and a sensible `pool_recycle`. |
| Alembic: `relation "alembic_version" does not exist` | First run — that's fine; `alembic upgrade head` creates it. If it errors, confirm the proxy is up and `DATABASE_URL` points at `127.0.0.1:5432`. |
| LB returns 404 / 502 for a while | LB config takes a few minutes to propagate globally. Wait, then retry `curl http://$LB_IP/health`. |
| Managed cert stuck in `PROVISIONING` | DNS isn't pointing at the LB IP yet, or hasn't propagated. Verify the `A` record resolves to `$LB_IP`; wait up to ~60 min. |
| Cloud Build trigger: permission denied deploying | Grant the Cloud Build service account the *Cloud Run Admin* + *Service Account User* roles. |

## 🧹 Clean up (do this — Cloud SQL & the LB bill continuously)

Delete in roughly reverse order. The simplest, safest option for a learning project is to delete the whole project at the end.

```bash
# load balancer pieces
gcloud compute forwarding-rules delete taskflow-https-rule --global --quiet
gcloud compute forwarding-rules delete taskflow-http-rule  --global --quiet
gcloud compute target-https-proxies delete taskflow-https-proxy --quiet
gcloud compute target-http-proxies  delete taskflow-http-proxy  --quiet
gcloud compute ssl-certificates delete taskflow-cert --global --quiet
gcloud compute url-maps delete taskflow-urlmap --quiet
gcloud compute backend-services delete taskflow-bes --global --quiet
gcloud compute network-endpoint-groups delete taskflow-neg --region=$REGION --quiet
gcloud compute addresses delete taskflow-ip --global --quiet

# Cloud SQL (the big cost) + Cloud Run + secrets
gcloud sql instances delete $INSTANCE --quiet
gcloud run services delete taskflow-backend  --region $REGION --quiet
gcloud run services delete taskflow-frontend --region $REGION --quiet
gcloud secrets delete db-password --quiet
gcloud secrets delete jwt-secret  --quiet

# nuclear option — removes EVERYTHING and stops all billing for the project
gcloud projects delete $PROJECT
```

> **⚠️ Verify nothing is left running**
>
> After teardown, check Console → Billing → Reports the next day, and confirm Cloud SQL shows no instances. A forgotten Cloud SQL instance is the most common source of surprise charges.

## 🏁 Bonus Track Complete

You did it. TaskFlow is now a genuinely **cloud-native** application, deployed the way real teams ship software:

- **Durable, shared data** on managed Cloud SQL Postgres with connection pooling — the SQLite data-loss problem solved.
- A **global HTTP(S) load balancer** with managed TLS and (optionally) a custom domain — the managed evolution of Chunk 9.3's hand-rolled Nginx.
- A **CI/CD pipeline** where every reviewed, branch-protected merge to `main` (your B.1 workflow) automatically builds, tests, and deploys.

Tie it together in your head: **B.1** gave you the safe collaboration workflow, **B.2** got the containers onto Cloud Run, and **B.3** made it durable, scalable, secure, and automatic. That's a story you can demo live and defend in an interview — exactly the goal.

## 🎓 Course Complete — what's next

This was the final chunk of the entire course. From a blank HTML file in Module 1 to a load-balanced, auto-deploying, cloud-hosted full-stack app, you've built the whole thing. 🎉

Where to go from here:

- **Polish TaskFlow as a portfolio piece** — README with architecture diagram, screenshots, and a link to the live URL (keep it deployed on the free-tier-friendly bits, or redeploy on demand).
- **Add depth** — automated tests in CI, observability dashboards, Cloud SQL backups/PITR, a staging environment, or feature flags.
- **Go wider** — try the same deploy on another cloud, add Cloud CDN/Cloud Armor, or explore Kubernetes (GKE) once you want orchestration beyond Cloud Run.

Remember to **keep your cloud resources cleaned up** when you're not demoing. Congratulations — you're now a full-stack developer who can ship to production. 🚀

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
