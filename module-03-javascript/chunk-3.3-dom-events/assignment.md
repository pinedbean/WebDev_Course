*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.3 — Lab: Build a To-Do App

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build an interactive to-do list in **vanilla JavaScript**: a text box to add tasks, the ability to mark a task **complete** by clicking it, and a button to **remove** each task. This `todo.html` + `todo.js` is the project we'll refactor (3.5) and persist (3.6) for the rest of Module 3 — so build it cleanly.

## Before you start

- Make a folder, e.g. `~/Desktop/webdev-course/module-03-javascript/todo-app/`.
- Create `todo.html` and `todo.js` in it.
- You may add a little CSS in a `<style>` block — enough to make completed items look "done" (e.g. strikethrough).

> **⚠️ Try it yourself first**
>
> Use the lecture's patterns (select → create → append → listen). Only open
>
> solution.html
>
> when stuck or to compare.

## Tasks

### 1 Build the HTML structure

In `todo.html`, create: a heading, a `<form>` containing a text `<input>` and an "Add" submit button, and an empty `<ul>` where tasks will appear. Give the form, input, and list `id`s so you can select them. Load `todo.js` with a `<script>` before `</body>`.

### 2 Select your elements

At the top of `todo.js`, grab the form, the input, and the `<ul>` with `querySelector` and store them in `const`s.

### 3 Add a task on submit

Listen for the form's `submit` event. Call `preventDefault()`. Read and `.trim()` the input value; if it's empty, do nothing. Otherwise create an `<li>` containing the task text and a delete button, append it to the list, and clear the input.

> **💡 Structure each item**
>
> Put the text in a
>
> <span>
>
> and add a
>
> <button>
>
> with a class like
>
> delete-btn
>
> . That makes it easy to tell "complete" clicks from "delete" clicks later.

### 4 Mark complete by clicking

Using **event delegation** on the `<ul>`, when the task text is clicked, toggle a `done` class on that `<li>`. Style `.done` in your CSS (e.g. `text-decoration: line-through; opacity:.6;`).

### 5 Remove a task

In the same delegated click handler, if the clicked element is a delete button, remove its containing `<li>`. Use `event.target.matches(".delete-btn")` and `closest("li")`.

### 6 Show a live count

Display how many tasks remain (not completed). Add a small element (e.g. a `<p id="count">`) and write a `updateCount()` function that counts `<li>` items without the `done` class, calling it whenever tasks change.

## ✅ Deliverable — acceptance checklist

- `todo.html` opens in the browser and loads `todo.js` with no Console errors.
- Typing a task and pressing Enter (or clicking Add) appends it to the list and clears the box.
- Empty/whitespace-only input is ignored.
- Clicking a task's text toggles a completed (strikethrough) look via a `done` class.
- Each task has a working delete button that removes only that task.
- A live counter shows the number of remaining (incomplete) tasks.
- Delete/complete work for tasks added after page load (event delegation).

## 🚀 Stretch goals (optional)

- Add a "Clear completed" button that removes all `.done` items at once.
- Prevent duplicate tasks (ignore a task whose text already exists).
- Add a checkbox to each item instead of clicking the text, and toggle `done` from its `change` event.
- Show a friendly "No tasks yet" message when the list is empty.

> **📝 Keep this folder**
>
> Don't delete
>
> todo-app/
>
> when you finish — Chunk 3.5 refactors this exact app into ES modules under Vite, and Chunk 3.6 makes it remember your tasks with
>
> localStorage
>
> .

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
