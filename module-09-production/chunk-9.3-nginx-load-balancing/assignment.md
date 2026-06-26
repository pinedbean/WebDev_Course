*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.3 — Lab: Load-Balance the API

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Put an **Nginx reverse proxy / load balancer** in front of **2+ FastAPI replicas** and serve the frontend through it. The browser will talk to a single origin (Nginx), which serves the built frontend at `/` and round-robins API calls at `/api/` across the replicas. You'll add a way to *see* which replica answered, prove round-robin works, and confirm stateless JWT means no sticky sessions are needed. Final shape: **Nginx → multiple API instances → one shared SQLite**.

## Before you start

- You finished **9.2**: backend + frontend Dockerfiles and a working `docker compose up`.
- Your auth is **stateless JWT** (Module 7) — the property that makes this work.
- Docker Desktop running.

> **⚠️ Try it yourself first**
>
> Build from the lecture and these tasks. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Tasks

### 1 Make replicas identifiable

So you can observe load balancing, have the backend expose which instance answered. Add the container hostname to the `/health` response and to your request logs, e.g. `{"status":"ok","instance": socket.gethostname()}`. (Each replica's hostname is its container id, so it'll differ per replica.)

### 2 Enable WAL on SQLite

Multiple replicas will share one SQLite file. Turn on WAL mode so reads and a writer coexist better. In `app/database.py`'s SQLite pragma event (you have one from Module 6 for foreign keys), also run `PRAGMA journal_mode=WAL;`.

> **📝 This is a demo mitigation, not a fix**
>
> WAL helps you show load balancing without constant lock errors. It does
>
> not
>
> make SQLite a multi-writer database — that's the honest limit you'll address in 9.4.

### 3 Add an Nginx load-balancer service

Create `nginx/nginx.conf` with an `upstream` pool pointing at your API replicas and a `server` block that: serves the built frontend at `/` (with SPA fallback) and `proxy_pass`es `/api/` to the pool with the standard forwarded headers. Add an `nginx` (or `proxy`) service to Compose that mounts this config and publishes port `80`.

### 4 Run multiple API replicas

Scale the `api` service to 2+ instances. The simplest path: remove the host port mapping from `api` (only Nginx needs to reach it, internally) and start with `--scale`:

```bash
docker compose up --build --scale api=3
```

Make the Nginx `upstream` target the service name so Docker's DNS round-robins to all replicas (e.g. `server api:8000;`), or list explicit replica hostnames — your choice; the solution shows both.

### 5 Point the frontend at the same origin

Since Nginx serves both, set the frontend to call the relative path: `VITE_API_URL=/api` in `.env.production`, then rebuild the frontend image. Now the browser only ever talks to Nginx — no CORS, no host/port baked in.

### 6 Migrate the shared DB once

Apply migrations against the shared volume (run it in any one replica):

```bash
docker compose exec api alembic upgrade head
```

### 7 Prove round-robin

Hit the proxied health endpoint repeatedly and watch the `instance` value rotate across replicas:

```
for i in $(seq 1 6); do curl -s http://localhost/api/health; echo; done
```

You should see the hostname cycle through your replicas (e.g. a, b, c, a, b, c).

### 8 Prove stateless auth survives balancing

Through the browser (`http://localhost`), register/log in once and use the app normally. Even though consecutive requests land on different replicas, you stay logged in and see your data — because every replica verifies the same JWT with the shared `SECRET_KEY`. Confirm all replicas got the *same* `SECRET_KEY` env var.

## ✅ Deliverable — acceptance checklist

- An Nginx service load-balances `/api/` across **2+ FastAPI replicas** and serves the frontend at `/` (single origin).
- `nginx.conf` has an `upstream` pool and a `proxy_pass` with forwarded headers; SPA fallback still works.
- Repeated calls to `/api/health` show the `instance`/hostname rotating across replicas (round-robin visible).
- Logging in via the browser works and stays logged in even though requests hit different replicas (stateless JWT, shared `SECRET_KEY`).
- All replicas share one SQLite file via the named volume (WAL enabled); migrations applied once.
- You can articulate *why* no sticky sessions are needed, and the SQLite single-writer limitation.

## 🚀 Stretch goals (optional)

- Switch the strategy to `least_conn;` and add an artificially slow endpoint; observe the distribution change vs round-robin.
- Kill one replica (`docker compose stop <container>`) mid-loop and watch Nginx route around it — the app keeps serving.
- Add `max_fails`/`fail_timeout` to the upstream and a `healthcheck` in Compose tied to `/health`.
- Give each replica a `weight` and confirm the busier one gets more traffic.
- Add basic Nginx access logging and correlate its lines with your backend's `X-Request-ID` (pass the header through with `proxy_set_header`).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
