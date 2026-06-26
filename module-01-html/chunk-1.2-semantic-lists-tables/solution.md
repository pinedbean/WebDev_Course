*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We restructure `about.html` step by step into a clean, semantic page. The full file is at the bottom.

### 1 Header & nav

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

The `|` separators are temporary — CSS will style the nav properly in Module 2.

### 2 Wrap content in `<main>` + sections

```python
<main>
  <section>
    <h2>About Me</h2>
    <p>Hi! I'm Jane, an aspiring full-stack developer...</p>
  </section>

  <section>
    <h2>What I'm Learning</h2>
    <p>HTML, CSS, JavaScript, React, and FastAPI.</p>
  </section>
</main>
```

### 3 Skills list (with a nested sub-list)

```html
<section>
  <h2>Skills</h2>
  <ul>
    <li>HTML</li>
    <li>CSS</li>
    <li>JavaScript
      <ul>
        <li>DOM basics</li>
        <li>Fetch & APIs</li>
      </ul>
    </li>
    <li>Git & GitHub</li>
    <li>Problem solving</li>
  </ul>
</section>
```

### 4 Experience table

```html
<section>
  <h2>Experience</h2>
  <table>
    <caption>Work & project history</caption>
    <thead>
      <tr>
        <th>Year</th>
        <th>Role</th>
        <th>Organisation</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>2025</td>
        <td>Web Dev Student</td>
        <td>Self-taught</td>
      </tr>
      <tr>
        <td>2024</td>
        <td>Volunteer</td>
        <td>Local Library</td>
      </tr>
    </tbody>
  </table>
</section>
```

### 5 Footer

```html
<footer>
  <p>© 2026 Jane Doe ·
    <a href="mailto:jane@example.com">jane@example.com</a>
  </p>
</footer>
```

### 6 Validate

Go to [validator.w3.org](https://validator.w3.org/#validate_by_input), paste your whole file, and click Check. Common fixes: a missing closing tag, a stray `</section>`, or forgetting `alt` on the image. Aim for the green "No errors" banner.

## 📄 Complete `about.html`

```python
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — About</title>
</head>
<body>
  <header>
    <h1>Jane Doe</h1>
    <nav>
      <a href="index.html">Home</a> |
      <a href="about.html">About</a> |
      <a href="contact.html">Contact</a>
    </nav>
  </header>

  <main>
    <img src="profile.jpg" alt="Portrait of Jane Doe smiling">

    <section>
      <h2>About Me</h2>
      <p>Hi! I'm Jane, an aspiring full-stack developer based in Bangkok.</p>
    </section>

    <section>
      <h2>What I'm Learning</h2>
      <p>HTML, CSS, JavaScript, React, and FastAPI.</p>
    </section>

    <section>
      <h2>Skills</h2>
      <ul>
        <li>HTML</li>
        <li>CSS</li>
        <li>JavaScript
          <ul>
            <li>DOM basics</li>
            <li>Fetch & APIs</li>
          </ul>
        </li>
        <li>Git & GitHub</li>
        <li>Problem solving</li>
      </ul>
    </section>

    <section>
      <h2>Experience</h2>
      <table>
        <caption>Work & project history</caption>
        <thead>
          <tr><th>Year</th><th>Role</th><th>Organisation</th></tr>
        </thead>
        <tbody>
          <tr><td>2025</td><td>Web Dev Student</td><td>Self-taught</td></tr>
          <tr><td>2024</td><td>Volunteer</td><td>Local Library</td></tr>
        </tbody>
      </table>
    </section>
  </main>

  <footer>
    <p>© 2026 Jane Doe ·
      <a href="mailto:jane@example.com">jane@example.com</a>
    </p>
  </footer>
</body>
</html>
```

## 🎉 You're done

Your page now has a meaningful, accessible structure that screen readers and search engines understand — even though it still looks plain. That structure is exactly what CSS will hook into next module.

**Up next → Chunk 1.3: Forms & Inputs**, where you build the Contact page and complete the 3-page personal site (the Module 1 checkpoint).

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
