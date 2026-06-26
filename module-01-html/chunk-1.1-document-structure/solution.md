*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Follow the steps to build `about.html` piece by piece. Each step explains *what* you're adding and *why*. The complete file is at the bottom — compare it with yours.

### 1 The skeleton

Create `about.html` and start with the boilerplate. The `<title>` shows in the browser tab.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe</title>
</head>
<body>

</body>
</html>
```

### 2 The main heading

One `<h1>` — the page's single most important title.

```html
<h1>Jane Doe</h1>
```

### 3 Intro & sections

Use `<h2>` for section titles and `<p>` for paragraphs.

```python
<h2>About Me</h2>
<p>Hi! I'm Jane, an aspiring full-stack developer based in Bangkok.
   I love solving problems and building things people can use.</p>

<h2>What I'm Learning</h2>
<p>Right now I'm working through a course on HTML, CSS, JavaScript,
   React, and FastAPI. This page is my very first project.</p>
```

### 4 Your photo

If your image is in the same folder, use its filename. Otherwise use a placeholder URL. Always include `alt`.

```
<img src="profile.jpg" alt="Portrait of Jane Doe smiling">

<!-- No photo handy? Use a placeholder: -->
<img src="https://placehold.co/300x300" alt="Placeholder portrait">
```

> **⚠️ Image not showing?**
>
> The
>
> src
>
> path is relative to the HTML file. If
>
> profile.jpg
>
> is in the same folder,
>
> src="profile.jpg"
>
> is correct. Check the spelling and extension (
>
> .jpg
>
> vs
>
> .jpeg
>
> vs
>
> .png
>
> ) match exactly — paths are case-sensitive on the web.

### 5 Two links

An external link and a `mailto:` link. `target="_blank"` opens the external one in a new tab.

```html
<p>
  Find me on
  <a href="https://github.com" target="_blank">GitHub</a>
  or
  <a href="mailto:jane@example.com">send me an email</a>.
</p>
```

### 6 Open it

Double-click `about.html` in Finder, or in VS Code right-click the file → *Reveal in Finder* → open with your browser. Click your links to confirm they work.

## 📄 Complete `about.html`

```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe</title>
</head>
<body>
  <h1>Jane Doe</h1>

  <img src="profile.jpg" alt="Portrait of Jane Doe smiling">

  <h2>About Me</h2>
  <p>Hi! I'm Jane, an aspiring full-stack developer based in Bangkok.
     I love solving problems and building things people can use.</p>

  <h2>What I'm Learning</h2>
  <p>Right now I'm working through a course on HTML, CSS, JavaScript,
     React, and FastAPI. This page is my very first project.</p>

  <p>
    Find me on
    <a href="https://github.com" target="_blank">GitHub</a>
    or
    <a href="mailto:jane@example.com">send me an email</a>.
  </p>
</body>
</html>
```

## 🎉 You're done

You built your first real web page from scratch. It's plain (no styling yet) — that's expected; CSS in Module 2 makes it beautiful.

**Keep this file** — in Chunk 1.2 you'll upgrade it with semantic tags, a skills list, and an experience table.

**Up next → Chunk 1.2: Semantic HTML, Lists & Tables.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
