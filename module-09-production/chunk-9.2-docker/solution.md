*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll write four files, a Compose file, and bring the stack up. End state:

```text
project-root/
├── docker-compose.yml
├── .env                       (SECRET_KEY — git-ignored)
├── tasks-api/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── app/ ...
└── tasks-web/
    ├── Dockerfile             (multi-stage)
    ├── .dockerignore
    ├── nginx.conf
    └── src/ ...
```

### 1 `tasks-api/Dockerfile`

```dockerfile
FROM python:3.11-slim

# Faster, cleaner Python in containers.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install deps first so this layer is cached across code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now the application code.
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
```

> **📝 `PYTHONUNBUFFERED=1`**
>
> Without it, Python buffers stdout and your 8.1 JSON logs appear late (or not until the container stops). Setting it makes logs stream in real time — essential for
>
> docker compose logs -f
>
> .

```bash
# tasks-api/.dockerignore
__pycache__/
*.pyc
.venv/
tasks.db
.env
.git/
alembic/versions/__pycache__/
```

### 2 Confirm the DB path is env-driven

In `app/database.py`, the engine must read the URL from settings (not a hardcoded string), so Compose can point it at the volume:

```python
# app/database.py  (the key line)
from app.config import settings

engine = create_engine(
    settings.database_url,                       # e.g. sqlite:////data/tasks.db
    connect_args={"check_same_thread": False},
)
```

### 3 `tasks-web/Dockerfile` (multi-stage)

```dockerfile
# --- Stage 1: build ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- Stage 2: serve ---
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```
# tasks-web/.dockerignore
node_modules/
dist/
.env
.git/
```

### 4 `tasks-web/nginx.conf`

```
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;     # SPA fallback for React Router
    }
}
```

> **💡 We'll proxy /api here in 9.3**
>
> Right now the built frontend calls the API directly via the baked-in
>
> VITE_API_URL
>
> . In 9.3 this same
>
> nginx.conf
>
> grows a
>
> location /api/
>
> block that proxies to the backend — so the browser only ever talks to one origin.

### 5 `docker-compose.yml` + root `.env`

```yaml
# docker-compose.yml  (project root)
services:
  api:
    build: ./tasks-api
    environment:
      SECRET_KEY: ${SECRET_KEY}
      DATABASE_URL: sqlite:////data/tasks.db
      ENVIRONMENT: production
      FRONTEND_ORIGIN: http://localhost:5173
      LOG_LEVEL: INFO
    volumes:
      - tasks-data:/data
    ports:
      - "8000:8000"

  web:
    build: ./tasks-web
    ports:
      - "5173:80"
    depends_on:
      - api

volumes:
  tasks-data:
```

```
# .env  (project root, git-ignored)
SECRET_KEY=paste-a-64-hex-char-secret-here
```

> **⚠️ The volume holds `/data`, the DB is `/data/tasks.db`**
>
> Mounting
>
> tasks-data
>
> at
>
> /data
>
> +
>
> DATABASE_URL=sqlite:////data/tasks.db
>
> (four slashes) means the file lives in the volume.
>
> docker compose down
>
> removes containers but keeps the volume — that's why data survives.
>
> docker compose down -v
>
> would delete it.

### 6 Build & run

```bash
docker compose up --build
```

```
 ✔ Network project-root_default   Created
 ✔ Volume "project-root_tasks-data" Created
 ✔ Container project-root-api-1   Created
 ✔ Container project-root-web-1   Created
api-1  | {"timestamp":"...","level":"INFO","logger":"uvicorn.error","message":"Started server process","request_id":"-"}
api-1  | {"timestamp":"...","level":"INFO","logger":"uvicorn.error","message":"Uvicorn running on http://0.0.0.0:8000","request_id":"-"}
web-1  | ... nginx ... start worker processes
```

```bash
# in another terminal:
curl -s localhost:8000/health      # {"status":"ok"}
```

Open `http://localhost:5173` — the frontend loads from the Nginx container.

### 7 Migrate the fresh volume DB

```bash
docker compose exec api alembic upgrade head
```

```
INFO  [alembic.runtime.migration] Running upgrade  -> ..., create users and tasks
INFO  [alembic.runtime.migration] Running upgrade ... -> ..., add auth fields
```

Now register, log in, and create a task in the UI.

### 8 Prove persistence

```sql
docker compose down        # removes containers, KEEPS the volume
docker compose up          # back up; data still there
docker compose exec api sqlite3 /data/tasks.db "SELECT count(*) FROM tasks;"
# -> your task count, unchanged
```

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Container runs but you can't reach it from the browser | Bind to `0.0.0.0` in the `CMD` (not `127.0.0.1`), and check the host:container port map in Compose. |
| Every code change reinstalls all pip packages | You copied code before `requirements.txt`. Copy + install requirements *first* so the install layer caches. |
| Refreshing `/dashboard` in the deployed frontend 404s | Missing SPA fallback. Add `try_files $uri $uri/ /index.html;` in `nginx.conf`. |
| `sqlite3.OperationalError: unable to open database file` | The `/data` dir isn't mounted, or you used three slashes. Use `sqlite:////data/tasks.db` and mount `tasks-data:/data`. |
| Data disappears after `down` | You ran `down -v` (removes volumes) or stored the DB inside the container FS instead of the volume. |
| Logs don't appear until the container stops | Set `ENV PYTHONUNBUFFERED=1` in the backend Dockerfile. |
| Frontend can't reach the API in the browser | The browser uses the baked `VITE_API_URL` (host-visible `localhost:8000`), not the internal name. For browser calls, point it at the published host port. (9.3's reverse proxy removes this footgun.) |

## 📄 Complete `docker-compose.yml`

```yaml
services:
  api:
    build: ./tasks-api
    environment:
      SECRET_KEY: ${SECRET_KEY}
      DATABASE_URL: sqlite:////data/tasks.db
      ENVIRONMENT: production
      FRONTEND_ORIGIN: http://localhost:5173
      LOG_LEVEL: INFO
    volumes:
      - tasks-data:/data
    ports:
      - "8000:8000"

  web:
    build: ./tasks-web
    ports:
      - "5173:80"
    depends_on:
      - api

volumes:
  tasks-data:
```

## 🎉 You're done

The entire Tasks app now lives in containers: a slim Python image for the API, a tiny Nginx image carrying only the built frontend, both orchestrated by Compose, with the database safely in a named volume. One command — `docker compose up --build` — reproduces the whole stack on any machine with Docker. "Works on my machine" is now "works on every machine."

You're running *one* backend container. Next you'll put Nginx in front as a load balancer and run *several* backend replicas from the same image — real horizontal scaling.

**Up next → Chunk 9.3: Nginx Reverse Proxy & Load Balancing.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
