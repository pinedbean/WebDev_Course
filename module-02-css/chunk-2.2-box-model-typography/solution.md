*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We extend the `styles.css` from Chunk 2.1. Each step shows what to add and the result to expect. The full stylesheet and the `<head>` snippet are at the bottom.

### 1 The box-sizing reset

```
*, *::before, *::after { box-sizing: border-box; }
```

**Expected result:** nothing visibly changes *yet* — but from now on, when you set a `width` it includes padding and border, so later steps won't blow out your layout.

### 2 Link & apply a Google Font

In each page's `<head>` (above the `styles.css` link):

```
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
```

Then in `styles.css`:

```
body { font-family: "Inter", system-ui, sans-serif; }
h1, h2, h3 { font-family: "Poppins", system-ui, sans-serif; }
```

**Expected result:** headings switch to Poppins (geometric, friendly) and body text to Inter (clean, readable).

> **⚠️ Still the old font?**
>
> Check the
>
> family=
>
> name in the URL matches the quoted name in
>
> font-family
>
> exactly. If you're offline, the font can't download and you'll see the system fallback — that's the fallback doing its job, not a bug.

### 3 Body rhythm

```
body {
  font-family: "Inter", system-ui, sans-serif;
  line-height: 1.65;
  color: #1e293b;
  background: #f8fafc;
  max-width: 760px;
  margin: 0 auto;
  padding: 0 20px;
}
```

**Expected result:** paragraphs gain breathing room; the page stays a centered, readable column.

### 4 Sections as cards

```
section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 20px;
}
```

**Expected result:** on the About page, "About Me", "Skills", "Experience" each become a white rounded card with space between them. This is padding (inside) + margin (between) + border all at once.

### 5 Heading spacing

```
h1, h2 { line-height: 1.2; }
h1 { font-size: 2rem; margin-bottom: 0.5rem; }
h2 { font-size: 1.4rem; margin-top: 0.25rem; }
```

**Expected result:** titles sit tighter within themselves but don't crowd the text below. (Because the card already has padding, the heading no longer needs a big top margin.)

### 6 Header & footer

```
header { padding: 20px 0; border-bottom: 1px solid #e2e8f0; }
header h1 { margin: 0 0 8px; }
nav a { margin-right: 14px; }

footer {
  margin-top: 2rem;
  padding: 20px 0;
  font-size: 0.9rem;
}
footer p { color: #94a3b8; }
```

**Expected result:** the header is set off with a thin underline; nav links have room to breathe; the footer is quiet and small.

### 7 Polish: image & table

```
img {
  max-width: 100%;     /* never overflow its container */
  height: auto;
  border-radius: 12px;
}

table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #e2e8f0; padding: 10px 12px; text-align: left; }
th { background: #f1f5f9; }
```

**Expected result:** the profile photo has soft corners and can't break the layout; the experience table reads cleanly with collapsed borders and padded cells.

## 📄 Complete `styles.css` (cumulative)

```
/* Palette
   brand:   #2563eb   dark:  #1e293b
   muted:   #64748b   bg:    #f8fafc   border: #e2e8f0 */

*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: "Inter", system-ui, -apple-system, sans-serif;
  line-height: 1.65;
  color: #1e293b;
  background: #f8fafc;
  max-width: 760px;
  margin: 0 auto;
  padding: 0 20px;
}

h1, h2, h3 { font-family: "Poppins", system-ui, sans-serif; line-height: 1.2; }
h1 { color: #1e3a8a; font-size: 2rem; margin-bottom: 0.5rem; }
h2 { color: #2563eb; font-size: 1.4rem; margin-top: 0.25rem; }

header { padding: 20px 0; border-bottom: 1px solid #e2e8f0; }
header h1 { margin: 0 0 8px; }

nav a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
  margin-right: 14px;
}
nav a:hover { color: #1e3a8a; }

section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 20px;
  box-shadow: 0 4px 14px rgba(2,6,23,.06);
}

img { max-width: 100%; height: auto; border-radius: 12px; }

table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #e2e8f0; padding: 10px 12px; text-align: left; }
th { background: #f1f5f9; }

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

footer { margin-top: 2rem; padding: 20px 0; font-size: 0.9rem; }
footer p { color: #94a3b8; }
```

## 📄 The `<head>` on every page

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — Home</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="styles.css">
</head>
```

## 🎉 You're done

The same three HTML pages from Module 1 now look genuinely designed: a real typeface, cards with even spacing, and text that's comfortable to read. You did it by mastering the box model and a handful of type properties — no new HTML.

**Up next → Chunk 2.3: Flexbox Layout**, where you'll turn that pipe-separated nav into a real horizontal navbar and lay cards out in a row.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
