*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.3 — Lab: Login Experience End-to-End

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Build the React front of the auth system. You'll create login and register pages, an `AuthContext` that stores the JWT and exposes `login`/`logout`, an API helper that attaches the bearer header, and a **protected dashboard** that lists the logged-in user's tasks from the Tasks API. End result: a complete login experience, browser to backend.

## Before you start

- The Tasks API from 7.2 is running on `http://localhost:8000` with JWT login + protected `/tasks` + `/auth/me`.
- A React + Vite app (from Module 4) with **React Router** installed. New app if needed: `npm create vite@latest tasks-web -- --template react`, then `npm i react-router-dom`.
- **CORS:** your FastAPI app must allow the Vite origin (`http://localhost:5173`) via `CORSMiddleware` — you set this up in Chunk 5.5. Double-check it's there.

> **⚠️ Try it yourself first**
>
> Work from the lecture. Only open
>
> solution.html
>
> when stuck or to compare.

## Tasks

### 1 Configure the API base URL

Add a `.env` file with `VITE_API_URL=http://localhost:8000` (restart the dev server after creating it).

### 2 Build `src/api.js`

Export: `getToken()`, `apiFetch(path, options)` (attaches `Authorization: Bearer`, handles `401`), `loginRequest(email, password)` (**form-encoded** with `URLSearchParams`), and `registerRequest(email, password)` (JSON).

### 3 Build `src/context/AuthContext.jsx`

An `AuthProvider` holding `token`, `user`, and `loading`. On mount (and whenever the token changes) it fetches `/auth/me` to populate `user`. Expose `login(email, password)`, `logout()`, and `isAuthenticated`. Add a `useAuth()` hook.

### 4 Wrap the app

In `src/main.jsx`, wrap `<App />` with `<BrowserRouter>` then `<AuthProvider>`.

### 5 Build the Login & Register pages

Controlled forms in `src/pages/Login.jsx` and `src/pages/Register.jsx`. Login calls `login()` from context then navigates to `/dashboard`; Register calls `registerRequest` then sends the user to `/login`. Show an error message on failure.

### 6 Build `ProtectedRoute`

A guard that shows a loading state while auth resolves, redirects to `/login` when not authenticated, and otherwise renders its children.

### 7 Build the protected Dashboard

`src/pages/Dashboard.jsx`: greet the user (`user.email`), fetch and list their tasks via `apiFetch("/tasks")`, add a small "create task" form (POST `/tasks`), and a **Log out** button. Wire all three routes in `App.jsx` with the dashboard behind `ProtectedRoute`.

### 8 Test the full flow

1. Visit `/dashboard` while logged out → you're redirected to `/login`.
2. Register a new account, then log in → you land on the dashboard.
3. Create a task; confirm it appears and persists in the backend.
4. Refresh the page → you stay logged in (token from localStorage).
5. Log out → you're sent to `/login` and the dashboard is blocked again.

## ✅ Deliverable — acceptance checklist

- `api.js` attaches `Authorization: Bearer` to authenticated calls; login uses form-encoding, register uses JSON.
- `AuthContext` stores the token, loads `/auth/me`, and exposes `login`, `logout`, `isAuthenticated` via `useAuth`.
- Login and Register pages work and show errors on bad input.
- `/dashboard` is protected: logged-out users are redirected to `/login`.
- The dashboard lists only the current user's tasks and can create a new one.
- Refreshing keeps you logged in; logging out clears the token and blocks the dashboard.

## 🚀 Stretch goals (optional)

- Add a navbar that shows the user's email + a logout button only when authenticated.
- Redirect an *already logged-in* user away from `/login` straight to `/dashboard`.
- After login, send the user back to the page they originally tried to visit (read it from router location state).
- Add a toggle/complete and delete button per task, calling `PUT`/`DELETE` through `apiFetch`.
- Disable the submit button and show "Logging in…" while the request is in flight.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
