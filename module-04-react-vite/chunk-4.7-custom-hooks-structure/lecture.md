*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.7 — Reusable Hooks & Project Structure

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What a **custom hook** is and the rules every hook follows.
- Building a reusable **`useFetch`** hook to kill the duplicated fetch logic.
- A sensible **folder structure** for a growing React app.
- **Environment variables** in Vite (`import.meta.env`, the `VITE_` prefix, `.env` files).

In the lab you'll extract `useFetch`, reorganize the project — then build the 🏁 **Module 4 Checkpoint**: a recipe browser app.

## 1. The duplication problem

Look back at Chunks 4.4 and 4.5. Your `Recipes` page and your `RecipeDetail` page both contain almost identical code: three state variables (`loading`, `error`, `data`), a `useEffect` with a `try/catch/finally`, a `res.ok` check, and an `active` cleanup flag. The only thing that differs is the URL.

Copy-pasted logic is a maintenance trap — fix a bug in one place and you must remember the others. In React, you don't extract repeated *stateful* logic into a plain function (it can't call hooks). You extract it into a **custom hook**.

## 2. What is a custom hook?

A custom hook is just a JavaScript function whose name starts with `use` and that *calls other hooks* (`useState`, `useEffect`, …). It lets you package stateful behavior and reuse it across components. It's not a new feature — it's a naming convention plus composition.

> **📝 The Rules of Hooks**
>
> Every hook (built-in or custom) must obey two rules:
>
> - **Only call hooks at the top level** — never inside loops, conditions, or nested functions. React relies on hooks being called in the same order every render.
> - **Only call hooks from React functions** — components or other custom hooks, not regular functions.
>
> The
>
> use
>
> prefix is what lets React's tooling (and the ESLint plugin) enforce these for you.

## 3. Building `useFetch`

Take the exact pattern from 4.4 and lift it into a function that accepts a URL and returns the three states:

```python
// src/hooks/useFetch.js
import { useState, useEffect } from "react";

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = await res.json();
        if (active) setData(json);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, [url]);

  return { data, loading, error };
}
```

A custom hook returns whatever is useful — here an object `{ data, loading, error }`. Because it calls `useState`/`useEffect` internally, each component that uses it gets its *own* independent state.

## 4. Using the hook

Now the page components shrink dramatically. Compare to 4.4 — the entire fetch lifecycle is one line:

```python
import { useFetch } from "../hooks/useFetch";
import RecipeCard from "../components/RecipeCard";

function Recipes({ query }) {
  const url = `https://www.themealdb.com/api/json/v1/1/search.php?s=${query}`;
  const { data, loading, error } = useFetch(url);

  if (loading) return <p>⏳ Loading…</p>;
  if (error)   return <p>😕 {error}</p>;

  const meals = data?.meals ?? [];
  if (meals.length === 0) return <p>No recipes found.</p>;

  return (
    <div className="grid">
      {meals.map((m) => (
        <RecipeCard key={m.idMeal} title={m.strMeal} image={m.strMealThumb} />
      ))}
    </div>
  );
}
```

The detail page uses the very same hook with a different URL. One bug fix in `useFetch` now benefits every screen. *That* is the power of custom hooks.

> **💡 Optional chaining**
>
> data?.meals ?? []
>
> safely reads
>
> meals
>
> even before the data arrives (
>
> data
>
> starts as
>
> null
>
> ), then falls back to an empty array. It pairs perfectly with a hook that returns
>
> data: null
>
> while loading.

## 5. Project structure for a growing app

As features pile up, a flat `src/` becomes a mess. Group files by what they are. A clean, conventional layout:

```text
src/
├── main.jsx              ← entry point (providers, router)
├── App.jsx               ← route definitions
├── api/
│   └── recipes.js        ← functions that build API URLs / fetch
├── components/           ← reusable UI (RecipeCard, FavoriteButton, Layout)
│   ├── RecipeCard.jsx
│   └── Layout.jsx
├── pages/                ← one component per route/screen
│   ├── Home.jsx
│   ├── Recipes.jsx
│   └── RecipeDetail.jsx
├── hooks/                ← custom hooks (useFetch)
│   └── useFetch.js
├── context/              ← shared state providers
│   └── FavoritesContext.jsx
└── styles or *.css
```

The principles:

- **components/** = reusable pieces used in many places. **pages/** = top-level screens tied to routes.
- **hooks/**, **context/**, **api/** separate behavior, shared state, and network code from UI.
- Keep a component's file focused; if it grows past a screenful, look for a piece to extract.

> **📝 Centralize API calls**
>
> Putting URL-building and fetching in
>
> src/api/recipes.js
>
> (e.g.
>
> searchRecipes(query)
>
> ,
>
> getRecipe(id)
>
> ) means the API's shape lives in one file. If the endpoint changes, you edit one place — not every component.

## 6. Environment variables in Vite

You shouldn't hardcode things that change between environments — like an API base URL (your FastAPI backend will be `localhost` in dev and a real domain in production, coming in Module 5). Vite reads these from `.env` files.

Create a `.env` file at the project root. **Only variables prefixed with `VITE_` are exposed to your code** (a safety feature so you don't accidentally ship secrets):

```
# .env  (project root)
VITE_API_BASE=https://www.themealdb.com/api/json/v1/1
```

Read it through `import.meta.env`:

```javascript
const BASE = import.meta.env.VITE_API_BASE;

export function searchRecipes(query) {
  return fetch(`${BASE}/search.php?s=${encodeURIComponent(query)}`)
    .then((res) => res.json());
}
```

Vite also gives you built-ins: `import.meta.env.DEV` / `.PROD` (booleans) and `.MODE` ("development" or "production").

> **⚠️ Env vars are NOT secret in the frontend**
>
> Anything in a frontend build ships to the browser — users can read it.
>
> VITE_
>
> vars are for
>
> configuration
>
> (URLs, public keys), never real secrets (API keys with billing, passwords). Those belong on the backend. Also: restart
>
> npm run dev
>
> after editing
>
> .env
>
> , and add
>
> .env.local
>
> to
>
> .gitignore
>
> so machine-specific values aren't committed.

## ✅ Recap

- Extract repeated *stateful* logic into a **custom hook** — a `use*` function that calls other hooks.
- Follow the **Rules of Hooks**: top level only, React functions only.
- `useFetch(url)` packages the loading/error/data lifecycle so pages become tiny.
- Organize `src/` into **components / pages / hooks / context / api**; centralize API calls.
- Use Vite **env vars** (`VITE_` prefix, `import.meta.env`) for configuration — never for real secrets.

**Next:** open `assignment.html` — refactor your app, then build the 🏁 Module 4 Checkpoint recipe browser.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
