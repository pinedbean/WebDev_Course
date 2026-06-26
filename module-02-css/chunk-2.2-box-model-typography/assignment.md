*Full-Stack Web Dev · Module 2 — CSS & Layout*

# Chunk 2.2 — Lab: Spacing & Typography Polish

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Continue growing `styles.css`. Add the box-sizing reset, give your sections real padding/borders so they read as "cards", fix the vertical rhythm, and add a Google Font for headings and body. The site should go from "plain but consistent" to "this looks designed".

## Before you start

- You should already have `styles.css` from Chunk 2.1 linked to all three pages.
- Pick two fonts at [fonts.google.com](https://fonts.google.com) — one for headings, one for body (or one font in two weights). Suggestions: *Poppins* + *Inter*, or just *Inter* at 400/600/700.
- Keep a browser tab open on your site and refresh after each change.

> **⚠️ Try it yourself first**
>
> Reach for the lecture, not the solution. Spacing is something you tune by eye — experiment with values until it looks right to you.

## Tasks

### 1 Add the box-sizing reset

At the very top of `styles.css`, add the universal reset so all your width math behaves:

```
*, *::before, *::after { box-sizing: border-box; }
```

### 2 Add a Google Font

In the `<head>` of all three pages (above your `styles.css` link), paste the `<link>` tags Google Fonts gave you. Then set `font-family` in your CSS for `body` and headings, keeping a system fallback after your chosen font.

> **💡 Verify it loaded**
>
> Refresh and look closely — the letterforms should change. If they don't, recheck the
>
> <link>
>
> URL and that the name in
>
> font-family
>
> matches Google's exactly (in quotes).

### 3 Set a comfortable body rhythm

On `body`, set `line-height` to about `1.6`–`1.7` and confirm your `max-width` + side `padding` from last chunk are still there. Body text should feel airy, not cramped.

### 4 Turn sections into cards

Style every `<section>` with a white background, a subtle border, rounded corners, generous `padding`, and a `margin-bottom` to separate them. Your About page (with its multiple sections) should now look like a stack of neat cards.

```
section {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px 28px;
  margin-bottom: 20px;
}
```

### 5 Fix heading spacing

Give headings deliberate spacing — for example a tighter `line-height` on `h1`/`h2`, and a little `margin-top` on `h2` so sections don't crowd their titles. Tune by eye.

### 6 Style the header & footer

Add padding to the `<header>` and `<footer>`. Make the footer text muted (a grey from your palette) and a bit smaller. Add spacing between the nav links if they feel tight.

### 7 Polish one detail: the image or table

Pick one: give the profile `<img>` on the About page a `border-radius` and a `max-width: 100%` so it never overflows; OR style the experience `<table>` with `border-collapse: collapse` and padding on `th, td`. Either proves you can target a specific element cleanly.

### 8 Review the whole site

Click through all three pages. Check: consistent font, even spacing between cards, comfortable line-height, nothing cramped or touching the edges. Adjust until you're happy.

## ✅ Deliverable — acceptance checklist

- The `box-sizing: border-box` reset is at the top of `styles.css`.
- A Google Font is linked on all pages and applied via `font-family` (with a system fallback).
- Body has a comfortable `line-height` (~1.6) and stays a centered, capped-width column.
- Every `<section>` reads as a card (background, border, radius, padding, margin).
- Headings have deliberate spacing — no cramped titles.
- Header and footer are padded; footer text is muted and smaller.
- One polished detail: rounded responsive image OR a cleanly styled table.
- All three pages look consistent and intentional.

## 🚀 Stretch goals (optional)

- Add a `box-shadow` to your section cards for subtle depth: `box-shadow: 0 4px 14px rgba(2,6,23,.06);`
- Create a `.lead` class for the intro paragraph on the Home page — larger, muted, maybe centered.
- Use `rem` consistently for all font sizes and major spacing.
- Add `letter-spacing` to your headings or uppercase a small label.
- Find and fix any margin-collapse surprise (spacing that looks "half" what you set).
- Commit: `git add . && git commit -m "Box model + typography polish"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
