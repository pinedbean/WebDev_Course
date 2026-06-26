*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.1 — Vite + React Project Setup

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- **Why React exists** — the problem with hand-writing DOM updates (which you felt in Module 3).
- **Why Vite** — what a dev server and bundler do, and why it's so fast.
- How to scaffold a React app with `npm create vite@latest` and run the dev server.
- The anatomy of a Vite + React project, and how a component ends up on screen.
- **JSX** — the HTML-in-JavaScript syntax React uses.

In the lab you'll create a fresh React project and customize its landing component.

## 1. Where we left off — and the problem React solves

In Module 3 you built a to-do app in vanilla JavaScript. To add a single item you had to: create an element, set its `textContent`, build a delete button, attach a listener, and `appendChild` it. To mark something done you hunted for the element with `querySelector` and toggled a class by hand. Your data lived in one place (a JS array) and the screen lived in another (the DOM), and *you* were the glue keeping them in sync.

That manual syncing is where bugs breed. Forget to update the DOM after changing the array and the screen lies. This is the exact pain **React** was built to remove.

> **📝 The big idea**
>
> In React you
>
> describe what the UI should look like for a given set of data
>
> , and React figures out the DOM changes for you. You change the data; the screen follows automatically. This is called
>
> declarative
>
> UI (you declare the result) versus the
>
> imperative
>
> DOM code (step-by-step instructions) you wrote in Module 3.

## 2. What is React?

**React** is a JavaScript library for building user interfaces out of **components** — small, reusable functions that return a piece of UI. You compose those pieces into a whole app, the way you nest HTML elements.

Two ideas power everything in this module:

- **Components** — a function that returns markup. `<Navbar />`, `<TodoItem />`, `<App />`. You'll write dozens.
- **State** — the data a component remembers. When state changes, React **re-renders** the component (calls the function again) and updates only the parts of the real DOM that actually changed.

That "updates only what changed" magic comes from React keeping a lightweight copy of the UI in memory (often called the **virtual DOM**), comparing it to the previous version, and applying the minimal set of real DOM edits. You never call `appendChild` again.

> **💡 Function components & hooks only**
>
> Modern React (18+) is written with
>
> function components
>
> and
>
> hooks
>
> (functions like
>
> useState
>
> you'll meet in 4.3). Older tutorials use "class components" — you can safely ignore those for this course.

## 3. What is Vite, and why not just open an HTML file?

Browsers don't understand JSX (the HTML-in-JS you're about to see), and a real app is split across many files. Something has to translate and bundle that code for the browser. That something is a **build tool**. **Vite** (French for "quick", pronounced "veet") is the modern standard.

Vite gives you two things:

