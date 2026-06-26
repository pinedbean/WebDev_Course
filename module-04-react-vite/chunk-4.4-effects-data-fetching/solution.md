*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll build a `RecipeList` that fetches from TheMealDB with full loading/error/empty handling, plus a search box. It reuses the `RecipeCard` from Chunk 4.2. Full files at the bottom.

```text
recipe-box/
└── src/
    ├── App.jsx
    └── components/
        ├── RecipeCard.jsx   (from 4.2, lightly adapted)
        └── RecipeList.jsx   (new)
```

### 1 Confirm the API shape

Open this in your browser first so you know what you're parsing:

```
https://www.themealdb.com/api/json/v1/1/search.php?s=chicken
```

You'll get `{ "meals": [ { "idMeal": "...", "strMeal": "...", "strArea": "...", "strCategory": "...", "strMealThumb": "..." }, ... ] }`. A no-match search returns `{ "meals": null }`.

### 2 Adapt `RecipeCard` to API fields

Keep the card generic. We'll pass it `title`, `area`, `category`, and `image`:

```jsx
function RecipeCard({ title, area, category, image }) {
  return (
    <article className="card">
      <img src={image} alt={title} />
      <h3>{title}</h3>
      <p className="meta">{area} · {category}</p>
    </article>
  );
}

export default RecipeCard;
```

### 3 The fetch with three states

`RecipeList.jsx` takes a `query` prop and owns the request lifecycle.

```python
import { useState, useEffect } from "react";
import RecipeCard from "./RecipeCard";

function RecipeList({ query }) {
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;              // ignore stale responses
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const url =
          "https://www.themealdb.com/api/json/v1/1/search.php?s=" +
          encodeURIComponent(query);
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (active) setMeals(data.meals ?? []);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => { active = false; };   // cleanup
  }, [query]);

  if (loading) return <p className="status">⏳ Loading recipes…</p>;
  if (error)   return <p className="status error">😕 Couldn't load: {error}</p>;
  if (meals.length === 0) return <p className="status">No recipes found for “{query}”.</p>;

  return (
    <>
      <p className="status">Found {meals.length} recipes</p>
      <div className="grid">
        {meals.map((m) => (
          <RecipeCard
            key={m.idMeal}
            title={m.strMeal}
            area={m.strArea}
            category={m.strCategory}
            image={m.strMealThumb}
          />
        ))}
      </div>
    </>
  );
}

export default RecipeList;
```

> **💡 The `active` flag**
>
> If a faster, newer request resolves before an older one, the cleanup sets
>
> active = false
>
> on the old effect run so its late response is ignored. This prevents flickering wrong results — the race-condition guard from the lecture.

### 4 The search box in `App`

```python
import { useState } from "react";
import RecipeList from "./components/RecipeList";
import "./index.css";

function App() {
  const [query, setQuery] = useState("chicken");

  return (
    <main>
      <h1>🍳 Recipe Box</h1>
      <input
        className="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search recipes…"
      />
      <RecipeList query={query} />
    </main>
  );
}

export default App;
```

### 5 Verify in the Network tab

Open DevTools → Network. Each search should fire **one** request (or two in StrictMode dev mode — that's expected). If you see a flood of requests, your dependency array is wrong or missing.

## 📄 Complete `src/components/RecipeList.jsx`

```python
import { useState, useEffect } from "react";
import RecipeCard from "./RecipeCard";

function RecipeList({ query }) {
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true);
      setError(null);
      try {
        const url =
          "https://www.themealdb.com/api/json/v1/1/search.php?s=" +
          encodeURIComponent(query);
        const res = await fetch(url);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (active) setMeals(data.meals ?? []);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, [query]);

  if (loading) return <p className="status">⏳ Loading recipes…</p>;
  if (error)   return <p className="status error">😕 Couldn't load: {error}</p>;
  if (meals.length === 0) return <p className="status">No recipes found for “{query}”.</p>;

  return (
    <>
      <p className="status">Found {meals.length} recipes</p>
      <div className="grid">
        {meals.map((m) => (
          <RecipeCard
            key={m.idMeal}
            title={m.strMeal}
            area={m.strArea}
            category={m.strCategory}
            image={m.strMealThumb}
          />
        ))}
      </div>
    </>
  );
}

export default RecipeList;
```

## 📄 Add to `src/index.css`

```
.search { padding: 8px 12px; width: 100%; max-width: 320px; margin: 12px 0; }
.status { color: #475569; }
.status.error { color: #b91c1c; }
.card img { width: 100%; border-radius: 8px; display: block; }
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Hundreds of requests / browser freezes | Effect is missing its dependency array, or you put state you set *inside* the effect into the deps. Use `[query]` only. |
| `Cannot read properties of null (reading 'map')` | The API returned `meals: null`. Coerce: `setMeals(data.meals ?? [])`. |
| Loading spinner never goes away | You set `loading=false` only on success. Put it in `finally` so it runs on error too. |
| Effect runs twice on load | Normal in dev under `<React.StrictMode>`. It won't happen in the production build. |
| Images broken | Use `m.strMealThumb` for the `src`; check the field name matches the JSON exactly. |

## 🎉 You're done

Your app now shows live data, gracefully handles slow networks and failures, and re-fetches as the user searches. That loading/error/empty/success pattern is the backbone of every real frontend.

**Up next → Chunk 4.5: Routing with React Router** — you'll give the app real pages (Home, recipe list, recipe detail) with shareable URLs.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
