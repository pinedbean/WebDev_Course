*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.4 — CSS Grid Layout

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What **CSS Grid** is and how it differs from Flexbox (two dimensions vs one).
- Defining columns and rows with `grid-template-columns` / `-rows` and the `fr` unit.
- `gap`, `repeat()`, `minmax()`, and `auto-fit` for responsive grids with no media queries.
- Placing items by **spanning** tracks and by named **grid-template-areas**.
- Building a classic page layout: **header · sidebar · content · footer**.

In the lab you'll build a reusable dashboard-style page template with Grid.

## 1. Grid vs Flexbox — which when?

Both place elements, but they think differently:

|  | Flexbox (Chunk 2.3) | Grid (this chunk) |
| --- | --- | --- |
| Dimensions | **One** — a row OR a column | **Two** — rows AND columns |
| Best for | Navbars, button groups, card rows, aligning items in a line | Whole-page layouts, dashboards, image galleries, anything in a matrix |
| Driven by | Content (items size themselves, then flow) | The container (you define the tracks up front) |

> **💡 They're partners, not rivals**
>
> Real sites use both: Grid for the page skeleton, Flexbox
>
> inside
>
> grid cells for the little rows (like the navbar in the header cell). Use the simplest tool for each job.

## 2. Your first grid

Set `display: grid` on a container and declare its columns. The children flow into the cells automatically:

```
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;  /* three equal columns */
  gap: 10px;
}
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

Six children, three columns → the grid automatically wraps them into two rows. You never had to say "new row" — Grid figures it out.

## 3. The `fr` unit — fractions of free space

`fr` means "fraction of the available space". It's the secret to flexible grids. `1fr 1fr 1fr` = three equal columns. `1fr 2fr 1fr` = the middle column is twice as wide:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

You can mix fixed and flexible. A fixed sidebar plus a content area that takes the rest:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

```
grid-template-columns: 200px 1fr;   /* fixed + flexible */
```

## 4. `repeat()`, `minmax()` & `auto-fit`

### `repeat()` — don't write the same track 12 times

```
grid-template-columns: repeat(4, 1fr);   /* same as 1fr 1fr 1fr 1fr */
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

### `minmax()` + `auto-fit` — a responsive grid with no media queries

This is the magic line you'll reuse forever. "Make as many columns as fit, each at least 120px, sharing leftover space." Resize the window and watch the count change:

```
grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

> **📝 Why this is special**
>
> Flexbox can wrap, but every item has a fixed-ish width. Grid's
>
> auto-fit + minmax
>
> keeps the columns perfectly equal AND responsive at the same time — ideal for photo galleries and card grids.

## 5. Spanning multiple tracks

By default each item fills one cell. Make an item stretch across several columns with `grid-column: span N` (or rows with `grid-row`):

```
.featured { grid-column: span 2; }   /* take up two columns */
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

## 6. Named areas — `grid-template-areas`

For whole-page layouts, the clearest approach is to *draw* the layout with names. You name each region, then assign elements to those names. It reads like ASCII art:

```
.layout {
  display: grid;
  grid-template-columns: 180px 1fr;       /* sidebar + content */
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
  gap: 10px;
}
.layout > header  { grid-area: header;  }
.layout > .side   { grid-area: sidebar; }
.layout > main    { grid-area: content; }
.layout > footer  { grid-area: footer;  }
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

Repeating a name (`"header header"`) makes that area span those columns. The whole layout is visible at a glance in the CSS — and you can rearrange the entire page just by editing those strings. **This is exactly the dashboard layout you'll build in the lab.**

> **💡 Responsive areas (preview of 2.5)**
>
> On a phone you redraw the areas into a single stacked column inside a media query — header, then content, then sidebar, then footer — without touching the HTML. We'll do this next chunk.

## 7. Rows & full-height layouts

You can size rows too, and make the layout fill the viewport height with `min-height: 100vh` (100% of the viewport height) so the footer sits at the bottom:

```
.layout {
  display: grid;
  grid-template-columns: 180px 1fr;
  grid-template-rows: auto 1fr auto;   /* header / content grows / footer */
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
  min-height: 100vh;
  gap: 10px;
}
```

`auto` sizes a row to its content (good for header/footer); `1fr` on the middle row lets the content area expand to fill the leftover height.

## ✅ Recap

- `display: grid` lays children into **two dimensions**; you define tracks with `grid-template-columns`/`-rows`.
- `fr` distributes free space; mix with fixed sizes like `200px 1fr`.
- `repeat(auto-fit, minmax(120px, 1fr))` = responsive equal columns, no media query needed.
- Items can `span` tracks; whole pages are clearest with named `grid-template-areas`.
- Use Grid for the page skeleton, Flexbox inside the cells.

**Next:** open `assignment.html` and build a dashboard-style grid layout template.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
