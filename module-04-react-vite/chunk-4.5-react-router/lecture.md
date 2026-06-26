*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.5 — Routing with React Router

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What **client-side routing** is and why an SPA needs it.
- Installing and setting up **React Router 6+**.
- Defining **routes**, navigating with **`Link`**/**`NavLink`** (no page reloads).
- **Route params** (`/recipes/:id`) read with **`useParams`**.
- **Nested layouts** with a shared shell via **`Outlet`**, plus programmatic navigation.

In the lab you'll add Home, Recipes list, and Recipe detail pages with a shared navbar.

## 1. The problem: one page, many "pages"

Your app is a **Single Page Application** — there's one `index.html`. But users expect multiple pages: a home screen, a list, a detail view. They expect the URL to change, the Back button to work, and links to be shareable.

If you used normal `<a href>` links, the browser would do a full reload — fetching HTML from a server, throwing away all your React state, and flashing white. That defeats the point of an SPA.

**Client-side routing** solves this: JavaScript watches the URL and swaps which components render, all without a server round-trip. The URL updates and Back/Forward work, but the page never reloads. The standard tool is **React Router**.

## 2. Install & wrap the app

React Router is a separate package. Install it (you learned `npm install` in Chunk 3.5):

```bash
npm install react-router-dom
```

Then wrap your whole app in a `<BrowserRouter>` in `main.jsx`. This is what enables routing everywhere inside:

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

## 3. Defining routes

Inside `App`, you declare which component renders for which URL using `<Routes>` and `<Route>`. Each `<Route>` maps a URL `path` to an `element`:

```python
import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Recipes from "./pages/Recipes";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/recipes" element={<Recipes />} />
      <Route path="*" element={<NotFound />} />   {/* catch-all 404 */}
    </Routes>
  );
}
```

Only the `<Route>` whose `path` matches the current URL renders. `path="*"` matches anything not matched above — your 404 page.

> **📝 "Pages" are just components**
>
> A page component is nothing special — it's a normal component. Many teams put them in a
>
> src/pages/
>
> folder to separate "screens" from reusable
>
> src/components/
>
> .

## 4. Navigating with `Link` and `NavLink`

To move between routes, use `<Link to="...">` instead of `<a href="...">`. `Link` updates the URL and swaps components *without* reloading:

```python
import { Link } from "react-router-dom";

<nav>
  <Link to="/">Home</Link>
  <Link to="/recipes">Recipes</Link>
</nav>
```

`<NavLink>` is like `Link` but knows when it's the active route, so you can style the current tab:

```python
import { NavLink } from "react-router-dom";

<NavLink
  to="/recipes"
  className={({ isActive }) => (isActive ? "tab active" : "tab")}
>
  Recipes
</NavLink>
```

> **⚠️ Don't use `<a href>` for internal links**
>
> A plain
>
> <a>
>
> triggers a full browser reload and wipes your React state. Use
>
> Link
>
> /
>
> NavLink
>
> for internal navigation. Keep
>
> <a>
>
> only for external sites.

## 5. Route params — dynamic URLs

A detail page needs to know *which* recipe to show. Encode that in the URL with a **param** — a path segment starting with `:`:

```html
<Route path="/recipes/:id" element={<RecipeDetail />} />
```

Now `/recipes/52772` and `/recipes/52959` both render `RecipeDetail`. Inside it, read the param with the `useParams` hook:

```python
import { useParams } from "react-router-dom";

function RecipeDetail() {
  const { id } = useParams();   // "52772" from the URL

  // ...then fetch that one recipe (Chunk 4.4 pattern):
  // fetch(`.../lookup.php?i=${id}`)

  return <h2>Recipe #{id}</h2>;
}
```

Combine this with what you learned in 4.4: `useParams` gives you the `id`, you put `id` in a `useEffect` dependency array, and fetch that single recipe. Linking to it is just `<Link to={`/recipes/${meal.idMeal}`}>`.

> **💡 TheMealDB detail endpoint**
>
> Look up one meal by id:
>
> https://www.themealdb.com/api/json/v1/1/lookup.php?i=52772
>
> →
>
> { "meals": [ {one meal} ] }
>
> .

## 6. Nested layouts with `Outlet`

Most apps share a shell — a navbar and footer that stay put while the middle swaps. Instead of repeating the navbar in every page, define a **layout route** whose children render into an `<Outlet />` placeholder:

```python
// src/components/Layout.jsx
import { NavLink, Outlet } from "react-router-dom";

function Layout() {
  return (
    <>
      <header>
        <NavLink to="/">🍳 Recipe Box</NavLink>
        <NavLink to="/recipes">Recipes</NavLink>
      </header>
      <main>
        <Outlet />   {/* the matched child route renders here */}
      </main>
    </>
  );
}
export default Layout;
```

Then nest your pages inside the layout route:

```html
<Routes>
  <Route element={<Layout />}>
    <Route path="/" element={<Home />} />
    <Route path="/recipes" element={<Recipes />} />
    <Route path="/recipes/:id" element={<RecipeDetail />} />
    <Route path="*" element={<NotFound />} />
  </Route>
</Routes>
```

The header now shows on every page automatically; only the `<Outlet />` contents change as you navigate.

## 7. Programmatic navigation

Sometimes you navigate from code — after a form submit, or a "Back" button. Use the `useNavigate` hook:

```python
import { useNavigate } from "react-router-dom";

function BackButton() {
  const navigate = useNavigate();
  return <button onClick={() => navigate(-1)}>← Back</button>;
}

// navigate("/recipes")  → go to a path
// navigate(-1)           → go back one step (like the browser Back button)
```

## ✅ Recap

- **Client-side routing** swaps components based on the URL — no page reloads, Back/Forward work, links are shareable.
- Install `react-router-dom`; wrap the app in `<BrowserRouter>`.
- Map URLs to components with `<Routes>` / `<Route path element>`; `path="*"` is your 404.
- Navigate with `<Link>` / `<NavLink>` (never `<a>` for internal links).
- Dynamic segments like `:id` are read with `useParams()`.
- Share a shell with a layout route + `<Outlet />`; navigate from code with `useNavigate()`.

**Next:** open `assignment.html` and build a multi-page recipe app.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
