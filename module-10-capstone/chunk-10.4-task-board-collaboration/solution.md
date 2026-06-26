*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We build the board out of small components. New files:

```text
frontend/src/
├── App.jsx                 (add /projects/:id route)
├── pages/Board.jsx
└── components/
    ├── TaskCard.jsx
    ├── TaskForm.jsx
    └── MembersBar.jsx
plus board styles appended to index.css
```

### 1 Add the route

In `App.jsx`, add the Board inside the protected Layout routes:

```python
// src/App.jsx  (additions)
import Board from "./pages/Board";
// ...
<Route element={<Layout />}>
  <Route path="/" element={<Projects />} />
  <Route path="/projects/:id" element={<Board />} />
</Route>
```

### 2 TaskCard component

```jsx
// src/components/TaskCard.jsx
export default function TaskCard({ task, members, onMove, onEdit, onDelete }) {
  const assignee = members.find((m) => m.user_id === task.assignee_id);
  const overdue =
    task.due_date && task.status !== "done" &&
    task.due_date < new Date().toISOString().slice(0, 10);

  return (
    <article className="task-card">
      <h4>{task.title}</h4>
      {task.description && <p className="muted small">{task.description}</p>}
      <div className="meta">
        <span className="chip">{assignee ? assignee.name : "Unassigned"}</span>
        {task.due_date && (
          <span className={overdue ? "due overdue" : "due"}>📅 {task.due_date}</span>
        )}
      </div>
      <div className="card-actions">
        <select value={task.status}
                onChange={(e) => onMove(task, e.target.value)}>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <button className="link" onClick={() => onEdit(task)}>Edit</button>
        <button className="link danger" onClick={() => onDelete(task)}>Delete</button>
      </div>
    </article>
  );
}
```

### 3 TaskForm component (create + edit)

```python
// src/components/TaskForm.jsx
import { useState } from "react";

export default function TaskForm({ task, members, onSave, onCancel }) {
  const [form, setForm] = useState({
    title: task?.title ?? "",
    description: task?.description ?? "",
    status: task?.status ?? "todo",
    assignee_id: task?.assignee_id ?? "",
    due_date: task?.due_date ?? "",
  });
  const [error, setError] = useState("");

  const update = (field, value) => setForm((f) => ({ ...f, [field]: value }));

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      await onSave({
        title: form.title,
        description: form.description,
        status: form.status,
        assignee_id: form.assignee_id === "" ? null : Number(form.assignee_id),
        due_date: form.due_date === "" ? null : form.due_date,
      });
    } catch (err) { setError(err.message); }
  }

  return (
    <form className="task-form" onSubmit={submit}>
      <h3>{task ? "Edit task" : "New task"}</h3>
      {error && <p className="error">{error}</p>}
      <input value={form.title} required placeholder="Title"
             onChange={(e) => update("title", e.target.value)} />
      <textarea value={form.description} placeholder="Description"
                onChange={(e) => update("description", e.target.value)} />
      <div className="row">
        <label>Status
          <select value={form.status}
                  onChange={(e) => update("status", e.target.value)}>
            <option value="todo">To Do</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>
        </label>
        <label>Assignee
          <select value={form.assignee_id}
                  onChange={(e) => update("assignee_id", e.target.value)}>
            <option value="">Unassigned</option>
            {members.map((m) => (
              <option key={m.user_id} value={m.user_id}>{m.name}</option>
            ))}
          </select>
        </label>
        <label>Due date
          <input type="date" value={form.due_date ?? ""}
                 onChange={(e) => update("due_date", e.target.value)} />
        </label>
      </div>
      <div className="row">
        <button type="submit">Save</button>
        <button type="button" className="ghost-dark" onClick={onCancel}>Cancel</button>
      </div>
    </form>
  );
}
```

### 4 MembersBar component

