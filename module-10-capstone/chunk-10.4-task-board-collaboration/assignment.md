*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.4 — Lab: Build the Collaborative Task Board

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build TaskFlow's headline feature: a kanban board at `/projects/:id` with To Do / In Progress / Done columns. Create, edit, assign, and set due dates on tasks; move tasks between columns; filter by status and assignee; and invite teammates to collaborate. Wire everything to the API you built in 10.2.

## Before you start

- Backend (10.2) running at `:8000`; frontend (10.3) running at `:5173` with the API client + auth context in place.
- You have at least two registered users (so you can test assigning & inviting).
- Open the lecture's worked examples for the board grouping and form-normalization patterns.

> **⚠️ Build it yourself first**
>
> This is the big one — give it a real attempt before opening the solution. The pieces are all things you've done: fetch on mount, controlled forms, list rendering, PATCH on change.

## Tasks

### 1 Add the Board route

Create `src/pages/Board.jsx` and add it to `App.jsx` at `/projects/:id` (inside the protected Layout routes). Read the id with `useParams`.

### 2 Load project + members + tasks

On mount (and when the id changes), fetch the project, its members, and its tasks. Show loading and error states. Display the project name as the page title.

### 3 Render the three columns

Group tasks by status and render To Do / In Progress / Done columns, each listing its task cards. Show a count per column.

### 4 Task card with move & delete

Build `TaskCard.jsx` showing title, assignee name (looked up from members), and due date. Add a status control that PATCHes the task and updates state (the card jumps to the new column). Add a delete button (DELETE + remove from state).

### 5 Create & edit form

Build a single `TaskForm.jsx` used for both creating (a "+ New Task" button) and editing (the card's Edit button). Fields: title, description, status, assignee (select of members + Unassigned), due date. Normalize empty assignee/due to `null` before sending.

### 6 Filtering

Add filter controls for status and assignee. When a filter changes, re-fetch tasks using the backend's `?status=` / `?assignee_id=` query params. Include a "Clear filters" action.

### 7 Members bar & invite

Build `MembersBar.jsx` showing member chips. If the current user is the owner, show an invite-by-email form that POSTs to `/projects/:id/members` and appends the new member. Handle "no such user" (404) and "already a member" (409) errors gracefully.

### 8 End-to-end collaboration test

As user A: open a project, invite user B, create tasks, assign some to B, set due dates, move tasks across columns, and filter. Then log in as user B (in a private window) and confirm B sees the project, the board, and can move/create tasks.

## ✅ Deliverable — acceptance checklist

- Board at `/projects/:id` shows three status columns with the project's tasks.
- Creating a task adds it to the correct column; it persists across reloads.
- Editing a task (title/desc/assignee/due) saves and reflects immediately.
- Changing a task's status moves its card to the right column (persisted via PATCH).
- Deleting a task removes it from the board and the backend.
- Filtering by status and by assignee works (server-side query params) and can be cleared.
- Members are listed; the owner can invite by email; errors (404/409) are shown clearly.
- An invited second user can open the shared board and manage tasks.

## 🚀 Stretch goals (optional)

- Add drag-and-drop between columns (HTML5 DnD or a small library) that PATCHes status on drop.
- Highlight overdue tasks (due_date before today) in red.
- Show the form in a modal overlay instead of inline.
- Add an "assigned to me" quick filter using the current user's id.
- Optimistic UI: move the card instantly, then roll back if the PATCH fails.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
