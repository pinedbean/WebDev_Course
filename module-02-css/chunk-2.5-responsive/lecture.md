*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.5 — Responsive Design & Media Queries

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What "responsive" means and why **mobile-first** is the sane default.
- The **viewport meta tag** — the one line that makes phones behave.
- **Media queries**: syntax, common breakpoints, and how to layer them.
- Making images and layouts **fluid** so they never overflow.
- Testing in the browser's **device mode** (DevTools).

This is the capstone of Module 2. In the lab you'll make the whole site responsive across three breakpoints — and the 🏁 **Module Checkpoint** turns it into a polished portfolio.

## 1. What "responsive" means

People visit your site on phones, tablets, laptops, and big monitors. **Responsive design** means one set of HTML + CSS that *adapts* its layout to the screen — three columns on a desktop might become one column on a phone. No separate "mobile site", no app.

You've already met responsive behavior: your Flexbox card row (`flex-wrap`) and your Grid (`auto-fit`) reflow on their own. Those are great defaults. Media queries give you *explicit control* for the cases where automatic reflow isn't enough — like collapsing that dashboard sidebar on a phone.

## 2. The viewport meta tag (do this first)

Without this line, phones pretend to be ~980px wide and shrink your whole page to fit — making text tiny. You've had it in every file since Chunk 1.1; now you know what it does:

```
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

- `width=device-width` — use the device's real width (e.g. 390px on an iPhone), not a fake 980px.
- `initial-scale=1.0` — start at 100% zoom.

> **⚠️ Forget this and nothing else works**
>
> Media queries won't behave correctly without the viewport tag. It's the foundation. Confirm it's in the
>
> <head>
>
> of every page.

## 3. Mobile-first thinking

Write your **base CSS for the smallest screen** (a single, simple column), then *add* complexity for larger screens with `min-width` media queries. Why start small?

- The simplest layout is the most robust — it's hard to break a single column.
- You progressively *enhance*: add columns and sidebars only when there's room.
- It matches how most traffic actually arrives (mobile).

```
/* base = mobile: everything stacks in one column */
.cards { display: grid; grid-template-columns: 1fr; gap: 16px; }

/* enhance for tablet and up */
@media (min-width: 600px) {
  .cards { grid-template-columns: repeat(2, 1fr); }
}

/* enhance for desktop and up */
@media (min-width: 900px) {
  .cards { grid-template-columns: repeat(3, 1fr); }
}
```

> **💡 min-width vs max-width**
>
> Mobile-first uses
>
> min-width
>
> ("from this width
>
> up
>
> "). The opposite,
>
> max-width
>
> ("up to this width"), is desktop-first. Pick one direction and stay consistent — mixing them is confusing. This course uses mobile-first
>
> min-width
>
> .

## 4. Media query syntax

A media query is a conditional block: "apply these rules only when the condition is true." The condition is almost always the viewport width:

```
@media (min-width: 600px) {
  /* normal CSS rules, applied only when viewport ≥ 600px */
  .sidebar { display: block; }
  h1 { font-size: 3rem; }
}
```

You can combine conditions with `and`:

```
@media (min-width: 600px) and (max-width: 900px) {
  /* only on tablet-ish widths */
}
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

## 5. Choosing breakpoints

Breakpoints are the widths where your layout changes. Don't chase specific phone models — pick a few round numbers where your *content* starts to look cramped. A common, simple set:

| Range | Typical device | Common breakpoint |
| --- | --- | --- |
| < 600px | Phones | base styles (no query) |
| ≥ 600px | Tablets | `@media (min-width: 600px)` |
| ≥ 900px | Laptops / desktops | `@media (min-width: 900px)` |

Two or three breakpoints is plenty for most sites. Add one only when something genuinely breaks.

*(Interactive demo — open the `.html` version in a browser to try it live.)*

## 6. Fluid images & media

A fixed-size image will blow out of a narrow screen and cause horizontal scrolling. The one-line fix makes images shrink to fit their container while keeping their proportions:

```
img {
  max-width: 100%;   /* never wider than its container */
  height: auto;      /* keep the aspect ratio          */
}
```

You added this in Chunk 2.2 — now you know it's also a responsive essential. Prefer fluid units (`%`, `fr`, `rem`) over fixed `px` widths for anything that should adapt.

> **📝 Avoid fixed widths on containers**
>
> A rule like
>
> width: 800px
>
> can't shrink below 800px and will overflow a phone. Use
>
> max-width: 800px
>
> instead — it caps the width on big screens but still shrinks on small ones.

## 7. Making the dashboard responsive

Remember the cliff-hanger from Chunk 2.4: the 200px sidebar gets cramped on phones. Here's the fix — redraw the grid areas into a single stacked column below the breakpoint, no HTML changes:

```
/* base (Chunk 2.4): sidebar + content side by side */
.dashboard {
  display: grid;
  grid-template-columns: 200px 1fr;
  grid-template-areas:
    "header  header"
    "sidebar content"
    "footer  footer";
}

/* phones: stack everything in one column */
@media (max-width: 700px) {
  .dashboard {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header"
      "content"
      "sidebar"
      "footer";
  }
}
```

The same four elements, rearranged into a phone-friendly stack purely in CSS. This is the superpower of named grid areas.

> **💡 Responsive navbar too**
>
> On a phone your navbar links may not fit beside the brand. A simple fix without JavaScript: in a narrow media query, switch the header to
>
> flex-direction: column
>
> (or let the nav links
>
> flex-wrap
>
> ) so they stack neatly. A hamburger menu needs JS — that comes in Module 3.

## 8. Testing: the browser device mode

You don't need a real phone. Every browser has a device-emulation mode:

- Open DevTools: `Cmd`+`Option`+`I` (macOS) / `F12` (Windows/Linux).
- Click the **device toolbar** icon (a phone/tablet) — `Cmd`+`Shift`+`M` / `Ctrl`+`Shift`+`M`.
- Pick a device (iPhone, iPad) or drag the edges to any width. The reported width appears at the top.

Watch your breakpoints trigger as you resize. The quickest sanity check: drag down to ~360px and confirm **nothing overflows** and there's no horizontal scrollbar.

> **⚠️ The #1 responsive bug**
>
> A horizontal scrollbar on mobile almost always means one element is too wide — a fixed-width container, an image without
>
> max-width: 100%
>
> , or a
>
> pre
>
> /long word. Hunt it down with DevTools.

## ✅ Recap

- Responsive = one codebase that adapts; start **mobile-first** and enhance up with `min-width` queries.
- The **viewport meta tag** is mandatory — without it media queries misbehave.
- `@media (min-width: 600px) { ... }` applies rules only at/above a width; 2–3 breakpoints is plenty.
- Keep images/containers fluid: `img { max-width: 100%; height: auto; }` and prefer `max-width` over fixed `width`.
- Redraw `grid-template-areas` in a query to restack a layout for phones; test in DevTools device mode.

**Next:** open `assignment.html` — make the whole site responsive, then take on the 🏁 Module 2 portfolio checkpoint.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
