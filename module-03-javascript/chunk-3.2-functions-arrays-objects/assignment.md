*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.2 — Lab: Process a Product Catalog

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Write `catalog.js`, a script that takes an **array of product objects** and transforms it: filtering, mapping, sorting, and summarizing with functions and array methods. All output goes to the Console.

## Before you start

- Make a folder, e.g. `~/Desktop/webdev-course/module-03-javascript/catalog/`.
- Create `index.html` (loading `catalog.js` like in Chunk 3.1) and `catalog.js`.
- Start `catalog.js` with this dataset — copy it exactly:

```javascript
const products = [
  { name: "Keyboard",    price: 49.99, category: "accessories", inStock: true  },
  { name: "Mouse",       price: 19.99, category: "accessories", inStock: false },
  { name: "Monitor",     price: 199.0, category: "displays",    inStock: true  },
  { name: "Webcam",      price: 79.0,  category: "accessories", inStock: true  },
  { name: "Laptop Stand",price: 35.5,  category: "accessories", inStock: true  },
  { name: "USB-C Hub",   price: 29.99, category: "accessories", inStock: false },
  { name: "4K Monitor",  price: 349.0, category: "displays",    inStock: true  },
];
```

> **⚠️ Try it yourself first**
>
> Reach for
>
> map
>
> ,
>
> filter
>
> ,
>
> reduce
>
> , and
>
> sort
>
> from the lecture. Only open
>
> solution.html
>
> when stuck.

## Tasks

### 1 List all product names

Use `map` to build an array of just the names, and log it.

### 2 Only what's in stock

Use `filter` to get the in-stock products. Log how many there are (use `.length`) and their names.

### 3 Apply a discount (a reusable function)

Write a function `applyDiscount(product, percent)` that **returns a new object** with the price reduced by `percent`%. Use it with `map` to produce a "10% off" version of the in-stock list, then log the new names + prices.

> **💡 Build a new object**
>
> Use the spread operator to copy then override:
>
> { ...product, price: newPrice }
>
> . This keeps the original untouched.

### 4 Sort by price

Produce a copy of `products` sorted from cheapest to most expensive, and log the names in that order. (Remember to copy with `[...products]` before `sort`.)

### 5 Total & average value of in-stock items

Use `reduce` to total the prices of in-stock products. Then compute and log the average (total ÷ count), rounded to 2 decimals.

### 6 Find the most expensive product

Using `reduce` (or a loop), find and log the single most expensive product's name and price. Use **destructuring** to pull `name` and `price` out when you log it.

## ✅ Deliverable — acceptance checklist

- `catalog.js` runs from `index.html` with no Console errors.
- Task 1 logs all 7 names via `map`.
- Task 2 logs the in-stock count (5) and their names via `filter`.
- `applyDiscount` is a function that **returns a new object** and does not mutate the original.
- Task 4 logs names sorted by ascending price, original array unchanged.
- Task 5 logs the correct total and a 2-decimal average via `reduce`.
- Task 6 logs the most expensive product, using destructuring.
- You used arrow functions for your array-method callbacks.

## 🚀 Stretch goals (optional)

- Group products by `category` into an object like `{ accessories: [...], displays: [...] }` using `reduce`.
- Write `formatPrice(n)` that returns `"$49.99"` and use it everywhere you print a price.
- Chain methods into a single expression: in-stock → sorted by price → names.
- Add a `search(term)` function that returns products whose name includes `term` (case-insensitive with `.toLowerCase()`).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
