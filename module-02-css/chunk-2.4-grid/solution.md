*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We build the grid skeleton first, then fill it. The complete `projects.html` and the CSS additions are at the bottom.

### 1 The four-region skeleton

```html
<div class="dashboard">
  <header>
    <h1>Jane Doe</h1>
    <nav>
      <a href="index.html">Home</a>
      <a href="about.html">About</a>
      <a href="projects.html" class="active">Projects</a>
      <a href="contact.html">Contact</a>
    </nav>
  </header>

  <aside class="sidebar">
    <h3>Filter</h3>
    <a href="#">All</a>
    <a href="#">Web Apps</a>
    <a href="#">Experiments</a>
  </aside>

  <main class="content">
    <h2>Projects</h2>
    <div class="project-grid"> ... cards ... </div>
  </main>

  <footer><p>© 2026 Jane Doe</p></footer>
</div>
```

### 2 Define the grid

```
.dashboard {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
  gap: 16px;
  min-height: 100vh;
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px;
}
```

**Expected result:** a two-column grid where header and footer stretch across both columns, the sidebar takes a fixed 200px, and the content area takes the rest. The `1fr` middle row makes the content grow so the footer hugs the bottom of the screen.

### 3 Place each region

```
.dashboard > header  { grid-area: header;  }
.dashboard > .sidebar{ grid-area: sidebar; }
.dashboard > .content{ grid-area: content; }
.dashboard > footer  { grid-area: footer;  }
```

**Expected result:** each block snaps into its named region. Try swapping the order of the elements in the HTML — they still land in the right place, because the *area name* controls position, not source order.

### 4 Style the sidebar

```
.sidebar {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
}
.sidebar h3 { margin-top: 0; }
.sidebar a {
  display: block;
  padding: 8px 10px;
  border-radius: 8px;
  color: #1e293b;
  text-decoration: none;
}
.sidebar a:hover { background: #dbeafe; }
```

**Expected result:** a tidy panel of stacked links that highlight on hover.

### 5 Responsive project grid

```
.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
.project-grid .card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
}
```

**Expected result:** cards fill the content area, fitting as many ~200px columns as the width allows. Resize the window and the column count changes on its own — no media query.

> **⚠️ Only one column even on a wide screen?**
>
> Check you wrote
>
> auto-fit
>
> (not
>
> auto
>
> ) and that the container actually has width. If a parent is too narrow, even one 200px column may be all that fits.

### 6 Feature one card

```
.project-grid .featured { grid-column: span 2; }
```

Add `class="card featured"` to one card. **Expected result:** it stretches across two columns when there's room, drawing the eye.

## 📄 CSS additions (append to `styles.css`)

```
/* --- Dashboard / page grid --- */
.dashboard {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
  gap: 16px;
  min-height: 100vh;
  max-width: 1100px;
  margin: 0 auto;
  padding: 16px;
}
.dashboard > header  { grid-area: header;  }
.dashboard > .sidebar{ grid-area: sidebar; }
.dashboard > .content{ grid-area: content; }
.dashboard > footer  { grid-area: footer;  }

.sidebar {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
}
.sidebar h3 { margin-top: 0; }
.sidebar a {
  display: block;
  padding: 8px 10px;
  border-radius: 8px;
  color: #1e293b;
  text-decoration: none;
}
.sidebar a:hover { background: #dbeafe; }

.project-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
.project-grid .card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
}
.project-grid .featured { grid-column: span 2; }
```

## 📄 Complete `projects.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — Projects</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="dashboard">
    <header>
      <h1>Jane Doe</h1>
      <nav>
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
        <a href="projects.html" class="active">Projects</a>
        <a href="contact.html">Contact</a>
      </nav>
    </header>

    <aside class="sidebar">
      <h3>Filter</h3>
      <a href="#">All</a>
      <a href="#">Web Apps</a>
      <a href="#">Experiments</a>
    </aside>

    <main class="content">
      <h2>Projects</h2>
      <div class="project-grid">
        <div class="card featured">
          <h3>Personal Site</h3>
          <p>This very website — built across Modules 1 & 2.</p>
        </div>
        <div class="card"><h3>To-Do App</h3><p>Coming in Module 3.</p></div>
        <div class="card"><h3>Weather Fetch</h3><p>A live API demo.</p></div>
        <div class="card"><h3>TaskFlow</h3><p>The capstone app.</p></div>
      </div>
    </main>

    <footer><p>© 2026 Jane Doe</p></footer>
  </div>
</body>
</html>
```

> **📝 Two layout systems, one page**
>
> Notice the structure:
>
> Grid
>
> positions the four page regions, while your
>
> Flexbox
>
> navbar from Chunk 2.3 still arranges the brand and links
>
> inside
>
> the header cell. That's the normal, healthy way to combine them.

## 🎉 You're done

You now have a reusable, two-dimensional page template — header, sidebar, content, footer — described in a few readable lines of `grid-template-areas`, plus a self-adjusting card grid. This is the skeleton behind most dashboards and admin panels you'll ever build (including the capstone).

**One thing to notice:** on a phone-width screen that 200px sidebar gets cramped next to the content. That's the cliff-hanger for the final chunk.

**Up next → Chunk 2.5: Responsive Design & Media Queries**, where you make every layout adapt to phones, tablets, and desktops — and complete the Module 2 portfolio checkpoint.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
