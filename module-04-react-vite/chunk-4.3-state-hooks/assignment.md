*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.3 — Lab: The To-Do App, in React

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Rebuild the to-do app you made in Module 3 — but this time in React, using `useState`. The user can **add** a task, **toggle** it complete, and **delete** it. Notice how you never call `document.querySelector` or `appendChild` once.

## Before you start

- Work in your `recipe-box` project, or scaffold a fresh one — your call. Run `npm run dev`.
- Plan your components: a `TodoApp` that owns the state, a `TodoForm` to add, and a `TodoList`/`TodoItem` to display.

> **⚠️ Try it yourself first**
>
> You've done a to-do app before — this time the challenge is the React way (state, not the DOM). Reach for the solution only when stuck.

## Tasks

### 1 Hold the list in state

In a `TodoApp` component, create state for the list: `const [todos, setTodos] = useState([])`. Each todo is an object like `{ id, text, done }`.

### 2 Build the add form (controlled input)

Add a `<form>` with a controlled text `<input>` (its `value` from state, updated `onChange`). On submit, call `preventDefault()`, add a new todo immutably, and clear the input. Don't add empty/whitespace-only tasks.

### 3 Render the list

Map over `todos` to render each one with its `text`, a checkbox/toggle, and a delete button. Remember a unique `key`.

### 4 Toggle complete

Clicking a todo (or its checkbox) flips its `done` flag. Update state immutably with `.map()`. Show completed items with a strikethrough (a CSS class applied conditionally).

### 5 Delete a todo

A "✕" button removes that todo. Update state immutably with `.filter()` on the `id`.

### 6 Lift state up

Split the UI into at least two child components (e.g. `TodoForm` and `TodoList`) and keep the `todos` state in the parent `TodoApp`. Pass data down as props and pass handlers (`onAdd`, `onToggle`, `onDelete`) down too.

### 7 Show a count

Display how many tasks are left (e.g. "2 of 5 done"). Derive it from state — don't store a separate counter.

## ✅ Deliverable — acceptance checklist

- Adding a task via the form appends it to the list and clears the input.
- Empty/whitespace-only submissions are ignored.
- Clicking a task toggles its done state with a visible strikethrough.
- The ✕ button removes the correct task.
- The list lives in state in a parent component; children get props (data + handlers).
- A live count of completed/total tasks is derived from state.
- No direct DOM manipulation anywhere; the console is warning-free (keys present).

## 🚀 Stretch goals (optional)

- Add filter buttons: *All / Active / Completed* (store the current filter in state, derive the visible list).
- Add an "edit" mode that turns a todo's text into a controlled input.
- Add a "Clear completed" button.
- Persist the list to `localStorage` (a taste of Chunk 4.4's `useEffect` — or do it inside your handlers for now).
- Disable the Add button when the input is empty.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
