*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.6 — Lab: Favorites with Shared State

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Add a **favorites** feature to `recipe-box` whose state is shared across pages via **Context**. Users can favorite/unfavorite any recipe (from the list or detail page), see the favorites count in the navbar, view all favorites on a **Favorites** page, and use a **form with validation** to add their own custom recipe to the favorites list.

## Before you start

- Continue in `recipe-box` (with routing from 4.5). Run `npm run dev`.
- Plan a `src/context/FavoritesContext.jsx`, a `Favorites` page, and an add-recipe form component.

> **⚠️ Try it yourself first**
>
> The lecture's three-part Context pattern (create → provide → consume) is your template. Reach for the solution only when stuck.

## Tasks

### 1 Build the Favorites context

Create `src/context/FavoritesContext.jsx` with a `FavoritesProvider` that holds a `favorites` array and exposes `addFavorite`, `removeFavorite`, and an `isFavorite(id)` helper. Export a `useFavorites()` hook.

### 2 Provide it

Wrap your app in `<FavoritesProvider>` (in `main.jsx`, inside `<BrowserRouter>`) so every page can read it.

### 3 Favorite toggle on cards/detail

On each recipe card and on the detail page, add a ⭐ button. Use `useFavorites()` to toggle: if `isFavorite(id)`, call `removeFavorite`, otherwise `addFavorite`. The button reflects the current state (filled vs outline star).

### 4 Show the count in the navbar

In your `Layout` navbar, read `favorites.length` from context and show it next to a "Favorites" `NavLink` — proof there's no prop drilling.

### 5 A Favorites page

Add a `/favorites` route and page that lists all favorited recipes (reuse your card UI). Each has a remove button. Show an empty state when there are none.

### 6 Add-your-own form with validation

On the Favorites page, add a form (multi-field: title, area/cuisine, minutes) held in one state object. Validate on submit: title required, minutes must be a positive number. Show per-field error messages. On valid submit, call `addFavorite` with a generated `id` and clear the form.

### 7 Verify sharing

Favorite a recipe on the list page, then navigate to `/favorites` — it's there. The navbar count updates everywhere instantly. Removing it on one page updates the others.

## ✅ Deliverable — acceptance checklist

- A `FavoritesProvider` + `useFavorites()` hook manage a shared favorites list via Context.
- Favoriting works from both the recipe list and the detail page, and the button reflects current state.
- The navbar shows a live favorites count read directly from context (no props passed down).
- A `/favorites` page lists all favorites with remove buttons and a friendly empty state.
- A multi-field form held in one state object adds a custom recipe to favorites.
- The form validates (title required, minutes positive) and shows per-field errors; it clears on success.
- Changes made on one page are reflected on the others (shared state confirmed).

## 🚀 Stretch goals (optional)

- Persist favorites to `localStorage` so they survive a refresh (a `useEffect` that saves on change, and a lazy initializer that loads on mount).
- Disable the submit button while the form is invalid.
- Add a "toast" confirmation when a favorite is added.
- Add a second context (e.g. a light/dark `ThemeContext`) to practice the pattern again.
- Make `useFavorites()` throw a clear error if used outside the provider.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
