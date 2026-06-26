*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.1 — Lab: Stand Up Your First API

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Create the `tasks-api` project, set up a virtual environment, install FastAPI + Uvicorn, and build a small app with a `/hello` endpoint, a personalized `/hello/{name}` endpoint, and a `/health` check. Run it with Uvicorn and explore the interactive docs.

## Before you start

- Python 3.11+ installed (check with `python3 --version`). You set this up in Module 0.
- VS Code with the Python extension.
- A terminal (macOS Terminal / zsh, or PowerShell on Windows).

> **⚠️ Try it yourself first**
>
> Build from the lecture and your own attempts. Only open
>
> solution.html
>
> when stuck or to compare at the end. The exact errors you hit (and fix) are the real lesson.

## Tasks

### 1 Create the project folder

Make a folder named `tasks-api` (this becomes your backend for Modules 5–7). Place it somewhere sensible, e.g. `~/Desktop/webdev-course/module-05-fastapi/tasks-api`. Move into it and open it in VS Code with `code .`.

### 2 Create & activate a virtual environment

Inside `tasks-api`, create a venv called `.venv` and activate it. Confirm your prompt now starts with `(.venv)`.

> **💡 Windows note**
>
> Activation differs by OS — macOS/Linux use
>
> source .venv/bin/activate
>
> ; Windows PowerShell uses
>
> .venv\Scripts\Activate.ps1
>
> . The lecture shows both.

### 3 Install FastAPI and Uvicorn

With the venv active, install both packages with `pip`. Then freeze your dependencies into a `requirements.txt` so the project is reproducible.

### 4 Write `main.py`

Create `main.py` with a FastAPI app and three endpoints:

- `GET /hello` — returns `{"message": "Hello, FastAPI!"}`.
- `GET /hello/{name}` — takes a path parameter `name: str` and returns a greeting using that name.
- `GET /health` — returns `{"status": "ok"}` (you'll keep and reuse this endpoint across the whole module).

### 5 Run the server

Start Uvicorn with auto-reload, pointing it at your `app` object. Read the startup output — note the URL and port it prints.

### 6 Test in the browser

Visit each endpoint directly (e.g. `http://127.0.0.1:8000/hello` and `/hello/YourName` and `/health`) and confirm the JSON responses.

### 7 Explore the auto-docs

Open `http://127.0.0.1:8000/docs`. Expand the `/hello/{name}` endpoint, click *Try it out*, enter a name, and *Execute*. Confirm you get a 200 response with your greeting. Peek at `/redoc` too.

### 8 Create a `.gitignore`

Add a `.gitignore` in `tasks-api` that ignores `.venv/` and `__pycache__/` so you never commit your installed packages.

## ✅ Deliverable — acceptance checklist

- A `tasks-api` folder with an active `.venv` (prompt shows `(.venv)`).
- FastAPI + Uvicorn installed, and a `requirements.txt` listing them.
- `main.py` defines a FastAPI app with `/hello`, `/hello/{name}`, and `/health`.
- `uvicorn main:app --reload` starts the server with no errors.
- All three endpoints return the correct JSON in the browser.
- The Swagger UI at `/docs` lists your endpoints and "Try it out" works.
- A `.gitignore` excludes `.venv/` and `__pycache__/`.

## 🚀 Stretch goals (optional)

- Add a `GET /` root endpoint that returns a short welcome message and a hint to visit `/docs`.
- Give `/hello/{name}` an optional query parameter `greeting: str = "Hello"` so `/hello/Ada?greeting=Hi` returns "Hi, Ada!". (Preview of Chunk 5.2.)
- Set the app title and description: `FastAPI(title="Tasks API", description="...")` — see how it changes `/docs`.
- Run Uvicorn on a different port with `--port 8001` and confirm the docs move with it.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
