*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.3 — Frontend: Auth, Layout & Project Views

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to build a small **API client** that attaches the JWT to every request and centralizes error handling.
- How to manage login state app-wide with an **Auth Context** (Module 4.6 + 7.3) and persist the token.
- How to **protect routes** so unauthenticated users get bounced to `/login`.
- How to build the **app shell**: a layout with a nav bar and an `<Outlet>` for nested pages.
- How to fetch and render the **projects list** and a **create-project** form against the 10.2 API.

The lab delivers a usable, authenticated frontend wired to your backend.

## 1. The architecture of the frontend

Everything you learned in Module 4 and 7.3 comes together here. The shape:

```text
frontend/src/
├── main.jsx              (mount + BrowserRouter)
├── App.jsx              (route table)
├── api/client.js        (fetch wrapper: base URL + token + errors)
├── context/AuthContext.jsx  (user, token, login(), logout())
├── components/
│   ├── ProtectedRoute.jsx   (redirect if not logged in)
│   └── Layout.jsx           (nav bar + <Outlet/>)
└── pages/
    ├── Login.jsx
    ├── Register.jsx
    └── Projects.jsx         (list + create)
```

Data flows in one direction: a page calls the **api client**, which reads the token from the **auth context**, hits the **backend**, and the page renders the result. Keeping the fetch logic in one file means we add the token (and later, request IDs) in exactly one place.

## 2. The API client

Rather than scatter `fetch` calls everywhere, we wrap it once. It reads `VITE_API_URL` (set in 10.1), attaches the bearer token, parses JSON, and throws a useful error on non-2xx responses.

```javascript
// src/api/client.js
const BASE = import.meta.env.VITE_API_URL;  // http://localhost:8000/api/v1

export function getToken() {
  return localStorage.getItem("taskflow_token");
}

export async function api(path, { method = "GET", body, form } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let payload;
  if (form) {                       // login uses form-encoded data
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    payload = new URLSearchParams(form).toString();
  } else if (body) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const res = await fetch(`${BASE}${path}`, { method, headers, body: payload });
  if (res.status === 204) return null;        // no content (DELETE)
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.detail || `Request failed (${res.status})`);
  }
  return data;
}
```

> **📝 One place for the token**
>
> Because every call goes through
>
> api()
>
> , adding the
>
> Authorization
>
> header happens once. When you add request-ID echoing in 10.5, it's a one-line change here.

## 3. Storing the token: the trade-off

Where do you keep the JWT between page loads? You met this in 7.3. The honest summary:

| Option | Pro | Con |
| --- | --- | --- |
| `localStorage` | Simple; survives refresh; easy with a SPA | Readable by JS → vulnerable if you have an XSS hole |
| `httpOnly` cookie | JS can't read it (XSS-safer) | Needs CSRF protection + server cookie handling |

For this capstone we use `localStorage` — it's the common SPA choice and keeps the focus on the full-stack flow. We mitigate XSS by never using `dangerouslySetInnerHTML` and validating input (10.5). We'll call this out explicitly in the README's "security notes".

## 4. The Auth Context

Login state must be readable anywhere (the nav bar shows your name; protected routes check if you're in). That's exactly what React Context is for. The context holds the `user`, exposes `login()`/`register()`/`logout()`, and restores the session on refresh by calling `/auth/me`.

```jsx
// src/context/AuthContext.jsx  (essentials)
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getToken()) { setLoading(false); return; }
    api("/auth/me")                       // token already attached by client
      .then(setUser)
      .catch(() => localStorage.removeItem("taskflow_token"))
      .finally(() => setLoading(false));
  }, []);

  async function login(email, password) {
    const { access_token } = await api("/auth/login",
      { method: "POST", form: { username: email, password } });
    localStorage.setItem("taskflow_token", access_token);
    setUser(await api("/auth/me"));
  }

  function logout() {
    localStorage.removeItem("taskflow_token");
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
```

> **💡 Restore on refresh**
>
> Storing only the token (not the user object) and re-fetching
>
> /auth/me
>
> on mount keeps the user data fresh and confirms the token is still valid. The
>
> loading
>
> flag prevents a flash of the login page before we know who you are.

## 5. Protected routes

A tiny wrapper component gates everything behind login. If there's no user (and we're done loading), redirect to `/login`; otherwise render the child route via `<Outlet/>`.

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

And the route table composes it with the layout:

```html
// src/App.jsx
<Routes>
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />
  <Route element={<ProtectedRoute />}>        {/* everything below needs auth */}
    <Route element={<Layout />}>             {/* nav + <Outlet/> */}
      <Route path="/" element={<Projects />} />
      <Route path="/projects/:id" element={<Board />} />  {/* added in 10.4 */}
    </Route>
  </Route>
</Routes>
```

## 6. The app layout & nav

The layout is the persistent shell: a top nav with the app name, the logged-in user, and a logout button. `<Outlet/>` is where the active page renders (Module 4.5's nested layouts).

```python
// src/components/Layout.jsx
import { Link, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  return (
    <div>
      <header className="topbar">
        <Link to="/" className="brand">TaskFlow</Link>
        <div className="spacer" />
        <span>{user?.name}</span>
        <button onClick={() => { logout(); navigate("/login"); }}>
          Logout
        </button>
      </header>
      <main className="content"><Outlet /></main>
    </div>
  );
}
```

## 7. The projects page: list + create

This page does two things: fetch projects on mount, and create new ones. The fetch pattern is your Module 4.4 `useEffect` + loading/error states; the form is a controlled input from 4.3.

```jsx
// src/pages/Projects.jsx  (essentials)
export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    api("/projects").then(setProjects).catch((e) => setError(e.message));
  }, []);

  async function create(e) {
    e.preventDefault();
    try {
      const project = await api("/projects",
        { method: "POST", body: { name, description: "" } });
      setProjects((prev) => [...prev, project]);   // optimistic-ish update
      setName("");
    } catch (err) { setError(err.message); }
  }

  return (
    <section>
      <h1>My Projects</h1>
      {error && <p className="error">{error}</p>}
      <form onSubmit={create}>
        <input value={name} onChange={(e) => setName(e.target.value)}
               placeholder="New project name" required />
        <button>+ Create</button>
      </form>
      <ul className="project-grid">
        {projects.map((p) => (
          <li key={p.id}>
            <Link to={`/projects/${p.id}`}>{p.name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
```

> **⚠️ The cross-origin gotcha**
>
> Your frontend (port 5173) calls your backend (port 8000) — a different origin. That's why 10.2's
>
> main.py
>
> has CORS middleware allowing
>
> http://localhost:5173
>
> . If requests fail with a CORS error in the console, check that origin matches.

## ✅ Recap

- A single **API client** centralizes the base URL, the bearer token, and error parsing.
- The **Auth Context** holds the user, exposes `login/register/logout`, persists the token in `localStorage`, and restores the session via `/auth/me`.
- **ProtectedRoute** + a nested **Layout** with `<Outlet/>` give you a clean app shell where every inner page requires auth.
- The **Projects** page reuses Module 4's fetch-on-mount and controlled-form patterns against the real API.
- CORS must allow your Vite origin — already configured on the backend.

**Next:** open `assignment.html` and build the authenticated frontend shell + projects views.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
