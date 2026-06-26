*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.6 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll add a Favorites context, wire toggles across pages, build a Favorites page, and add a validated form. New/changed files:

```text
recipe-box/
└── src/
    ├── main.jsx                       (add the provider)
    ├── context/
    │   └── FavoritesContext.jsx       (new)
    ├── components/
    │   ├── Layout.jsx                 (navbar count)
    │   └── FavoriteButton.jsx         (new)
    └── pages/
        └── Favorites.jsx              (new: list + form)
```

### 1 The context + provider + hook

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
  function isFavorite(id) {
    return favorites.some((r) => r.id === id);
  }

  const value = { favorites, addFavorite, removeFavorite, isFavorite };
  return (
    <FavoritesContext.Provider value={value}>
      {children}
    </FavoritesContext.Provider>
  );
}

export function useFavorites() {
  const ctx = useContext(FavoritesContext);
  if (!ctx) throw new Error("useFavorites must be used inside <FavoritesProvider>");
  return ctx;
}
```

### 2 Provide it at the top

```python
// src/main.jsx
import { BrowserRouter } from "react-router-dom";
import { FavoritesProvider } from "./context/FavoritesContext";

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

### 3 A reusable favorite button

```python
// src/components/FavoriteButton.jsx
import { useFavorites } from "../context/FavoritesContext";

function FavoriteButton({ recipe }) {
  const { isFavorite, addFavorite, removeFavorite } = useFavorites();
  const fav = isFavorite(recipe.id);

  function toggle(e) {
    e.preventDefault();   // don't trigger the card's Link
    fav ? removeFavorite(recipe.id) : addFavorite(recipe);
  }

  return (
    <button onClick={toggle} aria-pressed={fav}>
      {fav ? "⭐ Saved" : "☆ Save"}
    </button>
  );
}

export default FavoriteButton;
```

Use it on cards and on the detail page, passing a normalized recipe object, e.g. `{ id: m.idMeal, title: m.strMeal, area: m.strArea, image: m.strMealThumb }`.

> **💡 `e.preventDefault()` inside a Link**
>
> Because the card is wrapped in a
>
> <Link>
>
> , clicking the button would also navigate. Calling
>
> preventDefault()
>
> in the button handler stops that, so the click only toggles the favorite.

### 4 Navbar count (no drilling)

```python
// src/components/Layout.jsx
import { NavLink, Outlet } from "react-router-dom";
import { useFavorites } from "../context/FavoritesContext";

function Layout() {
  const { favorites } = useFavorites();
  const cls = ({ isActive }) => (isActive ? "tab active" : "tab");
  return (
    <>
      <header className="nav">
        <NavLink to="/" className={cls} end>🍳 Home</NavLink>
        <NavLink to="/recipes" className={cls}>Recipes</NavLink>
        <NavLink to="/favorites" className={cls}>⭐ Favorites ({favorites.length})</NavLink>
      </header>
      <main><Outlet /></main>
    </>
  );
}

export default Layout;
```

### 5 The Favorites page: list + validated form

```python
// src/pages/Favorites.jsx
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
    if (!(Number(v.minutes) > 0)) next.minutes = "Minutes must be a positive number";
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
      minutes: Number(form.minutes),
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
      <form onSubmit={handleSubmit} noValidate>
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

Add the route in `App.jsx`: `<Route path="/favorites" element={<Favorites />} />` (inside the layout route).

### 6 A little CSS

```
.field-error { color: #b91c1c; font-size: 13px; display: block; }
.fav-list { list-style: none; padding: 0; }
.fav-list li { display: flex; align-items: center; gap: 8px; padding: 6px 0; }
.fav-list li button { margin-left: auto; }
form > div { margin-bottom: 10px; }
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Cannot destructure property ... of useContext(...) as it is null` | The component isn't inside `<FavoritesProvider>`. Make sure the provider wraps `<App />` in `main.jsx`. |
| Clicking the star also navigates | Call `e.preventDefault()` in the toggle handler (the button is inside a `Link`). |
| Only one field updates / fields clobber each other | Each input needs a unique `name`, and the handler must spread: `{ ...prev, [name]: value }`. |
| Validation never blocks submit | You forgot `e.preventDefault()` or didn't `return` early when errors exist. |
| Navbar count doesn't update | Read `favorites` from `useFavorites()` inside `Layout`, not a stale prop. |

## 🎉 You're done

You built app-wide shared state with Context, wired it into deeply-nested components with no prop drilling, and drove it from a validated multi-field form. This is the standard pattern for auth, themes, carts, and favorites in real apps.

**Up next → Chunk 4.7: Reusable Hooks & Project Structure** — you'll extract a `useFetch` hook, clean up the folders, and then tackle the 🏁 Module 4 Checkpoint.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
