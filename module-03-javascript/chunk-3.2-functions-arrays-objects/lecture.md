*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.2 — Functions, Arrays & Objects

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Writing reusable **functions** — declarations vs arrow functions, parameters and return values.
- **Arrays**: storing lists and looping with `forEach`.
- The big three transforms: `map`, `filter`, `reduce`.
- **Objects**: modeling a thing with named properties, plus **destructuring**.

In the lab you'll process an array of product objects — filtering, sorting, and summarizing it.

## 1. Functions: packaging logic

A **function** is a reusable block of code with a name. You define it once and *call* it as many times as you like, optionally passing in **arguments** and getting back a **return value**.

```javascript
function greet(name) {
  return `Hello, ${name}!`;
}

const message = greet("Jane");   // call it
console.log(message);            // "Hello, Jane!"
console.log(greet("Sam"));       // "Hello, Sam!"
```

- `name` is a **parameter** — a placeholder for whatever you pass in.
- `"Jane"` is the **argument** — the actual value for this call.
- `return` hands a value back to whoever called the function. Without `return`, a function gives back `undefined`.

> **⚠️ return vs console.log**
>
> They are not the same!
>
> console.log
>
> just
>
> prints
>
> to the console.
>
> return
>
> actually
>
> produces a value
>
> you can store and reuse. A function that only logs can't be combined with other code.

## 2. Arrow functions

Arrow functions are a shorter syntax for writing functions, introduced in modern JavaScript. They're everywhere in React and in the array methods below, so get comfortable with them:

```javascript
// Function declaration
function add(a, b) {
  return a + b;
}

// Arrow function — same thing
const add = (a, b) => {
  return a + b;
};

// If the body is a single return, drop the braces and the word "return":
const add = (a, b) => a + b;

// One parameter? Parentheses are optional:
const double = n => n * 2;
```

| Form | When to use |
| --- | --- |
| `function name() {}` | Top-level named helpers; fine anywhere. |
| `const f = () => {}` | Short callbacks, especially passed into array methods. |

> **📝 Implicit return**
>
> n => n * 2
>
> automatically returns
>
> n * 2
>
> — no braces, no
>
> return
>
> keyword. The moment you add
>
> { }
>
> , you must write
>
> return
>
> yourself.

## 3. Arrays

An **array** is an ordered list of values, written with square brackets. Items are numbered from **0**:

```javascript
const fruits = ["apple", "banana", "cherry"];

fruits[0];        // "apple"   (first item)
fruits[2];        // "cherry"
fruits.length;    // 3
fruits.push("date");     // add to the end → length 4
fruits.includes("banana"); // true
```

### Looping with `forEach`

To do something with every item, `forEach` runs a function once per element:

```
fruits.forEach((fruit, index) => {
  console.log(`${index}: ${fruit}`);
});
// 0: apple
// 1: banana
// 2: cherry
```

The function you pass in receives each item (and optionally its index). `forEach` is for *side effects* like logging — it doesn't build a new array. For that, you want `map`.

## 4. The big three: map, filter, reduce

These three methods are the heart of working with data in JavaScript. Each takes a function and returns something new — they never modify the original array.

### `map` — transform every item

Returns a **new array** of the same length, with each item passed through your function:

```javascript
const numbers = [1, 2, 3, 4];
const doubled = numbers.map(n => n * 2);
console.log(doubled);   // [2, 4, 6, 8]
console.log(numbers);   // [1, 2, 3, 4]  ← original untouched
```

### `filter` — keep some items

Returns a **new, possibly shorter array** containing only items for which your function returns `true`:

```javascript
const numbers = [1, 2, 3, 4, 5, 6];
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens);     // [2, 4, 6]
```

### `reduce` — boil a list down to one value

Combines all items into a single result (a sum, a max, a joined string). It carries an **accumulator** from item to item:

```javascript
const numbers = [10, 20, 30];
const total = numbers.reduce((sum, n) => sum + n, 0);
//                            ↑acc  ↑item        ↑start value
console.log(total);     // 60
```

Read it as: start `sum` at `0`; for each `n`, the new `sum` is `sum + n`. After the last item, `reduce` returns the final `sum`.

> **💡 They chain**
>
> Because
>
> map
>
> and
>
> filter
>
> return arrays, you can chain them:
>
> products.filter(p => p.inStock).map(p => p.name)
>
> gives the names of in-stock products in one readable line.

## 5. Objects

An **object** groups related data under named **properties** (key: value pairs). Where an array is a list, an object is a labeled record of one "thing":

```yaml
const product = {
  name: "Keyboard",
  price: 49.99,
  inStock: true,
};

product.name;        // "Keyboard"   (dot notation)
product["price"];    // 49.99        (bracket notation)
product.price = 39.99;   // update a property
product.brand = "Acme";  // add a new property
```

Objects can hold anything as values — including arrays and other objects. A list of products is just an **array of objects**, which is how almost all real app data looks:

```javascript
const products = [
  { name: "Keyboard", price: 49.99, inStock: true },
  { name: "Mouse",    price: 19.99, inStock: false },
  { name: "Monitor",  price: 199.0, inStock: true },
];
```

## 6. Destructuring

**Destructuring** pulls properties out of an object (or items out of an array) into their own variables — less typing, clearer code:

```javascript
const product = { name: "Keyboard", price: 49.99 };

// Without destructuring:
const name = product.name;
const price = product.price;

// With destructuring — same result, one line:
const { name, price } = product;
console.log(name, price);   // "Keyboard" 49.99
```

It's especially handy in function parameters, so you can name exactly what you need:

```javascript
function label({ name, price }) {
  return `${name}: $${price}`;
}
label(product);   // "Keyboard: $49.99"
```

Arrays destructure by position:

```
const [first, second] = ["gold", "silver", "bronze"];
console.log(first);   // "gold"
console.log(second);  // "silver"
```

## 7. Worked example: processing products

Combining everything — filter the in-stock items, sort them by price, and total their value:

```javascript
const products = [
  { name: "Keyboard", price: 49.99, inStock: true },
  { name: "Mouse",    price: 19.99, inStock: false },
  { name: "Monitor",  price: 199.0, inStock: true },
  { name: "Webcam",   price: 79.0,  inStock: true },
];

// 1) keep only in-stock
const available = products.filter(p => p.inStock);

// 2) sort by price, cheapest first (a copy, sorted in place)
const sorted = [...available].sort((a, b) => a.price - b.price);

// 3) total price of available products
const total = available.reduce((sum, p) => sum + p.price, 0);

console.log(sorted.map(p => p.name));   // ["Keyboard", "Webcam", "Monitor"]
console.log(`Total in stock: $${total}`); // "Total in stock: $327.99"
```

> **📝 The spread `...`**
>
> sort
>
> changes the array it's called on.
>
> [...available]
>
> makes a fresh copy first (the
>
> spread
>
> operator copies all items into a new array), so the original order is preserved. The sorter
>
> (a, b) => a.price - b.price
>
> returns a negative number when
>
> a
>
> should come first.

## ✅ Recap

- Functions package logic; `return` hands back a value. Arrow functions `=>` are the short form.
- Arrays are ordered lists; `forEach` loops for side effects.
- `map` transforms, `filter` selects, `reduce` summarizes — all return new values, none mutate.
- Objects model one thing with named properties; an array of objects is your typical dataset.
- Destructuring unpacks properties/items into variables in one line.

**Next:** open `assignment.html` and transform a catalog of products.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
