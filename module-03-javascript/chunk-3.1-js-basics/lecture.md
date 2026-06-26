*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.1 — JavaScript Basics

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What JavaScript is and where it runs (the browser console).
- Declaring data with `let` and `const`, and the basic **types**.
- **Operators** (math, comparison, logic) and **template literals**.
- Making decisions with `if`/`else` and repeating work with **loops**.

In the lab you'll write a `basics.js` file that solves 5 small problems — a temperature converter, FizzBuzz, and more.

## 1. What is JavaScript?

You've built the **skeleton** (HTML) and the **skin** (CSS). JavaScript is the **muscles** — it makes pages *do* things: respond to clicks, validate forms, load data, update the screen without a reload.

Unlike HTML and CSS, JavaScript is a real **programming language**: it has variables, logic, math, and loops. Every browser ships with a JavaScript engine built in, so you don't install anything to start.

| Language | Role | Module |
| --- | --- | --- |
| HTML | Structure & content | Module 1 |
| CSS | Styling & layout | Module 2 |
| **JavaScript** | Behavior & logic | **Module 3 (here)** |

## 2. Where to run it: the Console

The fastest place to experiment is the browser's **DevTools Console**. Open any page, then:

- **macOS:** press `⌥ Option` + `⌘ Cmd` + `J` (Chrome) to jump straight to the Console.
- **Windows/Linux:** press `Ctrl` + `Shift` + `J`.
- Or right-click the page → *Inspect* → click the **Console** tab.

Type an expression, press `Enter`, and the console prints the result. `console.log(...)` prints whatever you pass it:

```
console.log("Hello, JavaScript!");
console.log(2 + 2);   // 4
```

> **💡 Why a separate file?**
>
> The console is great for quick tests, but real code lives in a
>
> .js
>
> file. You can run a file by linking it from an HTML page with
>
> <script src="basics.js"></script>
>
> just before the closing
>
> </body>
>
> tag — that's exactly what the lab does.

## 3. Variables: `let` and `const`

A **variable** is a named box that holds a value. You create one with `let` or `const`:

```javascript
let score = 0;          // can be reassigned later
const name = "Jane";    // a constant — cannot be reassigned

score = 10;             // ✅ allowed
// name = "Bob";        // ❌ TypeError: Assignment to constant variable
```

| Keyword | Reassignable? | Use it when… |
| --- | --- | --- |
| `const` | No | The value won't be reassigned (your default choice). |
| `let` | Yes | The value will change (a counter, a running total). |
| `var` | Yes | Old, pre-2015 style. **Avoid it** — it has confusing scope rules. |

> **📝 Rule of thumb**
>
> Reach for
>
> const
>
> first. Only switch to
>
> let
>
> when you actually need to reassign the variable. This makes your intent obvious and prevents accidental changes.

## 4. Data types

Every value has a **type**. The ones you'll use constantly:

| Type | Example | What it is |
| --- | --- | --- |
| `string` | `"hello"`, `'hi'` | Text, in quotes. |
| `number` | `42`, `3.14`, `-7` | Any number (no separate int/float). |
| `boolean` | `true`, `false` | Yes/no, on/off. |
| `undefined` | `undefined` | A variable with no value yet. |
| `null` | `null` | Intentionally "empty". |

JavaScript figures out the type for you. You can check it with `typeof`:

```
typeof "hello";   // "string"
typeof 42;        // "number"
typeof true;      // "boolean"
typeof undefined; // "undefined"
```

Arrays and objects are types too — they hold collections of values. You'll meet them properly in Chunk 3.2.

## 5. Operators

### Arithmetic

```
10 + 3   // 13   addition
10 - 3   // 7    subtraction
10 * 3   // 30   multiplication
10 / 3   // 3.333…   division
10 % 3   // 1    remainder (the "modulo" — super useful!)
2 ** 3   // 8    exponent (2 to the power of 3)
```

The **remainder** operator `%` tells you what's left over after dividing. `n % 2 === 0` is the classic test for "is n even?".

### Comparison (always return a boolean)

