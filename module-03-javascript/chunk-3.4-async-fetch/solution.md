*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.4 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Build the quote machine step by step. Each step shows the code and expected behavior. The complete `quotes.html` and `quotes.js` are at the bottom.

### 1 The page shell

```html
<h1>Random Quote</h1>
<blockquote id="quote"></blockquote>
<p id="author"></p>
<button id="new-btn">New quote</button>

<script src="quotes.js"></script>
```

### 2 Async fetch function

```javascript
const API = "https://dummyjson.com/quotes/random";

async function loadQuote() {
  const response = await fetch(API);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return await response.json();   // { id, quote, author }
}
```

> **⚠️ Check response.ok**
>
> Remember:
>
> fetch
>
> only rejects on network failure, not on a 404/500. The
>
> if (!response.ok) throw
>
> line is what turns a bad status into a real error your
>
> catch
>
> can handle.

### 3 + 4 + 5 Render with loading & error states

```javascript
const quoteEl = document.querySelector("#quote");
const authorEl = document.querySelector("#author");
const btn = document.querySelector("#new-btn");

async function showQuote() {
  quoteEl.textContent = "Loading…";   // loading state
  authorEl.textContent = "";
  btn.disabled = true;                // prevent double-clicks
  try {
    const data = await loadQuote();
    quoteEl.textContent = `"${data.quote}"`;   // success
    authorEl.textContent = `— ${data.author}`;
  } catch (error) {
    quoteEl.textContent = "Couldn't load a quote — check your connection and try again.";
    console.error(error);             // error state
  } finally {
    btn.disabled = false;             // always re-enable
  }
}
```

**Expected:** a flicker of "Loading…", then a quote and author. With a broken URL, you see the friendly error message and the button still works.

> **💡 Why finally?**
>
> The
>
> finally
>
> block runs whether the fetch succeeded or failed, so the button always gets re-enabled. That's the perfect place for cleanup that must always happen.

### 6 Wire up the button & first load

```
btn.addEventListener("click", showQuote);
showQuote();   // load one immediately on page open
```

**Expected:** a quote appears on load; each click swaps in a new one.

## 📄 Complete `quotes.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Random Quote</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         max-width:560px;margin:60px auto;padding:0 16px;color:#1e293b;text-align:center;}
    blockquote{font-size:22px;font-style:italic;margin:24px 0 8px;line-height:1.4;}
    #author{color:#64748b;font-weight:600;margin-top:0;}
    button{cursor:pointer;border:none;border-radius:8px;padding:12px 20px;
           background:#2563eb;color:#fff;font-size:16px;margin-top:16px;}
    button:disabled{opacity:.5;cursor:default;}
  </style>
</head>
<body>
  <h1>Random Quote</h1>
  <blockquote id="quote"></blockquote>
  <p id="author"></p>
  <button id="new-btn">New quote</button>

  <script src="quotes.js"></script>
</body>
</html>
```

## 📄 Complete `quotes.js`

```javascript
const API = "https://dummyjson.com/quotes/random";

const quoteEl = document.querySelector("#quote");
const authorEl = document.querySelector("#author");
const btn = document.querySelector("#new-btn");

async function loadQuote() {
  const response = await fetch(API);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  return await response.json();
}

async function showQuote() {
  quoteEl.textContent = "Loading…";
  authorEl.textContent = "";
  btn.disabled = true;
  try {
    const data = await loadQuote();
    quoteEl.textContent = `"${data.quote}"`;
    authorEl.textContent = `— ${data.author}`;
  } catch (error) {
    quoteEl.textContent = "Couldn't load a quote — check your connection and try again.";
    console.error(error);
  } finally {
    btn.disabled = false;
  }
}

btn.addEventListener("click", showQuote);
showQuote();
```

## 🧰 Troubleshooting

- **"undefined" appears instead of a quote.** The property name is wrong — open the API URL in a browser and confirm it's `data.quote` and `data.author` (not `text`).
- **Nothing happens / stuck on "Loading…".** Check the Console. A typo in the URL or being offline triggers the `catch` — verify the message shows.
- **"await is only valid in async function".** You used `await` outside an `async` function. Make sure it's inside `loadQuote`/`showQuote`.
- **CORS error.** Some APIs block browser requests. dummyjson allows them; if you swap APIs and hit CORS, pick a different public API that permits cross-origin requests.

## 🎉 You're done

You loaded live data over the network without freezing the page, parsed JSON, and handled loading and error states like a real app. This async pattern is identical to what you'll use to talk to your own FastAPI backend later in the course.

**Up next → Chunk 3.5: ES Modules & Modern JS Tooling** — you'll split the to-do app into modules and run it with npm and the Vite dev server.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
