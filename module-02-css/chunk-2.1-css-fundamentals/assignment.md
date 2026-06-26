*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.1 — Lab: Give Your Site a Stylesheet

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Create one external stylesheet, `styles.css`, link it from all three pages of your Module 1 personal site (`index.html`, `about.html`, `contact.html`), and apply a consistent color palette using element, class, and descendant selectors. By the end, the same CSS file controls the look of your whole site.

## Before you start

- Open your Module 1 site folder (the one with `index.html`, `about.html`, `contact.html`) in VS Code with `code .`
- If you don't have it, recreate the three pages from the Chunk 1.3 solution first — Module 2 styles that exact markup.
- Open one of the pages in your browser and keep it visible. After each change, save and refresh (`Cmd`+`R`) to watch it update.

> **⚠️ Try it yourself first**
>
> Build from the lecture and your own experimentation. Only open
>
> solution.html
>
> when you're stuck or to compare at the end. Wrestling with selectors is how they stick.

> **💡 No HTML rewrites needed**
>
> You'll add a single
>
> <link>
>
> line per page and maybe one or two
>
> class
>
> attributes. The structure stays the same — CSS hooks onto the semantic HTML you already wrote.

## Tasks

### 1 Create & link the stylesheet

In the same folder as your HTML pages, create an empty file named `styles.css`. Then, in the `<head>` of **each** of the three pages, add a link to it (just below the `<title>`):

```
<link rel="stylesheet" href="styles.css">
```

Prove the link works: put `body { background: #f8fafc; }` in `styles.css`, save, refresh. If the background changes on all three pages, you're wired up.

### 2 Choose a palette (3–5 colors)

Decide on a small, consistent palette and write it at the top of `styles.css` as a comment so you remember it. Aim for: one brand color, one dark text color, one muted/secondary, one light background, one border color. Example:

```
/* Palette
   brand:   #2563eb
   dark:    #1e293b
   muted:   #64748b
   bg:      #f8fafc
   border:  #e2e8f0
*/
```

### 3 Set page-wide defaults on `body`

Using an **element selector**, give `body` your font, text color, background, and center the content. The font and color will *inherit* down to everything else.

- A system font stack (e.g. `system-ui, -apple-system, sans-serif`).
- Your dark text color and light background.
- `max-width` (around `760px`), `margin: 0 auto;` to center, and a little side `padding`.

### 4 Style headings with your palette

Give `h1` and `h2` colors from your palette. Use a **grouping selector** if they share properties (e.g. the same font), and individual rules where they differ.

### 5 Style the nav links with a descendant selector

Target only the links inside the header nav using `nav a`. Give them your brand color, remove the underline (`text-decoration: none;`), and make them bold. Leave links in the body content alone.

### 6 Add one reusable class

Create a class — for example `.button` — and apply it to one link (such as "get in touch" on the Home page or the form's submit button area). Style it with a background color, white text, and some padding so it looks like a button. This proves you can use **class selectors**, the reusable workhorse.

```html
<a class="button" href="contact.html">Get in touch</a>
```

### 7 Add a hover effect

Make links react to the mouse. Add a rule using the `:hover` state so nav links (or your button) change color when hovered:

```
nav a:hover { color: #1e3a8a; }
```

### 8 Verify consistency across all three pages

Open `index.html`, `about.html`, and `contact.html` in turn. They should all share the same colors, font, and centered layout — because they all load the same `styles.css`. Fix anything that looks off.

## ✅ Deliverable — acceptance checklist

- `styles.css` exists and is linked from all three pages via `<link rel="stylesheet">`.
- A palette comment documents 3–5 chosen colors.
- `body` sets font, text color, background, and centers the content with `max-width` + `margin: 0 auto`.
- `h1` and `h2` use palette colors.
- A **descendant selector** (`nav a`) styles the nav links without affecting other links.
- At least one reusable **class** (e.g. `.button`) is defined and applied.
- At least one `:hover` effect works.
- All three pages look visually consistent.

## 🚀 Stretch goals (optional)

- Define your palette once with **CSS custom properties** (variables) on `:root`, e.g. `--brand: #2563eb;`, then use `color: var(--brand);` throughout. (Peek at the top of this very page's `<style>` for the pattern.)
- Style the experience `<table>` on the About page: add `border-collapse: collapse;` and padding on `th, td`.
- Give the form inputs on the Contact page a subtle border and padding.
- Add a `:visited` color for links, and try an `a:hover` underline.
- Commit your work: `git add . && git commit -m "Add external stylesheet and palette"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
