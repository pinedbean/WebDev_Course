*Full-Stack Web Dev · Module 0 — Setup & Tooling*

# Chunk 0.1 — Your Development Environment

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How the web actually works: the **client–server** model and the **HTTP request/response** cycle.
- What a developer "**stack**" is, and what each layer does.
- Which tools we'll install and *why* each one matters.
- How a request flows through **our** stack: React → FastAPI → SQLite.

By the end you'll understand the big picture. In the **lab**, you'll install everything and verify it works.

## 1. How the web works

Every website you visit is a conversation between two computers:

- **The client** — your browser (Chrome, Safari, Firefox). It *requests* things.
- **The server** — a computer somewhere on the internet that *responds* with what was asked for.

When you type an address and press Enter, your browser sends an **HTTP request**. The server reads it, does some work, and sends back an **HTTP response**:

> 🧑 YouBrowser / Client  →  — request →  →  ☁️ Server  →  ← response —  →  🧑 YouPage renders

A request is just text. It says *what* you want (the URL), *how* you want it (the method), and some extra info (headers). The main HTTP methods you'll use all course long:

| Method | Means | Example |
| --- | --- | --- |
| `GET` | Read / fetch data | Load a list of tasks |
| `POST` | Create new data | Add a new task |
| `PUT` / `PATCH` | Update existing data | Rename a task |
| `DELETE` | Remove data | Delete a task |

The server replies with a **status code** telling you how it went: `200` OK, `201` Created, `404` Not Found, `500` Server Error. You'll see these constantly.

> **📝 Note**
>
> You don't need to memorize this yet. Just hold onto one idea:
>
> the browser asks, the server answers.
>
> Everything else builds on that.

## 2. What is a "stack"?

A **stack** is the set of technologies layered together to make a full application. We split it into three parts:

| Layer | Job | Runs where | Our tech |
| --- | --- | --- | --- |
| **Frontend** | What the user sees & clicks | In the browser | HTML, CSS, JavaScript, **React + Vite** |
| **Backend** | Business logic, rules, security | On the server | **FastAPI** (Python) |
| **Database** | Stores data permanently | On the server | **SQLite** |

The word "stack" just means these layers sit on top of each other. A "**full-stack developer**" is comfortable in all three — which is exactly what this course makes you.

## 3. The tools we'll install (and why)

You can't build without tools. Here's what we set up in the lab, and the role each plays:

### Node.js & npm

**Node.js** lets JavaScript run *outside* the browser — we need it to run the React/Vite development server and build tools. **npm** (comes with Node) installs JavaScript packages, like an app store for code.

### Python

Our backend (FastAPI) is written in **Python**. We need Python 3.11+ installed to run the server and install backend packages with `pip`.

### VS Code (the code editor)

Where you'll write all your code. It's free, fast, and has helpful extensions. We'll add a few:

- **Prettier** — auto-formats your code so it stays clean.
- **ESLint** — flags JavaScript mistakes as you type.
- **Python** — adds Python support, linting, and debugging.

### A modern browser + DevTools

Chrome or Firefox, with their built-in **Developer Tools** (right-click → Inspect). You'll live here while debugging — inspecting elements, reading the console, and watching network requests.

### Git (next chunk)

**Git** tracks every change to your code and lets you save snapshots. We'll set it up properly in Chunk 0.2 — just know it's coming.

> **💡 Tip**
>
> Install the
>
> LTS
>
> ("Long-Term Support") version of Node.js, not the "Current" one. LTS is the stable, recommended release for real projects.

## 4. How a request flows through OUR stack

Let's make it concrete with the app we'll eventually build (TaskFlow). When a user clicks "Add Task":

> React(browser)  →  →  →  FastAPI(server)  →  →  →  SQLite(database)

1. **React** captures the click and sends a `POST` request to the backend.
2. **FastAPI** receives it, checks the data is valid, and saves it.
3. **SQLite** stores the new task on disk.
4. The response travels back up the chain, and React updates the screen.

Every feature you build for the rest of this course is a variation of this round trip. The tools you install today are what make each layer run on your machine.

## ✅ Recap

- The web is a **request/response** conversation between a **client** (browser) and a **server**.
- A **stack** = frontend + backend + database. Ours is React/Vite + FastAPI + SQLite.
- We install **Node.js** (run the frontend), **Python** (run the backend), **VS Code** (write code), and a **browser with DevTools** (debug).
- Every feature is just a request flowing **React → FastAPI → SQLite** and back.

**Next:** open `assignment.html` and set up your environment. The step-by-step answers are in `solution.html` if you get stuck.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
