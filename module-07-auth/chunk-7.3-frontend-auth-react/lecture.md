*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.3 — Frontend Auth Flow in React

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The end-to-end **frontend auth flow**: login → store token → attach it → protect pages → logout.
- Where to **store the token** (localStorage vs memory vs cookies) and the honest trade-offs.
- Calling the FastAPI login/register endpoints from React (including the form-encoded token request).
- Attaching the `Authorization: Bearer` header to every API call with a small helper.
- Building an **auth context** (`useAuth`), **protected routes** with redirects, and **logout**.

This reuses everything from Module 4 (components, state, Router, Context). In the lab you'll build login/register pages and a protected dashboard wired to the Tasks API from 7.2.

## 1. The big picture

Your backend already issues JWTs and guards routes. The frontend's job is to manage the token's life cycle in the browser:

>

Everything below is just the React plumbing for those four moments.

## 2. Where do we store the token?

This is the most important security decision on the frontend, and there's no perfect answer — only trade-offs. Be honest about them.

| Option | Survives refresh? | Main risk |
| --- | --- | --- |
| `localStorage` | Yes | Readable by **any JavaScript** on the page → vulnerable to **XSS** (a malicious script can steal it). |
| In-memory (React state only) | No (lost on reload) | Safer from XSS exfiltration, but the user is logged out every refresh. |
| `httpOnly` cookie | Yes | Invisible to JS (good vs XSS), but introduces **CSRF** concerns and needs backend cookie handling. |

> **⚠️ The honest truth about localStorage**
>
> Tutorials (and this course) use
>
> localStorage
>
> because it's simple and survives refresh. But understand the cost:
>
> if an attacker can run JavaScript on your page (XSS), they can read the token from localStorage and impersonate the user.
>
> The real defense is preventing XSS in the first place (React escapes output by default — never use
>
> dangerouslySetInnerHTML
>
> with untrusted data) and keeping token lifetimes short. Production apps that need maximum safety often move to
>
> httpOnly
>
> cookies + CSRF protection. We cover XSS/CSRF properly in 7.4.

We'll use `localStorage` with a clear understanding of the trade-off, plus short-lived tokens from 7.2.

## 3. A tiny API helper

Centralize fetching so the token logic lives in one place. This helper reads the token from storage and attaches the header automatically.

```javascript
// src/api.js
const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export function getToken() {
  return localStorage.getItem("token");
}

export async function apiFetch(path, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, { ...options, headers });
  if (res.status === 401) {
    // token missing/expired — force a clean logout
    localStorage.removeItem("token");
    throw new Error("Unauthorized");
  }
  if (!res.ok) throw new Error((await res.json()).detail || "Request failed");
  return res.status === 204 ? null : res.json();
}
```

> **📝 Vite env vars**
>
> In Vite, only variables prefixed
>
> VITE_
>
> are exposed to the browser, read via
>
> import.meta.env.VITE_API_URL
>
> . Put
>
> VITE_API_URL=http://localhost:8000
>
> in a
>
> .env
>
> file (you learned this in Chunk 4.7). Never put secrets in frontend env vars — they ship to the browser.

## 4. Calling login & register

Remember from 7.2: the **login** endpoint expects `application/x-www-form-urlencoded` (OAuth2 password flow), while **register** takes JSON. Two different content types.

```javascript
// src/api.js  (auth calls)
const BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function loginRequest(email, password) {
  // OAuth2 form: "username" + "password", form-encoded
  const body = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) throw new Error("Invalid email or password");
  return res.json();                 // { access_token, token_type }
}

export async function registerRequest(email, password) {
  const res = await fetch(`${BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Registration failed");
  }
  return res.json();                 // UserOut
}
```

The `URLSearchParams` object makes the browser send form-encoded data automatically — this is the single most common stumbling block when wiring a React frontend to an OAuth2 token endpoint.

## 5. The auth context

Many components need to know "am I logged in? who am I?" Threading that through props is painful, so we use **Context** (Chunk 4.6). The provider owns the token + user and exposes `login`, `logout`, and a `useAuth` hook.

```python
// src/context/AuthContext.jsx
import { createContext, useContext, useEffect, useState } from "react";
import { loginRequest, apiFetch } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On load (or when the token changes), fetch the current user.
  useEffect(() => {
    if (!token) { setUser(null); setLoading(false); return; }
    apiFetch("/auth/me")
      .then(setUser)
      .catch(() => { setToken(null); localStorage.removeItem("token"); })
      .finally(() => setLoading(false));
  }, [token]);

  async function login(email, password) {
    const { access_token } = await loginRequest(email, password);
    localStorage.setItem("token", access_token);
    setToken(access_token);          // triggers the effect -> loads /auth/me
  }

  function logout() {
    localStorage.removeItem("token");
    setToken(null);
    setUser(null);
  }

  const value = { user, token, loading, login, logout, isAuthenticated: !!token };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
  return ctx;
}
```

Wrap your app once (inside the Router) so every page can call `useAuth()`:

```python
// src/main.jsx
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

## 6. Protected routes & redirects

A protected route checks auth state and either renders the page or redirects to login. With React Router we wrap protected pages in a small guard component that uses `<Navigate>`.

```python
// src/components/ProtectedRoute.jsx
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) return <p>Loading…</p>;          // wait for /auth/me to resolve
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}
```

Use it in your routes:

```python
// src/App.jsx
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Login />} />
    </Routes>
  );
}
```

> **💡 Why the loading check matters**
>
> On a hard refresh you have a token but haven't fetched
>
> /auth/me
>
> yet. Without the
>
> loading
>
> guard, the route would briefly think you're unauthenticated and bounce you to login. Always wait for auth to resolve before redirecting.

## 7. A login form & logout

The login page is a controlled form (Chunk 4.3) that calls `login()` from context and navigates on success.

```python
// src/pages/Login.jsx
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>Log in</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <input type="email" value={email} placeholder="Email"
             onChange={(e) => setEmail(e.target.value)} required />
      <input type="password" value={password} placeholder="Password"
             onChange={(e) => setPassword(e.target.value)} required />
      <button type="submit">Log in</button>
      <p>No account? <Link to="/register">Register</Link></p>
    </form>
  );
}
```

Logout is just calling `logout()` and navigating away:

```jsx
const { user, logout } = useAuth();
const navigate = useNavigate();

<button onClick={() => { logout(); navigate("/login"); }}>
  Log out ({user?.email})
</button>
```

## ✅ Recap

- The flow is four moments: **login → store → attach → protect (+ logout)**.
- Token storage is a trade-off; we use `localStorage` (survives refresh) knowing it's XSS-exposed, and keep tokens short-lived.
- A small `apiFetch` helper attaches `Authorization: Bearer` to every call and handles `401`.
- **Login is form-encoded** (`URLSearchParams`, OAuth2); register is JSON.
- `AuthContext` + `useAuth` share auth state; `ProtectedRoute` redirects unauthenticated users (waiting for `loading` first); logout clears everything.

**Next:** open `assignment.html` and build the full login experience.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
