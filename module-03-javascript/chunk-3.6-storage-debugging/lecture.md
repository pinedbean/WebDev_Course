*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.6 — Browser Storage & Debugging

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to persist data in the browser with `localStorage` and `sessionStorage`.
- **JSON serialization**: storing objects and arrays as text.
- Debugging with DevTools: the **Console**, **breakpoints**, the **Network** tab, and the storage inspector.

In the lab you'll make your to-do app remember tasks across reloads — then, for the **Module 3 Checkpoint**, build a brand-new **expense tracker** widget using everything from this module.

## 1. The problem: memory is temporary

Every variable in your to-do app lives in memory. Refresh the page and it's gone. To *remember* data between visits, you need persistent storage. The browser gives you a simple built-in option: **Web Storage**.

| API | Lifetime | Use it for |
| --- | --- | --- |
| `localStorage` | Stays until explicitly cleared (survives reloads & restarts). | Saving user data like a to-do list, preferences, theme. |
| `sessionStorage` | Cleared when the tab closes. | Temporary state for one session (e.g. a multi-step form). |

Both share the same API — we'll focus on `localStorage`.

## 2. The localStorage API

It's a simple key→value store. Both the key and the value must be **strings**:

```
localStorage.setItem("username", "Jane");   // save
localStorage.getItem("username");           // "Jane"  (read)
localStorage.removeItem("username");        // delete one key
localStorage.clear();                       // delete everything
```

> **⚠️ Strings only**
>
> localStorage
>
> can only store strings. If you save a number you'll read it back as text (
>
> "42"
>
> , not
>
> 42
>
> ). And if you try to save an object directly, you get the useless string
>
> "[object Object]"
>
> . The fix is JSON.

## 3. JSON serialization: storing objects & arrays

To store structured data (like your tasks array), convert it to a JSON **string** on the way in, and parse it back to an object on the way out:

```javascript
const tasks = [
  { id: "a1", text: "Buy milk", done: false },
  { id: "b2", text: "Walk dog", done: true },
];

// SAVE: object → JSON string
localStorage.setItem("tasks", JSON.stringify(tasks));

// LOAD: JSON string → object
const saved = JSON.parse(localStorage.getItem("tasks"));
console.log(saved[0].text);   // "Buy milk"
```

| Function | Direction |
| --- | --- |
| `JSON.stringify(value)` | JS object/array → JSON string (to save). |
| `JSON.parse(string)` | JSON string → JS object/array (to read). |

> **⚠️ Nothing saved yet?**
>
> getItem
>
> returns
>
> null
>
> if the key doesn't exist, and
>
> JSON.parse(null)
>
> throws. Guard it with a fallback:
>
> JSON.parse(localStorage.getItem("tasks")) || []
>
> or check for
>
> null
>
> first.

## 4. The load/save pattern

Two small helpers wrap all storage access in one place. Load once at startup; save after every change:

```javascript
const KEY = "todo-tasks";

function loadTasks() {
  const raw = localStorage.getItem(KEY);
  return raw ? JSON.parse(raw) : [];   // [] if nothing saved yet
}

function saveTasks(tasks) {
  localStorage.setItem(KEY, JSON.stringify(tasks));
}
```

In your modular app, the perfect home for these is `store.js`: call `loadTasks()` to initialize the array, and call `saveTasks()` at the end of `addTask`, `toggleTask`, and `removeTask`. The UI never needs to know storage exists.

> **💡 Wrap, don't scatter**
>
> Keeping every
>
> localStorage
>
> call inside
>
> store.js
>
> means the rest of your app stays unaware of
>
> how
>
> data persists. Swap to a real database backend later (you will!) and only one file changes.

## 5. Inspecting storage in DevTools

You can see exactly what your app saved. Open DevTools and find the storage panel:

- **Chrome/Edge:** *Application* tab → *Local Storage* → your site's origin.
- **Firefox:** *Storage* tab → *Local Storage*.

You'll see your keys and values as a table. You can edit or delete entries here to test how your app reacts — incredibly handy for debugging persistence.

## 6. Debugging like a pro

Bugs are normal. The difference between guessing and fixing is knowing your tools. DevTools gives you several.

### Console methods

```
console.log("value:", value);   // everyday inspection
console.table(tasks);           // arrays of objects as a neat grid
console.error("Something broke");
console.warn("Heads up");
```

Read error messages carefully — they usually name the file and line. *"Cannot read properties of null (reading 'addEventListener')"* almost always means a `querySelector` returned `null` (wrong id, or script ran too early).

### Breakpoints (pause and look around)

Instead of sprinkling `console.log` everywhere, you can **pause** execution and inspect everything:

- Open the **Sources** tab, find your file, and click a line number to set a breakpoint.
- Trigger the code (e.g. click your button). Execution pauses on that line.
- Hover variables to see their values; use the *Scope* panel; step through with the controls (step over / into / out).
- Or drop a `debugger;` statement in your code — DevTools pauses there automatically when open.

### The Network tab

For fetches (Chunk 3.4), the **Network** tab shows every request: its URL, status code, timing, and the response body. If data isn't appearing, check here first — is the request even firing? Is it a 404? What did the server actually return?

> **📝 A debugging mindset**
>
> 1)
>
> Reproduce it reliably.
>
> 2)
>
> Read the actual error.
>
> 3)
>
> Form a hypothesis ("the id is wrong").
>
> 4)
>
> Check it with a log or breakpoint.
>
> 5)
>
> Fix and re-test. Change one thing at a time.

## 7. About the Module 3 Checkpoint

After persisting the to-do app, you'll build a fresh widget — an **expense tracker** — that exercises the whole module at once:

| Skill | From | In the expense tracker |
| --- | --- | --- |
| Variables, operators | 3.1 | Totals, math on amounts. |
| Arrays of objects, `reduce` | 3.2 | Store expenses; sum the balance. |
| DOM & events | 3.3 | Form to add, list to display, delete buttons. |
| localStorage + JSON | 3.6 | Remember expenses across reloads. |
| (Optional) modules/Vite | 3.5 | Split into store/ui/main if you like. |

Full instructions are in the assignment and solution pages for this chunk.

## ✅ Recap

- `localStorage` persists data indefinitely; `sessionStorage` lasts one tab session.
- Storage holds **strings only** — use `JSON.stringify` to save and `JSON.parse` to read objects/arrays.
- Guard reads with a fallback (`|| []`) since missing keys return `null`.
- Centralize storage in one place (your `store.js`).
- Debug with `console` methods, **breakpoints**, the **Network** tab, and the storage inspector.

**Next:** open `assignment.html` — persist the to-do app, then build the 🏁 checkpoint expense tracker.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
