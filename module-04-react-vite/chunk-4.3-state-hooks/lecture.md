*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.3 — State & Events with Hooks (useState)

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What **state** is and why props alone aren't enough.
- The **`useState`** hook — giving a component memory.
- Handling **events** in React (`onClick`, `onSubmit`, `onChange`).
- **Controlled inputs** — making React the source of truth for form fields.
- Updating arrays of state immutably, and **lifting state up** to share it.

In the lab you'll rebuild your Module 3 to-do app in React — and feel how much less DOM code it takes.

## 1. Props vs. state

So far your components have been static: data comes in as **props** (read-only, from the parent) and gets rendered. But interactive UI needs to *remember* things that change over time: the text in an input, whether a menu is open, the list of to-dos. That remembered, changeable data is **state**.

| Props | State |
| --- | --- |
| Passed in from the parent | Owned by the component itself |
| Read-only | Changeable (via a setter) |
| Like function arguments | Like the component's memory |

> **📝 The key rule**
>
> When state changes, React
>
> re-renders
>
> the component — it calls your function again with the new value and updates the DOM for you. You never touch the DOM directly. Change the data, the screen follows.

## 2. The `useState` hook

You add state with the `useState` hook. A "hook" is just a special function (its name starts with `use`) that lets a component tap into React features. Import it from `react`:

```python
import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

Unpack that one line — `const [count, setCount] = useState(0)`:

- `useState(0)` declares a state variable with an **initial value** of `0`.
- It returns a pair (array destructuring): the **current value** (`count`) and a **setter function** (`setCount`).
- Calling `setCount(newValue)` updates the value *and* tells React to re-render.

> **⚠️ Never assign state directly**
>
> count = count + 1
>
> does nothing useful — React won't notice and won't re-render.
>
> Always
>
> use the setter:
>
> setCount(count + 1)
>
> . The setter is what schedules the re-render.

## 3. Handling events

In Module 3 you wrote `button.addEventListener("click", ...)`. In React you attach handlers right in JSX with camelCase props like `onClick`, and you pass a **function** (not a call):

```jsx
// ✅ pass the function
<button onClick={handleClick}>Save</button>

// ✅ or an inline arrow function
<button onClick={() => setCount(count + 1)}>+1</button>

// ❌ this CALLS handleClick immediately on render — wrong
<button onClick={handleClick()}>Save</button>
```

Handlers receive the React **event object**, just like the DOM event you've seen:

```html
function SearchBox() {
  function handleSubmit(event) {
    event.preventDefault(); // stop the browser reloading the page
    console.log("submitted!");
  }
  return <form onSubmit={handleSubmit}>...</form>;
}
```

> **💡 preventDefault still matters**
>
> Forms still try to reload the page on submit by default. Call
>
> event.preventDefault()
>
> in your
>
> onSubmit
>
> handler to keep your SPA from refreshing — same concept as vanilla JS.

## 4. Controlled inputs

To read what a user types, you make the input a **controlled component**: its `value` comes from state, and an `onChange` handler writes every keystroke back into state. React becomes the single source of truth.

```javascript
function NameField() {
  const [name, setName] = useState("");

  return (
    <input
      value={name}
      onChange={(e) => setName(e.target.value)}
      placeholder="Your name"
    />
  );
}
```

Every keystroke fires `onChange` → `setName` updates state → React re-renders → the input shows the new `value`. The state and the input can never drift apart.

## 5. Updating arrays & objects immutably

To-do apps keep a list in state. The catch: you must **not mutate** the existing array — React decides whether to re-render by checking if you handed it a *new* array reference. Create a new array instead of pushing into the old one.

```sql
const [todos, setTodos] = useState([]);

// ✅ ADD — build a new array with the spread operator
setTodos([...todos, newTodo]);

// ✅ REMOVE — filter returns a new array
setTodos(todos.filter((t) => t.id !== id));

// ✅ UPDATE one item — map returns a new array
setTodos(todos.map((t) =>
  t.id === id ? { ...t, done: !t.done } : t
));

// ❌ DON'T mutate — React may not re-render
todos.push(newTodo);          // wrong
todos[0].done = true;         // wrong
```

You already know `map`, `filter`, and spread from Chunk 3.2. Here they become your everyday tools for "change state without mutating it".

> **📝 Why immutable?**
>
> React compares the old and new state by reference. If you mutate the same array, the reference is unchanged and React assumes nothing happened. A brand-new array (
>
> [...todos, x]
>
> ) signals "this changed, re-render".

## 6. Lifting state up

Where should the to-do list live? If a `<TodoForm>` adds items and a `<TodoList>` displays them, they both need access to the same array. The answer: put the state in their **closest common parent** and pass it down — state lives "up", data and handlers flow "down" as props.

```jsx
function TodoApp() {
  const [todos, setTodos] = useState([]);

  function addTodo(text) {
    setTodos([...todos, { id: Date.now(), text, done: false }]);
  }

  return (
    <>
      <TodoForm onAdd={addTodo} />        {/* pass a handler down */}
      <TodoList items={todos} />          {/* pass data down */}
    </>
  );
}
```

The parent owns the state. `TodoForm` doesn't store the list — it just calls `onAdd(text)`. `TodoList` doesn't own the list — it just renders the `items` prop. This one-way flow (data down, events up) keeps large apps predictable.

> **💡 Generate ids**
>
> Each todo needs a stable
>
> key
>
> for the list.
>
> Date.now()
>
> or
>
> crypto.randomUUID()
>
> both make easy unique ids when you create the item.

## 7. The whole loop, end to end

Here's the cycle every interactive React app runs:

1. Component renders using current state.
2. User does something → an event handler fires.
3. The handler calls a state setter with a new value.
4. React re-renders the component with the new state and patches the DOM.
5. Back to step 1.

Compare this to Module 3, where *you* manually found elements and rewrote them. React collapses all of that into "call the setter".

## ✅ Recap

- **State** is a component's changeable memory; changing it triggers a re-render.
- `const [value, setValue] = useState(initial)` — read `value`, change it only via `setValue`.
- Events use camelCase props (`onClick`, `onSubmit`) and take a function; call `e.preventDefault()` on form submit.
- **Controlled inputs**: `value` from state + `onChange` setting state.
- Update arrays/objects **immutably** with spread/`map`/`filter`, never `push`/direct assignment.
- **Lift state up** to the common parent; pass data and handlers down as props.

**Next:** open `assignment.html` and rebuild the to-do app in React.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
