*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll build a three-component to-do app. State lives in `TodoApp`; `TodoForm` and `TodoList` receive props. Full files are at the bottom. Target structure:

```text
recipe-box/
└── src/
    ├── App.jsx
    └── components/
        ├── TodoApp.jsx
        ├── TodoForm.jsx
        └── TodoList.jsx
```

### 1 State in the parent

In `TodoApp.jsx`, hold the list and the handlers. Each todo is `{ id, text, done }`.

```python
import { useState } from "react";
import TodoForm from "./TodoForm";
import TodoList from "./TodoList";

function TodoApp() {
  const [todos, setTodos] = useState([]);

  function addTodo(text) {
    const newTodo = { id: crypto.randomUUID(), text, done: false };
    setTodos([...todos, newTodo]);
  }

  function toggleTodo(id) {
    setTodos(todos.map((t) =>
      t.id === id ? { ...t, done: !t.done } : t
    ));
  }

  function deleteTodo(id) {
    setTodos(todos.filter((t) => t.id !== id));
  }

  const doneCount = todos.filter((t) => t.done).length;

  return (
    <section className="todo">
      <h2>✅ My Tasks</h2>
      <TodoForm onAdd={addTodo} />
      <p>{doneCount} of {todos.length} done</p>
      <TodoList items={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </section>
  );
}

export default TodoApp;
```

Notice `doneCount` is **derived** from state each render — no separate counter to keep in sync.

### 2 The controlled form

`TodoForm.jsx` owns only the input's text; it reports new todos up via `onAdd`.

```python
import { useState } from "react";

function TodoForm({ onAdd }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;        // ignore empty input
    onAdd(trimmed);
    setText("");                 // clear the field
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a task..."
      />
      <button type="submit" disabled={!text.trim()}>Add</button>
    </form>
  );
}

export default TodoForm;
```

### 3 The list & items

`TodoList.jsx` maps the items and wires each row's buttons to the handlers from props.

```jsx
function TodoList({ items, onToggle, onDelete }) {
  if (items.length === 0) {
    return <p className="empty">No tasks yet — add one above.</p>;
  }

  return (
    <ul className="list">
      {items.map((todo) => (
        <li key={todo.id}>
          <label className={todo.done ? "done" : ""}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() => onToggle(todo.id)}
            />
            {todo.text}
          </label>
          <button onClick={() => onDelete(todo.id)} aria-label="Delete">✕</button>
        </li>
      ))}
    </ul>
  );
}

export default TodoList;
```

> **💡 Empty state**
>
> Returning early with a friendly message when the list is empty is a small touch that makes the app feel finished.

### 4 Wire it into `App`

```python
import TodoApp from "./components/TodoApp";
import "./index.css";

function App() {
  return (
    <main>
      <h1>🍳 Recipe Box</h1>
      <TodoApp />
    </main>
  );
}

export default App;
```

### 5 A little CSS

Add to `src/index.css` for the strikethrough and layout:

```
.todo { max-width: 480px; }
.list { list-style: none; padding: 0; }
.list li { display: flex; align-items: center; gap: 8px; padding: 6px 0; }
.list li button { margin-left: auto; }
.done { text-decoration: line-through; color: #94a3b8; }
.empty { color: #94a3b8; }
```

## 📄 Complete `src/components/TodoApp.jsx`

```python
import { useState } from "react";
import TodoForm from "./TodoForm";
import TodoList from "./TodoList";

function TodoApp() {
  const [todos, setTodos] = useState([]);

  function addTodo(text) {
    setTodos([...todos, { id: crypto.randomUUID(), text, done: false }]);
  }
  function toggleTodo(id) {
    setTodos(todos.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  }
  function deleteTodo(id) {
    setTodos(todos.filter((t) => t.id !== id));
  }

  const doneCount = todos.filter((t) => t.done).length;

  return (
    <section className="todo">
      <h2>✅ My Tasks</h2>
      <TodoForm onAdd={addTodo} />
      <p>{doneCount} of {todos.length} done</p>
      <TodoList items={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
    </section>
  );
}

export default TodoApp;
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Typing in the input does nothing | The input is controlled but missing `onChange`. Add `onChange={(e) => setText(e.target.value)}`. |
| Page reloads when I submit | You forgot `e.preventDefault()` in the submit handler. |
| List doesn't update after adding | You mutated state (`todos.push(...)`). Use `setTodos([...todos, item])`. |
| "A component is changing an uncontrolled input..." | Initialize the input's state to `""`, not `undefined`. |
| Checkbox warning in console | A controlled checkbox needs both `checked` and `onChange`. |

## 🎉 You're done

Compare this to your Module 3 to-do app: no `querySelector`, no `createElement`, no manual DOM syncing. You changed state and React redrew the screen. That's the payoff.

**Up next → Chunk 4.4: Side Effects & Data Fetching** — you'll use `useEffect` to load real recipes from a public API with proper loading and error states.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
