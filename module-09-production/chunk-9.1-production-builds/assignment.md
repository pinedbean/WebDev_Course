*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.1 — Lab: Build for Production

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Turn the dev-mode Tasks app into **production-ready artifacts**. You'll create a real Vite production build of the frontend (a static `dist/`), configure it with a build-time `VITE_API_URL`, prove it runs with `preview`, and configure the backend for production: an `environment` setting, a prod run command with workers (no reload), and clean secrets hygiene. No Docker yet — that's 9.2.

## Before you start

- You finished **Module 8**: the Tasks API has structured logging, health checks, and error handling.
- Frontend (`tasks-web/`) and backend (`tasks-api/`) both run in dev.
- Node LTS + npm and your Python venv are available.

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Part A — Frontend production build

### 1 Create environment files

In `tasks-web/`, create `.env.production` with the API URL the built app should call, and a committed `.env.example` documenting the variable. Make sure `.env` (local) is in `.gitignore`.

```
# .env.production
VITE_API_URL=http://localhost:8000
```

(Use `localhost:8000` for now; in 9.3 it becomes the URL Nginx proxies. The point is that it's read at build time.)

### 2 Build it

Run the production build and watch what it produces.

```bash
npm run build
```

Confirm a `dist/` folder appears with an `index.html` and an `assets/` folder containing hashed, minified `.js`/`.css` files.

### 3 Inspect the artifacts

List the `dist/` tree and open one of the hashed JS files. Confirm it's minified (one long line, short variable names) and that your `VITE_API_URL` value appears baked into the bundle. Reflect: anything in a `VITE_` var is visible here — so it must never be a secret.

### 4 Preview the build

Serve the built files and click through the app (with your backend running):

```bash
npm run preview      # http://localhost:4173
```

Log in, view tasks, create one. It should behave like dev — but it's now static files, not the dev server.

> **💡 If API calls fail in preview**
>
> The built app calls whatever
>
> VITE_API_URL
>
> you baked in. If requests 404 or hit the wrong port, fix
>
> .env.production
>
> and
>
> rebuild
>
> — preview serves the last build, it doesn't re-read env.

## Part B — Backend production config

### 5 Add an `environment` setting

Extend `app/config.py`'s `Settings` with `environment: str = "development"` (and `log_level` if you didn't already in 8.1). Set `ENVIRONMENT=production` in your backend env when running for prod.

### 6 Make prod behave differently where it matters

Use the setting to (a) disable the interactive docs in production (pass `docs_url=None` when `environment == "production"`), and (b) confirm your 8.1 logging uses JSON in production. Keep dev exactly as it was.

### 7 Write the production run command

Pin a production server. Add `gunicorn` (or rely on uvicorn workers) to `requirements.txt`, then run the backend the production way — no reload, bind all interfaces, multiple workers — and confirm it serves:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Hit `/health` and a real endpoint to confirm it works without `--reload`.

### 8 Write a short PRODUCTION.md note

Create a brief `PRODUCTION.md` (or a section in your README) listing: the frontend build command and where artifacts land, the required backend env vars, and the production run command. You'll expand this into the deployment runbook in 9.4.

## ✅ Deliverable — acceptance checklist

- `tasks-web/dist/` exists with `index.html` + hashed, minified assets in `assets/`.
- `.env.production` sets `VITE_API_URL`; `.env.example` is committed; real `.env` files are git-ignored.
- `npm run preview` serves the built app and it works against the running backend.
- Backend `Settings` has an `environment` field; docs are disabled when `environment == "production"`.
- The backend runs in production mode (`--host 0.0.0.0`, no `--reload`, multiple workers) and answers `/health`.
- No secrets appear in any `VITE_` variable or in the `dist/` bundle; a `PRODUCTION.md` documents build + run steps.

## 🚀 Stretch goals (optional)

- Compare bundle sizes: run `du -sh dist` and note how small the minified app is. Add `build.sourcemap` in `vite.config.js` and rebuild to see source maps generated separately.
- Add a `start.sh` script with the production gunicorn command so you don't retype it.
- Verify docs are gone in prod: run with `ENVIRONMENT=production` and confirm `/docs` returns 404.
- Set a non-secret `VITE_APP_VERSION` from a git tag and display it in the footer (a tiny taste of build metadata).
- Confirm a missing `SECRET_KEY` still makes the backend refuse to start (your Module 7 settings validation) — fail-fast is a production feature.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
