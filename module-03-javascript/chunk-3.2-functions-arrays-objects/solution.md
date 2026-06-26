*Full-Stack Web Dev · Module 3 — JavaScript Core*

# Chunk 3.2 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Each step shows the code and the expected Console output. The complete `catalog.js` is at the bottom. Compare it with yours — there are many valid ways to write these.

### 1 List all product names

```javascript
const names = products.map(p => p.name);
console.log(names);
```

**Expected:** `["Keyboard", "Mouse", "Monitor", "Webcam", "Laptop Stand", "USB-C Hub", "4K Monitor"]`

### 2 Only what's in stock

```javascript
const available = products.filter(p => p.inStock);
console.log(`In stock: ${available.length}`);
console.log(available.map(p => p.name));
```

**Expected:** `In stock: 5` then `["Keyboard", "Monitor", "Webcam", "Laptop Stand", "4K Monitor"]`

### 3 Apply a discount

```javascript
function applyDiscount(product, percent) {
  const newPrice = product.price * (1 - percent / 100);
  return { ...product, price: Math.round(newPrice * 100) / 100 };
}

const discounted = available.map(p => applyDiscount(p, 10));
console.log(discounted.map(p => `${p.name}: $${p.price}`));
```

**Expected:** `["Keyboard: $44.99", "Monitor: $179.1", "Webcam: $71.1", "Laptop Stand: $31.95", "4K Monitor: $314.1"]`

> **📝 Why `{ ...product, price: ... }`**
>
> The spread copies every existing property, then
>
> price:
>
> overrides just that one. The original
>
> product
>
> object is never changed — a habit that prevents whole categories of bugs.

### 4 Sort by price

```javascript
const byPrice = [...products].sort((a, b) => a.price - b.price);
console.log(byPrice.map(p => `${p.name} ($${p.price})`));
```

**Expected (cheapest first):** `Mouse, USB-C Hub, Laptop Stand, Keyboard, Webcam, Monitor, 4K Monitor`

> **⚠️ Copy before you sort**
>
> sort
>
> reorders the array
>
> in place
>
> . Without
>
> [...products]
>
> you'd permanently scramble your original data.

### 5 Total & average of in-stock items

```javascript
const total = available.reduce((sum, p) => sum + p.price, 0);
const average = total / available.length;
console.log(`Total: $${total.toFixed(2)}`);
console.log(`Average: $${average.toFixed(2)}`);
```

**Expected:** `Total: $712.49` and `Average: $142.50`

> **💡 toFixed**
>
> number.toFixed(2)
>
> returns a string with exactly two decimals — perfect for money. Note it rounds, so use it for display, not for further math.

### 6 Most expensive product

```javascript
const priciest = products.reduce((max, p) =>
  p.price > max.price ? p : max
);
const { name, price } = priciest;
console.log(`Most expensive: ${name} at $${price}`);
```

**Expected:** `Most expensive: 4K Monitor at $349`

> **📝 reduce without a start value**
>
> Here we omit the second argument, so
>
> reduce
>
> uses the first item as the initial
>
> max
>
> and starts comparing from the second. The destructuring
>
> const { name, price } = priciest
>
> unpacks both properties at once.

## 📄 Complete `catalog.js`

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

// 1) All names
const names = products.map(p => p.name);
console.log("All names:", names);

// 2) In stock
const available = products.filter(p => p.inStock);
console.log(`In stock: ${available.length}`);
console.log(available.map(p => p.name));

// 3) Apply a discount (returns a NEW object)
function applyDiscount(product, percent) {
  const newPrice = product.price * (1 - percent / 100);
  return { ...product, price: Math.round(newPrice * 100) / 100 };
}
const discounted = available.map(p => applyDiscount(p, 10));
console.log("10% off:", discounted.map(p => `${p.name}: $${p.price}`));

// 4) Sort by price (copy first!)
const byPrice = [...products].sort((a, b) => a.price - b.price);
console.log("By price:", byPrice.map(p => `${p.name} ($${p.price})`));

// 5) Total & average of in-stock
const total = available.reduce((sum, p) => sum + p.price, 0);
const average = total / available.length;
console.log(`Total: $${total.toFixed(2)}`);
console.log(`Average: $${average.toFixed(2)}`);

// 6) Most expensive
const priciest = products.reduce((max, p) => (p.price > max.price ? p : max));
const { name, price } = priciest;
console.log(`Most expensive: ${name} at $${price}`);
```

## 🎉 You're done

You modeled real-world data as an array of objects and reshaped it with functions and `map`/`filter`/`reduce` — the exact pattern you'll use to render lists in the DOM and, later, in React.

**Up next → Chunk 3.3: The DOM & Events** — where data finally meets the screen. You'll start building the interactive **to-do app** that becomes this module's running project.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
