*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.2 — The Box Model & Typography

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The **box model**: how content, **padding**, **border**, and **margin** stack.
- Why `box-sizing: border-box` makes sizing sane, and the one-line reset everyone uses.
- Shorthand for spacing, and the gotcha of **margin collapse**.
- Typography: `font-family`, `font-size`, `font-weight`, `line-height`, and text styling.
- How to add a real **web font** (a Google Font) to your own project.

In the lab you'll fix the spacing and typography across Jane's site and give it a proper font.

## 1. Every element is a box

The single most important mental model in CSS: **the browser draws every element as a rectangular box.** A paragraph, an image, a `<nav>` — all boxes. Each box has four layers, from the inside out:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

| Layer | What it is | Think of a framed photo |
| --- | --- | --- |
| **content** | The actual text/image. | The photo itself. |
| **padding** | Space inside the border. | The mat/space around the photo. |
| **border** | The line around padding. | The frame. |
| **margin** | Space outside the border. | The gap to the next frame on the wall. |

> **💡 padding vs. margin**
>
> Padding
>
> is inside (it grows the box and is colored by the background).
>
> Margin
>
> is outside (invisible space between boxes). "Pad the inside, margin the outside."

## 2. Setting padding, border & margin

```
.card {
  padding: 20px;                 /* all four sides */
  border: 1px solid #e2e8f0;     /* width style color */
  margin: 16px;                  /* all four sides */
  border-radius: 12px;           /* rounded corners */
}
```

### Shorthand: one value, or two, or four

```
padding: 20px;             /* all sides: 20 */
padding: 10px 20px;        /* top&bottom: 10,  left&right: 20 */
padding: 10px 20px 30px;   /* top:10  left&right:20  bottom:30 */
padding: 10px 20px 30px 5px; /* top right bottom left (clockwise) */
```

The same pattern works for `margin`. Remember the clockwise order: **T R B L** (Top, Right, Bottom, Left) — "TRouBLe".

### Centering a block: `margin: 0 auto`

You used this in Chunk 2.1. With a set `max-width`, `auto` left/right margins split the leftover space evenly, centering the box horizontally:

```
main { max-width: 760px; margin: 0 auto; }
```

## 3. `box-sizing`: the fix you'll always want

Here's the trap. By default (`content-box`), `width` sets only the *content* width — then padding and border are **added on top**. So a "200px" box with padding is actually wider than 200px. That breaks layouts constantly.

*(Interactive demo — open the `.html` version in a browser to try it live.)*

With `box-sizing: border-box`, `width` means the *total* width including padding and border — what you almost always expect. So apply it to **everything** with this universal reset at the top of your stylesheet:

```
*, *::before, *::after {
  box-sizing: border-box;
}
```

> **📝 You've seen this already**
>
> Every lesson file in this course starts its
>
> <style>
>
> with
>
> *{box-sizing:border-box;}
>
> . It's that common. Add it once and forget about the math.

## 4. Margin collapse (the surprising one)

When two **vertical** margins meet, they don't add up — they *collapse* to the larger of the two. If a paragraph has `margin-bottom: 20px` and the next has `margin-top: 30px`, the gap between them is **30px**, not 50px.

```
p { margin: 20px 0; }
/* gap between two stacked paragraphs = 20px, not 40px */
```

> **⚠️ Only vertical, only margins**
>
> Collapse happens between top/bottom margins of block elements — not left/right, and never with padding. If spacing ever looks "half what I set", margin collapse is usually why. A common fix is to set margin in one direction only (e.g. only
>
> margin-bottom
>
> ).

## 5. Typography — making text readable

Good typography is most of what makes a site feel "designed". A few properties do the heavy lifting.

### font-family & the fallback stack

List fonts in order of preference; the browser uses the first one it has. Always end with a generic family (`serif`, `sans-serif`, `monospace`) as a safety net:

```
body { font-family: "Inter", system-ui, -apple-system, sans-serif; }
```

*(Interactive demo — open the `.html` version in a browser to try it live.)*

### font-size & font-weight

```
h1 { font-size: 2rem; font-weight: 700; }   /* 700 = bold   */
p  { font-size: 1rem; font-weight: 400; }   /* 400 = normal */
.subtle { font-weight: 300; }               /* 300 = light  */
```

### line-height — vertical breathing room

The space between lines of text. Set it **unitless** (a multiplier of the font size). `1.5`–`1.7` is comfortable for body text; headings can be tighter:

*(Interactive demo — open the `.html` version in a browser to try it live.)*

### Other text properties you'll use

```
.lead {
  color: #475569;
  text-align: center;        /* left | right | center | justify */
  letter-spacing: 0.02em;    /* space between letters */
  text-transform: uppercase; /* UPPER | lower | Capitalize */
  text-decoration: none;     /* remove the underline on links */
}
```

> **💡 Limit line length for readability**
>
> Lines of ~60–75 characters are easiest to read. That's why we cap text with
>
> max-width
>
> on a container instead of letting it stretch across a wide monitor.

## 6. Adding a web font (Google Fonts)

System fonts are fine, but a chosen font gives your site personality. **Google Fonts** hosts hundreds for free. Two steps in your *own* project:

**1.** Add a `<link>` in your page's `<head>` (Google gives you this when you pick a font at `fonts.google.com`):

```
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
```

**2.** Use it in your CSS — keep system fonts as the fallback:

```
body { font-family: "Inter", system-ui, sans-serif; }
h1, h2, h3 { font-family: "Poppins", system-ui, sans-serif; }
```

> **⚠️ Web fonts need the internet**
>
> A Google Font is loaded over the network. That's perfect for your real project. (These
>
> course
>
> lesson files deliberately stay offline-only, so they use a system font stack — but your portfolio can and should use a web font.) Always keep a system fallback so text still shows while the font loads or if you're offline.

*(Interactive demo — open the `.html` version in a browser to try it live.)*

## 7. Putting it together for Jane's site

Here's how the box model + typography improves the site you styled in Chunk 2.1:

```
*, *::before, *::after { box-sizing: border-box; }

body {
  font-family: "Inter", system-ui, sans-serif;
  line-height: 1.65;
  color: #1e293b;
  max-width: 760px;
  margin: 0 auto;
  padding: 0 20px;
}

h1, h2 { font-family: "Poppins", system-ui, sans-serif; line-height: 1.2; }
h2 { margin-top: 2rem; }

/* turn each <section> into a tidy card */
section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 20px;
}

footer { margin-top: 2rem; padding: 16px 0; color: #94a3b8; }
```

Same HTML as Module 1 — but now it breathes. That's padding, margin, and line-height working together.

## ✅ Recap

- Every element is a box: **content → padding → border → margin** (inside out).
- Add `*{box-sizing:border-box}` once so `width` includes padding & border.
- Spacing shorthand is clockwise **T R B L**; vertical margins **collapse** to the larger value.
- Tune type with `font-family` (with fallbacks), `font-size` in `rem`, `font-weight`, and a comfortable unitless `line-height`.
- Add a Google Font with a `<link>` + `font-family`, always keeping a system fallback.

**Next:** open `assignment.html` and tune spacing + typography across your whole site.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
