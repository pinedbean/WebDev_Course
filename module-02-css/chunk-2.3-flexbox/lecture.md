*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.3 — Flexbox Layout

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What **Flexbox** is and when to reach for it (one-dimensional layouts: a row *or* a column).
- The container/item relationship and the **main axis** vs **cross axis**.
- The everyday properties: `justify-content`, `align-items`, `gap`, `flex-wrap`, `flex-direction`.
- How `flex` on items controls growing, shrinking, and base size.
- Building a real **navbar** and a wrapping **card row**.

In the lab you'll convert Jane's pipe-separated nav into a proper navbar and add a row of cards.

## 1. Why Flexbox exists

Up to now, your elements have stacked vertically — that's the browser's default "block" flow. But real layouts need things *side by side*: a logo on the left and links on the right, three cards in a row, a centered button. Before Flexbox, doing this meant hacks (floats, inline-block, tables). **Flexbox** made it sane.

The rule of thumb: **Flexbox handles one dimension at a time** — you're arranging items along a single line (a row or a column). For full two-dimensional grids (rows *and* columns together), you'll use CSS Grid in the next chunk.

## 2. Container & items

Flexbox always involves two roles. You set `display: flex` on a **container** (the parent), and its *direct children* become flexible **items**:

```html
<div class="flex">          <!-- the flex CONTAINER -->
  <div class="item">A</div>  <!-- flex ITEM -->
  <div class="item">B</div>  <!-- flex ITEM -->
  <div class="item">C</div>  <!-- flex ITEM -->
</div>
```

```
.flex { display: flex; gap: 10px; }
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

That one line did it: the three boxes now sit in a row instead of stacking. Everything else in Flexbox is about *distributing and aligning* those items.

## 3. The two axes (the key mental model)

A flex container has two axes, and which is which depends on `flex-direction`:

- **Main axis** — the direction items flow. With the default `flex-direction: row`, the main axis runs left → right.
- **Cross axis** — perpendicular to it (top → bottom for a row).

This matters because the two big alignment properties each control one axis:

| Property | Controls | For a row, that's… |
| --- | --- | --- |
| `justify-content` | The **main** axis | horizontal position |
| `align-items` | The **cross** axis | vertical position |

> **💡 Remember it**
>
> justify = main
>
> (the way items flow).
>
> align = cross
>
> (the other way). If you flip
>
> flex-direction
>
> to
>
> column
>
> , the axes swap — and so does which property does what.

## 4. `justify-content` — along the main axis

Distributes items horizontally (in a row). The common values:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

*(Interactive demo — open the `.html` version in a browser to try it live.)*

*(Interactive demo — open the `.html` version in a browser to try it live.)*

*(Interactive demo — open the `.html` version in a browser to try it live.)*

```
.flex { display: flex; justify-content: space-between; }
```

`space-between` is the classic navbar trick: it pushes the first item to the far left and the last to the far right, putting all the empty space *between* them.

## 5. `align-items` — along the cross axis

Positions items vertically within the container's height (in a row). The default is `stretch` (items fill the height). Use `center` constantly to vertically center things:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

*(Interactive demo — open the `.html` version in a browser to try it live.)*

*(Interactive demo — open the `.html` version in a browser to try it live.)*

> **📝 The famous centering trick**
>
> To center something perfectly (both directions), combine the two:
>
> display:flex; justify-content:center; align-items:center;
>
> . This finally solved "how do I vertically center a div", a problem that haunted developers for a decade.

## 6. `gap` & `flex-wrap`

### `gap` — spacing between items

Adds consistent space between flex items without fiddling with margins. You've already used it (the footer nav on these pages is `display:flex; gap:12px`):

```
.flex { display: flex; gap: 16px; }
```

### `flex-wrap` — let items drop to the next line

By default, flex items try to stay on one line and shrink to fit. `flex-wrap: wrap` lets them wrap onto new lines when there's no room — essential for responsive card grids. Resize this window and watch the cards below wrap:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

```
.row { display: flex; flex-wrap: wrap; gap: 16px; }
```

## 7. Flexible items: the `flex` shorthand

So far we positioned items. Now make them *resize*. Put `flex` on the items themselves:

```
.item { flex: 1; }   /* every item grows to share space equally */
```

`flex: 1` is shorthand for "grow to fill available space, sharing it equally with siblings". Combine with `min-width` so items don't get too narrow before wrapping. That's exactly how a responsive card row works:

```
.card { flex: 1; min-width: 180px; }
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

| On the item | Meaning |
| --- | --- |
| `flex: 1` | Grow to fill, share space equally. |
| `flex: 0 0 200px` | Don't grow, don't shrink, stay 200px wide. |
| `flex-grow: 2` | Take twice as much extra space as a `flex-grow:1` sibling. |

## 8. Building a navbar (the lab's centerpiece)

A navbar is just a flex container with `space-between` (brand left, links right) and `align-items: center` (everything vertically centered). The links themselves are another little flex container with a `gap`:

```
.navbar {
  display: flex;
  justify-content: space-between;  /* brand left, links right */
  align-items: center;             /* vertically centered     */
  background: #1e293b;
  padding: 12px 18px;
}
.navbar .links { display: flex; gap: 18px; }
.navbar .links a { color: #cbd5e1; text-decoration: none; }
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

For Jane's site, you'll wrap her existing `<nav>` links and the `<h1>` in a header and flex them apart — replacing those temporary `|` separators from Module 1 for good.

## ✅ Recap

- `display: flex` on a container lays its children in a row (or column) — Flexbox is for **one dimension**.
- **justify-content** aligns along the **main** axis; **align-items** aligns along the **cross** axis.
- `gap` spaces items; `flex-wrap: wrap` lets them flow onto new lines.
- `flex: 1` on items makes them grow to share space; pair with `min-width` for responsive rows.
- Navbar pattern = `justify-content: space-between; align-items: center;`

**Next:** open `assignment.html` and build a real navbar + card row for your site.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