```python
// src/components/MembersBar.jsx
import { useState } from "react";

export default function MembersBar({ members, isOwner, onInvite }) {
  const [email, setEmail] = useState("");
  const [error, setError] = useState("");

  async function submit(e) {
    e.preventDefault();
    setError("");
    try {
      await onInvite(email);
      setEmail("");
    } catch (err) { setError(err.message); }
  }

  return (
    <div className="members-bar">
      <div className="chips">
        {members.map((m) => (
          <span key={m.user_id} className="chip">
            {m.name}{m.role === "owner" ? " (owner)" : ""}
          </span>
        ))}
      </div>
      {isOwner && (
        <form className="invite" onSubmit={submit}>
          <input type="email" value={email} placeholder="Invite by email" required
                 onChange={(e) => setEmail(e.target.value)} />
          <button>+ Invite</button>
        </form>
      )}
      {error && <p className="error small">{error}</p>}
    </div>
  );
}
```

### 5 The Board page (ties it together)

```python
// src/pages/Board.jsx
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import TaskCard from "../components/TaskCard";
import TaskForm from "../components/TaskForm";
import MembersBar from "../components/MembersBar";

const COLUMNS = [
  { key: "todo", title: "To Do" },
  { key: "in_progress", title: "In Progress" },
  { key: "done", title: "Done" },
];

export default function Board() {
  const { id } = useParams();
  const { user } = useAuth();

  const [project, setProject] = useState(null);
  const [members, setMembers] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [filters, setFilters] = useState({ status: "", assignee_id: "" });
  const [editing, setEditing] = useState(null);   // task | "new" | null
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // load project + members once
  useEffect(() => {
    Promise.all([
      api(`/projects/${id}`),
      api(`/projects/${id}/members`),
    ])
      .then(([p, m]) => { setProject(p); setMembers(m); })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [id]);

  // (re)load tasks whenever filters change
  useEffect(() => {
    const params = new URLSearchParams();
    if (filters.status) params.set("status", filters.status);
    if (filters.assignee_id) params.set("assignee_id", filters.assignee_id);
    const qs = params.toString() ? `?${params}` : "";
    api(`/projects/${id}/tasks${qs}`).then(setTasks).catch((e) => setError(e.message));
  }, [id, filters]);

  async function saveTask(data) {
    if (editing && editing !== "new") {
      const updated = await api(`/projects/${id}/tasks/${editing.id}`,
        { method: "PATCH", body: data });
      setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
    } else {
      const created = await api(`/projects/${id}/tasks`,
        { method: "POST", body: data });
      setTasks((prev) => [...prev, created]);
    }
    setEditing(null);
  }

  async function moveTask(task, status) {
    const updated = await api(`/projects/${id}/tasks/${task.id}`,
      { method: "PATCH", body: { status } });
    setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
  }

  async function deleteTask(task) {
    if (!confirm(`Delete "${task.title}"?`)) return;
    await api(`/projects/${id}/tasks/${task.id}`, { method: "DELETE" });
    setTasks((prev) => prev.filter((t) => t.id !== task.id));
  }

  async function invite(email) {
    const member = await api(`/projects/${id}/members`,
      { method: "POST", body: { email } });
    setMembers((prev) => [...prev, member]);
  }

  if (loading) return <p>Loading board…</p>;
  if (error) return <p className="error">{error}</p>;

  const isOwner = project && user && project.owner_id === user.id;

  return (
    <section>
      <div className="page-head">
        <h1>{project.name}</h1>
        <button onClick={() => setEditing("new")}>+ New Task</button>
      </div>

      <MembersBar members={members} isOwner={isOwner} onInvite={invite} />

      <div className="filters">
        <select value={filters.status}
                onChange={(e) => setFilters((f) => ({ ...f, status: e.target.value }))}>
          <option value="">All statuses</option>
          <option value="todo">To Do</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <select value={filters.assignee_id}
                onChange={(e) => setFilters((f) => ({ ...f, assignee_id: e.target.value }))}>
          <option value="">All assignees</option>
          {members.map((m) => (
            <option key={m.user_id} value={m.user_id}>{m.name}</option>
          ))}
        </select>
        <button className="ghost-dark"
                onClick={() => setFilters({ status: "", assignee_id: "" })}>
          Clear
        </button>
      </div>

      {editing && (
        <div className="modal-backdrop" onClick={() => setEditing(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <TaskForm
              task={editing === "new" ? null : editing}
              members={members}
              onSave={saveTask}
              onCancel={() => setEditing(null)}
            />
          </div>
        </div>
      )}

      <div className="board">
        {COLUMNS.map((col) => {
          const colTasks = tasks.filter((t) => t.status === col.key);
          return (
            <div key={col.key} className="column">
              <h2>{col.title} <span className="count">{colTasks.length}</span></h2>
              {colTasks.map((t) => (
                <TaskCard key={t.id} task={t} members={members}
                          onMove={moveTask} onEdit={setEditing} onDelete={deleteTask} />
              ))}
            </div>
          );
        })}
      </div>
    </section>
  );
}
```

