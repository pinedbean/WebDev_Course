*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.2 — Lab: Build a Recipe Card Grid

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

In your `recipe-box` app, build a reusable `RecipeCard` component and render a **grid of cards** from a data array using `.map()`. By the end you'll have a clean, repeating UI driven entirely by data — no copy-paste.

## Before you start

- Open the `recipe-box` project from Chunk 4.1 and run `npm run dev`.
- Create a `src/components/` folder — your components will live there.

> **⚠️ Try it yourself first**
>
> Lean on the lecture's worked examples. Only open
>
> solution.html
>
> when you're stuck or to compare.

## Tasks

### 1 Create the data

In `src/App.jsx`, define an array of at least **6 recipe objects**. Each object needs a unique `id` plus fields like `title`, `area` (cuisine), `minutes`, and a boolean `isFavorite`.

### 2 Build the `RecipeCard` component

Create `src/components/RecipeCard.jsx`. It receives props (`title`, `area`, `minutes`, `isFavorite`) — destructure them — and returns an `<article>` showing the title and details. `export default` it.

### 3 Add conditional rendering

Inside the card, show a **⭐ Favorite** badge only when `isFavorite` is true (use the `&&` pattern). Also show a "Quick" label when `minutes < 30`, otherwise "Takes a while" (use a ternary).

### 4 Render the grid with `.map()`

In `App.jsx`, `import` `RecipeCard` and map over your data array to render one card per recipe. Give each a `key={recipe.id}`. Wrap them in a `<div className="grid">`.

### 5 Make it a grid with CSS

In `src/index.css`, style `.grid` with CSS Grid (you learned Grid in Module 2) so the cards sit in a responsive grid, and give `.card` a border, padding, and rounded corners.

### 6 Clean check

Open DevTools → Console. There should be **no warnings** — especially no "Each child in a list should have a unique key" message.

## ✅ Deliverable — acceptance checklist

- A reusable `RecipeCard` component lives in `src/components/RecipeCard.jsx` and is imported into `App.jsx`.
- It receives data via **destructured props** and renders them.
- At least 6 cards render from a data array via `.map()`, each with a unique `key`.
- The ⭐ Favorite badge shows only on favorite recipes (conditional rendering).
- A "Quick" vs "Takes a while" label uses a ternary based on `minutes`.
- Cards display in a CSS grid; the console shows no key/list warnings.

## 🚀 Stretch goals (optional)

- Add an `<img>` to each card (use a placeholder URL like `https://placehold.co/300x200`) by adding an `image` field to your data.
- Extract a `RecipeGrid` component that takes the `recipes` array as a prop and does the mapping, so `App` stays tiny.
- Pass the whole object with spread: `<RecipeCard key={r.id} {...r} />`.
- Add a `Badge` component and use `children` to render different badge text.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
