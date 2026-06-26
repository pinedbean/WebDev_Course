*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.2 — Lab: Connect the Tasks API to SQLite

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Wire your Module 5 Tasks API to a real SQLite database using SQLAlchemy. You'll add a `database.py` (engine, session, Base, `get_db`), a `models.py` (the `Task` ORM model), make `TaskRead` ORM-aware, create the table on startup, and prove it works by reading a seeded task *from the database* through your API. (Full CRUD comes in 6.3 — today is about the connection.)

## Before you start

- Have your Module 5 `tasks-api` project open, with its virtual environment active: `cd tasks-api
source .venv/bin/activate      # Windows: .venv\Scripts\activate`
- Install SQLAlchemy into the venv: `pip install "sqlalchemy>=2.0"`
- No Module 5 project handy? The solution includes a minimal `main.py` you can start from.

> **⚠️ Try it yourself first**
>
> Build from the lecture and your memory of the four SQLAlchemy pieces. Only open
>
> solution.html
>
> when stuck or to compare at the end.

## Tasks

### 1 Create `app/database.py`

Set up the database wiring in one module: the `engine` (SQLite URL `sqlite:///./tasks.db` with `check_same_thread=False`), a `SessionLocal` factory, a `Base` class, and a `get_db()` dependency generator that yields a session and closes it in a `finally` block.

### 2 Create `app/models.py`

Define a `Task` SQLAlchemy model (table `tasks`) that imports `Base` from `database.py`. Include all five columns using `Mapped[...]` + `mapped_column(...)`: `id` (primary key), `title` (required), `description` (nullable), `completed` (bool, default False), and `created_at` (datetime, `server_default=func.now()`).

### 3 Make `TaskRead` ORM-aware

In your Pydantic schemas, add `model_config = ConfigDict(from_attributes=True)` to `TaskRead` so FastAPI can serialize an ORM `Task` object directly.

### 4 Create the table on startup

In `main.py`, import `Base`, `engine`, and your models, then call `Base.metadata.create_all(bind=engine)` when the app starts so the `tasks` table exists. (This is temporary — Alembic replaces it in 6.3.)

> **💡 Import models before create_all**
>
> create_all
>
> only creates tables for models that have actually been imported. Make sure
>
> models.py
>
> is imported in
>
> main.py
>
> before you call it, or no table will appear.

### 5 Read from the database in one endpoint

Update `GET /tasks` to take `db: Session = Depends(get_db)` and return all `Task` rows from the database (instead of the in-memory list). Set its `response_model=list[TaskRead]`.

### 6 Seed one row so there's something to read

So your endpoint returns real data, insert one task into the database — either with the SQLite CLI (`sqlite3 tasks.db`, then an `INSERT`) or by adding a tiny one-off startup snippet that creates a `Task` if the table is empty. Either is fine for this lab.

### 7 Run it & verify

Start the server and confirm three things:

```bash
uvicorn app.main:app --reload
```

- A `tasks.db` file appears in your project folder.
- `GET /tasks` at `http://127.0.0.1:8000/docs` returns your seeded task.
- Stop the server and start it again — the task is **still there** (persistence!).

## ✅ Deliverable — acceptance checklist

- `app/database.py` exists with `engine`, `SessionLocal`, `Base`, and `get_db()`.
- `app/models.py` defines a `Task` model mapped to the `tasks` table with all five columns.
- `TaskRead` has `ConfigDict(from_attributes=True)`.
- Running the app creates a `tasks.db` file and the `tasks` table.
- `GET /tasks` reads from the database (uses `Depends(get_db)`) and returns at least one seeded task.
- The data survives a server restart.

## 🚀 Stretch goals (optional)

- Open `tasks.db` with `sqlite3 tasks.db` and run `.schema tasks` — confirm SQLAlchemy generated the columns you expected.
- Make `GET /health` actually check the database by running a trivial query (e.g. `SELECT 1`) inside `get_db` and returning `{"status": "ok", "db": "ok"}`.
- Move the database URL into an environment variable / settings object instead of hard-coding it.
- Add a `GET /tasks/{task_id}` that reads a single row with `db.get(Task, task_id)` and returns 404 if missing.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
