*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll build `styles.css` declaration by declaration, link it to all three pages, and explain each result. The complete stylesheet and the one-line HTML change are at the bottom — compare them with yours.

### 1 Create & link the stylesheet

Make an empty `styles.css` in the same folder as your pages. Add this line to the `<head>` of **all three** HTML files:

```
<link rel="stylesheet" href="styles.css">
```

Test the wiring by adding one rule to `styles.css`:

```
body { background: #f8fafc; }
```

**Expected result:** all three pages get a faint grey-blue background.

> **⚠️ Nothing changed?**
>
> 99% of the time it's the
>
> href
>
> . The path is relative to the HTML file — if both files are in the same folder,
>
> href="styles.css"
>
> is right. Check spelling and that you saved both files. Open DevTools → Network tab and reload; a red
>
> styles.css
>
> means the browser couldn't find it.

### 2 Document the palette

A comment at the top keeps you honest. CSS comments use `/* ... */`:

```
/* Palette
   brand:   #2563eb   dark:  #1e293b
   muted:   #64748b   bg:    #f8fafc   border: #e2e8f0 */
```

### 3 Page-wide defaults on `body`

```
body {
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  color: #1e293b;
  background: #f8fafc;
  line-height: 1.6;
  max-width: 760px;
  margin: 0 auto;     /* top/bottom 0, left/right auto = centered */
  padding: 0 16px;
}
```

**Expected result:** the page content is now a centered column instead of stretching edge-to-edge, with a consistent font. Every paragraph and list inherits the font and color for free — that's inheritance doing the work.

### 4 Heading colors (element + grouping)

```
h1, h2 { font-family: system-ui, sans-serif; }   /* grouping */
h1 { color: #1e3a8a; }
h2 { color: #2563eb; }
```

**Expected result:** "Jane Doe" turns deep blue, and section headings (About Me, Skills…) turn a brighter blue across every page.

### 5 Nav links (descendant selector)

```
nav a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
  margin-right: 8px;
}
```

**Expected result:** the Home / About / Contact links lose their underline and turn bold blue — but links inside paragraphs (like "get in touch") are untouched, because `nav a` only matches links *inside* `<nav>`.

### 6 A reusable button class

In your HTML, add the class to one link. On the Home page:

```html
<a class="button" href="contact.html">Get in touch</a>
```

Then style it in CSS:

```
.button {
  display: inline-block;
  background: #2563eb;
  color: #fff;
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}
```

**Expected result:** that one link becomes a solid blue pill. Because it's a class, you can drop `class="button"` on any element later to reuse the style.

### 7 Hover states

```
nav a:hover   { color: #1e3a8a; }
.button:hover { background: #1e3a8a; }
```

**Expected result:** hovering a nav link or the button darkens it. `:hover` is a "pseudo-class" — a state the browser tracks for you.

### 8 Confirm consistency

Click through all three pages. They share one look because they share one stylesheet. If one page looks different, check that its `<link>` line is present and spelled the same.

## 📄 Complete `styles.css`

```
/* Palette
   brand:   #2563eb   dark:  #1e293b
   muted:   #64748b   bg:    #f8fafc   border: #e2e8f0 */

body {
  font-family: system-ui, -apple-system, "Segoe UI", sans-serif;
  color: #1e293b;
  background: #f8fafc;
  line-height: 1.6;
  max-width: 760px;
  margin: 0 auto;
  padding: 0 16px;
}

h1, h2 { font-family: system-ui, sans-serif; }
h1 { color: #1e3a8a; }
h2 { color: #2563eb; }

nav a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
  margin-right: 8px;
}
nav a:hover { color: #1e3a8a; }

.button {
  display: inline-block;
  background: #2563eb;
  color: #fff;
  padding: 10px 16px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
}
.button:hover { background: #1e3a8a; }

footer p { color: #94a3b8; }
```

## 📄 The HTML change (every page)

The only required HTML edit is one line in each `<head>`. Here it is in context on `index.html`:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — Home</title>
  <link rel="stylesheet" href="styles.css">
</head>
```

Plus the optional `class="button"` on one link for step 6.

## 🌟 Stretch: palette as CSS variables

If you tried the stretch goal, your palette lives in one place and the rest of the file references it. Change a variable and everything updates:

```
:root {
  --brand: #2563eb;
  --brand-dark: #1e3a8a;
  --ink: #1e293b;
  --bg: #f8fafc;
  --muted: #94a3b8;
}

body { color: var(--ink); background: var(--bg); }
h1   { color: var(--brand-dark); }
h2   { color: var(--brand); }
nav a, .button { color: var(--brand); }
```

> **💡 This is exactly what these lesson files do**
>
> Look at the very top of this page's
>
> <style>
>
> block —
>
> :root{--accent:#2563eb; ...}
>
> . Variables are how real projects stay consistent.

## 🎉 You're done

Your three plain pages now share one external stylesheet and a deliberate palette. You used element, class, and descendant selectors, leaned on inheritance and the cascade, and added hover states — all the fundamentals.

**Keep `styles.css`** — you'll grow it every chunk this module.

**Up next → Chunk 2.2: The Box Model & Typography**, where you'll control spacing precisely and add a real web font.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
