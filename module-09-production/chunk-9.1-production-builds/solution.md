*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Part A builds the frontend; Part B prepares the backend. New/changed files:

```text
tasks-web/                       tasks-api/
├── .env.production  (VITE_API_URL)  ├── app/config.py   (environment field)
├── .env.example     (template)      ├── app/main.py     (docs off in prod)
└── dist/            (build output)  ├── requirements.txt (gunicorn)
                                     └── PRODUCTION.md   (runbook notes)
```

## Part A — Frontend production build

### 1 Environment files

```
# tasks-web/.env.production   (read at build time)
VITE_API_URL=http://localhost:8000
```

```
# tasks-web/.env.example      (commit this; placeholders only)
VITE_API_URL=http://localhost:8000
```

```
# tasks-web/.gitignore  (make sure local envs are ignored)
.env
.env.local
.env.*.local
dist/
node_modules/
```

> **📝 Commit `.env.production`?**
>
> Only because its single value (the API URL) is
>
> not a secret
>
> . The instant you'd put a secret in a frontend env, the answer flips to "never commit." A safe habit: commit
>
> .env.example
>
> , gitignore the rest.

### 2 Build

```bash
cd tasks-web
npm run build
```

```
vite v5.x building for production...
✓ 42 modules transformed.
dist/index.html                   0.46 kB │ gzip:  0.30 kB
dist/assets/index-C1dE2fg.css     2.14 kB │ gzip:  0.89 kB
dist/assets/index-a1B2c3D4.js   146.31 kB │ gzip: 47.02 kB
✓ built in 1.23s
```

### 3 Inspect the output

```
ls -R dist
```

```
dist:
assets   index.html

dist/assets:
index-C1dE2fg.css   index-a1B2c3D4.js
```

Open the JS file — it's one minified line. Search it for your API URL and you'll find `http://localhost:8000` literally embedded. That's the build-time baking from the lecture, and the proof that `VITE_` vars are public.

```
grep -o "http://localhost:8000" dist/assets/index-*.js | head -1
# http://localhost:8000
```

### 4 Preview

```bash
# terminal 1 — backend
uvicorn app.main:app --reload

# terminal 2 — built frontend
npm run preview        # ➜ Local: http://localhost:4173/
```

Open `http://localhost:4173`, log in, and use the app. It behaves like dev but is now plain static files — exactly what a web server or CDN will serve in production.

## Part B — Backend production config

### 5 Extend `app/config.py`

```python
# app/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    environment: str = "development"            # "production" in prod
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    database_url: str = "sqlite:///./tasks.db"
    frontend_origin: str = "http://localhost:5173"
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
```

### 6 Use the setting in `app/main.py`

```python
# app/main.py  (relevant parts)
from app.config import settings
from app.logging_config import setup_logging

setup_logging(settings.log_level)

is_prod = settings.environment == "production"
app = FastAPI(
    title="Tasks API",
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
)
```

> **📝 Why hide docs in prod**
>
> The interactive
>
> /docs
>
> is a fantastic dev tool but advertises your entire API surface to anyone. Many teams disable it (or put it behind auth) in production. Keeping it on in dev and off in prod is a clean one-line policy.

### 7 Production run command

```bash
pip install "gunicorn"
pip freeze > requirements.txt
```

```bash
# the production way (pick one)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

gunicorn app.main:app -k uvicorn.workers.UvicornWorker \
    --workers 4 --bind 0.0.0.0:8000
```

Run it with prod settings and confirm:

```bash
ENVIRONMENT=production uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2

curl -s localhost:8000/health      # {"status":"ok"}
curl -i localhost:8000/docs        # HTTP/1.1 404 Not Found  (docs disabled)
```

> **⚠️ Workers + SQLite**
>
> Multiple workers all writing to one SQLite file can occasionally hit "database is locked" under load — a real limitation you'll confront head-on in 9.3/9.4 (and the move to Postgres). For now, on a low-traffic dev box, a couple of workers is fine.

### 8 `PRODUCTION.md` (starter runbook)

```
# PRODUCTION.md

## Frontend
- Build:   cd tasks-web && npm run build   -> outputs dist/
- Config:  .env.production sets VITE_API_URL (baked in at build time)
- Serve:   any static server / Nginx serves dist/ (see Chunk 9.3)

## Backend
- Required env: SECRET_KEY, DATABASE_URL, FRONTEND_ORIGIN, ENVIRONMENT, LOG_LEVEL
- Run:     uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
- Health:  GET /health (liveness), GET /health/ready (readiness)
- Notes:   no --reload in prod; docs disabled when ENVIRONMENT=production
```

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `npm run build` fails on an unused import / type | Build is stricter than dev. Read the error, remove the dead code, rebuild. (Dev tolerates things build won't.) |
| Preview shows a blank page | Open the console. Usually a bad `base` path or API URL. Fix `.env.production` / `vite.config.js` and **rebuild** before previewing. |
| API calls in preview go to the wrong place | `VITE_API_URL` is baked in. Edit `.env.production`, run `npm run build` again, then `npm run preview`. |
| Changed an env var but nothing changed | Frontend: rebuild. Backend: restart the process. Vite is build-time; FastAPI is runtime. |
| `/docs` still loads in prod | `ENVIRONMENT` isn't actually "production" in the process env, or you didn't pass `docs_url=None`. Print `settings.environment` to confirm. |
| `gunicorn: command not found` | Install it in the active venv and re-freeze: `pip install gunicorn`. |

## 🎉 You're done

You now have genuine production artifacts: a minified, hash-named static `dist/` for the frontend and a backend that runs without reload, with workers, env-driven config, and docs locked down in prod. You also internalized the crucial mental model — **Vite bakes config at build time, FastAPI reads it at runtime** — and the rule that secrets never ride in the frontend.

These artifacts still run "by hand" on your machine. Next you'll wrap each side in a container so it runs the same everywhere — your laptop, a teammate's, a server.

**Up next → Chunk 9.2: Containerizing with Docker.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
