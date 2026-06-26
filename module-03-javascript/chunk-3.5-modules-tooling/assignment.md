*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.5 — Lab: To-Do App on Vite + Modules

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Take the to-do app from Chunk 3.3 and give it a professional setup: scaffold a **Vite** project, then split the single `todo.js` into **ES modules** (data, UI, glue). You'll run it with `npm run dev` and watch hot reload in action.

## Before you start

- Confirm Node + npm are installed: `node -v` and `npm -v` should each print a version (Node 20+).
- Have your Chunk 3.3 `todo.html` / `todo.js` handy to copy logic from.
- Open your terminal in `~/Desktop/webdev-course/module-03-javascript/`.

> **⚠️ Try it yourself first**
>
> Follow the lecture's structure (store / ui / main). Only open
>
> solution.html
>
> when stuck or to compare.

## Tasks

### 1 Scaffold a Vite project

Run the commands below, then confirm the starter app opens at the printed `localhost` URL:

```bash
npm create vite@latest todo-vite -- --template vanilla
cd todo-vite
npm install
npm run dev
```

### 2 Clean out the starter

Vite's vanilla template fills `src/main.js` and `index.html` with demo content. Empty `src/main.js`, and replace the `<body>` of `index.html` with your to-do markup (form + input + Add button, a count element, and an empty `<ul>`). Keep the `<script type="module" src="/src/main.js"></script>` tag.

### 3 Create `src/store.js` (the data)

This module owns an array of task objects (each like `{ id, text, done }`) and exports functions to change it: `getTasks()`, `addTask(text)`, `toggleTask(id)`, and `removeTask(id)`. No DOM code here at all.

> **💡 Give tasks an id**
>
> Generate a unique id with
>
> crypto.randomUUID()
>
> or
>
> Date.now()
>
> . Working with ids (instead of DOM elements) makes toggling and removing reliable.

### 4 Create `src/ui.js` (the view)

Export a `renderTasks(tasks, listEl)` function that clears the list and rebuilds the `<li>` items from the data, plus an `updateCount(tasks, countEl)` helper. This module only touches the DOM — it doesn't own the data.

### 5 Wire it up in `src/main.js` (the glue)

Import from both modules. Select the form/input/list/count. On submit → `addTask` then re-render. On click → `toggleTask` or `removeTask` then re-render. Render once at startup.

### 6 Verify hot reload & build

With `npm run dev` running, change some text in `ui.js` and save — the page should update without a manual reload. Then stop the server and run `npm run build` to confirm it produces a `dist/` folder with no errors.

## ✅ Deliverable — acceptance checklist

- A Vite project that starts with `npm run dev` and serves the to-do app at `localhost`.
- Code is split into at least three modules: `store.js`, `ui.js`, and `main.js`.
- `store.js` exports the data functions and contains **no** DOM code.
- `ui.js` exports rendering functions and owns **no** data.
- `main.js` imports from both and wires up the events.
- Add / complete / delete and the live count all still work.
- Saving a source file triggers hot reload; `npm run build` succeeds.

## 🚀 Stretch goals (optional)

- Move the CSS into `src/style.css` and `import "./style.css"` from `main.js` — see Vite handle CSS imports.
- Add a `filter.js` module with All / Active / Completed filtering, imported by `main.js`.
- Add a small npm package (e.g. `npm i nanoid`) and use it to generate task ids — your first real dependency.
- Make a `README.md` documenting how to run the project (you'll thank yourself later).

> **📝 Keep this project**
>
> Chunk 3.6 adds
>
> localStorage
>
> persistence to this exact modular app — so keep the
>
> todo-vite
>
> folder.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
