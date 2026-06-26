*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.5 — Lab: Responsive Site + 🏁 Module 2 Checkpoint

**🧪 ASSIGNMENT** · **🏁 CHECKPOINT** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Two parts. **Part A**: make your existing site work across three breakpoints (phone, tablet, desktop) with media queries. **Part B** — the 🏁 Module 2 Checkpoint: pull everything from this module together to redesign the site into a polished, responsive **portfolio** you'd be proud to share.

## Before you start

- You have `styles.css` plus four pages: `index.html`, `about.html`, `projects.html`, `contact.html`.
- Confirm the viewport meta tag is in every page's `<head>`.
- Open DevTools device mode (`Cmd`+`Shift`+`M` / `Ctrl`+`Shift`+`M`) and keep it open while you work.

> **⚠️ Try it yourself first**
>
> Resize as you go. Find the widths where things look cramped — those are
>
> your
>
> breakpoints. Only check the solution to compare.

## Part A — Make it responsive

### 1 Audit at 360px

In device mode, set the width to ~360px (a small phone) and visit all four pages. Note every problem: overflow/horizontal scroll, cramped navbar, sidebar squished, text too big, images too wide. This list drives the rest of Part A.

### 2 Guarantee fluid images

Make sure `img { max-width: 100%; height: auto; }` is in your stylesheet so the profile photo (and any project images) never overflow.

### 3 Make the navbar stack on phones

Add a media query so that below ~600px the header switches to a column (or the nav wraps), so the brand and links don't collide. Example:

```
@media (max-width: 600px) {
  header { flex-direction: column; align-items: flex-start; gap: 10px; }
  nav { flex-wrap: wrap; }
}
```

### 4 Restack the dashboard grid

On `projects.html`, add a query that turns the `.dashboard` into a single column on phones by redrawing `grid-template-areas` (header → content → sidebar → footer). No HTML changes.

### 5 Tune typography per screen

Big desktop headings can be too large on a phone. Set comfortable base (mobile) sizes, then bump them up at a `min-width` breakpoint. Aim for at least **three breakpoints total** across your stylesheet.

```
h1 { font-size: 1.8rem; }                 /* mobile base */
@media (min-width: 600px) { h1 { font-size: 2.2rem; } }
@media (min-width: 900px) { h1 { font-size: 2.8rem; } }
```

### 6 Re-test at 3 widths

Check ~360px (phone), ~768px (tablet), ~1200px (desktop). At every width: no horizontal scrollbar, readable text, nothing overlapping, comfortable spacing.

## 🏁 Part B — Module 2 Checkpoint: the Portfolio Redesign

This is the capstone of the module. Combine everything — palette, box model, typography, Flexbox, Grid, responsiveness — to turn the plain Module 1 site into a portfolio that looks intentionally designed and works on any device.

### 7 Add a hero section to the Home page

Give `index.html` a strong opening: a large heading ("Hi, I'm Jane — full-stack developer"), a one-line tagline, and a prominent `.button` call-to-action ("View my work" → projects, or "Get in touch" → contact). Center it and give it generous vertical padding. This is the first thing visitors see.

### 8 Polish the cards & layout

Make your project cards and content cards consistent: same radius, padding, subtle `box-shadow`, and a hover effect (e.g. `transform: translateY(-3px)` with a `transition`). Ensure spacing is even and the page has a clear visual rhythm.

### 9 Unify the design system

Define your palette and key spacing as CSS variables on `:root` and use them everywhere. One brand color, consistent fonts (heading + body), consistent border-radius. Consistency is what separates "designed" from "thrown together".

### 10 Final responsive QA pass

Walk all four pages at phone / tablet / desktop in device mode. Fix the last rough edges. The portfolio should feel polished and effortless at every size.

## ✅ Deliverable — acceptance checklist

**Part A — responsive:**

- Viewport meta tag present on all pages; images use `max-width: 100%`.
- At least **three breakpoints** used across the stylesheet.
- Navbar adapts (stacks/wraps) on small screens.
- The projects dashboard restacks to one column on phones via redrawn grid areas.
- No horizontal scrollbar at 360px on any page.

**Part B — portfolio checkpoint:**

- Home page has a clear hero with heading, tagline, and a CTA button.
- Cards are consistent and have a hover effect with a transition.
- Palette & fonts are unified (ideally via CSS variables) across all pages.
- The whole site looks polished and works at phone, tablet, and desktop widths.

## 🚀 Stretch goals (optional)

- Add a `prefers-reduced-motion` guard so hover animations respect accessibility settings.
- Use `clamp()` for fluid type that scales smoothly without breakpoints: `font-size: clamp(1.8rem, 5vw, 3rem);`
- Add a sticky navbar with `position: sticky; top: 0;`.
- Run a Lighthouse audit in DevTools and improve the scores.
- Deploy it free with GitHub Pages and share the live link.
- Commit: `git add . && git commit -m "Responsive portfolio — Module 2 complete"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
