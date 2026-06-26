*Full-Stack Web Dev · Module 5 — Backend with FastAPI*

# Chunk 5.5 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll run two servers, enable CORS on the backend, and build a small React UI that does live CRUD against the Tasks API. Frontend files we'll touch:

```text
tasks-frontend/
├── .env
├── .gitignore
└── src/
    ├── api.js        (new)
    ├── App.jsx       (replaced)
    └── App.css       (a few styles)
```

### 1 Run both servers

Terminal 1 — backend (in `tasks-api`, venv active):

```bash
uvicorn app.main:app --reload
```

Terminal 2 — frontend (in `tasks-frontend`):

```bash
npm run dev
```

Note the exact frontend origin Vite prints (usually `http://localhost:5173/`). Before adding CORS, a fetch to the API will fail in the console with something like:

```
Access to fetch at 'http://localhost:8000/tasks' from origin
'http://localhost:5173' has been blocked by CORS policy:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

### 2 Enable CORS in `app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import health, tasks

settings = get_settings()
app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(tasks.router)
```

If your browser uses `127.0.0.1`, widen the setting in `app/config.py`:

```
cors_origins: list[str] = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

Uvicorn auto-reloads. The CORS error should disappear on the next request.

### 3 Frontend `.env`

```
# tasks-frontend/.env
VITE_API_URL=http://localhost:8000
```

Add it to `.gitignore`, then **restart** `npm run dev` (Vite reads `.env` only at startup).

### 4 `src/api.js`

```javascript
const BASE_URL = import.meta.env.VITE_API_URL;

export async function getTasks() {
  const res = await fetch(`${BASE_URL}/tasks`);
  if (!res.ok) throw new Error(`Failed to load tasks (${res.status})`);
  return res.json();
}

export async function createTask(title) {
  const res = await fetch(`${BASE_URL}/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
  if (!res.ok) throw new Error(`Failed to create task (${res.status})`);
  return res.json();
}

export async function toggleTask(id, completed) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) throw new Error(`Failed to update task (${res.status})`);
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${BASE_URL}/tasks/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error(`Failed to delete task (${res.status})`);
}
```

### 5 `src/App.jsx`

```python
import { useEffect, useState } from "react";
import { getTasks, createTask, toggleTask, deleteTask } from "./api";
import "./App.css";

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  async function load() {
    try {
      setError(null);
      setTasks(await getTasks());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  async function handleAdd(e) {
    e.preventDefault();
    const t = title.trim();
    if (!t) return;
    try {
      await createTask(t);
      setTitle("");
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleToggle(task) {
    try {
      await toggleTask(task.id, !task.completed);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    try {
      await deleteTask(id);
      load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <main className="app">
      <h1>✅ Tasks</h1>

      <form onSubmit={handleAdd} className="add-form">
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New task…"
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">⚠️ {error}</p>}
      {loading && <p>Loading…</p>}
      {!loading && tasks.length === 0 && <p>No tasks yet — add one above.</p>}

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task.id} className={task.completed ? "done" : ""}>
            <label>
              <input
                type="checkbox"
                checked={task.completed}
                onChange={() => handleToggle(task)}
              />
              {task.title}
            </label>
            <button onClick={() => handleDelete(task.id)}>🗑</button>
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;
```

### 6 A little `src/App.css`

```
.app { max-width: 480px; margin: 40px auto; font-family: system-ui, sans-serif; }
.add-form { display: flex; gap: 8px; margin-bottom: 16px; }
.add-form input { flex: 1; padding: 8px; }
.task-list { list-style: none; padding: 0; }
.task-list li { display: flex; justify-content: space-between; align-items: center;
  padding: 8px; border-bottom: 1px solid #e2e8f0; }
.task-list li.done label { text-decoration: line-through; color: #94a3b8; }
.error { color: #b91c1c; }
```

### 7 Verify end to end

| Action | Expected |
| --- | --- |
| Type a title, click Add | Task appears in the list (POST 201) |
| Check a task's box | Strikethrough; persists on refresh (PATCH 200) |
| Click 🗑 | Task disappears (DELETE 204) |
| Create a task in `/docs`, refresh the app | It shows up — same backend |
| Restart Uvicorn, refresh the app | List is empty — in-memory reset |
| Network tab on a POST | An `OPTIONS` preflight, then the `POST` |

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| CORS error persists after adding middleware | The browser origin doesn't match `cors_origins`. Add the exact one (mind `localhost` vs `127.0.0.1`) and let Uvicorn reload. |
| `import.meta.env.VITE_API_URL` is `undefined` | The var must start with `VITE_`, live in the frontend root `.env`, and you must restart `npm run dev`. |
| `Failed to fetch` / connection refused | The backend isn't running, or the URL/port is wrong. Confirm Uvicorn is up on `:8000`. |
| POST returns 422 | Body shape is wrong — send `{"title": "..."}` with `Content-Type: application/json` and `JSON.stringify`. |
| 405 Method Not Allowed on PATCH/DELETE | Check the URL includes the id (`/tasks/3`) and the method string is correct. |
| Checkbox won't stay checked | You must re-fetch (or update state) after the PATCH resolves; ensure `handleToggle` calls `load()`. |

## 🎉 You're done

Frontend and backend now talk: a click in React travels through CORS, Uvicorn, and FastAPI, mutates your data, and returns JSON that updates the UI. That's a real full-stack loop — the same architecture the capstone uses.

**Up next → Chunk 5.6: Error Handling & API Best Practices** — consistent error responses, global exception handlers, pagination, and versioning. It closes with the 🏁 Module 5 Checkpoint: a full CRUD Tasks API consumed by your React frontend.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
