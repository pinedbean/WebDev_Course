*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Follow the steps to scaffold `recipe-box` and write your first component. Each step gives the exact command/code and what you should see. The complete `App.jsx` is at the bottom.

### 1 Scaffold the project

From your Module 4 folder, run the generator:

```bash
npm create vite@latest
```

Answer the prompts (use arrow keys + Enter to select):

```
? Project name: › recipe-box
? Select a framework: › React
? Select a variant: › JavaScript
```

> **💡 Shortcut**
>
> You can skip the questions by passing them as flags:
>
> npm create vite@latest recipe-box -- --template react
>
> .

### 2 Install & run

Vite tells you exactly what to do next:

```bash
cd recipe-box
npm install
npm run dev
```

You should see:

```
  VITE v5.x.x  ready in 312 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h + enter to show help
```

Open `http://localhost:5173/` — the default page shows the Vite + React logos and a counter button.

> **⚠️ Port already in use?**
>
> If 5173 is taken, Vite automatically picks the next free port (5174, 5175...). Use whatever URL it prints. Leave this terminal running — the server stays alive until you press
>
> Ctrl
>
> +
>
> C
>
> .

### 3 What got generated

Open the folder in VS Code. The structure you care about:

```text
recipe-box/
├── index.html
├── package.json
├── vite.config.js
├── public/
│   └── vite.svg
└── src/
    ├── main.jsx      ← mounts <App /> into #root
    ├── App.jsx       ← the component you'll edit
    ├── App.css
    ├── index.css
    └── assets/
```

Read `src/main.jsx` — it's the wiring that puts `<App />` on the page.

### 4 Write your own `App.jsx`

Open `src/App.jsx`, select all, delete it, and replace it with your own component. We'll keep the default `import './App.css'` out for now to stay focused:

```jsx
function App() {
  const projectName = "Recipe Box";
  const tagline = "Find and save recipes — built with React.";

  return (
    <main>
      <h1>🍳 {projectName}</h1>
      <p>{tagline}</p>
      <p>This app grows across all of Module 4.</p>
    </main>
  );
}

export default App;
```

> **⚠️ "Adjacent JSX elements must be wrapped"?**
>
> That error means you returned two sibling elements without one parent. Wrap them in a single
>
> <main>
>
> /
>
> <div>
>
> or an empty Fragment
>
> <>...</>
>
> .

### 5 Confirm HMR

Save the file. The browser updates immediately — no refresh. Change "Recipe Box" to anything and watch it swap in real time. This instant feedback loop is HMR.

### 6 Fix the tab title

In `index.html`, update the title element:

```html
<title>Recipe Box</title>
```

The browser tab now reads "Recipe Box".

## 📄 Complete `src/App.jsx`

```jsx
function App() {
  const projectName = "Recipe Box";
  const tagline = "Find and save recipes — built with React.";

  return (
    <main>
      <h1>🍳 {projectName}</h1>
      <p>{tagline}</p>
      <p>This app grows across all of Module 4.</p>
    </main>
  );
}

export default App;
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `command not found: npm` | Node.js isn't installed or isn't on your PATH. Reinstall Node LTS (Module 0) and reopen the terminal. |
| Blank white page | Open DevTools → Console. A red error usually means a typo in JSX (unclosed tag, missing root element). |
| Page didn't update on save | Make sure you saved (`Cmd`+`S`) and that `npm run dev` is still running in the terminal. |
| `npm install` is very slow / fails | Check your internet connection; try again. It downloads into `node_modules/` once. |

## 🎉 You're done

You scaffolded a real React app, ran it with Vite, and replaced the boilerplate with your own component. You now have the project that the rest of Module 4 builds on.

**Keep `recipe-box` around** — in Chunk 4.2 you'll break the UI into reusable `Card` components and render a grid from data.

**Up next → Chunk 4.2: Components & Props.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
