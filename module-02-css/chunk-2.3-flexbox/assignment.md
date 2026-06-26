*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.3 — Lab: Navbar & Card Row with Flexbox

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Use Flexbox to (1) turn your header into a real navbar — brand on the left, links on the right — replacing Module 1's `|` separators, and (2) add a row of three "highlight" cards on the Home page that sit side-by-side and wrap gracefully on narrow screens. The navbar becomes a reusable component you'll keep using.

## Before you start

- You have `styles.css` with the box-model + typography work from Chunk 2.2.
- Recall your header markup from Module 1:

```html
<header>
  <h1>Jane Doe</h1>
  <nav>
    <a href="index.html">Home</a> |
    <a href="about.html">About</a> |
    <a href="contact.html">Contact</a>
  </nav>
</header>
```

> **⚠️ Try it yourself first**
>
> Reach for the lecture's navbar pattern and the live demos. Only check the solution when stuck.

## Tasks

### 1 Clean up the nav markup

In all three pages, remove the temporary `|` separators between the nav links. Flexbox `gap` will provide the spacing now. (Optional: mark the current page's link with `class="active"`.)

### 2 Flex the header into a navbar

Make the `<header>` a flex container that pushes the `<h1>` (brand) to the left and the `<nav>` to the right, vertically centered:

- `display: flex`
- `justify-content: space-between`
- `align-items: center`

### 3 Flex the nav links

Make `<nav>` its own flex container with a `gap` so the links sit in an evenly-spaced row. Remove underlines and apply your brand color (you may already have `nav a` styles from earlier — adjust them).

### 4 Style the navbar to look like a bar

Give the header a background color (e.g. your dark color), padding, white brand text, and light link text that brightens on `:hover`. This is your reusable navbar component.

> **💡 Make it consistent**
>
> Because the same header markup is on all three pages and styled by one stylesheet, your navbar instantly appears identically site-wide. That's the "reusable component" deliverable.

### 5 Add a card row to the Home page

On `index.html`, add a new section with three cards. Use a wrapper element with a class like `.card-row` and three child `.card` elements. For example:

```python
<section>
  <h2>What I Do</h2>
  <div class="card-row">
    <div class="card"><h3>Frontend</h3><p>HTML, CSS, JavaScript.</p></div>
    <div class="card"><h3>Backend</h3><p>FastAPI & databases.</p></div>
    <div class="card"><h3>Learning</h3><p>Building real projects.</p></div>
  </div>
</section>
```

### 6 Make the cards flex & wrap

Style `.card-row` as a flex container with a `gap` and `flex-wrap: wrap`. Give each `.card` `flex: 1` and a `min-width` (~180px) so the three sit side-by-side on wide screens but stack/wrap on narrow ones. Give cards a background, border, radius, and padding.

### 7 Test the wrap behavior

Drag your browser window narrow and watch the cards wrap from a 3-across row to fewer-across, then to a single column. That graceful reflow is the whole point of `flex-wrap` + `min-width`.

## ✅ Deliverable — acceptance checklist

- The `|` separators are gone from the nav on all pages.
- The header is a flex navbar: brand left, links right, vertically centered.
- Nav links sit in a row with `gap` spacing (no underlines, brand-colored, hover effect).
- The navbar has a background, padding, and looks like a real bar — identical on all three pages.
- The Home page has a `.card-row` with three cards.
- Cards use `display:flex` + `gap` + `flex-wrap:wrap`, with `flex:1` and a `min-width` on each card.
- Narrowing the window makes the cards wrap instead of overflow.

## 🚀 Stretch goals (optional)

- Style the `.active` nav link differently (e.g. a brighter color or an underline) so visitors know which page they're on.
- Make the card heights match no matter the text length — they already do with `align-items: stretch` (the default). Add an icon or emoji to each card's heading.
- On the Contact page, use Flexbox to lay the form label and input side-by-side on wide screens.
- Center the footer content with `display:flex; justify-content:center;`.
- Commit: `git add . && git commit -m "Flexbox navbar + card row"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
