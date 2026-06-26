*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

We'll build the React auth layer file by file. Final structure:

```text
tasks-web/
├── .env                       (VITE_API_URL)
└── src/
    ├── api.js                 (fetch helpers + auth headers)
    ├── main.jsx               (BrowserRouter + AuthProvider)
    ├── App.jsx                (routes)
    ├── context/
    │   └── AuthContext.jsx    (token/user state, login/logout)
    ├── components/
    │   └── ProtectedRoute.jsx (redirect guard)
    └── pages/
        ├── Login.jsx
        ├── Register.jsx
        └── Dashboard.jsx
```

### 1 The env file

```
# .env  (project root, next to package.json)
VITE_API_URL=http://localhost:8000
```

Restart `npm run dev` after adding it — Vite only reads env files at startup.

### 2 `src/api.js`

```javascript
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
    localStorage.removeItem("token");
    throw new Error("Unauthorized");
  }
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Request failed");
  }
  return res.status === 204 ? null : res.json();
}

export async function loginRequest(email, password) {
  const body = new URLSearchParams({ username: email, password });
  const res = await fetch(`${BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
  });
  if (!res.ok) throw new Error("Invalid email or password");
  return res.json();
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
  return res.json();
}

// Convenience helpers for the dashboard
export const getTasks = () => apiFetch("/tasks");
export const createTask = (title) =>
  apiFetch("/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }),
  });
```

### 3 `src/context/AuthContext.jsx`

```python
import { createContext, useContext, useEffect, useState } from "react";
import { loginRequest, apiFetch } from "../api";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("token"));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) { setUser(null); setLoading(false); return; }
    setLoading(true);
    apiFetch("/auth/me")
      .then(setUser)
      .catch(() => { localStorage.removeItem("token"); setToken(null); })
      .finally(() => setLoading(false));
  }, [token]);

  async function login(email, password) {
    const { access_token } = await loginRequest(email, password);
    localStorage.setItem("token", access_token);
    setToken(access_token);
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

### 4 `src/main.jsx`

```python
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import App from "./App";

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

### 5 `src/components/ProtectedRoute.jsx`

```python
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return <p>Loading…</p>;
  if (!isAuthenticated) return <Navigate to="/login" replace />;
  return children;
}
```

### 6 `src/App.jsx` — routes

```python
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

### 7 `src/pages/Login.jsx`

```python
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await login(email, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 320, margin: "40px auto" }}>
      <h1>Log in</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <input type="email" value={email} placeholder="Email" required
             onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} placeholder="Password" required
             onChange={(e) => setPassword(e.target.value)} />
      <button type="submit" disabled={busy}>{busy ? "Logging in…" : "Log in"}</button>
      <p>No account? <Link to="/register">Register</Link></p>
    </form>
  );
}
```

### 8 `src/pages/Register.jsx`

```python
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerRequest } from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await registerRequest(email, password);
      navigate("/login");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 320, margin: "40px auto" }}>
      <h1>Create account</h1>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      <input type="email" value={email} placeholder="Email" required
             onChange={(e) => setEmail(e.target.value)} />
      <input type="password" value={password} placeholder="Password (8+ chars)"
             minLength={8} required
             onChange={(e) => setPassword(e.target.value)} />
      <button type="submit">Register</button>
      <p>Have an account? <Link to="/login">Log in</Link></p>
    </form>
  );
}
```

### 9 `src/pages/Dashboard.jsx`

```python
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { getTasks, createTask } from "../api";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getTasks().then(setTasks).catch((e) => setError(e.message));
  }, []);

  async function handleAdd(e) {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      const task = await createTask(title);
      setTasks((prev) => [...prev, task]);
      setTitle("");
    } catch (e) {
      setError(e.message);
    }
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div style={{ maxWidth: 480, margin: "40px auto" }}>
      <header style={{ display: "flex", justifyContent: "space-between" }}>
        <h1>My Tasks</h1>
        <button onClick={handleLogout}>Log out ({user?.email})</button>
      </header>

      {error && <p style={{ color: "crimson" }}>{error}</p>}

      <form onSubmit={handleAdd}>
        <input value={title} placeholder="New task…"
               onChange={(e) => setTitle(e.target.value)} />
        <button type="submit">Add</button>
      </form>

      <ul>
        {tasks.map((t) => (
          <li key={t.id}>{t.completed ? "✅" : "⬜"} {t.title}</li>
        ))}
      </ul>
      {tasks.length === 0 && <p>No tasks yet — add one above.</p>}
    </div>
  );
}
```

### 10 Run both servers & test

```bash
# terminal 1 — backend (with SECRET_KEY exported)
uvicorn app.main:app --reload

# terminal 2 — frontend
npm run dev      # http://localhost:5173
```

**Expected:**

- Visiting `/dashboard` logged out bounces you to `/login`.
- Register → Login → you land on the dashboard greeting your email.
- Add a task; it appears and survives a backend restart (it's in `tasks.db`).
- Refresh the browser → still logged in. Log out → back to `/login`, dashboard blocked.
- In DevTools → Application → Local Storage you'll see the `token` key.

## 🔧 Troubleshooting

| Symptom | Fix |
| --- | --- |
| CORS error in the console | Add the Vite origin to FastAPI's `CORSMiddleware` `allow_origins=["http://localhost:5173"]` with `allow_headers=["*"]` (Chunk 5.5). |
| Login returns `422` | You sent JSON. Login must be form-encoded — use `URLSearchParams` and `Content-Type: application/x-www-form-urlencoded`. |
| Every request is `401` | The token isn't being attached. Confirm it's in localStorage and `apiFetch` adds the `Authorization` header. |
| Redirected to login on refresh even with a token | You're redirecting before `/auth/me` resolves. Keep the `loading` guard in `ProtectedRoute`. |
| `useAuth must be used inside <AuthProvider>` | A component using `useAuth` is rendered outside the provider. Ensure `AuthProvider` wraps `<App />` in `main.jsx`. |
| `import.meta.env.VITE_API_URL` is undefined | Env var must start with `VITE_` and the dev server must be restarted after editing `.env`. |

## 🎉 You're done

You have a complete login experience end-to-end: a React UI that registers and logs users in, stores the JWT, attaches it to every request, protects the dashboard, survives refresh, and logs out cleanly — all talking to your secured Tasks API.

It works, but it isn't fully *hardened* yet: there are no roles, the access token never refreshes, and the secret still lives in an env var by hand. The final chunk locks all of that down and ties the module together.

**Up next → Chunk 7.4: Authorization, Refresh & Security Hardening.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
