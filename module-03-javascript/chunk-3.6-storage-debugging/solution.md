*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.6 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Part A persists the to-do app; Part B builds the checkpoint expense tracker with complete, copy-pasteable code. Compare with your own work.

## Part A — Persist the To-Do App

### 1 + 2 Load & save in `store.js`

Add the two helpers and call them from your existing operations. Here's the updated `store.js` from Chunk 3.5 — the new lines are the `KEY`, `loadTasks`, `saveTasks`, and the `saveTasks(tasks)` calls:

```javascript
const KEY = "todo-tasks";

function loadTasks() {
  const raw = localStorage.getItem(KEY);
  return raw ? JSON.parse(raw) : [];     // [] when nothing saved
}

function saveTasks(tasks) {
  localStorage.setItem(KEY, JSON.stringify(tasks));
}

let tasks = loadTasks();                  // initialize FROM storage

export function getTasks() {
  return tasks;
}

export function addTask(text) {
  tasks.push({ id: crypto.randomUUID(), text, done: false });
  saveTasks(tasks);
}

export function toggleTask(id) {
  tasks = tasks.map(t => (t.id === id ? { ...t, done: !t.done } : t));
  saveTasks(tasks);
}

export function removeTask(id) {
  tasks = tasks.filter(t => t.id !== id);
  saveTasks(tasks);
}
```

> **💡 Nothing else changes**
>
> Because
>
> ui.js
>
> and
>
> main.js
>
> only ever ask the store for tasks, they're untouched. That's the payoff of putting all storage in one module.

### 3 Prove it persists

**Expected:** add tasks, mark one done, reload — everything returns exactly as left. If not, see the next step.

### 4 Debug with DevTools

Open *Application → Local Storage* and watch the `todo-tasks` value change as you edit. To step through code, add a breakpoint or a line:

```javascript
export function addTask(text) {
  debugger;     // execution pauses here when DevTools is open
  tasks.push({ id: crypto.randomUUID(), text, done: false });
  saveTasks(tasks);
}
```

> **⚠️ "Unexpected token in JSON"**
>
> If a parse error appears, your stored value is corrupt (e.g. you saved a non-JSON string earlier). Clear it: in the Console run
>
> localStorage.removeItem("todo-tasks")
>
> and reload.

## 🏁 Part B — Module 3 Checkpoint: Expense Tracker

A complete single-file build (HTML + inline JS). It uses functions, an array of objects, `reduce`, the DOM/events, and `localStorage` — the whole module in one widget. Steps below explain the key pieces; the full file follows.

### 5 + 6 Form & add (with validation)

```javascript
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const description = descInput.value.trim();
  const amount = Number(amountInput.value);

  if (description === "" || isNaN(amount) || amount <= 0) {
    alert("Enter a description and a positive amount.");
    return;
  }

  expenses.push({ id: crypto.randomUUID(), description, amount });
  save();
  render();
  form.reset();
  descInput.focus();
});
```

### 7 Render & total with `reduce`

```jsx
function render() {
  list.innerHTML = "";
  if (expenses.length === 0) {
    list.innerHTML = "<li class='empty'>No expenses yet</li>";
  } else {
    expenses.forEach(exp => {
      const li = document.createElement("li");
      li.dataset.id = exp.id;
      li.innerHTML =
        `<span>${exp.description}</span>` +
        `<span>$${exp.amount.toFixed(2)} ` +
        `<button class="delete-btn">✕</button></span>`;
      list.appendChild(li);
    });
  }
  const total = expenses.reduce((sum, e) => sum + e.amount, 0);
  totalEl.textContent = `$${total.toFixed(2)}`;
}
```

> **📝 innerHTML here is safe-ish**
>
> We use
>
> innerHTML
>
> for brevity. It's acceptable here because the values are short and local, but remember from Chunk 3.3: for untrusted user input prefer
>
> textContent
>
> /
>
> createElement
>
> to avoid injection.

### 8 Delete (event delegation)

```javascript
list.addEventListener("click", (event) => {
  if (event.target.matches(".delete-btn")) {
    const id = event.target.closest("li").dataset.id;
    expenses = expenses.filter(e => e.id !== id);
    save();
    render();
  }
});
```

### 9 Persist with localStorage

```javascript
const KEY = "expenses";
function load() {
  const raw = localStorage.getItem(KEY);
  return raw ? JSON.parse(raw) : [];
}
function save() {
  localStorage.setItem(KEY, JSON.stringify(expenses));
}
let expenses = load();   // restore on startup
```

**Expected:** add a few expenses, reload — the list and total are still there.

## 📄 Complete `expenses.html` (self-contained)

