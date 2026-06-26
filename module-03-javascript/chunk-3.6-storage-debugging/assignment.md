*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.6 — Lab: Persist & the Module Checkpoint

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Two parts. **Part A:** make your to-do app remember tasks across reloads with `localStorage`, and practice DevTools debugging. **Part B — the 🏁 Module 3 Checkpoint:** build a fresh **expense tracker** widget that pulls together everything you learned this module.

## Before you start

- Use your Vite to-do project from Chunk 3.5 for Part A (or the Chunk 3.3 plain version if you skipped Vite).
- For Part B, make a new folder, e.g. `module-03-javascript/expense-tracker/`.
- Keep DevTools open (Console + Application/Storage tabs) the whole time.

> **⚠️ Try it yourself first**
>
> Use the load/save pattern and the array methods from earlier chunks. Only open
>
> solution.html
>
> when stuck or to compare.

## Part A — Persist the To-Do App

### 1 Add load & save helpers

In your `store.js` (or top of `todo.js`), add `loadTasks()` and `saveTasks(tasks)` using `JSON.parse`/`JSON.stringify`. Initialize the tasks array from `loadTasks()`, with `[]` as the fallback when nothing is saved.

### 2 Save on every change

Call `saveTasks(tasks)` at the end of `addTask`, `toggleTask`, and `removeTask` so storage always matches the current list.

### 3 Prove it persists

Add a few tasks, mark one done, then **reload the page**. They should all reappear exactly as you left them, including completed state.

### 4 Inspect & debug with DevTools

Open the *Application/Storage* tab and find your key — confirm the JSON value updates as you add/remove tasks. Then set a **breakpoint** inside `addTask` (or add a `debugger;` line), add a task, and step through to watch the array change.

## 🏁 Part B — Module 3 Checkpoint: Expense Tracker

Build a small but complete **expense tracker** from scratch — a single page (`expenses.html` + `expenses.js`, or a Vite project if you prefer). It records what you spend, shows a running total, and remembers everything across reloads.

### 5 Build the form & layout

Create a form with a **description** text input, an **amount** number input, and an "Add expense" button. Below it: a big **total** display and a `<ul>` list of expenses.

### 6 Add expenses (array of objects)

On submit, validate the inputs (non-empty description, amount is a positive number with `Number(...)`), then push an expense object `{ id, description, amount }` into an array. Clear the form afterward.

> **💡 Convert & validate the amount**
>
> Number inputs still give you a
>
> string
>
> . Use
>
> Number(amountInput.value)
>
> and reject it if
>
> isNaN(amount)
>
> or
>
> amount <= 0
>
> .

### 7 Render the list & compute the total

Render each expense as a list item showing its description, formatted amount, and a delete button. Use `reduce` to sum all amounts and show the total (formatted to 2 decimals, e.g. `$142.50`).

### 8 Delete expenses

Each item's delete button removes that expense (by `id`) and re-renders, updating the total.

### 9 Persist with localStorage

Save the expenses array to `localStorage` after every add/delete, and load it on startup. Reload the page — your expenses and total must survive.

### 10 Polish

Show a friendly empty state ("No expenses yet"), and handle the total being `$0.00` when the list is empty. Make sure there are no Console errors.

## ✅ Deliverable — acceptance checklist

**Part A — Persistent to-do:**

- Tasks (and their done state) survive a page reload via `localStorage`.
- Storage is updated on add, toggle, and delete.
- You inspected the stored JSON in DevTools and used a breakpoint or `debugger;`.

**Part B — Expense tracker (Checkpoint):**

- A form adds an expense (description + positive numeric amount); invalid input is rejected.
- Expenses are stored as an array of objects and rendered as a list.
- A running total is computed with `reduce` and formatted to 2 decimals.
- Each expense can be deleted, updating the total.
- Expenses persist across reloads via `localStorage` (JSON serialized).
- Sensible empty state and no Console errors.

## 🚀 Stretch goals (optional)

- Add a **category** dropdown and show a per-category breakdown (group with `reduce`).
- Add income vs expense (signed amounts) and show a **balance** that goes red when negative.
- Show each expense's date (`new Date().toLocaleDateString()`).
- Build it as a Vite project split into `store.js` / `ui.js` / `main.js` like Chunk 3.5.
- Add a "Clear all" button that empties the list and storage (with a confirm dialog).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
