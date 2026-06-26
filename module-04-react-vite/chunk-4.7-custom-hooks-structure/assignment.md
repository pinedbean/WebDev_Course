*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.7 — Lab: Refactor + 🏁 Module 4 Checkpoint

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

This lab has two parts. **Part A:** refactor `recipe-box` — extract a reusable `useFetch` hook, centralize API calls, move to environment-based config, and reorganize the folders. **Part B (🏁 Checkpoint):** pull the whole module together into a polished **Recipe Browser** app consuming a public API.

## Before you start

- Open `recipe-box` (with everything from 4.1–4.6). Run `npm run dev`.
- This is the capstone of Module 4 — budget the full session.

> **⚠️ Try it yourself first**
>
> You've built every piece already; this is about composing and cleaning. Reach for the solution only when stuck.

## Part A — Refactor & Structure

### 1 Extract `useFetch`

Create `src/hooks/useFetch.js` that takes a `url` and returns `{ data, loading, error }` (the lifecycle from 4.4, including the `active` cleanup flag and `res.ok` check).

### 2 Use it everywhere

Replace the hand-written fetch code in your `Recipes` and `RecipeDetail` pages with `useFetch`. Confirm both pages still work and are now much shorter.

### 3 Centralize API calls

Create `src/api/recipes.js` with helpers that build URLs: `searchUrl(query)` and `lookupUrl(id)` (or full fetch functions). Use them from your pages so no raw URL strings live in components.

### 4 Environment config

Add a `.env` with `VITE_API_BASE=https://www.themealdb.com/api/json/v1/1`. Read it via `import.meta.env.VITE_API_BASE` in `api/recipes.js`. Restart the dev server and confirm everything still loads. Add `.env.local` to `.gitignore`.

### 5 Reorganize folders

Arrange `src/` into `api/`, `components/`, `pages/`, `hooks/`, `context/`. Fix imports. The app should run with no console errors after the move.

## 🏁 Part B — Module 4 Checkpoint: Recipe Browser

Build (or finish polishing) a small, self-contained **Recipe Browser** that consumes the public TheMealDB API and uses *everything* from Module 4. If your `recipe-box` already has these pieces, your job is to tie them into a coherent, finished app. The checkpoint app must demonstrate:

- **Components & props (4.2):** a reusable `RecipeCard` in a responsive grid.
- **State & events (4.3):** a controlled search input.
- **Data fetching (4.4) via your `useFetch` (4.7):** live results with loading, error, and empty states.
- **Routing (4.5):** Home, a Browse/list page, and a Recipe detail page (`/recipes/:id`) with a working Back button and a 404 route.
- **Forms & Context (4.6):** a Favorites feature shared across pages, with a live count in the navbar and a dedicated Favorites page.
- **Structure (4.7):** clean `api/components/pages/hooks/context` folders and env-based config.

> **💡 Prefer a different theme?**
>
> A movie browser works just as well. TheMealDB has a sibling,
>
> TheCocktailDB
>
> (same no-key style), and there are open APIs for books, Pokémon, and more. If you want movies specifically, TMDB/OMDb need a free API key — fine to use, just keep the key in
>
> .env
>
> and remember frontend env vars aren't truly secret.

## ✅ Deliverable — acceptance checklist

- A reusable `useFetch` hook in `src/hooks/` powers all data fetching.
- No raw API URL strings in components — they come from `src/api/`.
- The API base URL comes from a `VITE_` environment variable via `import.meta.env`.
- `src/` is organized into `api / components / pages / hooks / context` with working imports.
- **Checkpoint:** the Recipe Browser runs with no console errors and demonstrates components, state, fetching, routing, and Context.
- **Checkpoint:** search, loading/error/empty states, list → detail navigation, and shared favorites all work end to end.
- (Recommended) A short `README.md` describing the app and how to run it (`npm install` && `npm run dev`).

## 🚀 Stretch goals (optional)

- Persist favorites to `localStorage` so they survive refreshes.
- Add filtering by category (TheMealDB `/filter.php?c=Seafood`) as a second route or dropdown.
- Generalize `useFetch` to skip the request when `url` is falsy (so a detail page doesn't fetch with no id).
- Add a loading skeleton component and a nicer error UI.
- Run `npm run build` and `npm run preview` to confirm the production build works (sets you up for Module 9).
- Deploy the build to a static host (e.g. Netlify/GitHub Pages) and share the link.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
