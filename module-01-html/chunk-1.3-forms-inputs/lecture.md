*Full-Stack Web Dev · Module 1 — HTML Foundations*

# Chunk 1.3 — Forms & Inputs

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How `<form>` collects user input and where it goes.
- The common input types and how to label them properly.
- `<select>`, `<textarea>`, checkboxes, and radio buttons.
- Native browser **validation** (no JavaScript needed yet).

Forms are how users *send data to a server* — the gateway to logins, search boxes, comments, and your capstone later. This chunk's lab builds the Contact page and finishes your 3-page personal site (the Module 1 checkpoint).

## 1. The `<form>` element

A form wraps a group of inputs. Two key attributes:

- `action` — the URL the data is sent to.
- `method` — how it's sent: `get` (data in the URL, for searches) or `post` (data in the request body, for creating things).

```html
<form action="/submit" method="post">
  <!-- inputs go here -->
  <button type="submit">Send</button>
</form>
```

> **📝 For now**
>
> We have no server yet, so submitting won't save anything. That's fine — this chunk is about building the form's structure. In Module 5 (FastAPI) your forms will talk to a real backend.

## 2. Inputs & labels

The workhorse is `<input>`. Its `type` attribute changes its behavior and on-screen keyboard. Always pair an input with a `<label>` — clicking the label focuses the input, and screen readers read them together.

```html
<label for="email">Email</label>
<input type="email" id="email" name="email">
```

- `for` on the label must match the input's `id`.
- `name` is the key the server receives (e.g. `email=jane@x.com`).

Common input types:

| type | For |
| --- | --- |
| `text` | Single-line text (default). |
| `email` | Email — validates the @ format, email keyboard on mobile. |
| `password` | Hidden characters. |
| `number` | Numeric input with steppers. |
| `tel` / `url` | Phone numbers / web addresses. |
| `date` | A date picker. |
| `checkbox` | On/off, multiple selectable. |
| `radio` | Pick exactly one from a group (same `name`). |

## 3. Select, textarea, checkboxes & radios

### Dropdown — `<select>`

```html
<label for="topic">Topic</label>
<select id="topic" name="topic">
  <option value="general">General</option>
  <option value="support">Support</option>
  <option value="hello">Just saying hi</option>
</select>
```

### Multi-line text — `<textarea>`

```html
<label for="message">Message</label>
<textarea id="message" name="message" rows="5"></textarea>
```

### Radio buttons (choose one)

Group them by giving the same `name`:

```html
<input type="radio" id="email-c" name="contact" value="email">
<label for="email-c">Email</label>
<input type="radio" id="phone-c" name="contact" value="phone">
<label for="phone-c">Phone</label>
```

### Checkbox (on/off)

```html
<input type="checkbox" id="subscribe" name="subscribe">
<label for="subscribe">Subscribe to updates</label>
```

## 4. Native validation

The browser can validate inputs *before* submitting — free, no JavaScript. Add these attributes:

| Attribute | Effect |
| --- | --- |
| `required` | Field can't be empty. |
| `type="email"` | Must look like an email. |
| `minlength` / `maxlength` | Limit text length. |
| `min` / `max` | Limit numeric/date range. |
| `pattern` | Must match a regular expression. |
| `placeholder` | Hint text (not validation, but helpful). |

```
<input type="email" id="email" name="email"
       required placeholder="you@example.com">
```

If a required field is empty on submit, the browser blocks it and shows a message automatically.

> **⚠️ Validation ≠ security**
>
> Browser validation improves the
>
> user experience
>
> , but users can bypass it. Real safety happens on the
>
> server
>
> — you'll re-validate everything in FastAPI (Module 5). Never trust the client alone.

## 5. A complete contact form (live preview)

Here's a real, working form rendered below — try clicking labels, and pressing "Send" with the email empty to see native validation:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

The code that produces it is exactly what you'll write in the lab.

## ✅ Recap

- `<form>` groups inputs; `action` + `method` say where/how data is sent.
- Pair every input with a `<label for>` matching its `id`; `name` is the server key.
- Pick the right `type` (`email`, `number`, `date`…), and use `<select>`, `<textarea>`, radios, checkboxes.
- Add `required` and friends for native validation — but always re-validate on the server.

**Next:** build `contact.html` and assemble your 3-page site in `assignment.html`.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
