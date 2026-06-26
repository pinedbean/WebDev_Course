*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.1 — Lab: Five Small Problems

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Write a single file, `basics.js`, that solves **five small problems** using variables, operators, template literals, conditionals, and loops. You'll run it in the browser and watch the answers appear in the Console.

## Before you start

- Make a folder for this chunk, e.g. `~/Desktop/webdev-course/module-03-javascript/js-basics/`.
- Open it in VS Code (`code .`).
- Create two files: `index.html` and `basics.js`.
- In `index.html`, add a minimal page that loads your script. The whole point is to run `basics.js`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>JS Basics</title>
</head>
<body>
  <h1>Open the Console (look in DevTools)</h1>
  <script src="basics.js"></script>
</body>
</html>
```

Open `index.html` in your browser, then open the Console (macOS Chrome: `⌥`+`⌘`+`J`). Every `console.log(...)` in `basics.js` will print there. Edit, save, reload the page to re-run.

> **⚠️ Try it yourself first**
>
> Build each problem from memory and the lecture. Only open
>
> solution.html
>
> when you're stuck or to compare at the end.

## Tasks

### 1 Greeting with a template literal

Declare a `const name` (your name) and a `const age` (a number). Use a template literal to `console.log` a sentence like: *"Hi, I'm Jane and I'm 28 years old."*

### 2 Temperature converter

Declare `const celsius = 25;`. Compute Fahrenheit with the formula `C × 9/5 + 32`, store it in a variable, and log a sentence like *"25°C is 77°F."* Then change `celsius` to another value and reload to confirm it updates.

### 3 Even or odd

Declare a `const number`. Using `if`/`else` and the remainder operator `%`, log whether it is *"even"* or *"odd"*.

### 4 FizzBuzz (1 to 20)

Use a `for` loop from 1 to 20. Log *"Fizz"* for multiples of 3, *"Buzz"* for multiples of 5, *"FizzBuzz"* for multiples of both, otherwise the number itself.

### 5 Sum & simple "calculator" logic

Declare two numbers `a` and `b`. Log their sum, difference, product, and quotient — each as a labeled sentence using a template literal (e.g. *"7 + 3 = 10"*). Then use a loop to log the running total of all numbers from 1 to `b`.

## ✅ Deliverable — acceptance checklist

- `basics.js` exists and is loaded by `index.html`.
- Opening the page and the Console shows output from all five problems, with no red errors.
- Problem 1 uses a **template literal** (backticks + `${...}`).
- Problem 2 correctly converts °C to °F.
- Problem 3 reports even/odd using `%` and `if`/`else`.
- Problem 4 prints FizzBuzz for 1–20 with the combined case handled first.
- Problem 5 prints the four arithmetic results and a running total via a loop.
- You used `const` by default and `let` only where a value changes.

## 🚀 Stretch goals (optional)

- Make problem 2 round Fahrenheit to one decimal with `Math.round(f * 10) / 10`.
- Rewrite problem 3 using the ternary operator instead of `if`/`else`.
- Use `prompt("Enter a number")` to read a value from the user, then `Number(...)` to convert the text to a number before using it.
- Add a "countdown" with a `while` loop that logs from 5 down to 1, then `"Lift off! 🚀"`.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
