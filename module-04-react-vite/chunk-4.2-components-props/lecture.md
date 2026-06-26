*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.2 — Components & Props

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to split a UI into **reusable components**, each in its own file.
- **Props** — passing data into a component, like attributes/arguments.
- **Composition** — building big components out of small ones (and the `children` prop).
- **Conditional rendering** — showing UI only when it should appear.
- **Rendering lists** with `.map()` and why every item needs a `key`.

In the lab you'll build a `RecipeCard` component and render a grid of cards from a data array.

## 1. Why components?

In Chunk 4.1 your whole app was one `App` component. Real UIs repeat: a feed of posts, a list of products, a grid of recipe cards. You don't want to copy-paste the same markup ten times. Instead you write the markup **once** as a component and reuse it, feeding each copy different data.

Think of a component like a function that returns UI, and **props** as its arguments. Same shape, different inputs, different output.

> **📝 The mental model**
>
> A page is a tree of components:
>
> <App>
>
> contains a
>
> <RecipeGrid>
>
> which contains many
>
> <RecipeCard>
>
> . Each one is a small, focused, reusable function.

## 2. Props — passing data in

You pass data to a component using attribute-like syntax, and the component receives them as a single `props` object:

```html
function Greeting(props) {
  return <h2>Hello, {props.name}!</h2>;
}

// Using it — pass data with attributes:
<Greeting name="Jane" />
<Greeting name="Sam" />
```

The first renders "Hello, Jane!", the second "Hello, Sam!". Same component, different props.

### Destructuring props (the common style)

Reading `props.name`, `props.title` everywhere is noisy. Destructure the props object right in the function signature:

```html
function Greeting({ name }) {
  return <h2>Hello, {name}!</h2>;
}
```

You used destructuring on objects back in Chunk 3.2 — this is the same trick. You'll see this style in nearly all React code.

### Props can be any type

Strings use quotes; everything else (numbers, booleans, arrays, objects, functions) goes inside `{ }`:

```html
<RecipeCard
  title="Pad Thai"
  minutes={25}
  isFavorite={true}
  tags={["thai", "noodles"]}
/>
```

> **⚠️ Props are read-only**
>
> A component must
>
> never
>
> change its own props — treat them as read-only inputs from the parent. (Data a component owns and changes is "state", coming in Chunk 4.3.)

## 3. A component in its own file

Each component usually lives in its own file under `src/components/`, and is `export`ed/`import`ed using the ES modules you learned in Chunk 3.5. Here's a `RecipeCard`:

```jsx
// src/components/RecipeCard.jsx
function RecipeCard({ title, area, minutes }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      <p>{area} cuisine · {minutes} min</p>
    </article>
  );
}

export default RecipeCard;
```

And using it from `App.jsx`:

```python
// src/App.jsx
import RecipeCard from "./components/RecipeCard";

function App() {
  return (
    <main>
      <h1>🍳 Recipe Box</h1>
      <RecipeCard title="Pad Thai" area="Thai" minutes={25} />
      <RecipeCard title="Carbonara" area="Italian" minutes={20} />
    </main>
  );
}

export default App;
```

> **💡 Capitalize component names**
>
> Component names must start with a
>
> capital letter
>
> (
>
> RecipeCard
>
> , not
>
> recipeCard
>
> ). React treats lowercase tags as plain HTML elements and capitalized ones as your components.

## 4. Composition & the `children` prop

Components nest inside other components — that's **composition**. Sometimes you want a wrapper component that can hold *any* content. React passes whatever you put between the tags as a special prop called `children`:

```jsx
function Panel({ children }) {
  return <div className="panel">{children}</div>;
}

// Anything between the tags becomes `children`:
<Panel>
  <h3>Featured</h3>
  <p>Today's top recipe.</p>
</Panel>
```

This is how you build reusable layout shells (cards, modals, sidebars) that wrap arbitrary content.

## 5. Conditional rendering

Often a piece of UI should appear only sometimes — a "Favorite ⭐" badge, an "out of stock" label. Because JSX is JavaScript, you use normal JS to decide.

### The `&&` pattern (show or nothing)

```jsx
function RecipeCard({ title, isFavorite }) {
  return (
    <article className="card">
      <h3>{title}</h3>
      {isFavorite && <span>⭐ Favorite</span>}
    </article>
  );
}
```

`condition && element` renders the element only when the condition is true; otherwise it renders nothing.

### The ternary `? :` pattern (this or that)

```html
{minutes < 30 ? <span>Quick</span> : <span>Takes a while</span>}
```

> **⚠️ Watch out for `0`**
>
> With
>
> &&
>
> , a left side of
>
> 0
>
> renders the number
>
> 0
>
> on screen (because
>
> 0
>
> is falsy but still a renderable value). If a count might be zero, prefer a ternary or write
>
> count > 0 && ...
>
> .

## 6. Rendering lists with `.map()`

You rarely hardcode ten cards. Instead you keep data in an array and transform it into JSX with `.map()` — the same array method from Chunk 3.2, but now it returns elements:

```jsx
const recipes = [
  { id: 1, title: "Pad Thai", area: "Thai", minutes: 25 },
  { id: 2, title: "Carbonara", area: "Italian", minutes: 20 },
  { id: 3, title: "Tacos", area: "Mexican", minutes: 30 },
];

function App() {
  return (
    <main>
      <h1>🍳 Recipe Box</h1>
      <div className="grid">
        {recipes.map((recipe) => (
          <RecipeCard
            key={recipe.id}
            title={recipe.title}
            area={recipe.area}
            minutes={recipe.minutes}
          />
        ))}
      </div>
    </main>
  );
}
```

You loop over the data and return one `<RecipeCard />` per item. React renders the whole array.

### Why `key` matters

Notice `key={recipe.id}`. React needs a stable, unique `key` on each list item so it can track which item is which when the list changes (items added, removed, reordered). Without it, React warns in the console and may update the wrong rows.

> **💡 Good keys**
>
> Use a stable unique id from your data (
>
> recipe.id
>
> ). Avoid using the array index as a key when the list can reorder or items can be inserted/removed — it leads to subtle bugs.

## 7. Putting it together: spreading props

Passing `title={recipe.title} area={recipe.area} ...` for every field gets tedious. If the prop names match the object keys, you can spread the object:

```jsx
{recipes.map((recipe) => (
  <RecipeCard key={recipe.id} {...recipe} />
))}
```

`{...recipe}` passes every property of `recipe` as a prop. Still give an explicit `key` (it isn't a regular prop). This is a clean, common pattern for list rendering.

## ✅ Recap

- **Components** are reusable functions that return JSX; capitalize their names.
- **Props** pass data in (like arguments). Destructure them: `function Card({ title }) {...}`. Props are read-only.
- **Composition** nests components; the `children` prop holds whatever sits between a component's tags.
- **Conditional rendering**: `cond && element` for show/hide, `cond ? a : b` for either/or.
- **Lists**: `data.map(...)` returns elements; every item needs a stable unique `key`.

**Next:** open `assignment.html` and build a reusable card grid.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
