*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.4 — Task Board & Collaboration

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to render a **kanban board**: group tasks by status into To Do / In Progress / Done columns.
- How to **create, edit, assign, and set due dates** on tasks with a reusable form/modal.
- How to **move a task** between columns by PATCHing its status, and keep the UI in sync.
- How to **filter** the board by status and assignee using the backend query params.
- How to build **collaboration**: list members and invite teammates by email.

This is the headline feature. The lab delivers a working, collaborative task board.

## 1. The board as a derived view

The backend stores a flat list of tasks, each with a `status`. The board is just a *view* of that list, grouped into columns. We don't store columns — we **derive** them from the data on every render. This is the key mental model: one source of truth (the task array), three presentations (the columns).

```javascript
const COLUMNS = [
  { key: "todo",        title: "To Do" },
  { key: "in_progress", title: "In Progress" },
  { key: "done",        title: "Done" },
];

// group once per render
function groupByStatus(tasks) {
  return {
    todo:        tasks.filter((t) => t.status === "todo"),
    in_progress: tasks.filter((t) => t.status === "in_progress"),
    done:        tasks.filter((t) => t.status === "done"),
  };
}
```

Because columns are derived, "moving" a task is simply changing its `status` field — the grouping re-runs and the card appears in the new column. No special move logic needed.

## 2. Board page structure

The Board page (route `/projects/:id`) loads three things on mount: the project (for the title), its members (for assignee dropdowns and the members bar), and its tasks. Then it renders the columns.

```text
src/pages/Board.jsx        the page: loads project + members + tasks, renders columns
src/components/
├── TaskCard.jsx          one task (title, assignee, due date, status buttons)
├── TaskForm.jsx          create/edit form (title, desc, status, assignee, due)
├── MembersBar.jsx        member chips + "Invite" form
└── BoardFilters.jsx      status + assignee filter controls
```

```
// useParams gives us the project id from the URL (Module 4.5)
const { id } = useParams();

useEffect(() => {
  Promise.all([
    api(`/projects/${id}`),
    api(`/projects/${id}/members`),
    api(`/projects/${id}/tasks`),
  ]).then(([project, members, tasks]) => {
    setProject(project); setMembers(members); setTasks(tasks);
  }).catch((e) => setError(e.message));
}, [id]);
```

## 3. The task card & moving status

A card shows the title, the assignee's name (looked up from members), and the due date. It also offers a way to move the task. The simplest, accessible approach (no drag-and-drop library needed for the MVP) is a small status `<select>` or move buttons:

```jsx
function TaskCard({ task, members, onMove, onEdit, onDelete }) {
  const assignee = members.find((m) => m.user_id === task.assignee_id);
  return (
    <article className="task-card">
      <h4>{task.title}</h4>
      <div className="meta">
        <span>{assignee ? assignee.name : "Unassigned"}</span>
        {task.due_date && <span className="due">📅 {task.due_date}</span>}
      </div>
      <select value={task.status}
              onChange={(e) => onMove(task, e.target.value)}>
        <option value="todo">To Do</option>
        <option value="in_progress">In Progress</option>
        <option value="done">Done</option>
      </select>
      <button onClick={() => onEdit(task)}>Edit</button>
      <button onClick={() => onDelete(task)}>Delete</button>
    </article>
  );
}
```

And `onMove` in the Board patches the backend and updates local state:

```javascript
async function moveTask(task, status) {
  const updated = await api(`/projects/${id}/tasks/${task.id}`,
    { method: "PATCH", body: { status } });
  setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)));
}
```

> **📝 Update by replacing, not mutating**
>
> We rebuild the array with
>
> map
>
> , swapping the changed task for the server's response. Never mutate state in place — React compares references to decide what to re-render.

## 4. Create & edit with one form

One `TaskForm` handles both create and edit — if you pass an existing task, it pre-fills; otherwise it's blank. The fields map exactly to the API: title, description, status, `assignee_id` (a select of members, plus "Unassigned"), and `due_date` (a native date input).