> **📝 One `editing` state, three jobs**
>
> editing
>
> is
>
> null
>
> (closed),
>
> "new"
>
> (create), or a task object (edit). The same modal + form serve all three. Less state, fewer bugs.

### 6 Board styles (append to `index.css`)

```
/* board */
.page-head { display: flex; align-items: center; justify-content: space-between; }
.board {
  display: grid; gap: 16px;
  grid-template-columns: repeat(3, 1fr); margin-top: 16px;
}
@media (max-width: 760px) { .board { grid-template-columns: 1fr; } }
.column { background: #eef2f7; border-radius: 12px; padding: 12px; min-height: 120px; }
.column h2 { font-size: 15px; border: 0; margin: 4px 6px 12px; }
.count { background: #cbd5e1; border-radius: 999px; padding: 1px 8px; font-size: 12px; }
.task-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
  padding: 12px; margin-bottom: 10px;
}
.task-card h4 { margin: 0 0 6px; }
.small { font-size: 13px; }
.meta { display: flex; gap: 8px; align-items: center; margin: 6px 0; flex-wrap: wrap; }
.chip { background: #e0e7ff; color: #3730a3; border-radius: 999px; padding: 2px 10px; font-size: 12px; }
.due { font-size: 12px; color: #475569; }
.overdue { color: #b91c1c; font-weight: 600; }
.card-actions { display: flex; gap: 8px; align-items: center; margin-top: 8px; }
.card-actions select { padding: 4px; }
.link { background: none; color: #2563eb; padding: 4px; }
.link.danger { color: #b91c1c; }
.members-bar { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin: 8px 0 16px; }
.invite { display: flex; gap: 8px; }
.filters { display: flex; gap: 10px; margin-bottom: 8px; }
.ghost-dark { background: #e2e8f0; color: #1e293b; }
.modal-backdrop {
  position: fixed; inset: 0; background: rgba(15,23,42,.4);
  display: grid; place-items: center; z-index: 10;
}
.modal { background: #fff; border-radius: 14px; padding: 22px; width: 460px; max-width: 92vw; }
.task-form { display: grid; gap: 10px; }
.task-form .row { display: flex; gap: 10px; }
.task-form label { display: grid; gap: 4px; font-size: 13px; flex: 1; }
.task-form textarea { min-height: 70px; padding: 8px; border: 1px solid #cbd5e1; border-radius: 8px; }
```

### 7 Verify end-to-end

1. Open a project → board shows three columns.
2. "+ New Task" → fill the form, assign someone, set a due date → card appears in To Do.
3. Change its status dropdown to In Progress → card jumps columns; reload → it stays.
4. Edit it → change the title → saves. Delete one → it's gone.
5. Filter by assignee → only their tasks show; Clear → all return.
6. As owner, invite a second user by email → chip appears, and they show up in the assignee dropdown.
7. Log in as that user (private window) → the project is on their list and they can use the board.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| 422 when creating a task | Sending `assignee_id: ""` or `due_date: ""`. Normalize empty strings to `null` in the form's submit. |
| Card doesn't move after status change | You must replace the task in state with the PATCH response (`map`), not mutate it. |
| Invite always 404 | The invited email must belong to a *registered* user. Register them first. |
| Invite form missing | It only shows for the owner. Confirm `project.owner_id === user.id`. |
| Filters don't apply | The tasks `useEffect` must depend on `filters` and rebuild the query string. |

## 🎉 Done — what's next

TaskFlow is now a real, collaborative app: a working kanban board with assignees, due dates, filtering, and team invitations — fully wired to your secured backend. This is the feature you'll demo.

- ✅ Status columns derived from one task list.
- ✅ Create / edit / assign / due date / move / delete.
- ✅ Server-side filtering + member invitations.

**Up next → Chunk 10.5: Logging, Observability & Hardening.** You'll make it production-trustworthy with structured logging, request IDs, health checks, an error boundary, and a security pass.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
