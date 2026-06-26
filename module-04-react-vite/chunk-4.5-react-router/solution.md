*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.5 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll wire up routing, a shared layout, list, and detail pages. Target structure:

```text
recipe-box/
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── components/
    │   ├── Layout.jsx
    │   └── RecipeCard.jsx
    └── pages/
        ├── Home.jsx
        ├── Recipes.jsx
        ├── RecipeDetail.jsx
        └── NotFound.jsx
```

### 1 Install and wrap

```bash
npm install react-router-dom
```

```python
// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
```

### 2 The layout shell

```python
// src/components/Layout.jsx
import { NavLink, Outlet } from "react-router-dom";

const linkClass = ({ isActive }) => (isActive ? "tab active" : "tab");

function Layout() {
  return (
    <>
      <header className="nav">
        <NavLink to="/" className={linkClass} end>🍳 Home</NavLink>
        <NavLink to="/recipes" className={linkClass}>Recipes</NavLink>
      </header>
      <main>
        <Outlet />
      </main>
    </>
  );
}

export default Layout;
```

> **💡 The `end` prop**
>
> Add
>
> end
>
> to the Home
>
> NavLink
>
> so it's only "active" on the exact
>
> /
>
> path, not on every route that starts with
>
> /
>
> .

### 3 Routes in `App`

```python
// src/App.jsx
import { Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import Recipes from "./pages/Recipes";
import RecipeDetail from "./pages/RecipeDetail";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/recipes" element={<Recipes />} />
        <Route path="/recipes/:id" element={<RecipeDetail />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
```

### 4 Home & NotFound

```python
// src/pages/Home.jsx
import { Link } from "react-router-dom";

function Home() {
  return (
    <section>
      <h1>Welcome to Recipe Box 🍳</h1>
      <p>Search thousands of recipes from around the world.</p>
      <Link to="/recipes" className="btn">Browse recipes →</Link>
    </section>
  );
}
export default Home;
```

```python
// src/pages/NotFound.jsx
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

### 5 Recipes list — cards link to detail

Reuse your 4.4 fetch. Wrap each card in a `Link` to its detail route:

```python
// src/pages/Recipes.jsx
import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function Recipes() {
  const [query, setQuery] = useState("chicken");
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true); setError(null);
      try {
        const res = await fetch(
          "https://www.themealdb.com/api/json/v1/1/search.php?s=" +
          encodeURIComponent(query)
        );
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
        <p className="status">No recipes found.</p>
      )}
      <div className="grid">
        {meals.map((m) => (
          <Link key={m.idMeal} to={`/recipes/${m.idMeal}`} className="card-link">
            <article className="card">
              <img src={m.strMealThumb} alt={m.strMeal} />
              <h3>{m.strMeal}</h3>
              <p className="meta">{m.strArea} · {m.strCategory}</p>
            </article>
          </Link>
        ))}
      </div>
    </section>
  );
}

export default Recipes;
```

### 6 The detail page (`useParams` + fetch + back)

```python
// src/pages/RecipeDetail.jsx
import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

function RecipeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [meal, setMeal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;
    async function load() {
      setLoading(true); setError(null);
      try {
        const res = await fetch(
          `https://www.themealdb.com/api/json/v1/1/lookup.php?i=${id}`
        );
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (active) setMeal(data.meals ? data.meals[0] : null);
      } catch (err) {
        if (active) setError(err.message);
      } finally {
        if (active) setLoading(false);
      }
    }
    load();
    return () => { active = false; };
  }, [id]);

  if (loading) return <p className="status">⏳ Loading…</p>;
  if (error)   return <p className="status error">😕 {error}</p>;
  if (!meal)   return <p className="status">Recipe not found.</p>;

  return (
    <section>
      <button onClick={() => navigate(-1)}>← Back</button>
      <h1>{meal.strMeal}</h1>
      <p className="meta">{meal.strArea} · {meal.strCategory}</p>
      <img src={meal.strMealThumb} alt={meal.strMeal} width="320" />
      <h2>Instructions</h2>
      <p>{meal.strInstructions}</p>
    </section>
  );
}

export default RecipeDetail;
```

### 7 A little CSS

```
.nav { display: flex; gap: 16px; padding: 12px 24px; background: #fff; border-bottom: 1px solid #e2e8f0; }
.tab { text-decoration: none; color: #2563eb; font-weight: 600; }
.tab.active { color: #1e293b; border-bottom: 2px solid #2563eb; }
.card-link { text-decoration: none; color: inherit; }
.btn { display: inline-block; margin-top: 8px; }
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `useRoutes() may be used only in the context of a Router` | You forgot to wrap the app in `<BrowserRouter>` in `main.jsx`. |
| Clicking a card reloads the whole page | You used `<a href>` instead of `<Link to>`. |
| Detail page is blank | Check the route path is `/recipes/:id` and you read `const { id } = useParams()` with the same name. |
| Navbar repeats / missing | Make sure pages are nested inside the `<Route element={<Layout />}>` and the layout renders `<Outlet />`. |
| Home tab always "active" | Add the `end` prop to the Home `NavLink`. |

## 🎉 You're done

Your SPA now has real, shareable URLs, a shared layout, and a list → detail flow — all without a single page reload. This is exactly how production React apps are structured.

**Up next → Chunk 4.6: Forms & Shared State** — you'll build a "favorites" feature whose state is shared across pages using `useContext`.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
