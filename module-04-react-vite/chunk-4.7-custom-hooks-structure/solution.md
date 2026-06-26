*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.7 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Part A refactors your app; Part B assembles the 🏁 Checkpoint Recipe Browser. Here's the finished structure both parts produce:

```text
recipe-box/
├── .env                          VITE_API_BASE=...
├── index.html
└── src/
    ├── main.jsx                  router + favorites provider
    ├── App.jsx                   routes
    ├── api/
    │   └── recipes.js            URL builders (env-based)
    ├── hooks/
    │   └── useFetch.js           reusable fetch lifecycle
    ├── context/
    │   └── FavoritesContext.jsx  shared favorites state
    ├── components/
    │   ├── Layout.jsx            navbar + Outlet + fav count
    │   ├── RecipeCard.jsx
    │   └── FavoriteButton.jsx
    ├── pages/
    │   ├── Home.jsx
    │   ├── Recipes.jsx
    │   ├── RecipeDetail.jsx
    │   ├── Favorites.jsx
    │   └── NotFound.jsx
    └── index.css
```

## Part A — Refactor & Structure

### 1 The `useFetch` hook

```python
// src/hooks/useFetch.js
import { useState, useEffect } from "react";

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!url) return;            // skip when there's no url
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

### 2 Centralized API + env config

```
# .env  (project root)
VITE_API_BASE=https://www.themealdb.com/api/json/v1/1
```

```javascript
// src/api/recipes.js
const BASE = import.meta.env.VITE_API_BASE;

export function searchUrl(query) {
  return `${BASE}/search.php?s=${encodeURIComponent(query)}`;
}
export function lookupUrl(id) {
  return `${BASE}/lookup.php?i=${id}`;
}
```

> **⚠️ Restart after editing `.env`**
>
> Vite reads env files at startup. Stop (
>
> Ctrl
>
> +
>
> C
>
> ) and re-run
>
> npm run dev
>
> so
>
> import.meta.env.VITE_API_BASE
>
> is defined. If it's
>
> undefined
>
> , check the
>
> VITE_
>
> prefix and that you restarted.

### 3 Pages shrink to almost nothing

Both list and detail now compose the hook + the api helper. See the full files in Part B below.

## 🏁 Part B — Module 4 Checkpoint: Recipe Browser (complete code)

Below is every file of the finished app. It composes all of Module 4. Create the files exactly, run `npm install react-router-dom` if you haven't, then `npm run dev`.

## 📄 `src/main.jsx`

```python
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { FavoritesProvider } from "./context/FavoritesContext";
import App from "./App.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <FavoritesProvider>
        <App />
      </FavoritesProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

## 📄 `src/App.jsx`

```python
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Recipes from "./pages/Recipes";
import RecipeDetail from "./pages/RecipeDetail";
import Favorites from "./pages/Favorites";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/recipes" element={<Recipes />} />
        <Route path="/recipes/:id" element={<RecipeDetail />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
```

## 📄 `src/context/FavoritesContext.jsx`

```python
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
  function isFavorite(id) {
    return favorites.some((r) => r.id === id);
  }

  return (
    <FavoritesContext.Provider
      value={{ favorites, addFavorite, removeFavorite, isFavorite }}
    >
      {children}
    </FavoritesContext.Provider>
  );
}

export function useFavorites() {
  const ctx = useContext(FavoritesContext);
  if (!ctx) throw new Error("useFavorites must be used inside FavoritesProvider");
  return ctx;
}
```

## 📄 `src/components/Layout.jsx`

```python
import { NavLink, Outlet } from "react-router-dom";
import { useFavorites } from "../context/FavoritesContext";

const cls = ({ isActive }) => (isActive ? "tab active" : "tab");

function Layout() {
  const { favorites } = useFavorites();
  return (
    <>
      <header className="nav">
        <NavLink to="/" className={cls} end>🍳 Home</NavLink>
        <NavLink to="/recipes" className={cls}>Recipes</NavLink>
        <NavLink to="/favorites" className={cls}>⭐ Favorites ({favorites.length})</NavLink>
      </header>
      <main className="container"><Outlet /></main>
    </>
  );
}

export default Layout;
```

## 📄 `src/components/RecipeCard.jsx`

