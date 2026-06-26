*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.1 — Python Refresher & FastAPI Setup

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What a **backend / API** is and how it fits with the React frontend you already built.
- How to isolate a project's packages with a **virtual environment** (venv) and install with `pip`.
- Just-enough modern Python: functions, **type hints**, and dicts.
- What **ASGI** and **Uvicorn** are, and why FastAPI needs them.
- How to write your first endpoint and explore the **auto-generated `/docs`**.

In the lab you'll create the `tasks-api` project, install FastAPI + Uvicorn, and serve a `/hello` endpoint.

## 1. Frontend, meet backend

Through Module 4 you built **frontends** — code that runs in the browser and renders UI. But where does the *data* come from? In Chunk 4.4 you fetched recipes from someone else's public API. Now you'll build your **own** API.

A **backend** is a program that runs on a server, waits for HTTP requests, does work (reads/writes data, applies rules), and sends back responses — usually **JSON**. An **API** (Application Programming Interface) is the set of URLs (**endpoints**) your backend exposes.

| Layer | Runs where | Job | Built with |
| --- | --- | --- | --- |
| Frontend | The user's browser | Show UI, capture input | React + Vite (Module 4) |
| Backend / API | A server | Logic, validation, data | FastAPI (this module) |
| Database | A server | Persist data | SQLite (Module 6) |

Across Modules 5–7 you'll build one backend: a **Tasks API**. This module keeps data **in memory** (a Python list) so we can focus on the API itself. Module 6 swaps in a real SQLite database; Module 7 adds login. It's a stepping stone toward the Module 10 capstone, **TaskFlow**.

> **📝 Why FastAPI?**
>
> It's modern, fast, and uses plain Python type hints to
>
> automatically
>
> validate data and generate interactive documentation. You write less code and get more safety — perfect for learning and for real production apps.

## 2. Virtual environments & pip

Python projects need third-party packages (like FastAPI). If you install everything globally, two projects can end up needing different versions of the same package and clash. The fix is a **virtual environment**: a private, per-project folder of packages.

Python ships with the `venv` tool. You create one folder (conventionally `.venv`), **activate** it, then any `pip install` lands inside that folder only.

```bash
# 1. Create a project folder and move into it
mkdir tasks-api
cd tasks-api

# 2. Create a virtual environment named .venv
python3 -m venv .venv

# 3. Activate it  (macOS / Linux — zsh/bash)
source .venv/bin/activate

# 3. Activate it  (Windows PowerShell)
.venv\Scripts\Activate.ps1
```

Once active, your prompt shows `(.venv)` at the front. Now install packages:

```bash
pip install fastapi uvicorn
```

| Command | What it does |
| --- | --- |
| `python3 -m venv .venv` | Creates the isolated environment folder `.venv`. |
| `source .venv/bin/activate` | Turns it on (macOS/Linux). The prompt gains `(.venv)`. |
| `pip install <pkg>` | Installs a package into the active venv. |
| `pip freeze > requirements.txt` | Saves the exact versions so others can reproduce them. |
| `deactivate` | Turns the venv off. |

> **⚠️ Activate every session**
>
> The venv is only active in the terminal where you ran
>
> activate
>
> . Open a new terminal? Run
>
> source .venv/bin/activate
>
> again. If
>
> pip install
>
> or
>
> uvicorn
>
> "isn't found", you almost certainly forgot to activate.

> **💡 Keep `.venv` out of Git**
>
> Add
>
> .venv/
>
> to your
>
> .gitignore
>
> . You commit
>
> requirements.txt
>
> (the recipe), never the installed packages (the cooked meal).

## 3. Just-enough Python

You know JavaScript, so Python will feel familiar. Here are the differences that matter for FastAPI.

### Functions & indentation

Python uses a colon and **indentation** instead of curly braces. No semicolons.

```python
def greet(name):
    message = "Hello, " + name
    return message

print(greet("Ada"))   # Hello, Ada
```

### Type hints

You can annotate what types a function expects and returns. Python does not *enforce* these at runtime, but FastAPI **reads them** to validate requests and build docs. This is the secret sauce — get comfortable writing them.

```python
def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}"      # f-string = JS template literal
```

Common types: `int`, `float`, `str`, `bool`, `list`, `dict`. A value that may be missing is written `str | None` ("a string or nothing"). A list of strings is `list[str]`.

### Dicts & lists

