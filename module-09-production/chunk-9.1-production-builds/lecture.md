*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.1 — Production Builds & Environments

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why **development** and **production** need different configurations.
- What `npm run build` actually does to a Vite app, and why you never ship the dev server.
- How **environment variables** work in Vite (**build-time**) vs FastAPI (**runtime**) — and why the difference matters.
- How to keep **secrets** out of your code and your frontend bundle.
- How a production frontend is just **static files**, and how a production backend runs (multiple workers, no reload).

In the lab you'll produce real build artifacts: a minified frontend `dist/` and a prod-configured backend.

## 1. Dev mode is a lie you tell yourself (on purpose)

Everything you've run so far was optimized for *your* convenience: `npm run dev` hot-reloads on every save, `uvicorn --reload` restarts on code changes, error pages show full stack traces, and CORS is wide open to `localhost:5173`. That's perfect for building — and **wrong for production**, where you want the opposite: fast, minified, cached, locked down, and stable.

"Going to production" is mostly about flipping those defaults. Same code, different configuration.

|  | Development | Production |
| --- | --- | --- |
| Frontend | Vite dev server, hot reload, source maps | Pre-built static files (minified, hashed) |
| Backend reload | `--reload` on | Off; multiple worker processes |
| Errors | Full tracebacks shown | Clean 500s (you built this in 8.2) |
| Config | Hardcoded localhost is fine | From environment variables |
| Goal | Fast feedback while coding | Speed, security, stability |

## 2. What `npm run build` does

The Vite dev server serves your source files on the fly and re-transforms them as you edit — great for iteration, far too slow and unoptimized to put in front of real users. For production you run a one-time **build**:

```bash
npm run build      # runs "vite build"
```

Vite takes all your `.jsx`, CSS, and assets and produces a `dist/` folder of plain, optimized static files. Along the way it:

- **Bundles** many modules into a few files (fewer network requests).
- **Minifies** JS/CSS (strips whitespace, shortens names → smaller downloads).
- **Tree-shakes** — drops code you never import.
- **Hashes filenames** — `index-a1b2c3.js` — so browsers can cache aggressively yet always get the new file when it changes (cache busting).
- Rewrites `index.html` to point at the hashed files.

>

The result is a **static site**: just HTML, CSS, JS, and images. There's no Node.js running it — any web server (Nginx, a CDN, even a dumb file host) can serve `dist/`. To sanity-check the build locally before shipping, Vite gives you a tiny static server:

```bash
npm run preview    # serves the built dist/ at http://localhost:4173
```

> **⚠️ `preview` is for testing, not production**
>
> vite preview
>
> proves your build works, but it's a minimal server not meant to face real traffic. In production a proper web server (Nginx, in Chunk 9.3) serves
>
> dist/
>
> .

## 3. Environment variables: build-time vs runtime

This is the single most-misunderstood part of going to production, so go slow here. Both halves of your stack use environment variables, but at *completely different moments*.

### Backend (FastAPI): runtime env vars

Your FastAPI app reads `settings.secret_key`, `settings.database_url`, etc. *when it starts* (you built this with `pydantic-settings` in Module 7). The same built code can run with different values just by changing the environment — dev points at `tasks.db`, prod points at a real database, and you never rebuild anything. Change a variable, restart the process, done.

### Frontend (Vite): build-time env vars

The browser has no environment — it just downloads files. So Vite **bakes** env vars into the bundle *at build time*. Only variables prefixed `VITE_` are exposed, via `import.meta.env`:

```javascript
// reads at build time, frozen into the bundle:
const BASE = import.meta.env.VITE_API_URL;
```

Whatever `VITE_API_URL` was when you ran `npm run build` is literally substituted into the output JS. To point the frontend at a different API, you must **rebuild** with a new value.

|  | FastAPI (runtime) | Vite (build-time) |
| --- | --- | --- |
| When read | When the process starts | When `npm run build` runs |
| To change a value | Edit env + restart | Edit env + **rebuild** |
| Where it lives | Server process env | Baked into the JS files |
| Prefix required | No | `VITE_` |

> **⚠️ The #1 frontend secret mistake**
>
> Because
>
> VITE_
>
> vars are baked into JS that ships to the browser,
>
> anyone can read them
>
> (just open DevTools → Sources). Never put a secret — API keys, the JWT signing secret, DB passwords — in a
>
> VITE_
>
> variable. Those belong on the
>
> backend
>
> only. The frontend should only hold non-secret config like the API URL.

