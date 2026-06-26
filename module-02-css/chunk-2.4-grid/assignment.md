*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.4 — Lab: A Grid Dashboard Layout

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build a reusable, dashboard-style page layout with CSS Grid: a full-width **header**, a **sidebar**, a main **content** area, and a full-width **footer**. Inside the content area, drop a responsive grid of project cards. You'll create a new page, `projects.html`, that fits your personal site and doubles as a layout template you can reuse.

## Before you start

- Work in your personal-site folder alongside `index.html` / `about.html` / `contact.html` and `styles.css`.
- You'll add a 4th page, `projects.html`, and add a "Projects" link to your navbar on every page.
- Keep your navbar from Chunk 2.3 — it lives in the grid's header area.

> **⚠️ Try it yourself first**
>
> Sketch the grid on paper (the four areas) before coding. Lean on the lecture's
>
> grid-template-areas
>
> example. Only open the solution to compare.

## Tasks

### 1 Create the page skeleton

Make `projects.html` with the standard boilerplate and your `<link>`s (font + `styles.css`). Inside `<body>`, build the four regions wrapped in one grid container:

```html
<div class="dashboard">
  <header> ...your navbar... </header>
  <aside class="sidebar"> ...links/filters... </aside>
  <main class="content"> ...project cards... </main>
  <footer> ...copyright... </footer>
</div>
```

### 2 Define the grid with named areas

Style `.dashboard` as a grid: two columns (a fixed sidebar + a flexible content column), three rows, and `grid-template-areas` that place header and footer full-width with sidebar/content in the middle. Add a `gap` and `min-height: 100vh`.

### 3 Assign each region to its area

Give `header`, `.sidebar`, `.content`, and `footer` their `grid-area` names so they land in the right spots.

### 4 Fill the sidebar

Put a small vertical list of links or section labels in the sidebar (e.g. "All", "Web Apps", "Experiments"). Give it a distinct background and padding so it reads as a panel.

### 5 Build a responsive card grid in the content area

Inside `.content`, add a `<h2>Projects</h2>` and a grid of 4–6 project cards. Use the magic line so columns adjust to the width automatically:

```
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
```

Each card: a title, a one-line description, and maybe a tag. Style them like your earlier cards.

### 6 Make one card featured (span)

Add a class like `.featured` to one card and make it `grid-column: span 2` so it stands out across two columns. (On very narrow screens it will naturally fall back to one column.)

### 7 Add the Projects link to the navbar

Add `<a href="projects.html">Projects</a>` to the nav on all four pages so the site stays linked together.

### 8 Test it

Open `projects.html`. Confirm: header spans the top, sidebar sits left, content fills the rest, footer spans the bottom and sticks to the page bottom. Resize — the project cards should reflow column counts smoothly.

## ✅ Deliverable — acceptance checklist

- `projects.html` exists, linked from the navbar on every page.
- A `.dashboard` grid uses `grid-template-areas` with header, sidebar, content, footer.
- Header and footer span the full width; sidebar is fixed-ish width, content is flexible (`fr`).
- The layout fills the viewport height (`min-height: 100vh`) with a footer at the bottom.
- The content area holds a responsive card grid using `repeat(auto-fit, minmax(...))`.
- At least one card spans two columns via `grid-column: span 2`.
- Resizing reflows the card columns without horizontal scrolling.

## 🚀 Stretch goals (optional)

- Apply the same grid idea to your About page: put the photo and the intro side-by-side in a 2-column grid at the top.
- Add `grid-template-rows: auto 1fr auto` so the content row grows and pins the footer down precisely.
- Give the sidebar links a hover background and active state.
- Add a subtle `box-shadow` and hover lift (`transform: translateY(-2px)`) to project cards.
- Commit: `git add . && git commit -m "Grid dashboard layout + projects page"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
