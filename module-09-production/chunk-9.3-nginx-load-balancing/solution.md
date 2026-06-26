*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We add a small instance marker, enable WAL, introduce an Nginx LB service, and scale the API. End state:

```text
project-root/
├── docker-compose.yml          (api scaled, nginx LB added)
├── nginx/
│   └── nginx.conf              (upstream + proxy_pass + SPA)
├── tasks-api/
│   └── app/
│       ├── database.py         (WAL pragma)
│       └── main.py             (instance in /health)
└── tasks-web/
    └── .env.production         (VITE_API_URL=/api)
```

> **📝 The architecture**
>
> Browser →
>
> Nginx :80
>
> → (
>
> /
>
> = built frontend) & (
>
> /api/
>
> = round-robin to api replicas) →
>
> shared SQLite volume
>
> . The backend no longer publishes a host port — only Nginx is public.

### 1 Make replicas identifiable

```python
# app/main.py  (additions)
import socket

INSTANCE = socket.gethostname()      # the container id inside Docker

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "instance": INSTANCE}
```

Optionally include it in the request log too, so your 8.1 lines show which replica served:

```
# app/middleware.py  (inside the logger.info extra)
extra={..., "instance": socket.gethostname()}
```

### 2 Enable WAL in `app/database.py`

```python
# app/database.py  (extend your existing pragma listener)
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")     # readers + a writer coexist
    cursor.execute("PRAGMA busy_timeout=5000")    # wait up to 5s on a lock
    cursor.close()
```

> **💡 `busy_timeout` reduces lock errors**
>
> Instead of failing instantly on a momentary write lock, a replica waits up to 5s for it to clear. Combined with WAL, this is enough to demo balancing smoothly — but it's still one writer under the hood.

### 3 `nginx/nginx.conf`

```
upstream api_pool {
    # Docker's internal DNS resolves "api" to ALL replicas; Nginx round-robins.
    server api:8000;
}

server {
    listen 80;
    server_name _;

    # The built frontend.
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # The API — note the trailing slash on proxy_pass strips the /api prefix.
    location /api/ {
        proxy_pass http://api_pool/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

> **📝 The trailing-slash trick**
>
> location /api/
>
> +
>
> proxy_pass http://api_pool/;
>
> (with the trailing
>
> /
>
> ) means a request to
>
> /api/health
>
> reaches the backend as
>
> /health
>
> . The backend keeps its clean paths; the
>
> /api
>
> prefix exists only at the edge.

This LB image needs the built frontend too. Simplest approach: reuse the multi-stage frontend build and just swap in this config. The Compose below builds the frontend image and mounts the LB config over it.

### 4 `docker-compose.yml` — scale api, add the proxy

```yaml
services:
  api:
    build: ./tasks-api
    environment:
      SECRET_KEY: ${SECRET_KEY}            # SAME key for every replica
      DATABASE_URL: sqlite:////data/tasks.db
      ENVIRONMENT: production
      FRONTEND_ORIGIN: http://localhost
      LOG_LEVEL: INFO
    volumes:
      - tasks-data:/data
    # NOTE: no "ports:" — only Nginx is public now.
    expose:
      - "8000"

  web:
    build: ./tasks-web                      # multi-stage: builds dist/ onto nginx
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    ports:
      - "80:80"
    depends_on:
      - api

volumes:
  tasks-data:
```

Here the `web` service doubles as the load balancer: it already serves the built frontend (from 9.2), and mounting our new config adds the `/api/` proxy. Bring it up with several API replicas:

```bash
docker compose up --build --scale api=3
```

> **💡 Why `server api:8000;` reaches all 3 replicas**
>
> When you scale a service, Docker's embedded DNS returns
>
> all
>
> replica IPs for the service name
>
> api
>
> . Nginx load-balances across the addresses it resolves. (For finer control you can instead define separate
>
> api1
>
> /
>
> api2
>
> services and list each in the upstream — both approaches are valid.)

### 5 Same-origin frontend

```
# tasks-web/.env.production
VITE_API_URL=/api
```

Rebuild so the new value is baked in (recall 9.1 — Vite bakes at build time):

```bash
docker compose build web
docker compose up -d --scale api=3
```

Now `apiFetch("/tasks")` calls `/api/tasks` on the same origin as the page. No CORS, no host/port.

### 6 Migrate once

```bash
docker compose exec api alembic upgrade head
```

(Compose targets one replica for `exec`; they all share the same volume, so once is enough.)

### 7 Watch round-robin

```
for i in $(seq 1 6); do curl -s http://localhost/api/health; echo; done
```

```json
{"status":"ok","instance":"a1b2c3d4e5f6"}
{"status":"ok","instance":"f6e5d4c3b2a1"}
{"status":"ok","instance":"9a8b7c6d5e4f"}
{"status":"ok","instance":"a1b2c3d4e5f6"}
{"status":"ok","instance":"f6e5d4c3b2a1"}
{"status":"ok","instance":"9a8b7c6d5e4f"}
```

Three distinct instance ids cycling = Nginx is spreading requests across all three replicas. 🎉

### 8 Confirm stateless auth survives balancing

Open `http://localhost`, register, log in, create tasks, refresh — it all works, even though consecutive requests hit different replicas. Spot-check the shared secret:

```bash
# every replica should print the SAME key
docker compose exec api printenv SECRET_KEY
```

Because the JWT is verified locally against that shared `SECRET_KEY`, any replica accepts the token — no sticky sessions, no shared session store. This is the Module 7 design paying off.

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `/api/health` 404s | Trailing-slash mismatch. Use `location /api/` with `proxy_pass http://api_pool/;` (note the final `/`). |
| Same instance every time | Only one replica is running, or Nginx cached one resolved IP. Scale with `--scale api=3`; for long-lived DNS, add a `resolver` directive or define explicit replica services. |
| Random 401s after logging in | Replicas have *different* `SECRET_KEY`s. Pass the same env var to all; verify with `docker compose exec api printenv SECRET_KEY`. |
| `database is locked` under load | Enable WAL + `busy_timeout` (step 2). It's the SQLite single-writer limit — expected; the real fix is Postgres (9.4). |
| Frontend calls go to `localhost:8000` still | You didn't rebuild after setting `VITE_API_URL=/api`. `docker compose build web` then up. |
| Backend logs show Nginx's IP as the client | Add the `proxy_set_header X-Forwarded-For`/`X-Real-IP` lines and read them in the app if you need the true client IP. |
| Refresh on `/dashboard` 404s | Keep the SPA `try_files … /index.html` in the `location /` block. |

## 📄 Complete `nginx/nginx.conf`

```
upstream api_pool {
    server api:8000;
}

server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://api_pool/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🎉 You're done

You built a real load-balanced stack: **Nginx → 2+ FastAPI replicas → one shared SQLite**. The browser hits a single origin; Nginx serves the frontend and round-robins API calls; you watched the instance id rotate to prove it; and you confirmed that stateless JWT lets any replica serve any request with no sticky sessions. You also saw, honestly, where SQLite's single-writer model becomes the bottleneck.

The system runs beautifully on your machine. The last step is shipping it: deploying somewhere real, running migrations safely in production, managing secrets, and automating the whole thing with CI/CD — plus a clear-eyed plan for outgrowing SQLite.

**Up next → Chunk 9.4: Deployment & CI/CD Basics (and the 🏁 Module 9 Checkpoint).**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
