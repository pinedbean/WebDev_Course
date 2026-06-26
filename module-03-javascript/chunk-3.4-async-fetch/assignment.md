*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.4 — Lab: A Live Quote Machine

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build a page that fetches a **random quote** from a public API and displays it on screen, with a button to load a new one — and proper **loading** and **error** states. You'll use `async/await`, `fetch`, and JSON.

## Before you start

- Make a folder, e.g. `~/Desktop/webdev-course/module-03-javascript/quote-machine/`.
- Create `quotes.html` and `quotes.js`.
- We'll use a free, no-signup API that needs no key:

```
https://dummyjson.com/quotes/random
```

It returns JSON shaped like this:

```json
{
  "id": 42,
  "quote": "Life is what happens when you're busy making other plans.",
  "author": "John Lennon"
}
```

> **💡 Inspect the API first**
>
> Open that URL directly in a browser tab and refresh a few times. Seeing the raw JSON tells you exactly which property names (
>
> quote
>
> ,
>
> author
>
> ) to read in your code.

> **⚠️ Try it yourself first**
>
> Use the lecture's loading → success → error pattern. Only open
>
> solution.html
>
> when stuck.

## Tasks

### 1 Build the page shell

In `quotes.html`: a heading, a `<blockquote id="quote">` (or any element) to hold the text, a `<p id="author">`, and a "New quote" `<button id="new-btn">`. Load `quotes.js` before `</body>`.

### 2 Write an async fetch function

Write `async function loadQuote()` that fetches the URL, checks `response.ok`, parses JSON with `await response.json()`, and returns the data.

### 3 Show a loading state

Before awaiting the fetch, set the quote element's text to `"Loading…"` and disable the button so it can't be clicked twice mid-request. Re-enable it when done.

### 4 Render the quote

On success, put the quote text in the quote element and `— author` in the author element. Use a template literal.

### 5 Handle errors

Wrap the fetch in `try/catch`. On failure, show a friendly message like *"Couldn't load a quote — check your connection and try again."* instead of crashing.

> **💡 Test your error path**
>
> Temporarily change the URL to a broken one (e.g. add
>
> xyz
>
> ) and reload to confirm your error message appears. Then fix the URL.

### 6 Wire up the button & first load

Add a `click` listener on the button that calls your render function. Also call it once on page load so a quote appears immediately.

## ✅ Deliverable — acceptance checklist

- `quotes.html` loads a quote automatically when opened.
- A brief *"Loading…"* state shows while fetching.
- The quote text and author render from the live API response.
- Clicking "New quote" fetches and shows a different quote.
- The fetch uses `async/await` and checks `response.ok`.
- A broken URL / offline shows a friendly error message, not a crash.
- No uncaught errors in the Console.

## 🚀 Stretch goals (optional)

- Add a "Copy" button that copies the current quote to the clipboard (`navigator.clipboard.writeText(...)`).
- Fetch **several** quotes at once from `https://dummyjson.com/quotes?limit=5` and render them as a list (the data lives under `data.quotes`).
- Add a fade-in animation by toggling a CSS class when a new quote arrives.
- Swap in a different public API (e.g. `https://catfact.ninja/fact`) and adapt the property names — a great test of reading JSON shapes.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
