*Full-Stack Web Dev · Module 4 — React + Vite*

# Chunk 4.1 — Lab: Scaffold & Customize a React App

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Create a brand-new React project with Vite, run the dev server, and replace the generated boilerplate with your own **landing component**. This project — `recipe-box` — is the app you'll grow across all of Module 4.

## Before you start

- Confirm Node.js is installed: run `node --version` (you want v18 or newer).
- Pick a home for the project, e.g. `~/Desktop/webdev-course/module-04-react-vite/`.
- Have VS Code and a browser ready.

> **⚠️ Try it yourself first**
>
> Work from the lecture and the prompts below. Only open
>
> solution.html
>
> when you're stuck or to compare at the end.

## Tasks

### 1 Scaffold the project

In your terminal, `cd` into your Module 4 folder and run `npm create vite@latest`. When prompted, name the project `recipe-box`, choose the **React** framework and the **JavaScript** variant.

### 2 Install & run

Follow the three commands Vite prints: `cd recipe-box`, `npm install`, then `npm run dev`. Open the `http://localhost:5173/` URL in your browser and confirm you see the default Vite + React counter page.

### 3 Open the project & explore

In a second terminal tab (leave the server running) or via Finder, open the folder in VS Code (`code .`). Find and read these files: `index.html`, `src/main.jsx`, `src/App.jsx`. Notice how `main.jsx` renders `<App />` into `#root`.

### 4 Replace `App.jsx` with your own landing component

Delete the boilerplate inside `src/App.jsx` and write your own. It should be a single function component that returns JSX containing:

- An `<h1>` with your project name (e.g. `🍳 Recipe Box`).
- At least one `<p>` describing the app.
- At least one value pulled in with `{ }` from a JavaScript variable (e.g. store the project name in a `const` and render `{projectName}`).

Remember the JSX rules: one root element, `className` not `class`, close every tag.

### 5 See HMR in action

With the browser visible next to your editor, change some text in `App.jsx` and **save**. Watch the page update instantly without a manual refresh. That's Hot Module Replacement.

### 6 Tidy up `index.html`

Open `index.html` and change the `<title>` to your project name so the browser tab reads "Recipe Box" instead of "Vite + React".

## ✅ Deliverable — acceptance checklist

- A `recipe-box/` project created with Vite (React + JavaScript).
- `npm run dev` runs and the app loads at `http://localhost:5173/` with no console errors.
- `src/App.jsx` is your own component (boilerplate removed).
- The landing page shows your project name in an `<h1>` and at least one `{ }` JavaScript expression renders correctly.
- Editing and saving a file updates the browser automatically (HMR works).
- The browser tab title is your project name.

## 🚀 Stretch goals (optional)

- Add a second variable (e.g. `const tagline = "Find & save recipes"`) and render it.
- Use a Fragment `<>...</>` instead of a wrapper `<div>` as your root element.
- Edit `src/index.css` to change the page background color and confirm HMR picks up CSS changes too.
- Stop the server with `Ctrl`+`C`, then run `npm run build` followed by `npm run preview` to see the production build. (You'll use this for real in Module 9.)
- Initialize git in the project and make a first commit (`git init`, `git add .`, `git commit -m "Scaffold recipe-box"`). Note the generated `.gitignore` already excludes `node_modules`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