- A **dev server** — run `npm run dev` and it serves your app at a local URL with **Hot Module Replacement (HMR)**: save a file and the browser updates instantly, often without losing your place.
- A **build** command — `npm run build` bundles and optimizes everything into static files for production (you'll use this in Module 9).

You met Vite briefly at the end of Module 3. Now it becomes your everyday tool.

> **📝 You need Node.js**
>
> Vite runs on
>
> Node.js
>
> (installed back in Module 0). Check it's ready:
>
> node --version
>
> should print v18 or newer. Vite 5+ requires Node 18+.

## 4. Scaffolding a project with `create vite`

You don't build the boilerplate by hand. One command generates a ready-to-run project:

```bash
npm create vite@latest
```

It asks you a few questions interactively:

| Prompt | Your answer |
| --- | --- |
| Project name | `recipe-box` (our Module 4 project) |
| Select a framework | **React** |
| Select a variant | **JavaScript** (we'll skip TypeScript for now) |

Then you install dependencies and start the server:

```bash
cd recipe-box
npm install
npm run dev
```

Vite prints a local URL — open it in your browser:

```
  VITE v5.x.x  ready in 312 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

> **💡 What is npm doing?**
>
> npm create vite@latest
>
> downloads and runs the latest project generator.
>
> npm install
>
> reads
>
> package.json
>
> and downloads React + Vite into a
>
> node_modules/
>
> folder.
>
> npm run dev
>
> runs the "dev" script defined in
>
> package.json
>
> . You learned about
>
> package.json
>
> and npm in Chunk 3.5 — same ideas.

## 5. A tour of the project

Open the folder in VS Code. Here's what matters (some files trimmed):

```text
recipe-box/
├── index.html          ← the ONE real HTML page the browser loads
├── package.json        ← project metadata + scripts + dependencies
├── vite.config.js      ← Vite configuration
├── public/             ← static files served as-is (favicon, images)
└── src/                ← all your React code lives here
    ├── main.jsx        ← entry point: mounts React into the page
    ├── App.jsx         ← your root component
    ├── App.css         ← styles for App
    └── index.css       ← global styles
```

Two files deserve a closer look.

### `index.html` — surprisingly empty

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Vite + React</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

There's no visible content — just an empty `<div id="root">` and a script tag. This is a **Single Page Application (SPA)**: the HTML is a shell, and React builds the entire page inside `#root` with JavaScript.

### `main.jsx` — the entry point

```python
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

Read it top to bottom: import React, find the `#root` div, and **render** your `<App />` component into it. `<React.StrictMode>` is a development helper that points out potential problems — leave it on.

## 6. JSX — HTML inside JavaScript

That `<App />` and the markup components return is **JSX**. It looks like HTML but it lives inside `.jsx` files and Vite compiles it to real JavaScript. Here's a minimal component:

```jsx
function App() {
  const name = "Jane";
  return (
    <div>
      <h1>Hello, {name}! 👋</h1>
      <p>My first React component.</p>
    </div>
  );
}

export default App;
```

A component is just a function that `return`s JSX. The curly braces `{name}` drop a JavaScript value into the markup — any expression works: `{2 + 2}`, `{user.email}`, `{items.length}`.

JSX looks like HTML but has a few important rules:

| Rule | Why / example |
| --- | --- |
| **Return one root element** | A function returns one thing. Wrap siblings in a `<div>` or an empty `<>...</>` (a "Fragment"). |
| **`className`, not `class`** | `class` is a reserved word in JS, so JSX uses `className="card"`. |
| **Close every tag** | Even self-closing ones: `<img />`, `<br />`, `<input />`. |
| **camelCase attributes** | `onclick` → `onClick`, `tabindex` → `tabIndex`. |
| **`{ }` for JS** | Embed expressions: `{count}`, `{user.name}`, `{price * 2}`. |

> **⚠️ JSX is not HTML**
>
> It's JavaScript that
>
> looks
>
> like HTML. That's why
>
> class
>
> becomes
>
> className
>
> and why you can write
>
> {anyExpression}
>
> right in the middle of your markup. Mixing up the two is the most common beginner stumble — when in doubt, remember: it's JS.

## 7. How a component reaches the screen

Putting it together, here is the full path from a file to a pixel:

1. The browser loads `index.html` and runs `<script src="/src/main.jsx">`.
2. `main.jsx` calls `createRoot(...).render(<App />)`.
3. React calls your `App()` function, gets the JSX it returns, and turns it into real DOM nodes inside `#root`.
4. Later, when data (state) changes, React calls `App()` again, compares the new result with the old one, and updates only what differs.

You write components; React owns the DOM. That trade is the whole point.

## 8. Editing your first component

With `npm run dev` running, open `src/App.jsx`, delete the generated boilerplate, and replace it with something of your own:

```jsx
function App() {
  const projectName = "Recipe Box";
  return (
    <main>
      <h1>🍳 {projectName}</h1>
      <p>A React app I'm building in Module 4.</p>
    </main>
  );
}

export default App;
```

Save the file. Thanks to HMR, the browser updates the instant you hit save — no refresh, no rebuild. That tight feedback loop is what makes React development feel fast.

## ✅ Recap

- React lets you write **declarative** UI: describe the result for given data, and React updates the DOM for you.
- Apps are built from **components** — functions that return **JSX**.
- **Vite** is the build tool: `npm create vite@latest` scaffolds, `npm run dev` serves with instant Hot Module Replacement.
- An SPA loads one near-empty `index.html`; `main.jsx` mounts `<App />` into `#root`.
- JSX rules: one root element, `className`, close all tags, camelCase attributes, `{ }` for JavaScript.

**Next:** open `assignment.html` and scaffold your own React app.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
