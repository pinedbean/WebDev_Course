*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Run these from the root of your TaskFlow repo. To keep commands short we set shell variables first — paste this block and reuse `$REGION`, `$PROJECT`, etc. throughout. Replace the values with your own.

```bash
export PROJECT=taskflow-prod-$RANDOM       # must be globally unique
export REGION=asia-southeast1              # pick one near you
export REPO=taskflow
export REG=$REGION-docker.pkg.dev/$PROJECT/$REPO
```

> **📝 Interactive logins are in YOUR terminal**
>
> gcloud auth login
>
> and billing linking open a browser on your own machine. The commands here assume you ran them in your terminal and are authenticated.

### 1 Authenticate & create the project

```bash
gcloud auth login                          # browser sign-in (your terminal)
gcloud projects create $PROJECT --name="TaskFlow"
gcloud config set project $PROJECT
gcloud config set run/region $REGION

# link billing (find your account id with: gcloud billing accounts list)
gcloud billing projects link $PROJECT \
  --billing-account=XXXXXX-XXXXXX-XXXXXX
```

Confirm:

```bash
gcloud config list
# [core] project = taskflow-prod-12345
# [run]  region  = asia-southeast1
```

### 2 Enable the APIs

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  secretmanager.googleapis.com \
  cloudbuild.googleapis.com
```

Expected: `Operation ... finished successfully.` (takes ~30s the first time).

### 3 Create the Artifact Registry repo

```javascript
gcloud artifacts repositories create $REPO \
  --repository-format=docker \
  --location=$REGION \
  --description="TaskFlow container images"

# let local Docker authenticate to push (only needed for the local-build route)
gcloud auth configure-docker $REGION-docker.pkg.dev
```

### 4 Build & push the backend image

**Recommended — build in the cloud** (no architecture issues, no local Docker push):

```bash
cd backend
gcloud builds submit --tag $REG/backend:1.0.0 .
cd ..
```

**Alternative — build locally** (must target amd64, especially on Apple Silicon):

```bash
docker build --platform linux/amd64 -t $REG/backend:1.0.0 ./backend
docker push $REG/backend:1.0.0
```

Verify the image landed:

```bash
gcloud artifacts docker images list $REG
# ... /taskflow/backend  1.0.0
```

### 5 Store the JWT secret & grant access

```bash
# create the secret from a generated value (piped via stdin)
printf '%s' "$(openssl rand -hex 32)" | \
  gcloud secrets create jwt-secret --data-file=-

# find the project number, used in the default Cloud Run service account
export PROJNUM=$(gcloud projects describe $PROJECT --format='value(projectNumber)')

# allow Cloud Run's runtime service account to read the secret
gcloud secrets add-iam-policy-binding jwt-secret \
  --member="serviceAccount:$PROJNUM-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

> **📝 Why the compute service account?**
>
> Unless you specify
>
> --service-account
>
> , Cloud Run runs as the default compute service account
>
> PROJECTNUMBER-compute@developer.gserviceaccount.com
>
> . That's the identity that must be allowed to read the secret.

### 6 Deploy the backend

```bash
gcloud run deploy taskflow-backend \
  --image $REG/backend:1.0.0 \
  --region $REGION \
  --port 8000 \
  --allow-unauthenticated \
  --set-env-vars ENV=production \
  --set-secrets JWT_SECRET=jwt-secret:latest
```

Expected tail of the output:

```
Service [taskflow-backend] revision [taskflow-backend-00001-abc] has been deployed
and is serving 100 percent of traffic.
Service URL: https://taskflow-backend-xxxxxxxx-as.a.run.app
```

Capture the URL and smoke-test `/health`:

```bash
export BACKEND_URL=$(gcloud run services describe taskflow-backend \
  --region $REGION --format='value(status.url)')
curl $BACKEND_URL/health
# {"status":"ok"}
```

### 7 Build & deploy the frontend (with the backend URL baked in)

Vite reads `VITE_API_URL` at *build* time. If your frontend Dockerfile accepts it as a build arg (typical pattern), pass it through. A minimal example of that Dockerfile shape:

```
# frontend/Dockerfile (multi-stage) — relevant lines
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build
# ... then copy dist/ into an nginx stage serving on :80
```

Build with the arg and deploy. With Cloud Build you pass build args via `--substitutions`, or just build locally to inject the arg cleanly:

```bash
docker build --platform linux/amd64 \
  --build-arg VITE_API_URL=$BACKEND_URL/api/v1 \
  -t $REG/frontend:1.0.0 ./frontend
docker push $REG/frontend:1.0.0

gcloud run deploy taskflow-frontend \
  --image $REG/frontend:1.0.0 \
  --region $REGION \
  --port 80 \
  --allow-unauthenticated
```

```bash
export FRONTEND_URL=$(gcloud run services describe taskflow-frontend \
  --region $REGION --format='value(status.url)')
echo $FRONTEND_URL
```

> **⚠️ Wrong API URL = blank app / network errors**
>
> If the frontend calls
>
> localhost:8000
>
> in production, you forgot to set
>
> VITE_API_URL
>
> at build time. Rebuild the frontend image with the correct
>
> $BACKEND_URL
>
> and redeploy — you can't fix it with a runtime env var.

### 8 Fix CORS & open the live app

