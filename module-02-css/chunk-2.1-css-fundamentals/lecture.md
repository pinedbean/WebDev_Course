*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.1 — CSS Fundamentals & Selectors

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What CSS is and the three ways to attach it to a page (inline, internal, **external**).
- The anatomy of a CSS **rule**: selector, property, value.
- The core **selectors**: element, class, id, descendant, and grouping.
- How the browser resolves conflicts: the **cascade**, inheritance, and **specificity**.
- How to write **colors** (named, hex, rgb, hsl) and which **units** to use (`px`, `rem`, `em`, `%`).

In the lab you'll create a single `styles.css` file and apply a consistent palette across all three pages of your personal site from Module 1.

## 1. What is CSS, and why a separate language?

In Module 1 you built a 3-page site — Home, About, Contact — for "Jane Doe". It works, but it's plain: black text, blue underlined links, no spacing. That's because HTML only describes *structure*. **CSS** (Cascading Style Sheets) describes *presentation*: colors, fonts, spacing, and layout.

Keeping them separate is one of the most important ideas in web development. The same HTML can look completely different just by swapping the CSS — and you can restyle 50 pages by editing one stylesheet. Remember the analogy from Chunk 1.1:

| Language | Role | Analogy |
| --- | --- | --- |
| HTML | Structure & content | The skeleton |
| **CSS** | **Styling & layout** | **The skin & clothes** |
| JavaScript | Behavior & interactivity | The muscles |

This whole module is the "skin & clothes" layer. By the end you'll turn Jane's plain site into a polished, responsive portfolio.

## 2. The anatomy of a CSS rule

CSS is a list of **rules**. Each rule picks some elements with a **selector**, then sets one or more **declarations** (a **property** and a **value**) inside curly braces:

```text
h1 {
  color: navy;
  font-size: 32px;
}
```

- `h1` — the **selector** ("which elements?").
- `color` and `font-size` — **properties** ("what to change?").
- `navy` and `32px` — **values** ("change it to what?").
- Each declaration ends with a **semicolon** `;`. The whole block is wrapped in `{ }`.

> **💡 Read it out loud**
>
> "Select every
>
> h1
>
> , set its color to navy and its font-size to 32 pixels." If you can say a rule in plain English, you understand it.

## 3. Three ways to include CSS

### a) Inline — on a single element (avoid)

A `style` attribute right on the tag. It only affects that one element and is hard to maintain:

```html
<h1 style="color: navy; font-size: 32px;">Jane Doe</h1>
```

### b) Internal — a `<style>` block in the `<head>`

