*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.5 — Lab: A Multi-Page Recipe App

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Turn `recipe-box` into a real multi-page app with React Router: a **Home** page, a **Recipes** list (your fetch from 4.4), and a **Recipe detail** page reached by clicking a card. All wrapped in a shared navbar layout, with a 404 page for unknown URLs.

## Before you start

- Open `recipe-box` and run `npm run dev`.
- You'll reuse the fetch logic from 4.4. Detail endpoint: `https://www.themealdb.com/api/json/v1/1/lookup.php?i=ID`.
- Plan a `src/pages/` folder for screen components and a `src/components/Layout.jsx`.

> **⚠️ Try it yourself first**
>
> Use the lecture as your map. Only open the solution when stuck or to compare.

## Tasks

### 1 Install & wrap

Run `npm install react-router-dom`. In `main.jsx`, wrap `<App />` in `<BrowserRouter>`.

### 2 Build the pages

Create `src/pages/Home.jsx` (a welcome screen with a link to Recipes), `src/pages/Recipes.jsx` (the search + grid from 4.4), `src/pages/RecipeDetail.jsx` (one recipe), and `src/pages/NotFound.jsx` (a friendly 404).

### 3 Define routes in `App`

Use `<Routes>`/`<Route>` to map: `/` → Home, `/recipes` → Recipes, `/recipes/:id` → RecipeDetail, `*` → NotFound.

### 4 Add a shared layout with a navbar

Create `Layout.jsx` with a navbar of `<NavLink>`s and an `<Outlet />`. Nest all your routes inside a layout route so the navbar shows on every page. Style the active link.

### 5 Make cards link to detail

Wrap each `RecipeCard` in (or give it) a `<Link to={`/recipes/${idMeal}`}>` so clicking a card navigates to its detail page — with no full reload.

### 6 Fetch one recipe in detail

In `RecipeDetail`, read the `id` with `useParams()`, fetch that single recipe (lookup endpoint) with the loading/error pattern from 4.4, and show its image, title, category, area, and instructions. Add a "← Back" button using `useNavigate(-1)`.

### 7 Verify routing behavior

Click around: the URL changes, no white flash, the Back button works, and visiting a bad URL (e.g. `/nope`) shows your 404. Refreshing `/recipes` still loads it.

## ✅ Deliverable — acceptance checklist

- `react-router-dom` installed; app wrapped in `<BrowserRouter>`.
- Four routes work: Home `/`, Recipes `/recipes`, Detail `/recipes/:id`, and a `*` 404.
- A shared navbar (from a layout + `<Outlet />`) appears on every page, with the active link styled.
- Clicking a recipe card navigates to its detail page using `Link` (no page reload).
- The detail page reads `:id` with `useParams` and fetches that one recipe with loading/error handling.
- A working "Back" button uses `useNavigate`.
- The browser Back/Forward buttons and an unknown URL all behave correctly.

## 🚀 Stretch goals (optional)

- Add an **About** page and link to it from the navbar.
- On the detail page, render the ingredient list (TheMealDB stores them as `strIngredient1..20`).
- Show a loading skeleton on the detail page instead of plain "Loading…".
- Use a **query string** for the search term (e.g. `/recipes?q=beef`) with `useSearchParams` so searches are shareable.
- Highlight the active nav tab with an underline animation.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
