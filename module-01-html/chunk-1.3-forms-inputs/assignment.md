*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.3 — Lab: Contact Form + 3-Page Site

**🧪 ASSIGNMENT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build `contact.html` with a validating contact form, then create `index.html` (home), and link all three pages together into a working personal site. This is the **Module 1 checkpoint**.

## Part A — Build the contact form

### 1 Create `contact.html`

Start from the skeleton, and reuse the same `<header>` + `<nav>` as your About page so navigation is consistent.

### 2 Add a form inside `<main>`

Inside a `<section>` with an `<h2>Contact Me</h2>`, add a `<form>` containing, each with a proper `<label>`:

- A **Name** text input (`required`).
- An **Email** input (`type="email"`, `required`).
- A **Topic** `<select>` with at least 3 options.
- A **preferred contact method** using radio buttons (Email / Phone).
- A **Message** `<textarea>` (`required`, `minlength="10"`).
- A "subscribe to updates" **checkbox**.
- A submit `<button>`.

### 3 Test validation

Open `contact.html` and try to submit with the email empty or invalid — the browser should block it and show a message. Fix anything that doesn't behave.

## 🏁 Part B — Module 1 Checkpoint: the 3-page site

Tie everything together into a real (if unstyled) personal website.

### 4 Create `index.html` (Home)

A welcome page with the shared header/nav, a short intro paragraph, and a link inviting visitors to your About and Contact pages.

### 5 Wire up the navigation

Ensure the `<nav>` on all three pages links correctly to `index.html`, `about.html`, and `contact.html`. Click through every link in the browser — no dead ends.

### 6 Validate all three pages

Run each page through the W3C validator and clear all errors.

## ✅ Deliverable — acceptance checklist

- Three files exist: `index.html`, `about.html`, `contact.html`.
- Each page shares the same semantic `<header>` + `<nav>`.
- The contact form has labelled inputs covering: text, email, select, radio group, textarea, checkbox, submit.
- Email and message are `required`; submitting empty is blocked by the browser.
- All nav links work in the browser (you can click between all 3 pages).
- All three pages pass the W3C validator.

## 🚀 Stretch goals (optional)

- Group related fields with `<fieldset>` + `<legend>` (e.g. wrap the radio buttons).
- Add a `pattern` to a phone field, e.g. `pattern="[0-9]{10}"`.
- Add the page name to each `<title>` (e.g. "Jane Doe — Contact").
- Commit & push: `git add . && git commit -m "Add contact form and 3-page site" && git push`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
