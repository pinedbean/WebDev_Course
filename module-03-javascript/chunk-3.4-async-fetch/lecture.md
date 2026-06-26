*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.4 — Async JavaScript & Fetch

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why some operations are **asynchronous** and how the event loop keeps the page responsive.
- The evolution: **callbacks → Promises → async/await**.
- Calling an API with `fetch` and parsing **JSON**.
- Handling **loading** and **error** states gracefully.

In the lab you'll build a page that fetches live data from a public API and renders it on screen.

## 1. Why "async"? The event loop intuition

JavaScript runs your code on a **single thread** — one thing at a time. So what happens when you ask for data from a server that takes 800ms to reply? If JS just *waited*, the whole page would freeze: no scrolling, no clicks, nothing.

Instead, slow operations (network requests, timers, file reads) are **asynchronous**: JavaScript kicks them off, immediately moves on to other work, and comes back to handle the result *later* when it's ready. The mechanism that schedules "later" is the **event loop**.

```
console.log("1");
setTimeout(() => console.log("2 (later)"), 0);
console.log("3");

// Output order: 1, 3, 2 (later)
```

Even with a `0`ms timer, `"2"` prints last — the timer's callback waits until the current code finishes. That's the event loop deferring async work.

> **📝 The restaurant analogy**
>
> A waiter (the single thread) doesn't stand frozen at your table while the kitchen cooks. They take your order, serve other tables, and return when your food is ready. Async lets one thread stay busy and responsive.

## 2. Callbacks: the original approach

The oldest way to handle "do this when it's done" is to pass a **callback** function:

```
setTimeout(() => {
  console.log("Runs after 1 second");
}, 1000);
```

This works, but when one async step depends on another, callbacks nest into a hard-to-read pyramid nicknamed **"callback hell"**:

```
getUser(1, (user) => {
  getPosts(user, (posts) => {
    getComments(posts[0], (comments) => {
      // ...deeper and deeper
    });
  });
});
```

Promises and `async/await` were invented to flatten this out.

## 3. Promises

A **Promise** is an object representing a value that isn't ready *yet* — it will either **resolve** (success, with a value) or **reject** (failure, with an error). You attach handlers with `.then()` and `.catch()`:

```
fetch("https://api.example.com/data")
  .then((response) => response.json())   // when the response arrives…
  .then((data) => console.log(data))     // …then when JSON is parsed…
  .catch((error) => console.error(error)); // …or if anything failed
```

| State | Meaning |
| --- | --- |
| **pending** | Still working, no result yet. |
| **fulfilled** | Done successfully — `.then()` runs. |
| **rejected** | Failed — `.catch()` runs. |

Chaining `.then()` calls is already much flatter than nested callbacks. But there's an even cleaner syntax built on top of Promises…

## 4. async / await (the modern way)

`async`/`await` lets you write asynchronous code that *reads* like ordinary top-to-bottom code. Mark a function `async`, then `await` any Promise inside it — execution pauses there (without freezing the page) until the Promise settles:

```javascript
async function loadData() {
  const response = await fetch("https://api.example.com/data");
  const data = await response.json();
  console.log(data);
}
loadData();
```

This is exactly the same work as the `.then()` chain above, but flatter and easier to follow. `await` can only be used inside an `async` function.

> **💡 await pauses, it doesn't block**
>
> While an
>
> await
>
> is waiting, JavaScript is free to handle clicks, animations, and other code. The function resumes only when the awaited Promise is ready.

## 5. fetch & JSON

`fetch(url)` is the browser's built-in way to make HTTP requests. It returns a Promise that resolves to a **Response** object. To get the actual data you call `response.json()` (which is *also* async, so it gets its own `await`):

```javascript
const response = await fetch("https://api.example.com/quote");
const data = await response.json();
console.log(data.text, data.author);
```

### What is JSON?

**JSON** (JavaScript Object Notation) is the universal text format for sending data between servers and apps. It looks just like JavaScript objects and arrays:

```json
{
  "text": "Stay hungry, stay foolish.",
  "author": "Steve Jobs",
  "tags": ["motivation", "tech"]
}
```

`response.json()` parses that text into a real JavaScript object you can use with dot notation. Going the other way, `JSON.stringify(obj)` turns an object back into a JSON string (you'll use that in Chunk 3.6 for storage).

## 6. Handling errors properly

Two things can go wrong, and they're handled differently:

- **The network fails** (no connection, bad URL) → `fetch`'s Promise *rejects*, caught by `try/catch` or `.catch()`.
- **The server responds with an error status** (404, 500) → `fetch` still *resolves*! You must check `response.ok` yourself.

```javascript
async function loadQuote() {
  try {
    const response = await fetch("https://api.example.com/quote");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);   // turn a bad status into an error
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to load:", error.message);
  }
}
```

> **⚠️ fetch doesn't reject on 404**
>
> A common surprise: a 404 or 500 does
>
> not
>
> trigger
>
> catch
>
> on its own — only network-level failures do. Always check
>
> if (!response.ok)
>
> and throw, so your
>
> catch
>
> handles HTTP errors too.

## 7. Loading & error states in the UI

Because data takes time, a good UI tells the user what's happening. The standard pattern has three visible states: **loading → success → error**.

```javascript
const output = document.querySelector("#output");

async function showQuote() {
  output.textContent = "Loading…";          // 1) loading
  try {
    const response = await fetch("https://api.example.com/quote");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    output.textContent = `"${data.text}" — ${data.author}`;  // 2) success
  } catch (error) {
    output.textContent = "Could not load a quote. Try again.";  // 3) error
  }
}
```

Set "Loading…" *before* the await, fill in real data on success, and show a friendly message on failure. You'll build exactly this in the lab.

## ✅ Recap

- JavaScript is single-threaded; **async** work is deferred by the **event loop** so the page never freezes.
- Callbacks → Promises (`.then()`/`.catch()`) → `async/await` — each cleaner than the last.
- `fetch(url)` returns a Response; `await response.json()` parses the body.
- **JSON** is the text format for data; `JSON.parse`/`JSON.stringify` convert to and from it.
- Wrap fetches in `try/catch` *and* check `response.ok` — fetch won't reject on a 404.
- Show **loading** and **error** states so the UI feels alive.

**Next:** open `assignment.html` and build a live API-powered page.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
