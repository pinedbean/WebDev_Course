*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

First the navbar, then the card row. The full CSS additions and the updated header/home markup are at the bottom.

### 1 Clean nav markup

Remove the `|` characters in every page's header. The links now stand alone:

```html
<header>
  <h1>Jane Doe</h1>
  <nav>
    <a href="index.html" class="active">Home</a>
    <a href="about.html">About</a>
    <a href="contact.html">Contact</a>
  </nav>
</header>
```

(Put `class="active"` on whichever link matches the current page.)

### 2 Flex the header

```
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1e293b;
  padding: 14px 22px;
  border-radius: 10px;
}
header h1 { margin: 0; color: #fff; font-size: 1.4rem; }
```

**Expected result:** "Jane Doe" sits at the far left, the nav at the far right, both vertically centered on a dark bar. `space-between` does the left/right split; `align-items: center` lines them up.

### 3 Flex the links

```
nav { display: flex; gap: 18px; }
nav a {
  color: #cbd5e1;
  text-decoration: none;
  font-weight: 600;
}
nav a:hover, nav a.active { color: #fff; }
```

**Expected result:** the three links sit in an evenly-spaced row (the `gap` replaces the old `|`), light grey, brightening to white on hover and for the active page.

### 4 Card markup on the Home page

Add this section inside `<main>` on `index.html`:

```python
<section>
  <h2>What I Do</h2>
  <div class="card-row">
    <div class="card"><h3>🎨 Frontend</h3><p>HTML, CSS, and JavaScript.</p></div>
    <div class="card"><h3>⚙️ Backend</h3><p>FastAPI & databases.</p></div>
    <div class="card"><h3>🚀 Learning</h3><p>Building real projects.</p></div>
  </div>
</section>
```

### 5 Flex the card row

```
.card-row { display: flex; gap: 16px; flex-wrap: wrap; }
.card {
  flex: 1;
  min-width: 180px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
}
.card h3 { margin: 0 0 6px; color: #1e3a8a; }
.card p  { margin: 0; color: #475569; }
```

**Expected result:** three equal-width cards sit side-by-side with even gaps. Because each has `flex: 1`, they share the row equally.

> **⚠️ Cards overflowing instead of wrapping?**
>
> You're missing either
>
> flex-wrap: wrap
>
> on the row or
>
> min-width
>
> on the cards. Without
>
> min-width
>
> , flex items shrink forever and never wrap. With it, they wrap once they hit that floor.

### 6 Test the reflow

Narrow the window: 3 across → 2 across → 1 column. No horizontal scrollbar should ever appear. That's responsive behavior with zero media queries — Flexbox handled it. (You'll add explicit breakpoints in Chunk 2.5 for finer control.)

## 📄 CSS additions (append to `styles.css`)

```
/* --- Navbar (reusable component) --- */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #1e293b;
  padding: 14px 22px;
  border-radius: 10px;
}
header h1 { margin: 0; color: #fff; font-size: 1.4rem; }

nav { display: flex; gap: 18px; }
nav a {
  color: #cbd5e1;
  text-decoration: none;
  font-weight: 600;
}
nav a:hover, nav a.active { color: #fff; }

/* --- Card row --- */
.card-row { display: flex; gap: 16px; flex-wrap: wrap; }
.card {
  flex: 1;
  min-width: 180px;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
}
.card h3 { margin: 0 0 6px; color: #1e3a8a; }
.card p  { margin: 0; color: #475569; }
```

## 📄 Updated header (used on all three pages)

```html
<header>
  <h1>Jane Doe</h1>
  <nav>
    <a href="index.html" class="active">Home</a>
    <a href="about.html">About</a>
    <a href="contact.html">Contact</a>
  </nav>
</header>
```

Change which link gets `class="active"` per page (Home on index, About on about, Contact on contact).

## 🎉 You're done

You built a reusable Flexbox navbar that appears identically on every page, and a card row that automatically wraps as the screen narrows. `justify-content`, `align-items`, `gap`, `flex-wrap`, and `flex: 1` are now in your toolkit — you'll use them constantly, including inside React components later.

**Up next → Chunk 2.4: CSS Grid Layout**, where you'll arrange a whole *page* in two dimensions (header, sidebar, content, footer).

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
