*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.4 — Side Effects & Data Fetching (useEffect)

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What a **side effect** is, and why fetching data is one.
- The **`useEffect`** hook and its **dependency array**.
- How to fetch data **on mount** with `fetch` + `async/await` (from Chunk 3.4).
- Managing the three states of any request: **loading**, **error**, and **success**.
- Cleanup, and why effects sometimes run twice in development.

In the lab you'll replace your hardcoded recipe data with live recipes from a public API.

## 1. What is a "side effect"?

A component's main job is pure: take props + state, return JSX. But real apps need to reach outside that calculation — fetch from an API, set a timer, read `localStorage`, change the document title. Anything that touches the world *outside* rendering is a **side effect**.

You can't just fetch inside the component body, because that runs on *every* render — you'd fire endless requests, each triggering a state update, triggering another render... an infinite loop. React gives you a controlled place to run effects: the **`useEffect`** hook.

## 2. The `useEffect` hook

`useEffect` runs a function *after* the component renders. Its shape:

```python
import { useEffect } from "react";

useEffect(() => {
  // effect code runs after render
}, [/* dependency array */]);
```

The second argument — the **dependency array** — controls *when* the effect re-runs. This is the single most important thing to understand:

| Dependency array | When the effect runs |
| --- | --- |
| `[]` (empty) | Once, after the first render ("on mount"). Perfect for fetching initial data. |
| `[query]` | On mount, and again whenever `query` changes. |
| omitted | After *every* render — almost always a mistake (loops!). |

```
// runs once, when the component first appears
useEffect(() => {
  console.log("mounted!");
}, []);
```

> **⚠️ The dependency array is not optional**
>
> Forgetting
>
> []
>
> is the classic beginner bug. With no array, the effect runs after every render; if the effect sets state, that render triggers the effect again — an infinite fetch loop. List the values your effect depends on, and only those.

## 3. Fetching data on mount

You already know `fetch` and `async/await` from Chunk 3.4. The new part is wrapping them in `useEffect` and storing the result in state so React renders it.

A subtle rule: the effect function itself can't be `async` (it must return either nothing or a cleanup function, not a Promise). So define an `async` function *inside* the effect and call it:

```python
import { useState, useEffect } from "react";

function Recipes() {
  const [meals, setMeals] = useState([]);

  useEffect(() => {
    async function load() {
      const res = await fetch(
        "https://www.themealdb.com/api/json/v1/1/search.php?s=chicken"
      );
      const data = await res.json();
      setMeals(data.meals);   // store result → triggers a re-render
    }
    load();
  }, []);   // [] = fetch once on mount

  return (
    <ul>
      {meals.map((m) => <li key={m.idMeal}>{m.strMeal}</li>)}
    </ul>
  );
}
```

> **💡 TheMealDB — a free, no-key API**
>
> themealdb.com
>
> returns JSON like
>
> { "meals": [ ... ] }
>
> . No API key, no signup — ideal for practice. A search with no matches returns
>
> { "meals": null }
>
> , so guard for that.

## 4. The three states of every request

A network request is never instant and can fail. A polished UI tracks **three** things, each in its own state variable:

- **loading** — is the request in flight? (show a spinner/skeleton)
- **error** — did it fail? (show a message)
- **data** — the successful result (render it)

```jsx
function Recipes({ query }) {
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(
          `https://www.themealdb.com/api/json/v1/1/search.php?s=${query}`
        );
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        setMeals(data.meals ?? []);   // null → empty array
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);            // always stop loading
      }
    }
    load();
  }, [query]);   // re-fetch whenever query changes

  if (loading) return <p>Loading…</p>;
  if (error)   return <p>😕 Something went wrong: {error}</p>;
  if (meals.length === 0) return <p>No recipes found.</p>;

  return (
    <ul>
      {meals.map((m) => <li key={m.idMeal}>{m.strMeal}</li>)}
    </ul>
  );
}
```

Read the bottom: a clear ladder of early returns for loading, error, empty, then the happy path. This loading/error/empty/success pattern is everywhere in real apps — internalize it.

> **📝 `fetch` and errors**
>
> fetch
>
> only rejects on network failure, not on HTTP errors like 404 or 500. That's why we check
>
> if (!res.ok) throw ...
>
> ourselves — exactly as you learned in Chunk 3.4.

## 5. Re-fetching when inputs change

Putting `query` in the dependency array means: whenever the user changes the search term (which lives in state from a controlled input), the effect re-runs and fetches fresh results. You don't wire up any "search button" logic — React reacts to the dependency changing.

```jsx
function App() {
  const [query, setQuery] = useState("chicken");
  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <Recipes query={query} />
    </>
  );
}
```

Change the box → `query` changes → `Recipes` re-renders with a new prop → its effect's dependency changed → it re-fetches. Beautifully automatic.

## 6. Cleanup & the "double run" in dev

If your effect starts something ongoing (a timer, a subscription, an in-flight request you want to cancel), return a **cleanup function**. React runs it before the effect re-runs and when the component unmounts:

```javascript
useEffect(() => {
  const id = setInterval(() => tick(), 1000);
  return () => clearInterval(id);   // cleanup
}, []);
```

You may also notice effects running **twice** on mount during development. That's `<React.StrictMode>` intentionally mounting, unmounting, and remounting your component to help you catch missing cleanup. It only happens in dev, never in the production build — don't try to "fix" it by removing StrictMode.

> **💡 Avoiding race conditions**
>
> For a search that re-fetches, a request can resolve after a newer one. A simple guard: a boolean flag in cleanup.
>
> let active = true;
>
> ...
>
> if (active) setMeals(...)
>
> ...
>
> return () => { active = false; };
>
> . You'll formalize this when you extract a
>
> useFetch
>
> hook in Chunk 4.7.

## ✅ Recap

- A **side effect** reaches outside rendering (fetching, timers, storage). Run it in `useEffect`, never in the render body.
- The **dependency array** controls timing: `[]` = once on mount; `[x]` = on mount + whenever `x` changes; omitted = every render (avoid).
- Define an `async` function inside the effect and call it; the effect itself isn't async.
- Track **loading**, **error**, and **data** states; render a clear ladder of early returns.
- Check `res.ok` yourself; `fetch` won't throw on 404/500.
- Return a **cleanup** function for ongoing work; effects double-run in dev under StrictMode (harmless).

**Next:** open `assignment.html` and build a live, data-driven recipe page.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
