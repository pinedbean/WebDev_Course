*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.5 — Solution (Step-by-Step)

**✅ SOLUTION** · **🏁 + Module 2 Checkpoint**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Part A makes the site responsive; Part B is the portfolio checkpoint. The complete, final `styles.css` and the redesigned `index.html` are at the bottom — they bring together every technique from Module 2.

## Part A — Responsive, step by step

### 1 Audit & fluid images

After auditing at 360px, the first guaranteed fix is fluid images (you likely have this already):

```
img { max-width: 100%; height: auto; }
```

**Expected result:** the profile photo shrinks to fit instead of forcing the page wider than the screen.

### 2 Navbar stacks on phones

```
@media (max-width: 600px) {
  header { flex-direction: column; align-items: flex-start; gap: 10px; }
  nav { flex-wrap: wrap; gap: 12px; }
}
```

**Expected result:** below 600px the brand sits on its own line with the links wrapping beneath — no collision, no overflow.

### 3 Restack the dashboard grid

```
@media (max-width: 700px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "content"
      "sidebar"
      "footer";
  }
}
```

**Expected result:** the projects page becomes a clean single column — header, then projects, then the filter sidebar, then footer. Same HTML, redrawn areas.

> **⚠️ Still two columns on mobile?**
>
> Make sure this query comes
>
> after
>
> the base
>
> .dashboard
>
> rule in your file, and that the width condition actually matches (check the reported width in DevTools).

### 4 Responsive typography

```
h1 { font-size: 1.8rem; }
@media (min-width: 600px) { h1 { font-size: 2.2rem; } }
@media (min-width: 900px) { h1 { font-size: 2.8rem; } }
```

**Expected result:** headings are comfortable on a phone and grow gracefully on bigger screens. That's three breakpoints already (600 max for nav, 700 max for grid, 600/900 min for type).

## 🏁 Part B — Portfolio checkpoint, step by step

### 5 The hero section (Home)

Replace the plain "Welcome" section on `index.html` with a hero:

```html
<section class="hero">
  <h1>Hi, I'm Jane 👋</h1>
  <p class="tagline">Aspiring full-stack developer building for the web.</p>
  <a class="button" href="projects.html">View my work</a>
</section>
```

```
.hero { text-align: center; padding: 64px 20px; }
.hero .tagline { font-size: 1.25rem; color: var(--muted); margin-bottom: 24px; }
```

**Expected result:** a confident, centered opening with a clear call-to-action button.

### 6 Card hover polish

```
.card { transition: transform .15s ease, box-shadow .15s ease; }
.card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px rgba(2,6,23,.10); }
```

**Expected result:** cards lift slightly and gain a shadow on hover — a small touch that reads as "polished".

### 7 Unify with CSS variables

Hoist your palette, fonts, and radius into `:root` and reference them everywhere. Now a single edit re-themes the whole site (see the full file below).

### 8 Final QA

Walk every page at 360 / 768 / 1200px. **Expected result:** consistent palette and type, even spacing, working hover states, and zero overflow at any width.

## 📄 Final `styles.css` (complete Module 2 stylesheet)

