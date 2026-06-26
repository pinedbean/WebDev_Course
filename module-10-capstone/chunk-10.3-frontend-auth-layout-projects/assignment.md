*Full-Stack Web Dev · Module 10 — Capstone: TaskFlow*

# Chunk 10.3 — Lab: Auth Frontend, Layout & Projects

**🧪 ASSIGNMENT** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build the authenticated frontend shell for TaskFlow: an API client, an auth context with login/register/logout, protected routing, an app layout with nav, and a projects page (list + create) wired to your 10.2 backend. By the end you can register, log in, see your projects, create one, refresh without losing your session, and log out.

## Before you start

- Your 10.2 backend runs at `http://localhost:8000` (start `uvicorn` in the `backend/` venv).
- Your 10.1 frontend scaffold exists with `react-router-dom` installed and `VITE_API_URL` in `frontend/.env`.
- Run the dev server: `cd frontend && npm run dev`.

> **⚠️ Build it yourself first**
>
> Recall Module 4.5–4.7 (router, context, custom hooks) and 7.3 (auth flow). Try each piece before peeking at the solution.

## Tasks

### 1 Build the API client

Create `src/api/client.js` with an `api(path, options)` helper that prefixes `VITE_API_URL`, attaches the bearer token from `localStorage`, sends JSON (or form-encoded for login), parses the response, and throws an `Error` with the backend's `detail` on failure. Handle 204 (no content).

### 2 Create the Auth Context

Create `src/context/AuthContext.jsx` with `user`, `loading`, and `login()`, `register()`, `logout()`. On mount, if a token exists, call `/auth/me` to restore the session. Export a `useAuth()` hook. Wrap the app in the provider in `main.jsx`.

### 3 Login & Register pages

Build `src/pages/Login.jsx` and `Register.jsx` with controlled inputs. On submit, call the context method, then navigate to `/`. Show the error message on failure (e.g. wrong password, email taken). Each page links to the other.

### 4 Protected route + Layout

Create `src/components/ProtectedRoute.jsx` (redirect to `/login` if no user; show "Loading…" while `loading`) and `src/components/Layout.jsx` (top nav with the brand, the user's name, and a logout button; an `<Outlet/>` for pages).

### 5 Route table in `App.jsx`

Set up routes: public `/login` and `/register`; everything else nested under `ProtectedRoute` → `Layout`, with `/` rendering the Projects page. Add a placeholder `/projects/:id` route (you fill it in 10.4).

### 6 Projects page

Build `src/pages/Projects.jsx`: fetch `/projects` on mount with loading + error states; render a grid/list of project cards linking to `/projects/:id`; include a create form that POSTs `/projects` and prepends/appends the new project without a full reload.

### 7 Style the shell

Add enough CSS (in `index.css` or per-component) to make it look like an app: a styled top bar, a clean auth form card, and a responsive project grid. It doesn't need to be fancy — just tidy and readable.

### 8 Verify the full flow

Register a new user → land on Projects. Create a project. Refresh the page — you're still logged in and the project is there. Log out — you're redirected to `/login` and can't reach `/` by typing the URL.

## ✅ Deliverable — acceptance checklist

- An API client attaches the JWT and surfaces backend error messages.
- Auth context provides `user`/`login`/`register`/`logout`; session restores via `/auth/me` on refresh.
- Register and Login pages work and show errors (duplicate email, wrong password).
- Visiting `/` while logged out redirects to `/login`.
- The layout shows the app name, the logged-in user's name, and a working logout button.
- Projects page lists the user's projects and creates new ones without a full reload.
- The UI is styled enough to look like a real app and is responsive.

## 🚀 Stretch goals (optional)

- Extract a `useApi` / `useFetch` hook (Module 4.7) so pages don't repeat loading/error boilerplate.
- Add a global 401 handler in the client that logs the user out and redirects on an expired token.
- Show a friendly empty state ("No projects yet — create your first!") when the list is empty.
- Disable the create button and show a spinner while the POST is in flight.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
