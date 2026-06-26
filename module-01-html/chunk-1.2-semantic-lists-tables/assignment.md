*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.2 — Lab: Make It Semantic

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Upgrade the `about.html` page you built in Chunk 1.1: wrap it in proper semantic landmarks, add a navigation bar, a **skills list**, and an **experience table**. Then validate it.

## Before you start

- Open your existing `about.html` in VS Code.
- Work on a copy if you want to keep the original: it's fine to edit in place — Git has your back if you committed it.

## Tasks

### 1 Add a header & nav

At the top of `<body>`, add a `<header>` containing your name in an `<h1>` and a `<nav>` with links to `index.html`, `about.html`, and `contact.html` (the last two will exist soon — link them now).

### 2 Wrap content in `<main>` and `<section>`s

Put your About and Learning content inside a single `<main>`. Wrap each topic in its own `<section>`, each led by an `<h2>`.

### 3 Add a skills list

Add a "Skills" `<section>` with an unordered list (`<ul>`) of at least five skills. Bonus: nest a sub-list under one item.

### 4 Add an experience table

Add an "Experience" `<section>` containing a `<table>` with a `<caption>`, a header row using `<th>` (Year, Role, Organisation), and at least two data rows. Use `<thead>` and `<tbody>`.

### 5 Add a footer

Add a `<footer>` with a copyright line and a contact email link.

### 6 Validate

Paste your code into [validator.w3.org](https://validator.w3.org/#validate_by_input) and fix any reported errors until it passes cleanly.

## ✅ Deliverable — acceptance checklist

- Page uses `<header>`, `<nav>`, `<main>`, multiple `<section>`, and `<footer>`.
- Exactly one `<main>` and one `<h1>`.
- A skills `<ul>` with 5+ items.
- An experience `<table>` with caption, `<thead>` header row (`<th>`), and 2+ body rows.
- A footer with a `mailto:` contact link.
- The page passes the W3C validator with no errors.

## 🚀 Stretch goals (optional)

- Add an `<aside>` with a "Fun fact" about you.
- Use an ordered list `<ol>` for your "learning roadmap".
- Add a description list `<dl>` defining 3 tech terms you've learned.
- Commit: `git commit -am "Make about page semantic; add skills + experience"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