```python
import { Link } from "react-router-dom";
import FavoriteButton from "./FavoriteButton";

function RecipeCard({ recipe }) {
  return (
    <article className="card">
      <Link to={`/recipes/${recipe.id}`} className="card-link">
        <img src={recipe.image} alt={recipe.title} />
        <h3>{recipe.title}</h3>
        <p className="meta">{recipe.area} · {recipe.category}</p>
      </Link>
      <FavoriteButton recipe={recipe} />
    </article>
  );
}

export default RecipeCard;
```

## 📄 `src/components/FavoriteButton.jsx`

```python
import { useFavorites } from "../context/FavoritesContext";

function FavoriteButton({ recipe }) {
  const { isFavorite, addFavorite, removeFavorite } = useFavorites();
  const fav = isFavorite(recipe.id);

  function toggle(e) {
    e.preventDefault();
    fav ? removeFavorite(recipe.id) : addFavorite(recipe);
  }

  return (
    <button className="fav-btn" onClick={toggle} aria-pressed={fav}>
      {fav ? "⭐ Saved" : "☆ Save"}
    </button>
  );
}

export default FavoriteButton;
```

## 📄 `src/pages/Home.jsx`

```python
import { Link } from "react-router-dom";

function Home() {
  return (
    <section>
      <h1>Welcome to Recipe Box 🍳</h1>
      <p>Search thousands of recipes and save your favorites.</p>
      <Link to="/recipes" className="btn">Start browsing →</Link>
    </section>
  );
}

export default Home;
```

## 📄 `src/pages/Recipes.jsx`

```python
import { useState } from "react";
import { useFetch } from "../hooks/useFetch";
import { searchUrl } from "../api/recipes";
import RecipeCard from "../components/RecipeCard";

function toRecipe(m) {
  return {
    id: m.idMeal,
    title: m.strMeal,
    area: m.strArea,
    category: m.strCategory,
    image: m.strMealThumb,
  };
}

function Recipes() {
  const [query, setQuery] = useState("chicken");
  const { data, loading, error } = useFetch(searchUrl(query));
  const meals = data?.meals ?? [];

  return (
    <section>
      <h1>Recipes</h1>
      <input
        className="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search recipes…"
      />
      {loading && <p className="status">⏳ Loading…</p>}
      {error && <p className="status error">😕 {error}</p>}
      {!loading && !error && meals.length === 0 && (
        <p className="status">No recipes found for “{query}”.</p>
      )}
      <div className="grid">
        {meals.map((m) => (
          <RecipeCard key={m.idMeal} recipe={toRecipe(m)} />
        ))}
      </div>
    </section>
  );
}

export default Recipes;
```

## 📄 `src/pages/RecipeDetail.jsx`

```python
import { useParams, useNavigate } from "react-router-dom";
import { useFetch } from "../hooks/useFetch";
import { lookupUrl } from "../api/recipes";
import FavoriteButton from "../components/FavoriteButton";

function RecipeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, loading, error } = useFetch(lookupUrl(id));

  if (loading) return <p className="status">⏳ Loading…</p>;
  if (error)   return <p className="status error">😕 {error}</p>;

  const meal = data?.meals ? data.meals[0] : null;
  if (!meal) return <p className="status">Recipe not found.</p>;

  const recipe = {
    id: meal.idMeal,
    title: meal.strMeal,
    area: meal.strArea,
    category: meal.strCategory,
    image: meal.strMealThumb,
  };

  return (
    <section>
      <button onClick={() => navigate(-1)}>← Back</button>
      <h1>{meal.strMeal}</h1>
      <p className="meta">{meal.strArea} · {meal.strCategory}</p>
      <FavoriteButton recipe={recipe} />
      <img src={meal.strMealThumb} alt={meal.strMeal} width="320" />
      <h2>Instructions</h2>
      <p>{meal.strInstructions}</p>
    </section>
  );
}

export default RecipeDetail;
```

## 📄 `src/pages/Favorites.jsx`

