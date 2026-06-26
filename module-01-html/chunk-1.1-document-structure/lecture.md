*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.1 — HTML Document Structure

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What HTML is and the anatomy of an **element** (tags + attributes).
- The required skeleton of every HTML page.
- Core content elements: headings, paragraphs, **links**, and **images**.
- How nesting and indentation keep your markup readable.

In the lab you'll build an "About Me" page from a blank file.

## 1. What is HTML?

**HTML** (HyperText Markup Language) is how we describe the *structure and content* of a web page. It is not a programming language — there's no logic or math. You "mark up" text by wrapping it in **tags** that tell the browser what each piece *is*: a heading, a paragraph, a link, an image.

HTML is one of three frontend languages, each with a job:

| Language | Role | Analogy |
| --- | --- | --- |
| **HTML** | Structure & content | The skeleton |
| CSS | Styling & layout | The skin & clothes |
| JavaScript | Behavior & interactivity | The muscles |

This module is all about the skeleton. CSS comes in Module 2.

## 2. Anatomy of an element

Most elements have an **opening tag**, some **content**, and a **closing tag**:

```text
<p>Hello world</p>
```

- `<p>` — the opening tag (here, a paragraph).
- `Hello world` — the content.
- `</p>` — the closing tag (note the slash).

Tags can carry **attributes** — extra info written as `name="value"` inside the opening tag:

```text
<a href="https://example.com">Visit</a>
```

Here `href` is the attribute name and the URL is its value. A few elements are **self-closing** (no content, no closing tag), like images: `<img src="cat.jpg" alt="A cat">`.

> **💡 Tip**
>
> Tag names are lowercase, attribute values go in quotes, and every opening tag (except self-closing ones) needs a matching closing tag.

## 3. The document skeleton

Every HTML page starts from the same boilerplate. Memorize this shape — you'll type it constantly:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>My Page</title>
</head>
<body>
  <h1>Hello!</h1>
  <p>This is my first page.</p>
</body>
</html>
```

| Part | What it's for |
| --- | --- |
| `<!DOCTYPE html>` | Tells the browser "this is modern HTML5". Always first. |
| `<html lang="en">` | The root element; `lang` helps screen readers & search engines. |
| `<head>` | Info *about* the page (not shown on screen): title, character set, viewport, links to CSS. |
| `<meta charset="UTF-8">` | Lets the page show any character/emoji correctly. |
| viewport meta | Makes the page scale properly on phones (vital for responsive design later). |
| `<title>` | The text in the browser tab. |
| `<body>` | Everything the user actually sees on the page. |

> **📝 head vs body**
>
> If you can
>
> see
>
> it on the page, it goes in the
>
> <body>
>
> . If it's information
>
> about
>
> the page, it goes in the
>
> <head>
>
> .

## 4. Core content elements

### Headings

Six levels, `<h1>` (most important) to `<h6>` (least). Use them to create an outline — **one** `<h1>` per page, then nest down logically. Don't pick a heading just because of its size (that's CSS's job).

```html
<h1>Jane Doe</h1>
<h2>About Me</h2>
<h3>Hobbies</h3>
```

### Paragraphs & line breaks

```html
<p>I'm learning full-stack web development.</p>
```

### Links — `<a>`

The "hyper" in HyperText. The `href` attribute is the destination:

```html
<a href="https://developer.mozilla.org">MDN docs</a>     <!-- external -->
<a href="about.html">About page</a>                       <!-- another page in your site -->
<a href="mailto:you@example.com">Email me</a>             <!-- opens email app -->
```

### Images — `<img>`

Self-closing. `src` is the file/URL; `alt` is text shown if the image fails and read aloud by screen readers — never skip it.

```
<img src="profile.jpg" alt="Portrait of Jane Doe">
```

> **⚠️ Always write alt text**
>
> alt
>
> is required for accessibility. Describe the image's meaning. If it's purely decorative, use an empty
>
> alt=""
>
> .

## 5. Nesting & indentation

Elements live inside other elements, forming a tree. Indent nested elements so the structure is obvious, and always close tags in the reverse order you opened them:

```html
<body>
  <h1>My Site</h1>
  <p>Read the <a href="docs.html">docs</a> to begin.</p>
</body>
```

Here `<a>` is nested inside `<p>`, which is nested inside `<body>`. Browsers forgive sloppy nesting sometimes, but clean nesting prevents weird bugs.

## ✅ Recap

- HTML marks up **content & structure** with tags; attributes add info as `name="value"`.
- Every page uses the same skeleton: `<!DOCTYPE>` → `<html>` → `<head>` (about the page) + `<body>` (the visible page).
- Core elements: headings `h1–h6`, `<p>`, links `<a href>`, images `<img src alt>`.
- Nest neatly and always include `alt` text.

**Next:** open `assignment.html` and build your About Me page.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
