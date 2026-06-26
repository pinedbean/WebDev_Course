*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.5 — ES Modules & Modern JS Tooling

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why we split code into **modules**, and how `import` / `export` work.
- The difference between a plain script and an ES module.
- What **npm** and `package.json` are and why every project has them.
- What a **bundler/dev server** does, and how to start one with **Vite**.

In the lab you'll refactor the to-do app from Chunk 3.3 into clean modules and run it under a Vite dev server with hot reload.

## 1. Why modules?

So far your scripts have been single files where every variable is global. That works for tiny apps, but it breaks down fast:

- **Name clashes** — two files both define `count` and silently overwrite each other.
- **No clear structure** — one giant file is hard to navigate and reuse.
- **Hidden dependencies** — you can't tell what relies on what.

**ES Modules** fix this: each `.js` file is its own private scope, and you explicitly say what it shares (`export`) and what it needs (`import`). Nothing leaks globally unless you opt in.

## 2. export & import

A module **exports** the values it wants to share. Another module **imports** them by name. There are two flavors:

### Named exports (use for most things)

```javascript
// file: math.js
export function add(a, b) {
  return a + b;
}
export const PI = 3.14159;
```

```python
// file: main.js
import { add, PI } from "./math.js";
console.log(add(2, 3));   // 5
console.log(PI);          // 3.14159
```

### Default export (one "main" thing per file)

```javascript
// file: greet.js
export default function greet(name) {
  return `Hello, ${name}!`;
}
```

```python
// file: main.js
import greet from "./greet.js";   // no braces; you choose the name
console.log(greet("Jane"));
```

| Style | Export | Import |
| --- | --- | --- |
| Named | `export const x` | `import { x } from "..."` |
| Default | `export default ...` | `import anyName from "..."` |

> **📝 The path matters**
>
> Relative imports start with
>
> ./
>
> or
>
> ../
>
> and (in the browser) need the file extension:
>
> "./math.js"
>
> . Imports of installed packages use just the name:
>
> import { thing } from "some-package"
>
> .

## 3. Modules vs plain scripts

A regular `<script src="app.js">` runs in the global scope and can't use `import`. To turn a script into a module in the browser, add `type="module"`:

```html
<script type="module" src="main.js"></script>
```

|  | Plain script | Module (`type="module"`) |
| --- | --- | --- |
| Scope | Global (variables leak) | Private to the file |
| `import`/`export` | ❌ Not allowed | ✅ Yes |
| Runs | Immediately, in order | Deferred until HTML parsed |
| Strict mode | Off by default | On automatically |

> **⚠️ Modules need a server**
>
> Because of browser security rules, opening an HTML file that uses
>
> type="module"
>
> by
>
> double-clicking
>
> (the
>
> file://
>
> protocol) often fails with a CORS error. Modules must be served over
>
> http://
>
> — which is exactly the problem a dev server like Vite solves.

## 4. npm & package.json

**npm** (Node Package Manager) ships with Node.js. It does two jobs: it installs **packages** (reusable code other people wrote, like Vite or React), and it runs project **scripts**. Every npm project has a `package.json` — the project's ID card and recipe book:

```json
{
  "name": "todo-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

| Field | What it's for |
| --- | --- |
| `name` / `version` | Identify the project. |
| `scripts` | Named commands you run with `npm run <name>`. |
| `dependencies` | Packages your app needs to run. |
| `devDependencies` | Packages only needed while developing (Vite, test tools). |

### Key commands

```bash
npm init -y          # create a package.json with defaults
npm install vite     # add a package (also written: npm i)
npm install          # install everything package.json lists
npm run dev          # run the "dev" script
```

> **📝 node_modules & the lockfile**
>
> Installing creates a
>
> node_modules/
>
> folder (the actual package code — don't commit it;
>
> .gitignore
>
> it) and a
>
> package-lock.json
>
> (exact versions, so teammates get identical installs — do commit it).

## 5. What a bundler/dev server does

Browsers can load modules natively, but for a real project that's slow and limited. Tools like **Vite** give you:

- **A dev server** over `http://localhost` so modules load correctly.
- **Hot Module Replacement (HMR)** — save a file and the page updates instantly, no manual reload.
- **A production build** — bundling and minifying all your files into a few small, optimized assets for deployment.
- Support for importing CSS, images, and installed packages with a single `import`.

Think of the dev server as a fast, smart helper that serves your code while you build, then packages it tidily when you ship.

## 6. Starting a Vite project

The fastest way is Vite's scaffolding tool. In your terminal (macOS/zsh):

```bash
npm create vite@latest todo-app -- --template vanilla
cd todo-app
npm install
npm run dev
```

Vite prints a local URL like `http://localhost:5173/`. Open it and you'll see the starter page; edits to the source files appear instantly.

| Command | What it does |
| --- | --- |
| `npm create vite@latest` | Scaffolds a new project (pick a template). |
| `npm install` | Downloads the dependencies it listed. |
| `npm run dev` | Starts the dev server with hot reload. |
| `npm run build` | Builds optimized files into `dist/` for production. |

> **📝 Windows / Linux**
>
> The commands are identical across platforms. On Windows use PowerShell or the Git Bash terminal; the
>
> --
>
> before
>
> --template
>
> is required so npm passes the flag through to Vite.

A vanilla Vite project's key files: `index.html` (the entry page, which loads `/src/main.js` as a module), `src/` (your code), and `package.json`. You'll drop your refactored to-do modules into `src/`.

## 7. Planning the to-do refactor

Your Chunk 3.3 to-do is one `todo.js`. We'll split it by responsibility — a classic, scalable structure:

| Module | Responsibility | Exports |
| --- | --- | --- |
| `store.js` | Hold the task data & logic (add/toggle/remove) | `addTask`, `removeTask`, `toggleTask`, `getTasks` |
| `ui.js` | Render the list into the DOM | `renderTasks` |
| `main.js` | Wire events to the store and UI (entry point) | — |

This separation — **data** vs **view** vs **glue** — is the same idea behind React components and the backend structure you'll build later. Learning it here pays off all course long.

## ✅ Recap

- **Modules** give each file its own scope; share with `export`, pull in with `import`.
- Browser modules need `type="module"` and must be served over `http://` — hence a dev server.
- **npm** installs packages and runs scripts; `package.json` records both.
- **Vite** provides a dev server with hot reload and a production build.
- Scaffold with `npm create vite@latest`, then `npm install` and `npm run dev`.
- Split apps by responsibility: data (`store`), view (`ui`), glue (`main`).

**Next:** open `assignment.html` and move the to-do app into Vite + modules.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