```python
import { useState } from "react";
import { useFavorites } from "../context/FavoritesContext";

function Favorites() {
  const { favorites, addFavorite, removeFavorite } = useFavorites();
  const [form, setForm] = useState({ title: "", area: "", minutes: "" });
  const [errors, setErrors] = useState({});

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }
  function validate(v) {
    const next = {};
    if (!v.title.trim()) next.title = "Title is required";
    if (!(Number(v.minutes) > 0)) next.minutes = "Minutes must be positive";
    return next;
  }
  function handleSubmit(e) {
    e.preventDefault();
    const found = validate(form);
    setErrors(found);
    if (Object.keys(found).length > 0) return;
    addFavorite({
      id: crypto.randomUUID(),
      title: form.title.trim(),
      area: form.area.trim() || "Custom",
      category: "Custom",
      image: "https://placehold.co/300x200?text=My+Recipe",
    });
    setForm({ title: "", area: "", minutes: "" });
  }

  return (
    <section>
      <h1>⭐ Favorites</h1>
      {favorites.length === 0 ? (
        <p className="status">No favorites yet — save some recipes!</p>
      ) : (
        <ul className="fav-list">
          {favorites.map((r) => (
            <li key={r.id}>
              {r.title} <span className="meta">({r.area})</span>
              <button onClick={() => removeFavorite(r.id)}>Remove</button>
            </li>
          ))}
        </ul>
      )}

      <h2>Add your own</h2>
      <form onSubmit={handleSubmit} noValidate className="recipe-form">
        <div>
          <input name="title" value={form.title} onChange={handleChange} placeholder="Title" />
          {errors.title && <span className="field-error">{errors.title}</span>}
        </div>
        <div>
          <input name="area" value={form.area} onChange={handleChange} placeholder="Cuisine" />
        </div>
        <div>
          <input name="minutes" type="number" value={form.minutes} onChange={handleChange} placeholder="Minutes" />
          {errors.minutes && <span className="field-error">{errors.minutes}</span>}
        </div>
        <button type="submit">Add to favorites</button>
      </form>
    </section>
  );
}

export default Favorites;
```

## 📄 `src/pages/NotFound.jsx`

```python
import { Link } from "react-router-dom";

function NotFound() {
  return (
    <section>
      <h1>404 — Page not found</h1>
      <Link to="/">← Back home</Link>
    </section>
  );
}

export default NotFound;
```

## 📄 `src/index.css`

```
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  background: #f1f5f9;
  color: #1e293b;
}
.container { max-width: 900px; margin: 0 auto; padding: 24px; }
.nav { display: flex; gap: 16px; padding: 12px 24px; background: #fff; border-bottom: 1px solid #e2e8f0; }
.tab { text-decoration: none; color: #2563eb; font-weight: 600; }
.tab.active { color: #1e293b; border-bottom: 2px solid #2563eb; }
.search { padding: 8px 12px; width: 100%; max-width: 320px; margin: 12px 0; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }
.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; }
.card img { width: 100%; border-radius: 8px; display: block; }
.card-link { text-decoration: none; color: inherit; }
.meta { color: #64748b; font-size: 14px; }
.fav-btn { margin-top: 8px; }
.status { color: #475569; }
.status.error { color: #b91c1c; }
.field-error { color: #b91c1c; font-size: 13px; display: block; }
.fav-list { list-style: none; padding: 0; }
.fav-list li { display: flex; align-items: center; gap: 8px; padding: 6px 0; }
.fav-list li button { margin-left: auto; }
.recipe-form > div { margin-bottom: 10px; }
.btn { display: inline-block; margin-top: 8px; }
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `import.meta.env.VITE_API_BASE` is undefined | Check the `VITE_` prefix, that `.env` is in the project root (not `src/`), and that you restarted `npm run dev`. |
| Hook ESLint warning: "missing dependency" | The dependency array of `useFetch` should be `[url]`. Build the URL outside the hook (in the api helper) so it's a plain string. |
| "Invalid hook call" | You called a hook conditionally or outside a component/hook. Move it to the top level of a component or custom hook. |
| Detail fetch fires with no id | Our `useFetch` bails when `url` is falsy; make sure `lookupUrl(id)` returns a real URL once `id` exists. |
| Imports break after moving files | Update relative paths (`../` vs `./`). VS Code can auto-update imports on move — accept the prompt. |

## 🎉 Module 4 complete!

You built a complete, multi-page React app from scratch: scaffolded with Vite, composed from reusable components and props, made interactive with `useState`, connected to a live API with `useEffect`/`useFetch`, routed with React Router, and given app-wide shared state via Context — all in a clean, environment-configured project structure.

Across Module 4 you can now:

- Scaffold and run React apps with Vite, and write JSX confidently.
- Build component trees with props, composition, conditional rendering, and keyed lists.
- Manage state and events with hooks, and fetch data with loading/error handling.
- Add client-side routing, shared state with Context, and forms with validation.
- Extract custom hooks and organize a real-world project.

**Up next → Module 5: Backend with FastAPI.** You'll build the API that this frontend will eventually talk to — and in Chunk 5.5 you'll connect your React app to it. Your Recipe Browser is your proof that the frontend half is solid.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
