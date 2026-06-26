*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.2 — Containerizing with Docker

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The "works on my machine" problem and how **containers** solve it.
- The difference between an **image** and a **container**.
- How to read and write a **Dockerfile** (the key instructions and why order matters).
- How **layer caching** and `.dockerignore` make builds fast and small.
- **Multi-stage builds** — build the frontend with Node, ship it with Nginx.
- How **Docker Compose** runs the whole app (frontend + backend + a persistent DB) with one command.

In the lab you'll containerize the Tasks app and bring it all up with `docker compose up`.

## 1. The problem containers solve

Your app currently depends on *your* machine: a specific Python version, a venv, Node, the right packages, environment variables you set by hand. Move it to a server (or a teammate's laptop) and any difference breaks it — "but it works on my machine!" is a genuine, costly problem.

A **container** packages your app *together with everything it needs to run* — the OS libraries, the Python/Node runtime, your dependencies, your code — into one sealed, portable unit. If it runs in the container on your laptop, it runs identically in the container on the server. The environment travels *with* the app.

> **📝 Container vs virtual machine**
>
> A VM virtualizes a whole computer (its own OS kernel) — heavy, slow to boot. A container shares the host's kernel and isolates just your app and its dependencies — lightweight, starts in milliseconds. That's why containers became the standard unit of deployment.

## 2. Images vs containers

Two words people mix up constantly. The relationship is exactly like a class and an object, or a recipe and a meal:

| Image | Container |
| --- | --- |
| A read-only **template** (your app + deps, frozen) | A **running instance** of an image |
| Built once, stored, shared | Started, stopped, deleted, replaced |
| The recipe / the class | The meal / the object |

You **build** an image from a `Dockerfile`, then **run** one or more containers from that image. This is the key to scaling: in 9.3 you'll run *several* containers from the *same* backend image behind a load balancer.

>

## 3. Anatomy of a Dockerfile

A `Dockerfile` is a text file of instructions for building an image, top to bottom. Here's a backend one for the Tasks API, fully annotated:

```dockerfile
# Start from an official image that already has Python 3.11.
FROM python:3.11-slim

# All following commands run inside this directory in the image.
WORKDIR /app

# Copy ONLY requirements first (see layer caching below), then install.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source code.
COPY . .

# Document the port the app listens on (informational).
EXPOSE 8000

# The command that runs when a container starts.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Instruction | What it does |
| --- | --- |
| `FROM` | The base image to build on (here, a slim Linux + Python 3.11). |
| `WORKDIR` | Sets/creates the working directory for later instructions. |
| `COPY` | Copies files from your project into the image. |
| `RUN` | Executes a command *at build time* (installing deps, etc.). |
| `EXPOSE` | Documents which port the app uses (doesn't publish it — Compose does that). |
| `CMD` | The default command run *at container start*. Note `--host 0.0.0.0` (from 9.1!). |

> **💡 Why `--host 0.0.0.0` is mandatory in a container**
>
> Inside the container,
>
> localhost
>
> means "only this container." Bind to
>
> 0.0.0.0
>
> so the port is reachable from outside the container. Forgetting this is the most common "my container runs but I can't reach it" bug.

## 4. Layer caching & `.dockerignore`

Each instruction creates a **layer**, and Docker caches layers. On rebuild, it reuses cached layers until it hits one whose inputs changed — then it (and everything after) reruns. This is why the backend Dockerfile copies `requirements.txt` and installs *before* copying the code:

- You edit your app code (common) → only the `COPY . .` layer and below rerun. The expensive `pip install` layer is reused. Builds take seconds.
- If you'd copied everything first, every code change would bust the install cache and reinstall all dependencies. Builds take minutes.

Order your Dockerfile from **least-frequently-changing to most-frequently-changing**.

A `.dockerignore` file (like `.gitignore`) keeps junk out of the image — smaller, faster, safer builds:

```
# backend .dockerignore
__pycache__/
*.pyc
.venv/
tasks.db
.env
.git/
```

> **⚠️ Never bake secrets or the dev DB into an image**
>
> Ignore
>
> .env
>
> and
>
> tasks.db
>
> . Secrets come in at
>
> run
>
> time via environment variables (Compose does this), and the database lives in a
>
> volume
>
> outside the image — never inside it.

## 5. Multi-stage builds (the frontend)

The frontend is interesting: you need **Node** to *build* it (`npm run build`), but you only need a tiny web server to *serve* the resulting static files. Shipping a full Node image just to serve static files would be bloated. A **multi-stage build** uses one stage to build and a second, clean stage to run — and the build tools are left behind.

```dockerfile
# --- Stage 1: build the static files with Node ---
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build              # produces /app/dist

# --- Stage 2: serve them with Nginx ---
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

The magic is `COPY --from=build`: the final image is just Nginx + your `dist/` — a few megabytes, no Node, no `node_modules`. The build stage did its job and was discarded.

That tiny `nginx.conf` serves the SPA and, crucially, sends every unknown path back to `index.html` so client-side routing (React Router from Module 4) works on refresh:

```
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;   # SPA fallback
    }
}
```

> **📝 Why the SPA fallback matters**
>
> Your built app is one
>
> index.html
>
> + JS. If a user refreshes on
>
> /dashboard
>
> , the server gets a request for a file that doesn't exist.
>
> try_files … /index.html
>
> says "serve index.html and let React Router sort out the route." Without it, refresh on any sub-route 404s.

## 6. Docker Compose — running the whole app

Building and running each container by hand (with the right ports, env vars, networks, volumes) is tedious and error-prone. **Docker Compose** describes your whole multi-container app in one `docker-compose.yml` and runs it with a single command:

```bash
docker compose up --build      # build images & start everything
docker compose down            # stop & remove everything
docker compose logs -f api     # follow one service's logs
```

A Compose file lists **services** (each becomes a container), their build context, ports, environment, volumes, and dependencies:

```yaml
services:
  api:
    build: ./tasks-api
    environment:
      SECRET_KEY: ${SECRET_KEY}            # passed in at runtime
      DATABASE_URL: sqlite:////data/tasks.db
    volumes:
      - tasks-data:/data                   # DB persists outside the container
    ports:
      - "8000:8000"

  web:
    build: ./tasks-web
    ports:
      - "5173:80"
    depends_on:
      - api

volumes:
  tasks-data:                              # named volume = durable storage
```

Three ideas to lock in:

- **Services talk by name.** Compose puts them on a shared network, so the web container can reach the backend at `http://api:8000` — no IP addresses, no `localhost`.
- **Ports map host→container.** `"8000:8000"` means "host port 8000 → container port 8000." That's how *you* reach it from your browser.
- **Volumes give durability.** Containers are disposable; their filesystem vanishes when they're removed. A **named volume** mounted at the DB path keeps `tasks.db` alive across restarts and rebuilds.

> **⚠️ Without a volume, your data evaporates**
>
> If SQLite's file lives inside the container's own filesystem,
>
> docker compose down
>
> deletes it. Mounting a named volume at the database directory is what makes data survive. This is doubly important in 9.3 when multiple API replicas must share
>
> the same
>
> database file.

## 7. The shape you're building

>

One command spins up the frontend container and the backend container, wires them on a private network, and persists the database in a volume. In 9.3 you'll insert an Nginx load balancer and scale `api` to several replicas — and because you containerized cleanly here, that's a small change, not a rewrite.

## ✅ Recap

- Containers package your app *with* its environment, killing "works on my machine."
- An **image** is the frozen template; a **container** is a running instance. Build once, run many.
- A **Dockerfile** uses `FROM/WORKDIR/COPY/RUN/EXPOSE/CMD`; order it for **layer caching** (deps before code) and use `.dockerignore`.
- **Multi-stage builds** build the frontend with Node, then ship only `dist/` on Nginx — tiny final image.
- **Compose** runs the whole app: services talk by name, ports map host→container, and a **named volume** keeps the SQLite data durable.

**Next:** open `assignment.html` and bring the whole app up with one command.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
