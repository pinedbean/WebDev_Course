*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Work through each problem and compare with your own. Each step shows the code, the **expected Console output**, and notes on common mistakes. The complete `basics.js` is at the bottom.

### 1 Greeting with a template literal

```javascript
const name = "Jane";
const age = 28;
console.log(`Hi, I'm ${name} and I'm ${age} years old.`);
```

**Expected output:** `Hi, I'm Jane and I'm 28 years old.`

> **⚠️ Common mistake**
>
> Using straight quotes
>
> "..."
>
> instead of backticks
>
> `...`
>
> . Only backticks enable
>
> ${...}
>
> . The backtick key is above
>
> Tab
>
> on most keyboards.

### 2 Temperature converter

```javascript
const celsius = 25;
const fahrenheit = celsius * 9 / 5 + 32;
console.log(`${celsius}°C is ${fahrenheit}°F.`);
```

**Expected output:** `25°C is 77°F.` Change `celsius` to `0` and reload → `0°C is 32°F.`

> **📝 Why it works**
>
> Multiplication and division happen before addition, so
>
> celsius * 9 / 5 + 32
>
> is read as
>
> ((celsius * 9) / 5) + 32
>
> . When in doubt, add parentheses to make the order explicit.

### 3 Even or odd

```javascript
const number = 7;
if (number % 2 === 0) {
  console.log(`${number} is even`);
} else {
  console.log(`${number} is odd`);
}
```

**Expected output:** `7 is odd`. A number is even when dividing by 2 leaves no remainder, i.e. `number % 2 === 0`.

### 4 FizzBuzz (1 to 20)

```javascript
for (let i = 1; i <= 20; i++) {
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

**Expected output (first lines):** `1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz, 11, Fizz, 13, 14, FizzBuzz, …`

> **⚠️ Order matters**
>
> Test "divisible by both"
>
> first
>
> . If you check
>
> i % 3 === 0
>
> before the combined case, 15 prints "Fizz" and never reaches "FizzBuzz".

### 5 Sum & calculator logic

```javascript
const a = 7;
const b = 3;
console.log(`${a} + ${b} = ${a + b}`);
console.log(`${a} - ${b} = ${a - b}`);
console.log(`${a} * ${b} = ${a * b}`);
console.log(`${a} / ${b} = ${a / b}`);

// Running total from 1 to b
let total = 0;
for (let i = 1; i <= b; i++) {
  total = total + i;          // or: total += i;
  console.log(`running total after ${i}: ${total}`);
}
```

**Expected output:**

```
7 + 3 = 10
7 - 3 = 4
7 * 3 = 21
7 / 3 = 2.3333333333333335
running total after 1: 1
running total after 2: 3
running total after 3: 6
```

> **💡 Shorthand**
>
> total += i
>
> means
>
> total = total + i
>
> . There's also
>
> -=
>
> ,
>
> *=
>
> , and
>
> /=
>
> .

## 📄 Complete `basics.js`

```javascript
// ===== Problem 1: Greeting =====
const name = "Jane";
const age = 28;
console.log(`Hi, I'm ${name} and I'm ${age} years old.`);

// ===== Problem 2: Temperature converter =====
const celsius = 25;
const fahrenheit = celsius * 9 / 5 + 32;
console.log(`${celsius}°C is ${fahrenheit}°F.`);

// ===== Problem 3: Even or odd =====
const number = 7;
if (number % 2 === 0) {
  console.log(`${number} is even`);
} else {
  console.log(`${number} is odd`);
}

// ===== Problem 4: FizzBuzz =====
for (let i = 1; i <= 20; i++) {
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

// ===== Problem 5: Calculator + running total =====
const a = 7;
const b = 3;
console.log(`${a} + ${b} = ${a + b}`);
console.log(`${a} - ${b} = ${a - b}`);
console.log(`${a} * ${b} = ${a * b}`);
console.log(`${a} / ${b} = ${a / b}`);

let total = 0;
for (let i = 1; i <= b; i++) {
  total += i;
  console.log(`running total after ${i}: ${total}`);
}
```

## 🎉 You're done

You wrote real JavaScript: variables, types, operators, template literals, conditionals, and loops. These are the building blocks of *every* program you'll write from here on.

**Up next → Chunk 3.2: Functions, Arrays & Objects** — where you'll package logic into reusable functions and start transforming lists of data, the way real apps handle their content.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
