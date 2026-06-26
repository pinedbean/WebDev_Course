*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Build the to-do app piece by piece. Each step explains what to add and why. The two complete files — `todo.html` and `todo.js` — are at the bottom, ready to copy.

### 1 The HTML structure

A form (input + button), an empty list, and a count paragraph. Note the `id`s — they're how the JS finds each piece. The `<script>` goes last so the elements exist before it runs.

```html
<form id="todo-form">
  <input id="todo-input" type="text" placeholder="What needs doing?" autocomplete="off">
  <button type="submit">Add</button>
</form>
<p id="count"></p>
<ul id="todo-list"></ul>

<script src="todo.js"></script>
```

### 2 Select the elements

```javascript
const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const count = document.querySelector("#count");
```

**Expected:** nothing visible yet — but if any of these is `null`, recheck the matching `id` in your HTML.

### 3 Add a task on submit

A helper `createTask(text)` builds one list item; the submit handler validates input and uses it.

```javascript
function createTask(text) {
  const li = document.createElement("li");

  const span = document.createElement("span");
  span.textContent = text;
  span.classList.add("task-text");

  const del = document.createElement("button");
  del.textContent = "✕";
  del.classList.add("delete-btn");

  li.appendChild(span);
  li.appendChild(del);
  return li;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (text === "") return;             // ignore empty input
  list.appendChild(createTask(text));
  input.value = "";
  input.focus();
  updateCount();
});
```

> **⚠️ Page reloads on submit?**
>
> You forgot
>
> event.preventDefault()
>
> . Without it, the form does its default thing — reloading the page and wiping your list.

### 4 + 5 Complete & delete (one delegated listener)

A single click listener on the `<ul>` handles both actions, so it works for tasks added at any time.

```
list.addEventListener("click", (event) => {
  if (event.target.matches(".delete-btn")) {
    event.target.closest("li").remove();      // delete
  } else if (event.target.matches(".task-text")) {
    event.target.closest("li").classList.toggle("done");  // complete
  }
  updateCount();
});
```

**Expected:** clicking the ✕ removes a row; clicking the text strikes it through and back.

### 6 Live count of remaining tasks

```javascript
function updateCount() {
  const remaining = list.querySelectorAll("li:not(.done)").length;
  count.textContent = `${remaining} task(s) left`;
}
updateCount();   // run once at start so it shows "0 task(s) left"
```

**Expected:** the count updates after every add, complete, and delete. The CSS selector `li:not(.done)` counts only incomplete items.

## 📄 Complete `todo.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My To-Do</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         max-width:480px;margin:40px auto;padding:0 16px;color:#1e293b;}
    h1{font-size:24px;}
    form{display:flex;gap:8px;margin-bottom:12px;}
    #todo-input{flex:1;padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:16px;}
    button{cursor:pointer;border:none;border-radius:8px;padding:10px 14px;
           background:#2563eb;color:#fff;font-size:15px;}
    ul{list-style:none;padding:0;}
    li{display:flex;align-items:center;justify-content:space-between;
       gap:10px;padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;margin:6px 0;}
    .task-text{cursor:pointer;flex:1;}
    .done .task-text{text-decoration:line-through;opacity:.55;}
    .delete-btn{background:#ef4444;padding:4px 10px;}
    #count{color:#64748b;font-size:14px;}
  </style>
</head>
<body>
  <h1>My To-Do</h1>
  <form id="todo-form">
    <input id="todo-input" type="text" placeholder="What needs doing?" autocomplete="off">
    <button type="submit">Add</button>
  </form>
  <p id="count"></p>
  <ul id="todo-list"></ul>

  <script src="todo.js"></script>
</body>
</html>
```

## 📄 Complete `todo.js`

```javascript
const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");
const count = document.querySelector("#count");

function createTask(text) {
  const li = document.createElement("li");

  const span = document.createElement("span");
  span.textContent = text;
  span.classList.add("task-text");

  const del = document.createElement("button");
  del.textContent = "✕";
  del.classList.add("delete-btn");

  li.appendChild(span);
  li.appendChild(del);
  return li;
}

function updateCount() {
  const remaining = list.querySelectorAll("li:not(.done)").length;
  count.textContent = `${remaining} task(s) left`;
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (text === "") return;
  list.appendChild(createTask(text));
  input.value = "";
  input.focus();
  updateCount();
});

list.addEventListener("click", (event) => {
  if (event.target.matches(".delete-btn")) {
    event.target.closest("li").remove();
  } else if (event.target.matches(".task-text")) {
    event.target.closest("li").classList.toggle("done");
  }
  updateCount();
});

updateCount();
```

> **💡 Notice the separation**
>
> createTask
>
> only builds an element,
>
> updateCount
>
> only counts, and the listeners wire them to events. Splitting work into small, single-purpose functions is exactly what makes the 3.5 module refactor easy.

## 🎉 You're done

You built a fully interactive app with no framework — selecting elements, creating nodes, handling events, and delegating clicks. This is the foundation that React will later make even easier.

One thing you'll notice: **refresh the page and your tasks vanish.** That's because everything lives in memory. We'll fix that in Chunk 3.6 with `localStorage`.

**Up next → Chunk 3.4: Async JavaScript & Fetch** — loading live data from the network.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