## 4. Env files & secrets hygiene

Vite reads env files by mode. The important ones:

| File | Loaded when | Commit to git? |
| --- | --- | --- |
| `.env` | Always | No (local values) |
| `.env.development` | `npm run dev` | Sometimes (non-secret defaults) |
| `.env.production` | `npm run build` | Only if values are non-secret |
| `.env.example` | Never (template) | Yes — placeholders only |

The rules you already started in Module 7 hold across the whole project:

- **Never commit real secrets.** `.env` stays in `.gitignore`; commit a `.env.example` with blank/placeholder values so teammates know what to set.
- **Backend secrets live in the server environment** (or a secret manager in Chunk 9.4), not in code and not in the frontend.
- **If a secret ever lands in git history, rotate it.** Deleting the line isn't enough — it's in the history.

> **💡 A clean split for the Tasks app**
>
> Frontend
>
> .env.production
>
> :
>
> VITE_API_URL=https://api.yourdomain.com
>
> (not a secret — fine to commit). Backend env:
>
> SECRET_KEY
>
> ,
>
> DATABASE_URL
>
> ,
>
> FRONTEND_ORIGIN
>
> (secret-ish — never in the frontend, never committed).

## 5. Running the backend in production

In development you run a single auto-reloading process. In production you change two things.

**Turn off reload and turn on workers.** A single Python process handles one request at a time per CPU core (roughly). To use the whole machine you run **multiple worker processes**. The classic way is Gunicorn managing Uvicorn workers; modern Uvicorn can also spawn workers directly:

```bash
# development
uvicorn app.main:app --reload

# production (no reload; bind all interfaces; multiple workers)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# or, the battle-tested combo:
gunicorn app.main:app -k uvicorn.workers.UvicornWorker \
    --workers 4 --bind 0.0.0.0:8000
```

Two details that trip people up:

- `--host 0.0.0.0` means "accept connections on all network interfaces," not just `localhost`. Inside a container or on a server you need this so the outside world (and the load balancer) can reach it.
- Workers are separate processes that **don't share memory**. Anything you cached in a module-level Python variable exists once *per worker* — fine for the Tasks API because state lives in the database and auth is stateless JWT (which is exactly why this scales; more in 9.3).

> **📝 How many workers?**
>
> A common starting point is
>
> (2 × CPU cores) + 1
>
> . Don't over-tune now — the point is "more than one, and reload off." You'll wire the real command into Docker in 9.2.

## 6. Config that knows where it's running

Tie it together with one setting that flags the environment, so the same codebase behaves correctly in both worlds. You already have `pydantic-settings`; just add a field:

```
# app/config.py  (extend your Module 7 Settings)
class Settings(BaseSettings):
    environment: str = "development"          # "production" in prod
    secret_key: str
    database_url: str = "sqlite:///./tasks.db"
    frontend_origin: str = "http://localhost:5173"
    log_level: str = "INFO"
    model_config = SettingsConfigDict(env_file=".env")
```

Now you can branch on it where it matters — for example, the 8.1 logging picks JSON vs pretty text, and you'd never expose docs or verbose errors in prod:

```python
settings = get_settings()
app = FastAPI(
    title="Tasks API",
    docs_url="/docs" if settings.environment != "production" else None,
)
```

> **💡 One image, many environments**
>
> The goal — which Docker (9.2) makes literal — is a single build artifact you promote unchanged from dev to staging to prod, configured entirely by environment variables. No "prod branch," no editing code to deploy.

## ✅ Recap

- Production flips dev defaults: minified static frontend, no reload, multiple workers, clean errors, env-driven config.
- `npm run build` → a `dist/` of bundled, minified, tree-shaken, hash-named **static files**; `npm run preview` tests it locally.
- FastAPI env vars are read at **runtime** (change + restart); Vite `VITE_` vars are baked in at **build time** (change + **rebuild**).
- **Never** put secrets in `VITE_` vars — they ship to the browser. Secrets live on the backend, never in git.
- Run prod with `--host 0.0.0.0`, no `--reload`, and multiple workers (Uvicorn/Gunicorn). Stateless JWT means workers scale freely.

**Next:** open `assignment.html` and produce real production build artifacts.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