The backend must allow the frontend's origin. Update the env var and redeploy (this creates a new revision, no rebuild needed):

```bash
gcloud run services update taskflow-backend \
  --region $REGION \
  --update-env-vars CORS_ORIGINS=$FRONTEND_URL
```

Open `$FRONTEND_URL` in your browser. Register, log in, create a project and a task. TaskFlow is live on the public internet, behind Google's HTTPS, autoscaling, scale-to-zero. 🎉

### 9 See the SQLite limitation for yourself

Create some data, then force the service to recycle:

```bash
# wait a few minutes for it to scale to zero, OR deploy a new revision:
gcloud run services update taskflow-backend --region $REGION \
  --update-env-vars TOUCH=$RANDOM
```

Reload and log in again — your tasks may be **gone**. That's the ephemeral filesystem: the SQLite file lived inside an instance that was replaced. **This is the exact problem B.3 fixes** by moving to a shared, durable Cloud SQL Postgres database.

## 📄 Quick reference — the whole deploy

```bash
# 0. vars
export PROJECT=taskflow-prod-$RANDOM REGION=asia-southeast1 REPO=taskflow
export REG=$REGION-docker.pkg.dev/$PROJECT/$REPO

# 1. project + apis + registry
gcloud projects create $PROJECT && gcloud config set project $PROJECT
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  secretmanager.googleapis.com cloudbuild.googleapis.com
gcloud artifacts repositories create $REPO --repository-format=docker --location=$REGION

# 2. secret
printf '%s' "$(openssl rand -hex 32)" | gcloud secrets create jwt-secret --data-file=-

# 3. backend
gcloud builds submit --tag $REG/backend:1.0.0 ./backend
gcloud run deploy taskflow-backend --image $REG/backend:1.0.0 --region $REGION \
  --port 8000 --allow-unauthenticated --set-env-vars ENV=production \
  --set-secrets JWT_SECRET=jwt-secret:latest
export BACKEND_URL=$(gcloud run services describe taskflow-backend --region $REGION --format='value(status.url)')

# 4. frontend
docker build --platform linux/amd64 --build-arg VITE_API_URL=$BACKEND_URL/api/v1 -t $REG/frontend:1.0.0 ./frontend
docker push $REG/frontend:1.0.0
gcloud run deploy taskflow-frontend --image $REG/frontend:1.0.0 --region $REGION --port 80 --allow-unauthenticated
export FRONTEND_URL=$(gcloud run services describe taskflow-frontend --region $REGION --format='value(status.url)')

# 5. cors
gcloud run services update taskflow-backend --region $REGION --update-env-vars CORS_ORIGINS=$FRONTEND_URL
```

## 🛠️ Troubleshooting

| Symptom | Fix |
| --- | --- |
| Deploy fails: "container failed to start / listen on PORT" | Cloud Run injects `$PORT`. Make sure the backend binds `0.0.0.0:$PORT` (or set `--port 8000` and have the app listen on 8000). Check logs: `gcloud run services logs read taskflow-backend`. |
| `exec format error` in logs | Wrong CPU arch — you pushed an arm64 image. Rebuild with `--platform linux/amd64` or use `gcloud builds submit`. |
| Frontend loads but API calls fail (CORS error in console) | Backend's `CORS_ORIGINS` doesn't include the frontend URL. Run the `update-env-vars` step (no trailing slash mismatch). |
| Frontend calls `localhost` | `VITE_API_URL` wasn't set at build time. Rebuild the frontend image with the build arg. |
| "Permission denied on secret" | Service account lacks `secretAccessor`. Re-run the `add-iam-policy-binding` from step 5. |
| `gcloud builds submit` fails: API not enabled | Enable Cloud Build: `gcloud services enable cloudbuild.googleapis.com`. |
| 403 on the public URL | You didn't pass `--allow-unauthenticated`. Re-deploy or add the invoker binding for `allUsers`. |

## 🧹 Clean up (do this to avoid charges)

Cloud Run scales to zero, but Artifact Registry storage and any other resources keep costing. If you're **not continuing straight to B.3**, tear it down. (If you ARE doing B.3 next, keep the services — you'll build on them.)

```bash
# delete the Cloud Run services
gcloud run services delete taskflow-backend  --region $REGION --quiet
gcloud run services delete taskflow-frontend --region $REGION --quiet

# delete the image repo (frees storage)
gcloud artifacts repositories delete $REPO --location=$REGION --quiet

# delete the secret
gcloud secrets delete jwt-secret --quiet

# nuclear option: delete the whole project (stops ALL billing for it)
gcloud projects delete $PROJECT
```

> **💡 Budget alert**
>
> In the Console → Billing → Budgets & alerts, set a small monthly budget (e.g. $5) with email alerts. It won't stop spend automatically but it warns you early.

## 🎉 You're done

TaskFlow now runs on Google Cloud: two Cloud Run services, images in Artifact Registry, secrets in Secret Manager, and a live HTTPS URL anyone can visit. You also saw *first-hand* why SQLite can't stay — its data evaporates on Cloud Run's ephemeral disks.

**Up next → Chunk B.3: GCP Load Balancing, Managed Data & CI/CD.** You'll put a global HTTPS load balancer in front, migrate to **Cloud SQL Postgres** so data survives, and wire up CI/CD so every merge to `main` (from your B.1 workflow) auto-deploys.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