```jsx
function TaskForm({ task, members, onSave, onCancel }) {
  const [form, setForm] = useState({
    title: task?.title ?? "",
    description: task?.description ?? "",
    status: task?.status ?? "todo",
    assignee_id: task?.assignee_id ?? "",
    due_date: task?.due_date ?? "",
  });

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }));
  }

  function submit(e) {
    e.preventDefault();
    onSave({
      ...form,
      // normalize empty selections to null for the API
      assignee_id: form.assignee_id === "" ? null : Number(form.assignee_id),
      due_date: form.due_date === "" ? null : form.due_date,
    });
  }

  return (
    <form className="task-form" onSubmit={submit}>
      <input value={form.title} required placeholder="Title"
             onChange={(e) => update("title", e.target.value)} />
      <textarea value={form.description} placeholder="Description"
                onChange={(e) => update("description", e.target.value)} />
      <select value={form.assignee_id}
              onChange={(e) => update("assignee_id", e.target.value)}>
        <option value="">Unassigned</option>
        {members.map((m) => (
          <option key={m.user_id} value={m.user_id}>{m.name}</option>
        ))}
      </select>
      <input type="date" value={form.due_date}
             onChange={(e) => update("due_date", e.target.value)} />
      <button>Save</button>
      <button type="button" onClick={onCancel}>Cancel</button>
    </form>
  );
}
```

> **⚠️ Empty string vs null**
>
> HTML form values are always strings — an unselected assignee is
>
> ""
>
> , not
>
> null
>
> . The backend expects
>
> null
>
> or a number. Normalize at the boundary (in
>
> submit
>
> ) so the API always gets clean types.

## 5. Filtering — let the backend do the work

Your 10.2 tasks endpoint already accepts `?status=` and `?assignee_id=`. So filtering is just changing the URL you fetch. When a filter changes, re-fetch:

```javascript
const [filters, setFilters] = useState({ status: "", assignee_id: "" });

useEffect(() => {
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.assignee_id) params.set("assignee_id", filters.assignee_id);
  const qs = params.toString() ? `?${params.toString()}` : "";
  api(`/projects/${id}/tasks${qs}`).then(setTasks).catch(...);
}, [id, filters]);
```

> **💡 Server-side vs client-side filtering**
>
> For a small board you could filter the array in the browser. Filtering on the server (the query params) is the pattern that scales — it sends less data and reuses the validated backend logic. We use it here to practice the real-world approach.

## 6. Collaboration: members & invitations

The members bar shows who's on the project and lets the owner invite by email. It posts to `/projects/{id}/members`; the backend (10.2) looks up the email, adds a membership, or returns 404/409. On success, we append the new member so dropdowns immediately include them.

```javascript
async function invite(email) {
  try {
    const member = await api(`/projects/${id}/members`,
      { method: "POST", body: { email } });
    setMembers((prev) => [...prev, member]);
  } catch (err) {
    // 404 = no such user, 409 = already a member, 403 = not owner
    setInviteError(err.message);
  }
}
```

This is the collaboration loop closing: a second user you invited (10.2 testing) logs in, sees the shared project on their Projects page, opens the board, and can create/move tasks — because the membership row grants them access through the same dependencies you wrote in 10.2.

## 7. Keeping it honest about access

The UI should reflect permissions, but the **backend is the real gate**. Non-owners shouldn't see the Invite form (hide it when `project.owner_id !== user.id`), but even if someone forged the request, the `get_project_for_owner` dependency rejects it. UI checks are for usability; server checks are for security.

```jsx
const { user } = useAuth();
const isOwner = project && project.owner_id === user.id;
// ...
{isOwner && <InviteForm onInvite={invite} />}
```

## ✅ Recap

- The board is a **derived view** — group the flat task list by `status` into three columns.
- "Moving" a task = **PATCH its status**; the grouping re-runs automatically.
- One **TaskForm** serves create and edit; normalize empty strings to `null` at the API boundary.
- **Filtering** reuses the backend query params (`?status=`, `?assignee_id=`) and re-fetches on change.
- **Collaboration** = list members + invite by email; UI hides owner-only actions, but the backend dependencies enforce real access.

**Next:** open `assignment.html` and build the full collaborative task board.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
