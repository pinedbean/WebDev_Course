*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.4 — Lab: Fetch Live Recipes

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Replace the hardcoded recipe array from Chunk 4.2 with **live data from a public API**. Fetch recipes on mount with `useEffect`, render them in your `RecipeCard` grid, and handle the **loading**, **error**, and **empty** states properly.

## Before you start

- Work in `recipe-box`; run `npm run dev`.
- The API: **TheMealDB** (free, no key). Try this URL in your browser to see the JSON shape:  
 `https://www.themealdb.com/api/json/v1/1/search.php?s=chicken`
- Useful fields per meal: `idMeal`, `strMeal`, `strArea`, `strCategory`, `strMealThumb`.

> **⚠️ Try it yourself first**
>
> The loading/error/success ladder from the lecture is your blueprint. Only peek at the solution if you get stuck.

## Tasks

### 1 Three state variables

In a component (e.g. `RecipeList`), declare state for `meals` (array), `loading` (boolean, start `true`), and `error` (string/null).

### 2 Fetch on mount

In a `useEffect` with a `[]` dependency array, define an `async` function that fetches from TheMealDB, parses JSON, and stores `data.meals` in state. Call it inside the effect.

### 3 Handle errors

Wrap the fetch in `try/catch/finally`. Throw if `!res.ok`. On catch, store the error message. In `finally`, set `loading` to `false`. Remember the API returns `meals: null` when nothing matches — coerce to `[]`.

### 4 Render the three states

Before the grid: if `loading`, show a loading message; if `error`, show an error message; if the list is empty, say "No recipes found". Otherwise render the grid of `RecipeCard`s (reuse your Chunk 4.2 component — map the API fields onto its props).

### 5 Add a search box (re-fetch on change)

Add a controlled input for the search term, stored in state. Put that term in the effect's dependency array so changing it re-fetches. (Bonus: debounce it — see stretch goals.)

### 6 Test the failure path

Temporarily break the URL (e.g. a typo) and confirm your error UI appears instead of a blank page or a crash. Then fix it.

## ✅ Deliverable — acceptance checklist

- Recipes load from TheMealDB on mount via `useEffect` with a correct dependency array.
- A loading indicator shows while the request is in flight.
- A clear error message shows if the request fails (and the app doesn't crash).
- An empty-results message shows when a search has no matches.
- Successful results render in the `RecipeCard` grid with images and unique keys.
- Typing in the search box re-fetches and updates the results.
- No infinite request loop (check the Network tab — one request per search, not hundreds).

## 🚀 Stretch goals (optional)

- **Debounce** the search: wait ~400ms after the user stops typing before fetching (use `setTimeout` + cleanup in the effect).
- Add a cleanup flag to ignore stale responses (the race-condition guard from the lecture).
- Show a result count: "Found 12 recipes".
- Fetch categories from `.../categories.php` and render them as filter buttons.
- Throttle the network in DevTools (Slow 3G) to really see your loading state.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