```
5 > 3      // true
5 < 3      // false
5 >= 5     // true
5 <= 4     // false
5 === 5    // true   (strict equal: same value AND same type)
5 === "5"  // false  (number vs string)
5 !== 6    // true   (not equal)
```

> **⚠️ Use === not ==**
>
> Always prefer
>
> ===
>
> (strict equality) over
>
> ==
>
> . The double-equals version does sneaky type conversions:
>
> 0 == ""
>
> is
>
> true
>
> and
>
> 1 == "1"
>
> is
>
> true
>
> , which causes bugs. Triple-equals compares value
>
> and
>
> type, with no surprises.

### Logical

```
true && false   // false   AND: both must be true
true || false   // true    OR: at least one true
!true           // false   NOT: flips it
```

## 6. Template literals

To build strings from variables, use **backticks** (```) and `${...}` placeholders. This is far cleaner than gluing strings with `+`:

```javascript
const name = "Jane";
const age = 28;

// Old way — clunky:
console.log("Hi " + name + ", you are " + age + ".");

// Template literal — clean:
console.log(`Hi ${name}, you are ${age}.`);
// → "Hi Jane, you are 28."
```

Anything inside `${ }` is evaluated as JavaScript, so you can do math or call functions there too: ``Next year you'll be ${age + 1}.``. Backtick strings can also span multiple lines.

## 7. Making decisions: `if` / `else`

Run code only when a condition is true:

```javascript
const temp = 32;

if (temp >= 30) {
  console.log("It's hot 🔥");
} else if (temp >= 20) {
  console.log("Nice weather 🙂");
} else {
  console.log("Bring a jacket 🧥");
}
```

The condition in the parentheses must evaluate to `true` or `false`. JavaScript also treats some values as "truthy" or "falsy" — `0`, `""`, `null`, and `undefined` are **falsy**; almost everything else is **truthy**.

### Ternary — a compact if/else

```javascript
const label = temp >= 30 ? "hot" : "not hot";
// condition ? valueIfTrue : valueIfFalse
```

## 8. Loops

Loops repeat work. The classic `for` loop counts with a start, a condition, and a step:

```javascript
for (let i = 1; i <= 5; i++) {
  console.log(i);
}
// prints 1, 2, 3, 4, 5
```

Read it as: *start* `i` at 1; *keep going while* `i <= 5`; *after each pass* do `i++` (add 1). `i++` is shorthand for `i = i + 1`.

### The `while` loop

Repeats as long as a condition stays true — use it when you don't know the count up front:

```javascript
let count = 3;
while (count > 0) {
  console.log(count);
  count--;        // subtract 1 each time
}
// prints 3, 2, 1
```

> **⚠️ Infinite loops**
>
> A loop whose condition never becomes false runs forever and freezes the tab. Make sure something inside the loop moves toward the exit (here,
>
> count--
>
> ). If you ever freeze a page, close that tab.

## 9. Worked example: FizzBuzz

The famous beginner puzzle: print 1–15, but for multiples of 3 print "Fizz", multiples of 5 print "Buzz", and multiples of both print "FizzBuzz". It combines loops, conditionals, and the remainder operator:

```javascript
for (let i = 1; i <= 15; i++) {
  if (i % 3 === 0 && i % 5 === 0) {
    console.log("FizzBuzz");
  } else if (i % 3 === 0) {
    console.log("Fizz");
  } else if (i % 5 === 0) {
    console.log("Buzz");
  } else {
    console.log(i);
  }
}
```

Notice the order: we test "both" **first**, because 15 is divisible by 3 and 5 — if we checked "divisible by 3" first, we'd print "Fizz" and never reach the combined case.

## ✅ Recap

- JavaScript adds **behavior**; test it fast in the **Console**, ship it in a `.js` file.
- Use `const` by default, `let` when a value changes; avoid `var`.
- Core types: `string`, `number`, `boolean`, `undefined`, `null`.
- Prefer `===`; remember `%` (remainder) for even/odd and divisibility tests.
- Build strings with template literals ``${...}``.
- Branch with `if`/`else`; repeat with `for` and `while`.

**Next:** open `assignment.html` and write your `basics.js` solving 5 small problems.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