```
/* ===== Design tokens ===== */
:root {
  --brand: #2563eb;
  --brand-dark: #1e3a8a;
  --ink: #1e293b;
  --muted: #64748b;
  --bg: #f8fafc;
  --line: #e2e8f0;
  --radius: 12px;
  --font-body: "Inter", system-ui, -apple-system, sans-serif;
  --font-head: "Poppins", system-ui, sans-serif;
}

/* ===== Base (mobile-first) ===== */
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: var(--font-body);
  line-height: 1.65;
  color: var(--ink);
  background: var(--bg);
  margin: 0;
  padding: 0 16px;
}

main { max-width: 1000px; margin: 0 auto; }

h1, h2, h3 { font-family: var(--font-head); line-height: 1.2; }
h1 { color: var(--brand-dark); font-size: 1.8rem; }
h2 { color: var(--brand); font-size: 1.4rem; }

img { max-width: 100%; height: auto; border-radius: var(--radius); }

a { color: var(--brand); }

/* ===== Navbar ===== */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1e293b;
  padding: 14px 22px;
  border-radius: var(--radius);
  margin: 16px 0;
}
header h1 { margin: 0; color: #fff; font-size: 1.3rem; }
nav { display: flex; gap: 18px; }
nav a { color: #cbd5e1; text-decoration: none; font-weight: 600; }
nav a:hover, nav a.active { color: #fff; }

/* ===== Cards ===== */
section { background: #fff; border: 1px solid var(--line); border-radius: var(--radius);
  padding: 24px 28px; margin-bottom: 20px; }

.card {
  background: #fff; border: 1px solid var(--line); border-radius: var(--radius);
  padding: 18px;
  transition: transform .15s ease, box-shadow .15s ease;
}
.card:hover { transform: translateY(-3px); box-shadow: 0 10px 24px rgba(2,6,23,.10); }
.card h3 { margin: 0 0 6px; color: var(--brand-dark); }
.card p  { margin: 0; color: var(--muted); }

.card-row { display: flex; gap: 16px; flex-wrap: wrap; }
.card-row .card { flex: 1; min-width: 180px; }

/* ===== Hero ===== */
.hero { text-align: center; padding: 64px 20px; }
.hero .tagline { font-size: 1.25rem; color: var(--muted); margin-bottom: 24px; }

.button {
  display: inline-block; background: var(--brand); color: #fff;
  padding: 12px 22px; border-radius: 8px; text-decoration: none; font-weight: 600;
}
.button:hover { background: var(--brand-dark); }

/* ===== Dashboard / projects grid ===== */
.dashboard {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas: "header header" "sidebar content" "footer footer";
  gap: 16px;
  min-height: 100vh;
  max-width: 1100px;
  margin: 0 auto;
}
.dashboard > header  { grid-area: header; margin: 0; }
.dashboard > .sidebar{ grid-area: sidebar; }
.dashboard > .content{ grid-area: content; }
.dashboard > footer  { grid-area: footer; }

.sidebar { background: #f1f5f9; border: 1px solid var(--line); border-radius: var(--radius); padding: 18px; }
.sidebar a { display: block; padding: 8px 10px; border-radius: 8px; color: var(--ink); text-decoration: none; }
.sidebar a:hover { background: var(--accent-soft, #dbeafe); }

.project-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; }
.project-grid .featured { grid-column: span 2; }

/* ===== Tables & footer ===== */
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid var(--line); padding: 10px 12px; text-align: left; }
th { background: #f1f5f9; }

footer { margin-top: 2rem; padding: 20px 0; font-size: .9rem; }
footer p { color: #94a3b8; }

/* ===== Responsive breakpoints ===== */
@media (max-width: 600px) {
  header { flex-direction: column; align-items: flex-start; gap: 10px; }
  nav { flex-wrap: wrap; gap: 12px; }
}
@media (max-width: 700px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-areas: "header" "content" "sidebar" "footer";
  }
}
@media (min-width: 600px) { h1 { font-size: 2.2rem; } }
@media (min-width: 900px) { h1 { font-size: 2.8rem; } }

@media (prefers-reduced-motion: reduce) {
  .card { transition: none; }
}
```

## 📄 Redesigned `index.html` (with hero + card row)

```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — Home</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header>
    <h1>Jane Doe</h1>
    <nav>
      <a href="index.html" class="active">Home</a>
      <a href="about.html">About</a>
      <a href="projects.html">Projects</a>
      <a href="contact.html">Contact</a>
    </nav>
  </header>

  <main>
    <section class="hero">
      <h1>Hi, I'm Jane 👋</h1>
      <p class="tagline">Aspiring full-stack developer building for the web.</p>
      <a class="button" href="projects.html">View my work</a>
    </section>

    <section>
      <h2>What I Do</h2>
      <div class="card-row">
        <div class="card"><h3>🎨 Frontend</h3><p>HTML, CSS, and JavaScript.</p></div>
        <div class="card"><h3>⚙️ Backend</h3><p>FastAPI & databases.</p></div>
        <div class="card"><h3>🚀 Learning</h3><p>Building real projects.</p></div>
      </div>
    </section>
  </main>

  <footer>
    <p>© 2026 Jane Doe</p>
  </footer>
</body>
</html>
```

> **📝 Note the layout choice**
>
> The Home/About/Contact pages use the simple centered
>
> <main>
>
> column; only
>
> projects.html
>
> uses the full
>
> .dashboard
>
> grid. Mixing layouts per page is completely normal — one shared stylesheet supports both.

## How to verify (DevTools device mode)

- Open DevTools, toggle device mode, and step through 360px → 768px → 1200px on every page.
- **Pass criteria:** no horizontal scrollbar; navbar never collides; projects page is one column on phones; headings scale; cards lift on hover (desktop).
- If something overflows, find the culprit element in the Elements panel — it's usually a fixed width or an unconstrained image.

## 🎉 Module 2 complete!

You took the plain, semantic HTML site from Module 1 and turned it into a **polished, responsive portfolio**: a deliberate palette and web font, a clean box model and typography, a Flexbox navbar and card rows, a Grid dashboard, and media queries that make it shine from phone to desktop — all from **one external stylesheet**.

You can now style and lay out essentially any page. Add it to your GitHub and consider deploying it with GitHub Pages — it's a real portfolio you can share.

**Up next → Module 3: JavaScript Core**, where you make pages *interactive* — the third layer, "the muscles". First stop: JavaScript basics.

Don't forget to commit and push your work. 🚀

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
