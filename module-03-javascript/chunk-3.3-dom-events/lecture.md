*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.3 — The DOM & Events

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What the **DOM** is and how JavaScript reaches into the page.
- **Selecting** elements and changing their content, attributes, and styles.
- **Creating** and **removing** nodes to build UI from data.
- **Events**: listening for clicks/typing and reading the event object.

In the lab you'll build this module's headline project: an interactive **to-do app** (add, complete, remove) in vanilla JavaScript. We'll grow it across the rest of Module 3.

## 1. What is the DOM?

When the browser loads your HTML, it builds a live, in-memory tree of objects representing every element. That tree is the **DOM** — the **D**ocument **O**bject **M**odel. JavaScript can read and change this tree, and the browser instantly re-renders the page to match.

```html
<body>                ← document.body
  <h1>To-Do</h1>       ← an element node
  <ul>                ← an element node
    <li>Buy milk</li>  ← child of the ul
  </ul>
</body>
```

The global `document` object is your entry point into this tree. Everything in this chunk hangs off it.

> **📝 Run scripts after the HTML**
>
> Your script can only find elements that already exist. Put
>
> <script src="todo.js"></script>
>
> just before
>
> </body>
>
> so the HTML is parsed first. (Alternatively use
>
> defer
>
> on the script tag.)

## 2. Selecting elements

Two modern methods cover almost everything, and they take **CSS selectors** — the same syntax you learned in Module 2:

```javascript
// First match of a CSS selector:
const title = document.querySelector("h1");
const addBtn = document.querySelector("#add-btn");   // by id
const firstItem = document.querySelector(".item");   // by class

// ALL matches → a list you can loop over:
const items = document.querySelectorAll(".item");
items.forEach(item => console.log(item.textContent));
```

| Method | Returns |
| --- | --- |
| `querySelector(sel)` | The first matching element (or `null`). |
| `querySelectorAll(sel)` | A NodeList of all matches (use `forEach`). |

> **⚠️ null means "not found"**
>
> If a selector matches nothing,
>
> querySelector
>
> returns
>
> null
>
> , and using it throws
>
> "Cannot read properties of null"
>
> . Check your selector spelling and that the script runs after the element exists.

## 3. Changing content & styles

Once you hold an element, you can read and write its properties:

```javascript
const title = document.querySelector("h1");

title.textContent = "My Tasks";        // change the text
title.classList.add("highlight");      // add a CSS class
title.classList.remove("highlight");   // remove it
title.classList.toggle("done");        // add if absent, remove if present
title.style.color = "tomato";          // inline style (use sparingly)

const link = document.querySelector("a");
link.setAttribute("href", "https://example.com");  // change an attribute
```

| Property / method | What it does |
| --- | --- |
| `textContent` | Get/set the plain text inside an element (safe). |
| `classList.add / remove / toggle` | Manage CSS classes — the preferred way to style. |
| `style.color` etc. | Set one inline CSS property directly. |
| `setAttribute(name, value)` | Set any HTML attribute. |

> **💡 Prefer classes over inline styles**
>
> Toggling a class like
>
> done
>
> (and styling
>
> .done
>
> in CSS) keeps your look in the stylesheet where it belongs, instead of scattering colors through your JavaScript.

## 4. Creating & removing nodes

To add UI from data, build elements and attach them to the tree:

```javascript
const list = document.querySelector("ul");

// 1) create an element
const li = document.createElement("li");

// 2) fill it in
li.textContent = "Walk the dog";
li.classList.add("item");

// 3) attach it to the page
list.appendChild(li);

// remove an element later:
li.remove();
```

This three-step pattern — **create → configure → append** — is how you render lists, cards, rows, and every dynamic UI in vanilla JS.

> **📝 textContent vs innerHTML**
>
> textContent
>
> sets plain text and is always safe.
>
> innerHTML
>
> parses a string as HTML — convenient, but dangerous if the string contains user input (it can inject scripts). For user-typed data, prefer
>
> textContent
>
> .

## 5. Events

An **event** is something that happens: a click, a key press, a form submit. You react by attaching a **listener** with `addEventListener(type, handler)`. The handler runs each time the event fires.

```javascript
const btn = document.querySelector("#add-btn");

btn.addEventListener("click", () => {
  console.log("Button clicked!");
});
```

| Event | Fires when… |
| --- | --- |
| `click` | An element is clicked. |
| `input` | The value of an input changes (every keystroke). |
| `submit` | A form is submitted (Enter or a submit button). |
| `keydown` | A key is pressed. |

### The event object

The browser passes your handler an **event object** with details about what happened, including `event.target` (the element that triggered it):

```
document.querySelector("input").addEventListener("input", (event) => {
  console.log(event.target.value);   // the current text in the box
});
```

### Forms & preventDefault

By default, submitting a form reloads the page. In a JavaScript app you almost always stop that with `event.preventDefault()` so you can handle the input yourself:

```javascript
const form = document.querySelector("form");
form.addEventListener("submit", (event) => {
  event.preventDefault();             // stop the page reload
  const input = document.querySelector("input");
  console.log("You typed:", input.value);
  input.value = "";                   // clear the box
});
```

> **💡 Why a form, not just a button?**
>
> Wrapping the text box and button in a
>
> <form>
>
> gives you Enter-to-submit for free and is more accessible. You handle its
>
> submit
>
> event and call
>
> preventDefault()
>
> .

## 6. Event delegation (handling many items)

A to-do list grows over time — you can't attach a listener to a button that doesn't exist yet. The trick is **event delegation**: listen on a stable parent, then check `event.target` to see what was actually clicked. Events "bubble" up from the clicked element to its ancestors, so the parent hears them all:

```javascript
const list = document.querySelector("ul");

list.addEventListener("click", (event) => {
  if (event.target.matches(".delete-btn")) {
    event.target.closest("li").remove();   // delete that row
  }
});
```

One listener on the `<ul>` handles deletes for every item — current and future. `closest("li")` walks up from the clicked button to its containing list item.

## 7. Putting it together: a tiny to-do

Here's the skeleton you'll flesh out in the lab — add an item on submit, toggle complete or delete on click:

```javascript
const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const list = document.querySelector("#todo-list");

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (text === "") return;          // ignore empty input

  const li = document.createElement("li");
  li.textContent = text;

  const del = document.createElement("button");
  del.textContent = "✕";
  del.classList.add("delete-btn");
  li.appendChild(del);

  list.appendChild(li);
  input.value = "";
});

list.addEventListener("click", (event) => {
  if (event.target.matches(".delete-btn")) {
    event.target.closest("li").remove();
  } else {
    event.target.classList.toggle("done");   // click text to complete
  }
});
```

## ✅ Recap

- The **DOM** is the browser's live tree of your page; `document` is the way in.
- Select with `querySelector` / `querySelectorAll` using CSS selectors.
- Change pages via `textContent`, `classList`, `style`, `setAttribute`.
- Build UI with **create → configure → append**; remove with `.remove()`.
- React to users with `addEventListener`; read details from the **event object** and stop reloads with `preventDefault()`.
- **Delegate** clicks to a parent to handle items added later.

**Next:** open `assignment.html` and build the to-do app.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
