*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.3 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Build the frontend file by file. All JSX is complete and copy-pasteable. Files we create/edit:

```text
frontend/src/
├── main.jsx              (wrap app in AuthProvider + BrowserRouter)
├── App.jsx               (routes)
├── index.css             (app styling)
├── api/client.js
├── context/AuthContext.jsx
├── components/
│   ├── ProtectedRoute.jsx
│   └── Layout.jsx
└── pages/
    ├── Login.jsx
    ├── Register.jsx
    └── Projects.jsx
```

### 1 API client

```javascript
// src/api/client.js
const BASE = import.meta.env.VITE_API_URL;

export function getToken() {
  return localStorage.getItem("taskflow_token");
}
export function setToken(t) {
  localStorage.setItem("taskflow_token", t);
}
export function clearToken() {
  localStorage.removeItem("taskflow_token");
}

export async function api(path, { method = "GET", body, form } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let payload;
  if (form) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    payload = new URLSearchParams(form).toString();
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const res = await fetch(`${BASE}${path}`, { method, headers, body: payload });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`);
  return data;
}
```

### 2 Auth context

```python
// src/context/AuthContext.jsx
import { createContext, useContext, useEffect, useState } from "react";
import { api, getToken, setToken, clearToken } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getToken()) { setLoading(false); return; }
    api("/auth/me")
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const { access_token } = await api("/auth/login", {
      method: "POST", form: { username: email, password },
    });
    setToken(access_token);
    setUser(await api("/auth/me"));
  }

  async function register(name, email, password) {
    const { access_token } = await api("/auth/register", {
      method: "POST", body: { name, email, password },
    });
    setToken(access_token);
    setUser(await api("/auth/me"));
  }

  function logout() {
    clearToken();
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

### 3 Login & Register pages

```python
// src/pages/Login.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await login(email, password);
      navigate("/");
    } catch (err) { setError(err.message); }
  }

  return (
    <div className="auth-wrap">
      <form className="auth-card" onSubmit={onSubmit}>
        <h1>Log in to TaskFlow</h1>
        {error && <p className="error">{error}</p>}
        <label>Email
          <input type="email" value={email} required
                 onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>Password
          <input type="password" value={password} required
                 onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit">Log in</button>
        <p>No account? <Link to="/register">Register</Link></p>
      </form>
    </div>
  );
}
```

```python
// src/pages/Register.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function onSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await register(name, email, password);
      navigate("/");
    } catch (err) { setError(err.message); }
  }

  return (
    <div className="auth-wrap">
      <form className="auth-card" onSubmit={onSubmit}>
        <h1>Create your account</h1>
        {error && <p className="error">{error}</p>}
        <label>Name
          <input value={name} required
                 onChange={(e) => setName(e.target.value)} />
        </label>
        <label>Email
          <input type="email" value={email} required
                 onChange={(e) => setEmail(e.target.value)} />
        </label>
        <label>Password
          <input type="password" value={password} required minLength={8}
                 onChange={(e) => setPassword(e.target.value)} />
        </label>
        <button type="submit">Register</button>
        <p>Already have an account? <Link to="/login">Log in</Link></p>
      </form>
    </div>
  );
}
```

### 4 ProtectedRoute & Layout

```python
// src/components/ProtectedRoute.jsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute() {
  const { user, loading } = useAuth();
  if (loading) return <p style={{ padding: 24 }}>Loading…</p>;
  return user ? <Outlet /> : <Navigate to="/login" replace />;
}
```

```python
// src/components/Layout.jsx
import { Link, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  function onLogout() { logout(); navigate("/login"); }

  return (
    <div>
      <header className="topbar">
        <Link to="/" className="brand">TaskFlow</Link>
        <div className="spacer" />
        <span className="who">{user?.name}</span>
        <button className="ghost" onClick={onLogout}>Logout</button>
      </header>
      <main className="content"><Outlet /></main>
    </div>
  );
}
```

### 5 Routes & app bootstrap

```python
// src/App.jsx
import { Routes, Route } from "react-router-dom";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Projects from "./pages/Projects";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Projects />} />
          {/* /projects/:id Board route is added in Chunk 10.4 */}
        </Route>
      </Route>
    </Routes>
  );
}
```

```python
// src/main.jsx
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import App from "./App";
import "./index.css";

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

### 6 Projects page

```python
// src/pages/Projects.jsx
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client";

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api("/projects")
      .then(setProjects)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  async function create(e) {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      const project = await api("/projects", {
        method: "POST", body: { name, description: "" },
      });
      setProjects((prev) => [...prev, project]);
      setName("");
    } catch (err) { setError(err.message); }
    finally { setSaving(false); }
  }

  if (loading) return <p>Loading projects…</p>;

  return (
    <section>
      <div className="page-head">
        <h1>My Projects</h1>
      </div>
      {error && <p className="error">{error}</p>}

      <form className="inline-form" onSubmit={create}>
        <input value={name} placeholder="New project name" required
               onChange={(e) => setName(e.target.value)} />
        <button disabled={saving}>{saving ? "Creating…" : "+ Create"}</button>
      </form>

      {projects.length === 0 ? (
        <p className="muted">No projects yet — create your first one above.</p>
      ) : (
        <ul className="project-grid">
          {projects.map((p) => (
            <li key={p.id} className="project-card">
              <Link to={`/projects/${p.id}`}>
                <h3>{p.name}</h3>
                <p className="muted">{p.description || "No description"}</p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
```

### 7 Styling (`index.css`)

```
/* src/index.css — replace Vite's defaults */
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0; background: #f1f5f9; color: #1e293b;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
a { color: #2563eb; text-decoration: none; }

.topbar {
  display: flex; align-items: center; gap: 12px;
  background: #1e3a8a; color: #fff; padding: 14px 22px;
}
.topbar .brand { color: #fff; font-weight: 700; font-size: 20px; }
.topbar .spacer { flex: 1; }
.topbar .who { opacity: .9; }
.ghost {
  background: rgba(255,255,255,.15); color: #fff; border: 0;
  padding: 8px 14px; border-radius: 8px; cursor: pointer;
}
.content { max-width: 960px; margin: 0 auto; padding: 28px 22px; }

.auth-wrap { display: grid; place-items: center; min-height: 100vh; }
.auth-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 28px; width: 360px; display: grid; gap: 12px;
}
.auth-card label { display: grid; gap: 4px; font-size: 14px; }
.auth-card input, .inline-form input {
  padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 15px;
}
button {
  background: #2563eb; color: #fff; border: 0; padding: 10px 16px;
  border-radius: 8px; font-weight: 600; cursor: pointer;
}
button:disabled { opacity: .6; cursor: default; }
.error { color: #b91c1c; background: #fee2e2; padding: 8px 12px; border-radius: 8px; }
.muted { color: #64748b; }

.inline-form { display: flex; gap: 10px; margin: 16px 0 24px; }
.inline-form input { flex: 1; }

.project-grid {
  list-style: none; padding: 0; display: grid; gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}
.project-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px;
}
.project-card h3 { margin: 0 0 6px; }
```

### 8 Run & verify

With the backend up, run the frontend:

```bash
cd frontend && npm run dev
```

1. Open `http://localhost:5173` → redirected to `/login`.
2. Click Register, create an account → you land on Projects.
3. Create a project — it appears immediately.
4. Refresh — still logged in, project still listed (token + `/auth/me`).
5. Logout → back to `/login`; typing `/` redirects you back to login.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| CORS error in console | Backend must allow `http://localhost:5173` (10.2 `main.py`). Restart uvicorn after changing it. |
| `VITE_API_URL is undefined` | Vite only reads `VITE_`-prefixed vars and only at startup. Restart `npm run dev` after editing `.env`. |
| Login 422 | The client must send `form` (URL-encoded `username`/`password`) for `/auth/login`, not JSON. |
| Logged out after refresh | Confirm the token is saved under `taskflow_token` and `/auth/me` is called on mount. |
| Blank page, console error about Router | `useNavigate`/`Link` must be inside `<BrowserRouter>` — check `main.jsx`. |

## 🎉 Done — what's next

TaskFlow now has a real authenticated frontend: you can register, log in, stay logged in across refreshes, see your projects, create them, and log out — all wired to your secured API.

- ✅ API client with token + error handling.
- ✅ Auth context, protected routes, app layout.
- ✅ Projects list + create against the live backend.

**Up next → Chunk 10.4: Task Board & Collaboration.** You'll build the headline feature — a board with status columns, create/edit/assign/due-date, filtering, and member invitations.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
