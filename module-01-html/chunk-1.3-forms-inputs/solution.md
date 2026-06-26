*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.3 — Solution (Step-by-Step)

**✅ SOLUTION** · **+ Module 1 Checkpoint**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

First we build the contact form, then assemble the 3-page site. Full files for `contact.html` and `index.html` are at the bottom.

### 1 The form fields

Each control is paired with a `<label for>` that matches its `id`. Note the radio buttons share `name="contact"` so only one can be chosen.

```html
<form action="#" method="post">
  <label for="name">Name</label>
  <input type="text" id="name" name="name" required>

  <label for="email">Email</label>
  <input type="email" id="email" name="email" required
         placeholder="you@example.com">

  <label for="topic">Topic</label>
  <select id="topic" name="topic">
    <option value="general">General</option>
    <option value="support">Support</option>
    <option value="feedback">Feedback</option>
  </select>

  <fieldset>
    <legend>Preferred contact method</legend>
    <input type="radio" id="by-email" name="contact" value="email" checked>
    <label for="by-email">Email</label>
    <input type="radio" id="by-phone" name="contact" value="phone">
    <label for="by-phone">Phone</label>
  </fieldset>

  <label for="message">Message</label>
  <textarea id="message" name="message" rows="5"
            minlength="10" required></textarea>

  <input type="checkbox" id="subscribe" name="subscribe">
  <label for="subscribe">Subscribe to updates</label>

  <button type="submit">Send message</button>
</form>
```

> **💡 fieldset + legend**
>
> Wrapping the radio group in
>
> <fieldset>
>
> with a
>
> <legend>
>
> tells assistive tech "these options belong together" — exactly the stretch goal.

### 2 Why submitting does nothing (yet)

`action="#"` just points back at the page, and there's no server to receive the data. When you press Send with valid input, the page reloads — that's expected for now. In Module 5 you'll point `action` at a FastAPI endpoint that actually stores the message.

## 📄 Complete `contact.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — Contact</title>
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
    <section>
      <h2>Contact Me</h2>
      <form action="#" method="post">
        <label for="name">Name</label>
        <input type="text" id="name" name="name" required>

        <label for="email">Email</label>
        <input type="email" id="email" name="email" required
               placeholder="you@example.com">

        <label for="topic">Topic</label>
        <select id="topic" name="topic">
          <option value="general">General</option>
          <option value="support">Support</option>
          <option value="feedback">Feedback</option>
        </select>

        <fieldset>
          <legend>Preferred contact method</legend>
          <input type="radio" id="by-email" name="contact" value="email" checked>
          <label for="by-email">Email</label>
          <input type="radio" id="by-phone" name="contact" value="phone">
          <label for="by-phone">Phone</label>
        </fieldset>

        <label for="message">Message</label>
        <textarea id="message" name="message" rows="5" minlength="10" required></textarea>

        <p>
          <input type="checkbox" id="subscribe" name="subscribe">
          <label for="subscribe">Subscribe to updates</label>
        </p>

        <button type="submit">Send message</button>
      </form>
    </section>
  </main>

  <footer>
    <p>© 2026 Jane Doe</p>
  </footer>
</body>
</html>
```

## 📄 Complete `index.html` (Home)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jane Doe — Home</title>
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
    <section>
      <h2>Welcome</h2>
      <p>Hi, I'm Jane — an aspiring full-stack developer. This little
         site is where I'm learning to build for the web.</p>
      <p>Learn more <a href="about.html">about me</a>,
         or <a href="contact.html">get in touch</a>.</p>
    </section>
  </main>

  <footer>
    <p>© 2026 Jane Doe</p>
  </footer>
</body>
</html>
```

## Wiring & validating

- Keep the three files in the same folder so relative links like `href="about.html"` resolve.
- Open `index.html` in the browser and click every nav link — you should be able to reach all three pages and come back.
- Validate each page at [validator.w3.org](https://validator.w3.org/#validate_by_input). A frequent miss: a checkbox/radio without a matching `<label for>`, or a duplicate `id` on the page.

## 🎉 Module 1 complete!

You've built a real, validated, semantic 3-page website with navigation and a working form — using nothing but HTML. It's plain by design.

**Up next → Module 2: CSS & Layout**, where you'll turn this skeleton into something that actually looks good: colors, fonts, spacing, Flexbox, Grid, and responsive design.

Don't forget to commit and push your work to GitHub. 🚀

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
