*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.5 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll scaffold Vite, then write four files: `index.html`, `src/store.js`, `src/ui.js`, and `src/main.js`. Each step has the exact code and what to expect. Final files are at the bottom.

### 1 Scaffold & run Vite

```bash
npm create vite@latest todo-vite -- --template vanilla
cd todo-vite
npm install
npm run dev
```

**Expected:** Vite prints something like:

```
  VITE v5.x.x  ready in 320 ms

  ➜  Local:   http://localhost:5173/
```

Open that URL — you'll see Vite's starter page. Leave `npm run dev` running in the terminal while you work.

> **⚠️ "command not found" or old Node?**
>
> If
>
> npm create vite
>
> fails, check
>
> node -v
>
> is 20 or newer. The
>
> --
>
> before
>
> --template
>
> is required so npm forwards the flag to Vite, not to npm itself.

### 2 Replace `index.html`

The scaffold's `index.html` sits at the project root. Swap its body for the to-do markup, keeping the module script tag Vite expects.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>To-Do (Vite)</title>
</head>
<body>
  <h1>My To-Do</h1>
  <form id="todo-form">
    <input id="todo-input" type="text" placeholder="What needs doing?" autocomplete="off">
    <button type="submit">Add</button>
  </form>
  <p id="count"></p>
  <ul id="todo-list"></ul>

  <script type="module" src="/src/main.js"></script>
</body>
</html>
```

### 3 `src/store.js` — the data

Owns the tasks array and the operations on it. Notice: **zero DOM code**. It just manages state and hands back the current list.

```javascript
let tasks = [];

export function getTasks() {
  return tasks;
}

export function addTask(text) {
  tasks.push({ id: crypto.randomUUID(), text, done: false });
}

export function toggleTask(id) {
  tasks = tasks.map(t =>
    t.id === id ? { ...t, done: !t.done } : t
  );
}

export function removeTask(id) {
  tasks = tasks.filter(t => t.id !== id);
}
```

> **💡 Recognize the array methods?**
>
> map
>
> and
>
> filter
>
> from Chunk 3.2 are doing the real work here. Toggling returns a new array with one task flipped; removing returns a new array without the matching id.

### 4 `src/ui.js` — the view

Turns data into DOM. It rebuilds the whole list from the tasks array each render — simpler and more reliable than surgically patching nodes, and it sets us up perfectly for persistence in 3.6.

```javascript
export function renderTasks(tasks, listEl) {
  listEl.innerHTML = "";                 // clear, then rebuild
  tasks.forEach(task => {
    const li = document.createElement("li");
    li.dataset.id = task.id;             // remember which task this is
    if (task.done) li.classList.add("done");

    const span = document.createElement("span");
    span.textContent = task.text;
    span.classList.add("task-text");

    const del = document.createElement("button");
    del.textContent = "✕";
    del.classList.add("delete-btn");

    li.appendChild(span);
    li.appendChild(del);
    listEl.appendChild(li);
  });
}

export function updateCount(tasks, countEl) {
  const remaining = tasks.filter(t => !t.done).length;
  countEl.textContent = `${remaining} task(s) left`;
}
```

> **📝 data-id is the link**
>
> Storing
>
> li.dataset.id = task.id
>
> writes a
>
> data-id
>
> attribute on the element. When the user clicks,
>
> main.js
>
> reads it back to know which task in the store to toggle or remove.

### 5 `src/main.js` — the glue

Imports both modules, selects the elements, and wires events. A single `render()` redraws everything from the current store after any change.

```python
import { getTasks, addTask, toggleTask, removeTask } from "./store.js";
import { renderTasks, updateCount } from "./ui.js";

const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const count = document.querySelector("#count");

function render() {
  const tasks = getTasks();
  renderTasks(tasks, list);
  updateCount(tasks, count);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (text === "") return;
  addTask(text);
  input.value = "";
  input.focus();
  render();
});

list.addEventListener("click", (event) => {
  const li = event.target.closest("li");
  if (!li) return;
  const id = li.dataset.id;
  if (event.target.matches(".delete-btn")) {
    removeTask(id);
  } else if (event.target.matches(".task-text")) {
    toggleTask(id);
  }
  render();
});

render();   // initial paint
```

### 6 Verify hot reload & build

With the dev server running, edit the count text in `ui.js` (e.g. `"${remaining} to go"`) and save. **Expected:** the page updates instantly — no reload. Then:

```bash
npm run build      # creates dist/
npm run preview    # serves the production build locally
```

**Expected:** `build` finishes with a summary of generated files and no errors.

## 📄 Final project structure

```
todo-vite/
├── index.html
├── package.json
├── src/
│   ├── main.js     ← glue / entry point
│   ├── store.js    ← data & logic
│   └── ui.js       ← DOM rendering
└── (node_modules/, gitignored)
```

> **💡 Optional CSS**
>
> To style it, create
>
> src/style.css
>
> with the same rules from Chunk 3.3, then add
>
> import "./style.css";
>
> at the top of
>
> main.js
>
> . Vite bundles it automatically — no
>
> <link>
>
> needed.

## 🧰 Troubleshooting

- **Blank page, "Failed to resolve module specifier".** Check your import paths start with `./` and end in `.js`.
- **Edits don't show.** Make sure `npm run dev` is still running and you're viewing the `localhost` URL, not a double-clicked file.
- **`crypto.randomUUID is not a function`.** Very old browser — update it, or use `Date.now() + Math.random()` for ids.
- **Clicks do nothing.** Confirm each `<li>` gets a `data-id` and that `main.js` reads `li.dataset.id`.

## 🎉 You're done

Your to-do app now runs on the same professional toolchain real teams use: npm, ES modules, and a Vite dev server with hot reload. The data/view/glue split you built is exactly the mental model you'll carry into React in Module 4.

**Up next → Chunk 3.6: Browser Storage & Debugging** — you'll make this app remember tasks across reloads with `localStorage`, learn to debug with DevTools, and then build the Module 3 checkpoint widget.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