```jsx
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Expense Tracker</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         max-width:520px;margin:40px auto;padding:0 16px;color:#1e293b;}
    h1{font-size:24px;}
    form{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:16px;}
    input{padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:16px;}
    #desc{flex:1;min-width:180px;}
    #amount{width:120px;}
    button{cursor:pointer;border:none;border-radius:8px;padding:10px 14px;
           background:#2563eb;color:#fff;font-size:15px;}
    .total{font-size:28px;font-weight:700;margin:8px 0 16px;}
    ul{list-style:none;padding:0;}
    li{display:flex;justify-content:space-between;align-items:center;
       padding:10px 12px;border:1px solid #e2e8f0;border-radius:8px;margin:6px 0;}
    li span:last-child{display:flex;align-items:center;gap:10px;font-variant-numeric:tabular-nums;}
    .delete-btn{background:#ef4444;padding:4px 10px;}
    .empty{justify-content:center;color:#94a3b8;border-style:dashed;}
  </style>
</head>
<body>
  <h1>💸 Expense Tracker</h1>
  <form id="expense-form">
    <input id="desc" type="text" placeholder="Description" autocomplete="off">
    <input id="amount" type="number" placeholder="Amount" step="0.01" min="0">
    <button type="submit">Add expense</button>
  </form>
  <div>Total: <span class="total" id="total">$0.00</span></div>
  <ul id="expense-list"></ul>

  <script>
    const KEY = "expenses";
    const form = document.querySelector("#expense-form");
    const descInput = document.querySelector("#desc");
    const amountInput = document.querySelector("#amount");
    const list = document.querySelector("#expense-list");
    const totalEl = document.querySelector("#total");

    function load() {
      const raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : [];
    }
    function save() {
      localStorage.setItem(KEY, JSON.stringify(expenses));
    }

    let expenses = load();

    function render() {
      list.innerHTML = "";
      if (expenses.length === 0) {
        list.innerHTML = "<li class='empty'>No expenses yet</li>";
      } else {
        expenses.forEach(exp => {
          const li = document.createElement("li");
          li.dataset.id = exp.id;
          li.innerHTML =
            `<span>${exp.description}</span>` +
            `<span>$${exp.amount.toFixed(2)} ` +
            `<button class="delete-btn">✕</button></span>`;
          list.appendChild(li);
        });
      }
      const total = expenses.reduce((sum, e) => sum + e.amount, 0);
      totalEl.textContent = `$${total.toFixed(2)}`;
    }

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const description = descInput.value.trim();
      const amount = Number(amountInput.value);
      if (description === "" || isNaN(amount) || amount <= 0) {
        alert("Enter a description and a positive amount.");
        return;
      }
      expenses.push({ id: crypto.randomUUID(), description, amount });
      save();
      render();
      form.reset();
      descInput.focus();
    });

    list.addEventListener("click", (event) => {
      if (event.target.matches(".delete-btn")) {
        const id = event.target.closest("li").dataset.id;
        expenses = expenses.filter(e => e.id !== id);
        save();
        render();
      }
    });

    render();
  </script>
</body>
</html>
```

> **💡 Want the modular version?**
>
> To match Chunk 3.5, split this into a Vite project:
>
> store.js
>
> (the
>
> expenses
>
> array +
>
> load
>
> /
>
> save
>
> /
>
> add
>
> /
>
> remove
>
> /
>
> getTotal
>
> ),
>
> ui.js
>
> (
>
> renderExpenses
>
> ), and
>
> main.js
>
> (the glue). Same logic, cleaner structure.

## 🧰 Troubleshooting

- **Total shows `NaN`.** An amount was stored as a string. Always `Number(amountInput.value)` before pushing, and reject `isNaN`.
- **Expenses don't survive reload.** You forgot to call `save()` after a change, or you're reading with the wrong `KEY`. Check *Application → Local Storage*.
- **Delete removes the wrong item.** Confirm each `<li>` has a unique `data-id` and you filter by that exact id.
- **Everything broke after editing storage manually.** Run `localStorage.clear()` in the Console and reload to start fresh.

## 🎉 Module 3 complete!

You've gone from `console.log("Hello")` to a persistent, modular, network-aware set of interactive apps. In this module you learned:

- **3.1–3.2** — the JavaScript language: variables, control flow, functions, and transforming data with `map`/`filter`/`reduce`.
- **3.3** — the DOM & events: building an interactive to-do app by hand.
- **3.4** — async/await & fetch: loading live data with loading/error states.
- **3.5** — ES modules, npm, and Vite: structuring real projects.
- **3.6** — localStorage & debugging: persistence and DevTools — capped by your expense tracker checkpoint.

**Up next → Module 4: React + Vite.** Everything you just did by hand — state, events, rendering lists — React makes declarative and reusable. You're ready.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
