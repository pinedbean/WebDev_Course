*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.2 — Semantic HTML, Lists & Tables

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What **semantic HTML** means and why it matters (accessibility & SEO).
- The page-structure elements: `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`.
- Lists: unordered, ordered, and description lists.
- Tables for tabular data, done accessibly.

## 1. What "semantic" means

A `<div>` is a generic box with no meaning. **Semantic** elements describe the *purpose* of their content. Compare:

```html
<!-- Non-semantic: what is this? -->
<div class="top">...</div>

<!-- Semantic: clearly the page header -->
<header>...</header>
```

They can look identical on screen, but semantics matter to three audiences:

- **Screen readers** announce landmarks ("navigation", "main content") so blind users can jump around.
- **Search engines** understand your page better, helping SEO.
- **Other developers** (and future you) read the structure at a glance.

## 2. The page-structure elements

A typical page is laid out with these landmark elements:

```text
<header> — site title / logo
  <nav> — main navigation links

<main> — the unique content of this page
  <section> — a thematic grouping
  <article> — a self-contained piece (e.g. a blog post)
  <aside> — side content (related links, ads)

<footer> — copyright, contact, small print
```

| Element | Use it for |
| --- | --- |
| `<header>` | Top of the page or a section: title, logo, intro. |
| `<nav>` | A block of navigation links. |
| `<main>` | The primary, unique content. **One per page.** |
| `<section>` | A thematic group of content, usually with a heading. |
| `<article>` | A self-contained item that could stand alone (post, card, comment). |
| `<aside>` | Tangentially related content (sidebar, callouts). |
| `<footer>` | Bottom matter: copyright, links, contact. |

> **💡 section vs div**
>
> Use a
>
> <section>
>
> when the content is a meaningful group (it usually deserves a heading). Use a plain
>
> <div>
>
> only when you need a box purely for styling with no semantic meaning.

## 3. Lists

### Unordered list — `<ul>`

For items where order doesn't matter (bullets):

```html
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>
```

### Ordered list — `<ol>`

For steps or rankings (numbered automatically):

```html
<ol>
  <li>Learn HTML</li>
  <li>Learn CSS</li>
  <li>Learn JavaScript</li>
</ol>
```

### Description list — `<dl>`

For term/definition pairs:

```html
<dl>
  <dt>HTML</dt>
  <dd>The structure of a web page.</dd>
  <dt>CSS</dt>
  <dd>The styling of a web page.</dd>
</dl>
```

Lists also **nest** — put a `<ul>` inside an `<li>` for sub-items.

## 4. Tables

Tables are for **tabular data** (rows & columns that relate) — *not* for page layout. The key tags:

| Tag | Meaning |
| --- | --- |
| `<table>` | The whole table. |
| `<caption>` | A title/description of the table. |
| `<thead>` / `<tbody>` | Group the header rows vs the body rows. |
| `<tr>` | Table row. |
| `<th>` | Header cell (bold, and announced as a header). |
| `<td>` | Data cell. |

```html
<table>
  <caption>Work Experience</caption>
  <thead>
    <tr>
      <th>Year</th>
      <th>Role</th>
      <th>Company</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2024</td>
      <td>Junior Developer</td>
      <td>Acme Inc.</td>
    </tr>
  </tbody>
</table>
```

> **⚠️ Don't use tables for layout**
>
> In the early web, people built page layouts with tables. Don't — it breaks accessibility and responsiveness. Use tables only for genuine data grids. Layout is CSS's job (Module 2).

## 5. Accessibility recap

- Use semantic landmarks so assistive tech can navigate (`header`, `nav`, `main`, `footer`).
- Keep one `<h1>` and a logical heading order (don't skip levels for looks).
- Every `<img>` needs `alt`.
- Use `<th>` for table headers so cells are associated with their column.

## ✅ Recap

- **Semantic HTML** describes *purpose*, helping accessibility, SEO, and readability.
- Structure pages with `header`, `nav`, `main`, `section`, `article`, `aside`, `footer`.
- Lists: `<ul>` (bullets), `<ol>` (numbered), `<dl>` (term/definition).
- Tables for *data*: `table` → `thead`/`tbody` → `tr` → `th`/`td`.

**Next:** in the lab you'll restructure your About Me page semantically and add a skills list + experience table.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
