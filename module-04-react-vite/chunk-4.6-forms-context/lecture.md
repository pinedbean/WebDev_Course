*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.6 — Forms & Shared State (useContext)

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Handling **multi-field forms** cleanly with a single state object.
- Adding **validation** and showing field errors.
- The **prop-drilling** problem and why it gets painful.
- **`useContext`** — sharing state across the whole app without threading props.
- When Context is enough, and when to reach for a dedicated state library.

In the lab you'll build a form that adds items to a **shared favorites list** accessible from any page via Context.

## 1. Multi-field forms with one state object

In 4.3 you controlled a single input. Real forms have many fields. You *could* write a `useState` for each, but it's cleaner to hold the whole form in one object and update it with a single handler:

```python
import { useState } from "react";

function RecipeForm() {
  const [form, setForm] = useState({ title: "", area: "", minutes: "" });

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));   // update one field
  }

  return (
    <form>
      <input name="title"   value={form.title}   onChange={handleChange} />
      <input name="area"    value={form.area}    onChange={handleChange} />
      <input name="minutes" value={form.minutes} onChange={handleChange} />
    </form>
  );
}
```

Two things power this: each input has a `name` matching a key in `form`, and the **computed property** `[name]: value` updates just that key. One handler covers every field.

> **💡 The updater function form**
>
> setForm((prev) => ({ ...prev, [name]: value }))
>
> uses the "functional update" form. When your new state is built from the previous state, passing a function guarantees you're working from the latest value — safer than reading
>
> form
>
> directly.

## 2. Validation

Before accepting a submit, check the fields and collect any errors into state, then render them next to the inputs:

```javascript
const [errors, setErrors] = useState({});

function validate(values) {
  const next = {};
  if (!values.title.trim()) next.title = "Title is required";
  if (Number(values.minutes) <= 0) next.minutes = "Minutes must be positive";
  return next;
}

function handleSubmit(e) {
  e.preventDefault();
  const found = validate(form);
  setErrors(found);
  if (Object.keys(found).length > 0) return;   // stop if invalid
  // ...all good: use the data
}
```

```jsx
<input name="title" value={form.title} onChange={handleChange} />
{errors.title && <span className="field-error">{errors.title}</span>}
```

> **📝 Native validation still helps**
>
> HTML attributes like
>
> required
>
> ,
>
> type="number"
>
> ,
>
> min
>
> , and
>
> maxLength
>
> (from Module 1) give you free, built-in checks. Use them
>
> and
>
> JS validation — native for quick feedback, JS for rules the browser can't express.

## 3. The prop-drilling problem

Imagine a "favorites" feature. The favorites list is needed on the `Recipes` page (to show a ⭐ toggle), on the `RecipeDetail` page (a "Save" button), and on a new `Favorites` page (to list them). The count even shows in the navbar.

With what you know, the state would live high up (in `App`) and you'd pass `favorites` and `toggleFavorite` down through every layer — through `Layout`, into the navbar, into each page, into each card — even through components that don't use them, just to reach the ones that do. That tedious passing-through is called **prop drilling**, and it makes refactoring miserable.

> **⚠️ The smell**
>
> If you're passing a prop through three or more layers just so a deep child can use it, prop drilling is the smell — and Context is the cure.

## 4. `useContext` — state that any component can read

**Context** lets you put a value in one place and read it from *any* descendant component, no matter how deep, without passing props. There are three parts:

1. **Create** a context object with `createContext()`.
2. **Provide** a value by wrapping part of the tree in `<MyContext.Provider value={...}>`.
3. **Consume** it anywhere inside with `useContext(MyContext)`.

### Create + provide

A clean pattern is a dedicated provider component that owns the state and exposes it:

```python
// src/context/FavoritesContext.jsx
import { createContext, useContext, useState } from "react";

const FavoritesContext = createContext(null);

export function FavoritesProvider({ children }) {
  const [favorites, setFavorites] = useState([]);

  function addFavorite(recipe) {
    setFavorites((prev) =>
      prev.some((r) => r.id === recipe.id) ? prev : [...prev, recipe]
    );
  }
  function removeFavorite(id) {
    setFavorites((prev) => prev.filter((r) => r.id !== id));
  }

  const value = { favorites, addFavorite, removeFavorite };
  return (
    <FavoritesContext.Provider value={value}>
      {children}
    </FavoritesContext.Provider>
  );
}

// a small custom hook so components import one thing
export function useFavorites() {
  return useContext(FavoritesContext);
}
```

### Wrap the app

```html
// src/main.jsx
<BrowserRouter>
  <FavoritesProvider>
    <App />
  </FavoritesProvider>
</BrowserRouter>
```

### Consume anywhere

```python
// in ANY component inside the provider — no props needed
import { useFavorites } from "../context/FavoritesContext";

function NavbarCount() {
  const { favorites } = useFavorites();
  return <span>⭐ {favorites.length}</span>;
}

function SaveButton({ recipe }) {
  const { addFavorite } = useFavorites();
  return <button onClick={() => addFavorite(recipe)}>Save</button>;
}
```

The navbar and a deeply nested button both reach the same state directly. No drilling. Change a favorite anywhere and every consumer re-renders with the new value.

> **💡 The custom-hook wrapper**
>
> Exposing
>
> useFavorites()
>
> instead of making components call
>
> useContext(FavoritesContext)
>
> keeps imports tidy and lets you add a helpful error if it's used outside the provider. You'll formalize custom hooks in Chunk 4.7.

## 5. How forms + Context work together

Your form doesn't need to own the shared list. It collects and validates input, then calls a function from Context to add the item:

```javascript
function AddFavoriteForm() {
  const { addFavorite } = useFavorites();
  const [form, setForm] = useState({ title: "", area: "" });

  function handleSubmit(e) {
    e.preventDefault();
    if (!form.title.trim()) return;
    addFavorite({ id: crypto.randomUUID(), ...form });   // into shared state
    setForm({ title: "", area: "" });
  }
  // ...inputs + submit
}
```

This is "lifting state up" (4.3) taken to the app level: the form reports up to Context, and any page that reads Context instantly reflects the change.

## 6. When is Context enough — and when isn't it?

Context is perfect for low-frequency, app-wide data: the current user, theme, language, a favorites/cart list. It ships with React — no extra dependency.

It has limits. Every consumer re-renders when the context value changes, so Context is a poor fit for very large or rapidly-changing state. When an app's shared state grows complex (many slices, frequent updates, async flows), teams reach for a dedicated **state-management library**:

| Tool | Use it when… |
| --- | --- |
| `useState` + props | State is local to one component or a small subtree. |
| **Context** | A few pieces of app-wide state read in many places (auth, theme, favorites). |
| **Zustand / Redux Toolkit** | Large, complex, frequently-updated global state; you want devtools and structure. |

> **📝 Don't over-reach**
>
> Start with
>
> useState
>
> , lift it up when sharing is needed, and add Context when prop drilling hurts. Reach for a library only when Context genuinely strains — not by default. For this course,
>
> useState
>
> + Context covers everything.

## ✅ Recap

- Hold multi-field forms in **one state object**; update with `[name]: value` and one `onChange` handler.
- **Validate** on submit, store errors in state, render them by field; use native HTML validation too.
- **Prop drilling** (passing props through layers that don't use them) is the pain Context removes.
- **Context**: `createContext` → wrap in a `Provider value` → read with `useContext` anywhere inside.
- A form can call a Context function (e.g. `addFavorite`) to update app-wide shared state.
- Use Context for app-wide, low-frequency state; reach for a library only when it grows truly complex.

**Next:** open `assignment.html` and build a favorites feature with shared state.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
