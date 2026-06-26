*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll build the card grid file by file. Complete copy-pasteable files are at the bottom. Final structure:

```text
recipe-box/
└── src/
    ├── App.jsx
    ├── index.css
    └── components/
        └── RecipeCard.jsx
```

### 1 The data array

At the top of `src/App.jsx`, define the recipes. Each needs a unique `id`.

```javascript
const recipes = [
  { id: 1, title: "Pad Thai",       area: "Thai",    minutes: 25, isFavorite: true  },
  { id: 2, title: "Carbonara",      area: "Italian", minutes: 20, isFavorite: false },
  { id: 3, title: "Beef Tacos",     area: "Mexican", minutes: 30, isFavorite: true  },
  { id: 4, title: "Butter Chicken", area: "Indian",  minutes: 45, isFavorite: false },
  { id: 5, title: "Miso Ramen",     area: "Japanese",minutes: 40, isFavorite: false },
  { id: 6, title: "Greek Salad",    area: "Greek",   minutes: 15, isFavorite: true  },
];
```

### 2 The `RecipeCard` component

Create `src/components/RecipeCard.jsx`. Destructure the props in the signature.

```jsx
function RecipeCard({ title, area, minutes, isFavorite }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      <p className="meta">{area} · {minutes} min</p>
    </article>
  );
}

export default RecipeCard;
```

### 3 Conditional rendering inside the card

Add the favorite badge with `&&` and the speed label with a ternary:

```jsx
function RecipeCard({ title, area, minutes, isFavorite }) {
  return (
    <article className="card">
      {isFavorite && <span className="star">⭐ Favorite</span>}
      <h3>{title}</h3>
      <p className="meta">{area} · {minutes} min</p>
      <p>{minutes < 30 ? "⚡ Quick" : "🕒 Takes a while"}</p>
    </article>
  );
}

export default RecipeCard;
```

### 4 Map the data into cards

In `App.jsx`, import the component and map. Each card gets a `key`:

```python
import RecipeCard from "./components/RecipeCard";

function App() {
  return (
    <main>
      <h1>🍳 Recipe Box</h1>
      <div className="grid">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} {...recipe} />
        ))}
      </div>
    </main>
  );
}
```

We use `{...recipe}` to spread every field as a prop. `key` stays explicit.

### 5 Style the grid

Replace `src/index.css` with grid + card styles (CSS Grid from Module 2):

```
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0;
  padding: 24px;
  background: #f1f5f9;
  color: #1e293b;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
}
.card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
}
.card h3 { margin: 6px 0; }
.meta { color: #64748b; font-size: 14px; }
.star { color: #b45309; font-size: 13px; font-weight: 600; }
```

### 6 Check the console

Open DevTools → Console. You should see no warnings. If you see *"Each child in a list should have a unique key prop"*, you forgot the `key` on the mapped element — add `key={recipe.id}`.

## 📄 Complete `src/components/RecipeCard.jsx`

```jsx
function RecipeCard({ title, area, minutes, isFavorite }) {
  return (
    <article className="card">
      {isFavorite && <span className="star">⭐ Favorite</span>}
      <h3>{title}</h3>
      <p className="meta">{area} · {minutes} min</p>
      <p>{minutes < 30 ? "⚡ Quick" : "🕒 Takes a while"}</p>
    </article>
  );
}

export default RecipeCard;
```

## 📄 Complete `src/App.jsx`

```python
import RecipeCard from "./components/RecipeCard";
import "./index.css";

const recipes = [
  { id: 1, title: "Pad Thai",       area: "Thai",     minutes: 25, isFavorite: true  },
  { id: 2, title: "Carbonara",      area: "Italian",  minutes: 20, isFavorite: false },
  { id: 3, title: "Beef Tacos",     area: "Mexican",  minutes: 30, isFavorite: true  },
  { id: 4, title: "Butter Chicken", area: "Indian",   minutes: 45, isFavorite: false },
  { id: 5, title: "Miso Ramen",     area: "Japanese", minutes: 40, isFavorite: false },
  { id: 6, title: "Greek Salad",    area: "Greek",    minutes: 15, isFavorite: true  },
];

function App() {
  return (
    <main>
      <h1>🍳 Recipe Box</h1>
      <div className="grid">
        {recipes.map((recipe) => (
          <RecipeCard key={recipe.id} {...recipe} />
        ))}
      </div>
    </main>
  );
}

export default App;
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| Nothing renders / blank page | Check the import path: `./components/RecipeCard` (relative to `App.jsx`). Case matters. |
| Cards stack in one column | Confirm `.grid` CSS is loaded — import `./index.css` (or it's imported in `main.jsx`) and the wrapper has `className="grid"`. |
| A literal `0` appears on a card | You used `&&` with a numeric left side. Use a ternary or compare explicitly (`x > 0 && ...`). |
| Key warning persists | The `key` goes on the outermost element returned by `.map()` — here the `<RecipeCard>`, not inside it. |

## 🎉 You're done

You built a reusable component, fed it data through props, rendered a data-driven grid with `.map()` and keys, and showed UI conditionally. This is the core React workflow you'll use forever.

**Up next → Chunk 4.3: State & Events with Hooks** — you'll make components *interactive* with `useState` by rebuilding your Module 3 to-do app in React.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