Good for a quick one-page experiment (it's exactly what these lesson files use). It only styles *this* page, though:

```html
<head>
  <style>
    h1 { color: navy; }
  </style>
</head>
```

### c) External — a separate `.css` file (the real-world way) ✅

Put all your rules in `styles.css`, then link it from the `<head>` of *every* page. One file styles your whole site:

```html
<head>
  <link rel="stylesheet" href="styles.css">
</head>
```

And `styles.css` contains plain CSS — no HTML tags, no `<style>` wrapper:

```
/* styles.css */
h1 {
  color: navy;
}
```

> **📝 Why external wins**
>
> Edit the color once and all three of Jane's pages update. The browser also
>
> caches
>
> the file, so pages load faster. This is what you'll build in the lab.

> **⚠️ Comments are different in CSS**
>
> In HTML a comment is
>
> <!-- ... -->
>
> . In CSS it's
>
> /* ... */
>
> . Using the wrong one is a classic beginner bug.

## 4. Selectors — choosing what to style

The selector is the most important part of a rule. Here are the ones you'll use constantly.

### Element (type) selector

Matches every element of that type. Great for site-wide defaults.

```
p      { line-height: 1.6; }     /* every paragraph   */
a      { color: #2563eb; }       /* every link        */
h2     { color: #0f172a; }       /* every h2          */
```

### Class selector — `.name`

Matches any element with that `class` attribute. Classes are **reusable** — the workhorse of CSS. You add a class in HTML, then target it with a dot:

```html
<p class="lead">A short intro paragraph.</p>
<a class="button" href="contact.html">Contact me</a>
```

```
.lead   { font-size: 20px; color: #475569; }
.button { background: #2563eb; color: white; padding: 10px 16px; }
```

### ID selector — `#name`

Matches the one element with that `id`. IDs must be **unique** per page. Prefer classes for styling; reserve IDs for things like in-page anchor links.

```html
<header id="top"> ... </header>
```

```
#top { background: #1e293b; }
```

### Descendant selector — `A B` (a space)

"Any `B` inside an `A`." This is how you style links *only* inside the nav without touching links elsewhere:

```
nav a      { font-weight: 600; }   /* links inside <nav> only */
footer p   { color: #94a3b8; }     /* paragraphs inside <footer> */
```

### Grouping — `A, B, C` (commas)

Apply the same rule to several selectors at once. Don't repeat yourself:

```
h1, h2, h3 { font-family: Georgia, serif; }
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

| Selector | Matches | Example |
| --- | --- | --- |
| `p` | Every `<p>` | element |
| `.lead` | Anything with `class="lead"` | class |
| `#top` | The element with `id="top"` | id |
| `nav a` | `<a>` inside `<nav>` | descendant |
| `h1, h2` | Every `h1` and every `h2` | grouping |

## 5. The cascade, inheritance & specificity

"Cascading" is the C in CSS. When several rules target the same element, the browser needs a way to decide which one wins. Three ideas govern this.

### Inheritance

Some properties pass down from a parent to its children automatically — mostly text properties like `color` and `font-family`. Set the font on `body` once and every paragraph inherits it:

```
body { font-family: system-ui, sans-serif; color: #1e293b; }
/* every <p>, <li>, <h2>... inherits these unless overridden */
```

Layout properties like `margin`, `padding`, and `border` do **not** inherit — that would be chaos.

### The cascade (source order)

If two rules have equal strength, the **last one wins**. Order matters:

```
p { color: red; }
p { color: green; }   /* paragraphs end up green */
```

### Specificity

A more *specific* selector beats a less specific one, regardless of order. Think of it as a score — id > class > element:

#id

beats

.class

beats

element

```
p          { color: black; }   /* specificity: low    */
.intro     { color: blue;  }   /* specificity: medium */
#headline  { color: red;   }   /* specificity: high   */

<p>                            → black
<p class="intro">             → blue  (class beats element)
<p id="headline" class="intro"> → red (id beats class)
```

> **⚠️ `!important` is a trap**
>
> Adding
>
> !important
>
> to a value forces it to win, overriding everything. It feels handy but quickly leads to unmaintainable battles.
>
> Avoid it
>
> — instead, write a slightly more specific selector or fix your source order.

> **💡 Keep specificity low**
>
> Style with simple classes whenever you can. Low, even specificity makes your CSS easy to override later — which is exactly what you want for a growing site.

## 6. Colors

There are several ways to write the same color. You'll mostly use **hex** and **hsl**.

| Form | Example | Notes |
| --- | --- | --- |
| Named | `navy`, `tomato` | ~140 keywords; handy for quick tests. |
| Hex | `#2563eb` | Red/Green/Blue in base-16. The most common form. |
| RGB | `rgb(37, 99, 235)` | 0–255 per channel. `rgb(0 0 0 / 50%)` adds transparency. |
| HSL | `hsl(220, 83%, 53%)` | Hue, Saturation, Lightness — easiest to tweak by hand. |

*(Interactive demo — open the `.html` version in a browser to try it live.)*

> **💡 Where colors come from**
>
> Pick palettes from tools like
>
> coolors.co
>
> or your browser's DevTools color picker. A simple, consistent palette (1 brand color, 1 dark text color, 1–2 neutrals) looks more professional than a rainbow.

#1e3a8a

brand dark

#2563eb

brand

#1e293b

text

#64748b

muted

#94a3b8

border

## 7. Units — px, rem, em, %

Lengths need a unit. The four you'll use most:

| Unit | Means | Use it for |
| --- | --- | --- |
| `px` | Absolute pixels. | Borders, small fixed gaps, fine details. |
| `rem` | Relative to the **root** font-size (16px by default). `1rem = 16px`. | Font sizes & spacing — scales with the user's settings. |
| `em` | Relative to the *element's own* font-size. | Padding inside a button that should grow with its text. |
| `%` | Relative to the parent's size. | Fluid widths (e.g. `width: 100%`). |

```
html { font-size: 16px; }       /* the root */
h1   { font-size: 2rem; }       /* = 32px, and scales if root changes */
p    { font-size: 1rem; }       /* = 16px */
.box { padding: 1.5rem; width: 100%; }
```

> **📝 Default to `rem` for type & spacing**
>
> Using
>
> rem
>
> means if a user bumps their browser's base font size for readability, your whole layout scales with them. Reserve
>
> px
>
> for hairline borders and tiny details. You'll lean on these heavily in Chunk 2.5 (responsive design).

## 8. A first taste — styling Jane's site

Here's a tiny external stylesheet that already makes the personal site look intentional. You'll write your own version in the lab:

```
/* styles.css */
body {
  font-family: system-ui, -apple-system, sans-serif;
  color: #1e293b;
  background: #f8fafc;
  max-width: 760px;
  margin: 0 auto;          /* centers the page */
  padding: 0 16px;
}

h1 { color: #1e3a8a; }
h2 { color: #2563eb; }

nav a {
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
}

footer p { color: #94a3b8; }
```

Notice it uses element selectors (`body`, `h1`) and one descendant selector (`nav a`) — exactly the tools from this lecture. No HTML changes required; the markup from Module 1 already has `<nav>`, `<h1>`, and `<footer>` for these selectors to grab onto.

## ✅ Recap

- CSS styles HTML with **rules**: `selector { property: value; }`.
- Attach it three ways — inline, internal `<style>`, or (best) an **external** `styles.css` via `<link rel="stylesheet">`.
- Core selectors: **element**, **class** (`.x`), **id** (`#x`), **descendant** (`a b`), **grouping** (`a, b`).
- Conflicts resolve by **inheritance**, the **cascade** (last wins), and **specificity** (id > class > element). Avoid `!important`.
- Write colors as hex/hsl; default to `rem` for type & spacing, `px` for fine details.

**Next:** open `assignment.html` and give Jane's whole site a real stylesheet and palette.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