A Python `dict` is like a JS object; a `list` is like a JS array. JSON maps onto these almost 1:1.

```
task = {
    "id": 1,
    "title": "Buy milk",
    "completed": False,        # Python uses True / False / None
}

tasks = [task]                 # a list holding one dict
print(task["title"])           # Buy milk
print(len(tasks))              # 1
```

| JavaScript | Python |
| --- | --- |
| `const x = 1;` | `x = 1` |
| `true / false / null` | `True / False / None` |
| ``Hi ${name}`` | `f"Hi {name}"` |
| `obj.key / obj["key"]` | `obj["key"]` |
| `// comment` | `# comment` |

## 4. ASGI & Uvicorn — what actually runs your API

FastAPI is a *framework*: it describes your endpoints, but it doesn't open a network port by itself. It needs a **server** to accept HTTP connections and hand requests to your code. That server is **Uvicorn**.

They talk through a standard called **ASGI** (Asynchronous Server Gateway Interface) — a contract that says "here's how a Python web app and a Python web server pass requests and responses to each other." Because FastAPI speaks ASGI, you can run it under any ASGI server (Uvicorn is the popular default).

```text
Browser / React  ──HTTP──>  Uvicorn (ASGI server)  ──>  FastAPI (your code)
                                                            │
Browser / React  <──JSON──   Uvicorn                 <──   returns a dict
```

You start everything with one command, pointing Uvicorn at your app object:

```bash
uvicorn main:app --reload
```

- `main` — the file `main.py`.
- `app` — the variable inside it (your FastAPI instance).
- `--reload` — auto-restart when you save changes (dev only).

## 5. Your first endpoint

Here is a complete, runnable FastAPI app. Create `main.py` with this:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello, FastAPI!"}
```

Three ideas to unpack:

- `app = FastAPI()` creates the application object Uvicorn will run.
- `@app.get("/hello")` is a **decorator** — it attaches the function below it to **GET requests at `/hello`**. (A decorator is just "wrap this function with extra behavior". You'll mostly copy the pattern.)
- The function returns a Python `dict`. FastAPI automatically converts it to a JSON response. No manual serialization needed.

Run it with `uvicorn main:app --reload`, then visit `http://127.0.0.1:8000/hello` in your browser. You'll see:

```python
{"message":"Hello, FastAPI!"}
```

### Path parameters (a sneak peek)

Put a name in `{curly braces}` in the path and accept it as a typed function argument. FastAPI converts and validates it for you (Chunk 5.2 goes deep on this):

```python
@app.get("/hello/{name}")
def hello_name(name: str):
    return {"message": f"Hello, {name}!"}

# GET /hello/Ada  ->  {"message": "Hello, Ada!"}
```

## 6. The magic: interactive docs at `/docs`

Because FastAPI knows your paths, methods, and type hints, it generates live API documentation for free. With the server running, open:

```
http://127.0.0.1:8000/docs
```

This is **Swagger UI**. Every endpoint is listed, and you can click *"Try it out"* → *"Execute"* to send real requests right from the browser — no Postman or curl needed. There's a second, cleaner view at `/redoc`, and the raw machine-readable spec at `/openapi.json`.

> **💡 This is your new best friend**
>
> Throughout Module 5 you'll test endpoints at
>
> /docs
>
> constantly. It updates the instant you save your code (thanks to
>
> --reload
>
> ). Keep that tab open.

> **📝 127.0.0.1 vs localhost**
>
> Both mean "this same computer". Uvicorn prints
>
> http://127.0.0.1:8000
>
> ; you can type
>
> localhost:8000
>
> instead — they're equivalent.
>
> :8000
>
> is the
>
> port
>
> Uvicorn listens on.

## ✅ Recap

- A **backend/API** answers HTTP requests with JSON; your Tasks API will be the backend for your React app.
- A **venv** isolates a project's packages; `source .venv/bin/activate` turns it on, then `pip install fastapi uvicorn`.
- Python uses indentation, `True/False/None`, f-strings, and **type hints** that FastAPI reads to validate and document.
- **Uvicorn** (an ASGI server) runs your FastAPI app: `uvicorn main:app --reload`.
- A `@app.get("/path")` function that returns a dict becomes a JSON endpoint, fully documented at `/docs`.

**Next:** open `assignment.html` and stand up your own `tasks-api` server with a `/hello` endpoint.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
