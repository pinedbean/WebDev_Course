*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Build the `tasks-api` project step by step. Each step gives the exact command/code and the expected result. The complete `main.py` is at the bottom. Your end state:

```text
tasks-api/
├── .venv/              (created by venv; git-ignored)
├── .gitignore
├── main.py
└── requirements.txt
```

### 1 Create the project folder

```bash
mkdir -p ~/Desktop/webdev-course/module-05-fastapi/tasks-api
cd ~/Desktop/webdev-course/module-05-fastapi/tasks-api
code .
```

You're now inside `tasks-api`, with VS Code open on it.

### 2 Create & activate the venv

```bash
# macOS / Linux (zsh / bash)
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Your prompt should now begin with `(.venv)`. Confirm Python is the venv's copy:

```bash
which python        # macOS/Linux -> .../tasks-api/.venv/bin/python
python --version    # Python 3.11.x or newer
```

> **⚠️ "running scripts is disabled" on Windows**
>
> If PowerShell blocks activation, run once:
>
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
>
> , then activate again.

### 3 Install FastAPI + Uvicorn and freeze

```bash
pip install fastapi uvicorn
```

Expected tail of the output (versions will vary):

```
Successfully installed annotated-types-... fastapi-0.11x.x pydantic-2.x.x
  pydantic-core-2.x.x starlette-0.x.x uvicorn-0.3x.x ...
```

Note FastAPI pulled in **Pydantic 2** and **Starlette** automatically — you'll meet both later. Now save the lockfile:

```bash
pip freeze > requirements.txt
```

### 4 Write `main.py`

Create `main.py` in the project root:

```python
from fastapi import FastAPI

app = FastAPI(title="Tasks API", description="Backend for the WebDev course")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}
```

Note the `name: str` type hint — FastAPI uses it to document the parameter and (in later chunks) to convert/validate it.

### 5 Run the server

```bash
uvicorn main:app --reload
```

Expected output:

```
INFO:     Will watch for changes in these directories: ['.../tasks-api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [#####] using WatchFiles
INFO:     Started server process [#####]
INFO:     Application startup complete.
```

Leave this running. Edits to `main.py` auto-reload. Stop it with `Ctrl`+`C`.

### 6 Test in the browser

| Visit | You should see |
| --- | --- |
| `http://127.0.0.1:8000/health` | `{"status":"ok"}` |
| `http://127.0.0.1:8000/hello` | `{"message":"Hello, FastAPI!"}` |
| `http://127.0.0.1:8000/hello/Ada` | `{"message":"Hello, Ada!"}` |

### 7 Explore the auto-docs

Open `http://127.0.0.1:8000/docs`. You'll see all three endpoints. Expand `GET /hello/{name}` → *Try it out* → type `Ada` → *Execute*. The "Responses" panel shows status `200` and the JSON body. The cleaner read-only docs live at `/redoc`.

### 8 Add `.gitignore`

Create `.gitignore` in the project root:

```
# Python
.venv/
__pycache__/
*.pyc

# Env
.env
```

## 📄 Complete `main.py`

```python
from fastapi import FastAPI

app = FastAPI(title="Tasks API", description="Backend for the WebDev course")

@app.get("/health")
def health_check():
    """Simple liveness check — handy for monitoring later."""
    return {"status": "ok"}

@app.get("/hello")
def say_hello():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `command not found: uvicorn` | The venv isn't active. Run `source .venv/bin/activate` first. Confirm the `(.venv)` prefix. |
| `Error loading ASGI app. Could not import module "main"` | Run Uvicorn from the folder that contains `main.py`, and make sure the file is named exactly `main.py`. |
| `Attribute "app" not found in module "main"` | Your variable must be named `app` (i.e. `app = FastAPI()`), matching `main:app`. |
| `[Errno 48] Address already in use` | Port 8000 is taken (another Uvicorn?). Stop the other one, or run with `--port 8001`. |
| `pip: command not found` / installs go global | Use `python -m pip install ...`, and double-check the venv is active. |
| Browser shows "can't connect" | The server isn't running, or you used the wrong port. Re-check the URL Uvicorn printed. |

## 🎉 You're done

You have a running FastAPI server with interactive docs — your first backend. You learned venvs, `pip`, type hints, and how Uvicorn serves your app.

**Keep this project** — every chunk in Module 5 builds directly on `tasks-api`.

**Up next → Chunk 5.2: Routes, Path & Query Params** — you'll add real CRUD endpoints for an in-memory list of tasks.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
