# Full-Stack Web Development Course

> From zero to a deployable, production-style web application.
> **Stack:** HTML · CSS · JavaScript · React + Vite · FastAPI · SQLite · Auth · Logging · Load Balancing

---

## How This Course Works

- **Daily commitment:** 1–2 hours per day.
- **Chunked learning:** The course is split into **chunks**. Each chunk is self-contained and **completable in one 1–2 hour session**.
- **Every chunk has two parts:**
  - 📖 **Lecture** — concepts, the "why", and worked examples (~30–45 min).
  - 🧪 **Lab** — hands-on exercise you build yourself (~45–75 min).
- **Every chunk ends with a Deliverable** — something concrete you produced, so you always know you finished.
- **Checkpoints** — at the end of each module, a short review + mini-project to lock in the skills.
- **Capstone** — a real-world app (**TaskFlow**, a team task/project tracker) that you build incrementally across the whole course, ending with auth, logging, and a load-balanced production deployment.

### Conventions
- ✅ Deliverable — what you should have at the end of the chunk.
- 🎯 Objective — what you'll be able to do.
- ⏱️ Estimated time — fits inside a 1–2 hour session.

### Suggested pace
~9–11 weeks at 1 chunk/day, 5 days/week. Go slower if needed — the chunks are the unit, not the calendar.

---

## Curriculum at a Glance

| Module | Title | Chunks | Focus |
|-------|-------|--------|-------|
| 0 | Setup & Tooling | 2 | Environment, terminal, Git, VS Code |
| 1 | HTML Foundations | 3 | Structure & semantics |
| 2 | CSS & Layout | 5 | Styling, Flexbox, Grid, responsive |
| 3 | JavaScript Core | 6 | Language, DOM, async, fetch |
| 4 | React + Vite | 7 | Components, state, routing, data |
| 5 | Backend with FastAPI | 6 | REST APIs, validation, structure |
| 6 | Database with SQLite | 4 | SQL, ORM, migrations, relations |
| 7 | Authentication & Security | 4 | Login, JWT, password hashing |
| 8 | Logging & Observability | 2 | Structured logs, error tracking |
| 9 | Production & Load Balancing | 4 | Docker, Nginx, scaling, deploy |
| 10 | Capstone: TaskFlow | 6 | Real-world full-stack app |
| ⭐ B | **Bonus Track** (optional) | 3 | Git strategy & deploying on GCP |

**Total: ~49 core chunks + 3 bonus = ~52 chunks** (≈ 49–60 days of focused learning; the bonus track is optional and can be done any time after Module 9).

---

# Module 0 — Setup & Tooling
*Goal: a working developer environment you trust.*

### Chunk 0.1 — Your Development Environment
- 🎯 Install and configure the tools you'll use every day.
- 📖 **Lecture:** How the web works (client/server, HTTP request/response), what a "stack" is, the role of each tool.
- 🧪 **Lab:** Install Node.js (LTS), Python 3.11+, VS Code + extensions (Prettier, ESLint, Python), and a modern browser with DevTools. Verify versions in the terminal.
- ✅ **Deliverable:** A `versions.txt` listing your installed tool versions.
- ⏱️ 60–90 min.

### Chunk 0.2 — Terminal & Git Basics
- 🎯 Navigate the filesystem and version your work.
- 📖 **Lecture:** Shell basics (`cd`, `ls`, `mkdir`, paths), what Git is, commit/branch/push mental model.
- 🧪 **Lab:** Create a project folder, `git init`, make commits, create a GitHub account + repo, push your first commit.
- ✅ **Deliverable:** A GitHub repo `webdev-course` with a `README.md` and 3+ commits.
- ⏱️ 60–90 min.

---

# Module 1 — HTML Foundations
*Goal: structure any page with clean, semantic HTML.*

### Chunk 1.1 — HTML Document Structure
- 🎯 Build a valid HTML page from scratch.
- 📖 **Lecture:** Elements, tags, attributes, nesting, the `<head>` vs `<body>`, headings, paragraphs, links, images.
- 🧪 **Lab:** Build a personal "About Me" page with headings, text, links, and images.
- ✅ **Deliverable:** `about.html` that renders correctly in the browser.
- ⏱️ 60–90 min.

### Chunk 1.2 — Semantic HTML, Lists & Tables
- 🎯 Use the right element for the right job.
- 📖 **Lecture:** Semantic tags (`header`, `nav`, `main`, `section`, `article`, `footer`), ordered/unordered lists, tables, accessibility basics (alt text, landmarks).
- 🧪 **Lab:** Convert your About Me page to semantic layout; add a skills list and an experience table.
- ✅ **Deliverable:** A semantically structured page that passes the W3C validator.
- ⏱️ 60–90 min.

### Chunk 1.3 — Forms & Inputs
- 🎯 Collect user input with HTML forms.
- 📖 **Lecture:** `<form>`, input types, labels, `name`/`value`, `select`, `textarea`, `button`, native validation (`required`, `type=email`).
- 🧪 **Lab:** Build a "Contact" form with multiple input types and validation attributes.
- ✅ **Deliverable:** `contact.html` with a fully labeled, validating form.
- 🏁 **Module Checkpoint:** Combine pages into a 3-page personal site (Home, About, Contact) linked together.
- ⏱️ 60–90 min.

---

# Module 2 — CSS & Layout
*Goal: style and lay out pages that look good on any screen.*

### Chunk 2.1 — CSS Fundamentals & Selectors
- 🎯 Apply styles cleanly and predictably.
- 📖 **Lecture:** Ways to include CSS, selectors (element/class/id/descendant), specificity, the cascade, colors, units (`px`, `rem`, `%`).
- 🧪 **Lab:** Style your personal site with an external stylesheet and a consistent color palette.
- ✅ **Deliverable:** `styles.css` applied across all pages.
- ⏱️ 60–90 min.

### Chunk 2.2 — The Box Model & Typography
- 🎯 Control spacing and text precisely.
- 📖 **Lecture:** Margin/border/padding/content, `box-sizing`, fonts, line-height, web fonts, text styling.
- 🧪 **Lab:** Fix spacing and typography across your site; add a Google Font.
- ✅ **Deliverable:** A visually consistent, well-spaced site.
- ⏱️ 60–90 min.

### Chunk 2.3 — Flexbox Layout
- 🎯 Build one-dimensional layouts (rows/columns).
- 📖 **Lecture:** `display: flex`, main/cross axis, `justify-content`, `align-items`, `gap`, `flex-wrap`.
- 🧪 **Lab:** Build a responsive navbar and a card row with Flexbox.
- ✅ **Deliverable:** A reusable navbar component (HTML/CSS).
- ⏱️ 60–90 min.

### Chunk 2.4 — CSS Grid Layout
- 🎯 Build two-dimensional page layouts.
- 📖 **Lecture:** `display: grid`, columns/rows, `fr` units, `grid-template-areas`, placing items.
- 🧪 **Lab:** Build a dashboard-style page layout (header, sidebar, content, footer) with Grid.
- ✅ **Deliverable:** A grid-based layout template.
- ⏱️ 60–90 min.

### Chunk 2.5 — Responsive Design & Media Queries
- 🎯 Make layouts adapt to phones, tablets, desktops.
- 📖 **Lecture:** Mobile-first thinking, media queries, breakpoints, responsive images, viewport meta tag.
- 🧪 **Lab:** Make your personal site fully responsive across 3 breakpoints.
- ✅ **Deliverable:** A responsive site (verify in DevTools device mode).
- 🏁 **Module Checkpoint:** Redesign your personal site into a polished, responsive portfolio.
- ⏱️ 60–90 min.

---

# Module 3 — JavaScript Core
*Goal: make pages interactive and talk to servers.*

### Chunk 3.1 — JavaScript Basics
- 🎯 Read and write fundamental JS.
- 📖 **Lecture:** Variables (`let`/`const`), types, operators, template literals, conditionals, loops.
- 🧪 **Lab:** Console exercises: temperature converter, FizzBuzz, simple calculator logic.
- ✅ **Deliverable:** A `basics.js` file solving 5 small problems.
- ⏱️ 60–90 min.

### Chunk 3.2 — Functions, Arrays & Objects
- 🎯 Model data and reuse logic.
- 📖 **Lecture:** Function declarations vs arrow functions, parameters/returns, arrays + methods (`map`, `filter`, `reduce`, `forEach`), objects, destructuring.
- 🧪 **Lab:** Transform a list of data (e.g., filter/sort a list of products).
- ✅ **Deliverable:** A script that processes an array of objects.
- ⏱️ 60–90 min.

### Chunk 3.3 — The DOM & Events
- 🎯 Manipulate the page in response to users.
- 📖 **Lecture:** Selecting elements, changing content/styles, creating/removing nodes, event listeners, event object.
- 🧪 **Lab:** Build an interactive to-do list (add/remove items, mark complete) — vanilla JS.
- ✅ **Deliverable:** A working `todo.html` + `todo.js`.
- ⏱️ 60–90 min.

### Chunk 3.4 — Async JavaScript & Fetch
- 🎯 Load data from the network without freezing the page.
- 📖 **Lecture:** Callbacks → Promises → `async/await`, the event loop (intuition), `fetch`, JSON, error handling.
- 🧪 **Lab:** Fetch and display data from a public API (e.g., a quotes or weather API).
- ✅ **Deliverable:** A page that loads and renders live API data.
- ⏱️ 60–90 min.

### Chunk 3.5 — ES Modules & Modern JS Tooling
- 🎯 Organize code into reusable modules.
- 📖 **Lecture:** `import`/`export`, modules vs scripts, `npm` and `package.json`, what bundlers do, intro to Vite.
- 🧪 **Lab:** Refactor your to-do app into modules; run it with a Vite dev server.
- ✅ **Deliverable:** A modular to-do app running under Vite.
- ⏱️ 60–90 min.

### Chunk 3.6 — Browser Storage & Debugging
- 🎯 Persist data locally and debug effectively.
- 📖 **Lecture:** `localStorage`/`sessionStorage`, JSON serialization, DevTools (breakpoints, network tab, console).
- 🧪 **Lab:** Persist your to-do list across reloads using `localStorage`.
- ✅ **Deliverable:** A persistent to-do app.
- 🏁 **Module Checkpoint:** Build a small interactive widget (e.g., expense tracker) using everything from Module 3.
- ⏱️ 60–90 min.

---

# Module 4 — React + Vite
*Goal: build component-based UIs that scale.*

### Chunk 4.1 — Vite + React Project Setup
- 🎯 Scaffold and run a React app.
- 📖 **Lecture:** Why React, why Vite, project structure, JSX, how components render.
- 🧪 **Lab:** `npm create vite@latest` (React), run the dev server, edit your first component.
- ✅ **Deliverable:** A running React app with a customized landing component.
- ⏱️ 60–90 min.

### Chunk 4.2 — Components & Props
- 🎯 Break UIs into reusable pieces.
- 📖 **Lecture:** Function components, props, composition, conditional rendering, rendering lists with keys.
- 🧪 **Lab:** Build a `Card` component and render a grid of cards from data.
- ✅ **Deliverable:** A reusable card grid.
- ⏱️ 60–90 min.

### Chunk 4.3 — State & Events with Hooks
- 🎯 Make components interactive.
- 📖 **Lecture:** `useState`, event handling in React, controlled inputs, lifting state up.
- 🧪 **Lab:** Rebuild the to-do app in React with `useState`.
- ✅ **Deliverable:** A React to-do app.
- ⏱️ 60–90 min.

### Chunk 4.4 — Side Effects & Data Fetching
- 🎯 Sync components with external data.
- 📖 **Lecture:** `useEffect`, dependency arrays, fetching on mount, loading/error states.
- 🧪 **Lab:** Fetch and display data from a public API with loading + error UI.
- ✅ **Deliverable:** A data-driven React page.
- ⏱️ 60–90 min.

### Chunk 4.5 — Routing with React Router
- 🎯 Build multi-page single-page apps.
- 📖 **Lecture:** Client-side routing, routes, links, route params, nested layouts.
- 🧪 **Lab:** Add Home / List / Detail pages with navigation.
- ✅ **Deliverable:** A multi-route React app.
- ⏱️ 60–90 min.

### Chunk 4.6 — Forms & Shared State
- 🎯 Handle complex input and app-wide state.
- 📖 **Lecture:** Form handling patterns, validation, `useContext` for shared state, when to reach for a state library.
- 🧪 **Lab:** Build a form that adds items to a shared list via Context.
- ✅ **Deliverable:** A form-driven app with shared state.
- ⏱️ 60–90 min.

### Chunk 4.7 — Reusable Hooks & Project Structure
- 🎯 Keep a growing React codebase clean.
- 📖 **Lecture:** Custom hooks (e.g., `useFetch`), folder structure, env variables in Vite, component organization.
- 🧪 **Lab:** Extract a `useFetch` hook and reorganize your project.
- ✅ **Deliverable:** A refactored, well-structured React app.
- 🏁 **Module Checkpoint:** Build a small frontend app (e.g., a movie/recipe browser) consuming a public API.
- ⏱️ 60–90 min.

---

# Module 5 — Backend with FastAPI
*Goal: build a clean, documented REST API.*

### Chunk 5.1 — Python Refresher & FastAPI Setup
- 🎯 Stand up your first API.
- 📖 **Lecture:** Virtual environments, `pip`, just-enough Python (functions, types, dicts), what an API/endpoint is, ASGI/Uvicorn.
- 🧪 **Lab:** Create a venv, install FastAPI + Uvicorn, build a `/hello` endpoint, explore auto-docs at `/docs`.
- ✅ **Deliverable:** A running FastAPI server with interactive docs.
- ⏱️ 60–90 min.

### Chunk 5.2 — Routes, Path & Query Params
- 🎯 Design URL-driven endpoints.
- 📖 **Lecture:** HTTP methods (GET/POST/PUT/DELETE), path params, query params, status codes, JSON responses.
- 🧪 **Lab:** Build CRUD endpoints for an in-memory list of items.
- ✅ **Deliverable:** A working in-memory CRUD API.
- ⏱️ 60–90 min.

### Chunk 5.3 — Request Bodies & Pydantic Validation
- 🎯 Validate and shape data safely.
- 📖 **Lecture:** Pydantic models, request/response schemas, validation, automatic error responses.
- 🧪 **Lab:** Add typed request/response models to your CRUD API.
- ✅ **Deliverable:** A validated CRUD API with typed schemas.
- ⏱️ 60–90 min.

### Chunk 5.4 — Project Structure & Routers
- 🎯 Organize an API that can grow.
- 📖 **Lecture:** `APIRouter`, splitting routes into modules, dependency injection basics, settings/config.
- 🧪 **Lab:** Refactor endpoints into routers and a clean project layout.
- ✅ **Deliverable:** A modular FastAPI project.
- ⏱️ 60–90 min.

### Chunk 5.5 — CORS & Connecting React ↔ FastAPI
- 🎯 Make frontend and backend talk.
- 📖 **Lecture:** CORS, environment-based API URLs, request lifecycle across the stack.
- 🧪 **Lab:** Configure CORS and call your FastAPI endpoints from your React app.
- ✅ **Deliverable:** A React frontend reading/writing to your FastAPI backend.
- ⏱️ 60–90 min.

### Chunk 5.6 — Error Handling & API Best Practices
- 🎯 Build a robust, predictable API.
- 📖 **Lecture:** Exception handlers, consistent error responses, status codes, pagination, API versioning basics.
- 🧪 **Lab:** Add global error handling and pagination to your API.
- ✅ **Deliverable:** A polished, error-tolerant API.
- 🏁 **Module Checkpoint:** A full CRUD API consumed by a React frontend (still in-memory data).
- ⏱️ 60–90 min.

---

# Module 6 — Database with SQLite
*Goal: persist data with a real database.*

### Chunk 6.1 — SQL & SQLite Fundamentals
- 🎯 Query and modify relational data.
- 📖 **Lecture:** Relational model, tables/rows/columns, `CREATE`/`INSERT`/`SELECT`/`UPDATE`/`DELETE`, `WHERE`, why SQLite.
- 🧪 **Lab:** Use the SQLite CLI / DB Browser to create a table and run queries.
- ✅ **Deliverable:** A `.db` file with a table and sample data.
- ⏱️ 60–90 min.

### Chunk 6.2 — SQLAlchemy ORM with FastAPI
- 🎯 Talk to the database from Python.
- 📖 **Lecture:** What an ORM is, SQLAlchemy models, engine/session, dependency-injected DB sessions in FastAPI.
- 🧪 **Lab:** Define models and wire a DB session into your endpoints.
- ✅ **Deliverable:** FastAPI app connected to SQLite via SQLAlchemy.
- ⏱️ 60–90 min.

### Chunk 6.3 — Persisting CRUD & Migrations
- 🎯 Make your CRUD API durable.
- 📖 **Lecture:** Repository pattern, converting endpoints to DB-backed CRUD, schema changes & Alembic migrations.
- 🧪 **Lab:** Replace in-memory storage with SQLite; create your first migration.
- ✅ **Deliverable:** A persistent CRUD API.
- ⏱️ 60–90 min.

### Chunk 6.4 — Relationships & Queries
- 🎯 Model connected data.
- 📖 **Lecture:** One-to-many / many-to-many, foreign keys, joins, filtering/sorting, indexes (intro).
- 🧪 **Lab:** Add a related table (e.g., users ↔ tasks) and query across them.
- ✅ **Deliverable:** A relational data model with working queries.
- 🏁 **Module Checkpoint:** Full-stack CRUD app (React + FastAPI + SQLite) with persistent, related data.
- ⏱️ 60–90 min.

---

# Module 7 — Authentication & Security
*Goal: a real login system you can trust.*

### Chunk 7.1 — Auth Concepts & Password Hashing
- 🎯 Understand how login actually works.
- 📖 **Lecture:** Authentication vs authorization, sessions vs tokens, why never store plain passwords, hashing with bcrypt/argon2, salts.
- 🧪 **Lab:** Build register/login endpoints that hash and verify passwords.
- ✅ **Deliverable:** Secure user registration + login endpoints.
- ⏱️ 60–90 min.

### Chunk 7.2 — JWT Tokens & Protected Routes
- 🎯 Authorize requests statelessly.
- 📖 **Lecture:** JWT structure, signing/verifying, access tokens, `OAuth2PasswordBearer`, dependency-based route protection.
- 🧪 **Lab:** Issue JWTs on login and protect endpoints with a "current user" dependency.
- ✅ **Deliverable:** Protected API routes requiring a valid token.
- ⏱️ 60–90 min.

### Chunk 7.3 — Frontend Auth Flow in React
- 🎯 Wire login into the UI.
- 📖 **Lecture:** Storing tokens (trade-offs), attaching auth headers, protected routes/redirects, auth context, logout.
- 🧪 **Lab:** Build login/register pages and a protected dashboard route in React.
- ✅ **Deliverable:** A complete login experience end-to-end.
- ⏱️ 60–90 min.

### Chunk 7.4 — Authorization, Refresh & Security Hardening
- 🎯 Lock things down properly.
- 📖 **Lecture:** Roles/permissions, refresh tokens, token expiry, common vulnerabilities (XSS, CSRF, injection) and mitigations, secrets management.
- 🧪 **Lab:** Add role-based access (e.g., user vs admin) and basic hardening.
- ✅ **Deliverable:** Role-aware, hardened auth system.
- 🏁 **Module Checkpoint:** Secure full-stack app where users only see their own data.
- ⏱️ 60–90 min.

---

# Module 8 — Logging & Observability
*Goal: see what your app is doing in production.*

### Chunk 8.1 — Structured Logging in FastAPI
- 🎯 Produce useful, searchable logs.
- 📖 **Lecture:** Logging levels, structured (JSON) logs, request/response logging middleware, correlation/request IDs, log vs print.
- 🧪 **Lab:** Add structured logging + a request-logging middleware to your API.
- ✅ **Deliverable:** An API that emits structured logs with request IDs.
- ⏱️ 60–90 min.

### Chunk 8.2 — Error Tracking & Frontend Logging
- 🎯 Catch and diagnose failures.
- 📖 **Lecture:** Centralized error handling, log aggregation concepts, health-check endpoints, frontend error boundaries + reporting.
- 🧪 **Lab:** Add a `/health` endpoint, error logging, and a React error boundary.
- ✅ **Deliverable:** An observable app with health checks and error capture.
- ⏱️ 60–90 min.

---

# Module 9 — Production & Load Balancing
*Goal: deploy a scalable, production-style system.*

### Chunk 9.1 — Production Builds & Environments
- 🎯 Prepare the app for the real world.
- 📖 **Lecture:** Vite production builds, environment variables/secrets, dev vs prod config, serving static assets.
- 🧪 **Lab:** Produce a production build of the frontend and a prod-config backend.
- ✅ **Deliverable:** Production-ready build artifacts.
- ⏱️ 60–90 min.

### Chunk 9.2 — Containerizing with Docker
- 🎯 Package the app to run anywhere.
- 📖 **Lecture:** Images vs containers, Dockerfiles for FastAPI and the frontend, multi-stage builds, `docker compose`.
- 🧪 **Lab:** Write Dockerfiles and a `docker-compose.yml` for frontend + backend + DB.
- ✅ **Deliverable:** The full app running via `docker compose up`.
- ⏱️ 90–120 min.

### Chunk 9.3 — Nginx Reverse Proxy & Load Balancing
- 🎯 Scale horizontally behind a load balancer.
- 📖 **Lecture:** Reverse proxy vs load balancer, why scale out, running multiple API replicas, Nginx upstream + load-balancing strategies (round-robin), sticky sessions vs stateless JWT.
- 🧪 **Lab:** Add Nginx as a reverse proxy/load balancer in front of **2+ FastAPI replicas**; serve the frontend through it.
- ✅ **Deliverable:** A load-balanced stack: Nginx → multiple API instances → SQLite.
- ⏱️ 90–120 min.

### Chunk 9.4 — Deployment & CI/CD Basics
- 🎯 Ship it and keep shipping.
- 📖 **Lecture:** Deployment options (VPS/cloud/container hosts), running migrations in prod, env/secrets in prod, intro to CI/CD with GitHub Actions, SQLite in production: limits & when to move to Postgres.
- 🧪 **Lab:** Deploy the containerized app to a host (or simulate locally) and add a basic CI workflow.
- ✅ **Deliverable:** A deployed (or deploy-ready) app + a CI pipeline.
- 🏁 **Module Checkpoint:** A documented, load-balanced, containerized deployment.
- ⏱️ 90–120 min.

---

# Module 10 — Capstone: TaskFlow
*A real-world team task & project tracker. Each chunk delivers a usable slice.*

> **What you'll build:** TaskFlow — users sign up, create projects, add tasks with statuses/assignees/due dates, and collaborate. It ships with auth, logging, and a load-balanced production deployment. This is portfolio-grade and adaptable to real use.

### Chunk 10.1 — Capstone Planning & Data Modeling
- 🎯 Turn requirements into a design.
- 📖 **Lecture:** Defining MVP scope, user stories, entity-relationship design (Users, Projects, Tasks, Memberships), API contract design, wireframing.
- 🧪 **Lab:** Write the spec, ERD, and API contract for TaskFlow; scaffold repos (frontend + backend).
- ✅ **Deliverable:** `SPEC.md`, an ERD, and scaffolded projects.
- ⏱️ 90–120 min.

### Chunk 10.2 — Backend: Models, Auth & Core API
- 🎯 Build the data + auth foundation.
- 🧪 **Lab:** Implement SQLAlchemy models + migrations, user auth (register/login/JWT), and Projects/Tasks CRUD with ownership rules.
- ✅ **Deliverable:** A secured TaskFlow API with persistent data.
- ⏱️ 90–120 min.

### Chunk 10.3 — Frontend: Auth, Layout & Project Views
- 🎯 Build the core UI shell.
- 🧪 **Lab:** Build login/register, app layout/navigation, projects list + create, and protected routing in React.
- ✅ **Deliverable:** A usable authenticated frontend connected to the API.
- ⏱️ 90–120 min.

### Chunk 10.4 — Feature: Task Board & Collaboration
- 🎯 Deliver the headline feature.
- 🧪 **Lab:** Build the task board (statuses, create/edit/assign, due dates, filtering), wire it fully to the backend, add member invitations.
- ✅ **Deliverable:** A working, collaborative task board.
- ⏱️ 90–120 min.

### Chunk 10.5 — Logging, Observability & Hardening
- 🎯 Make it production-trustworthy.
- 🧪 **Lab:** Add structured logging + request IDs, health checks, a React error boundary, input validation, and security hardening pass.
- ✅ **Deliverable:** An observable, hardened TaskFlow.
- ⏱️ 90–120 min.

### Chunk 10.6 — Containerize, Load-Balance & Deploy
- 🎯 Ship the real thing.
- 🧪 **Lab:** Dockerize frontend + backend, add Nginx load balancing across multiple API replicas, write a deploy + CI workflow, and publish a polished `README` with screenshots.
- ✅ **Deliverable:** A deployed, load-balanced TaskFlow you can put on your resume.
- 🎓 **Course Complete.**
- ⏱️ 90–120 min.

---

# ⭐ Bonus Track — Git Strategy & Deploying on GCP
*Optional, but highly recommended once you've finished Module 9. These take TaskFlow from "runs on my machine / a single host" to "deployed on the cloud the way teams actually do it." Each chunk still fits the 1–2 hour format (the GCP chunks lean toward 90–120 min and may incur small cloud costs — the GCP free tier covers most of it).*

> **Prerequisites:** Module 9 (Docker + Nginx load balancing) and a containerized capstone. For the GCP chunks you'll need a Google Cloud account with billing enabled and the `gcloud` CLI installed.

### Chunk B.1 — Git Strategy & Collaborative Workflows
- 🎯 Work on code the way real teams do — safely and in parallel.
- 📖 **Lecture:** Branching strategies compared (**trunk-based**, **GitHub Flow**, **Git Flow**) and when to use each; feature branches; pull/merge requests & code review; **merge vs. rebase** and a sane default; resolving merge conflicts; conventional/semantic commit messages; tags & releases (SemVer); protecting `main` with branch protection rules; `.gitignore` hygiene and keeping secrets out of history.
- 🧪 **Lab:** Adopt **GitHub Flow** on your TaskFlow repo: create a feature branch, open a PR, do a self-review, resolve a deliberate conflict, squash-merge, and cut a `v1.0.0` release tag. Add branch protection + a PR template.
- ✅ **Deliverable:** A TaskFlow repo with a documented branching strategy (`CONTRIBUTING.md`), a merged PR, branch protection, and a tagged release.
- ⏱️ 60–90 min.

### Chunk B.2 — Deploy the Capstone to GCP (Cloud Run)
- 🎯 Get TaskFlow running on Google Cloud from your Docker images.
- 📖 **Lecture:** GCP fundamentals (projects, billing, IAM, regions); the `gcloud` CLI; **Artifact Registry** for container images; **Cloud Run** for serverless containers (autoscaling, scale-to-zero, request-based billing); environment variables & **Secret Manager**; mapping the FastAPI backend and the Vite frontend to services; the SQLite-in-the-cloud problem (ephemeral filesystems) and the path to **Cloud SQL (Postgres)** or a persistent volume.
- 🧪 **Lab:** Authenticate `gcloud`, create a project + Artifact Registry repo, build and push the backend & frontend images, deploy both to Cloud Run, wire up env vars/secrets, and reach your live public URL.
- ✅ **Deliverable:** A publicly reachable TaskFlow deployed on Cloud Run.
- ⏱️ 90–120 min.

### Chunk B.3 — GCP Load Balancing, Managed Data & CI/CD
- 🎯 Make the GCP deployment scalable, durable, and automatically shipped.
- 📖 **Lecture:** GCP **HTTP(S) Load Balancer** in front of Cloud Run (or multiple instances) — global anycast, health checks, autoscaling vs. the manual Nginx approach from Chunk 9.3 (and how they relate); HTTPS/managed TLS certs and a custom domain; migrating from SQLite to **Cloud SQL (Postgres)** with connection pooling; running migrations in the cloud; **CI/CD with Cloud Build** (or GitHub Actions deploying to GCP) — build → test → deploy on every merge to `main`.
- 🧪 **Lab:** Provision a managed Cloud SQL instance and point TaskFlow at it; put an HTTPS load balancer in front with a managed certificate; add a Cloud Build (or GitHub Actions) pipeline that auto-deploys on merge. Tie it back to the Git strategy from B.1.
- ✅ **Deliverable:** An auto-deploying, load-balanced TaskFlow on GCP with a managed database and HTTPS.
- 🏁 **Bonus Track Complete:** A cloud-native deployment story you can demo and defend in interviews.
- ⏱️ 90–120 min.

---

## Final Outcomes — What You'll Be Able to Do
- Build responsive, accessible UIs with **HTML/CSS/JavaScript**.
- Develop component-based frontends with **React + Vite**.
- Design and build documented REST APIs with **FastAPI**.
- Model and persist data with **SQLite + SQLAlchemy**.
- Implement secure **login/auth** (hashing, JWT, roles).
- Add **structured logging** and observability.
- **Containerize and load-balance** an app for production.
- Ship a **real-world capstone** end to end.
- *(Bonus)* Apply a professional **Git branching strategy** and code-review workflow.
- *(Bonus)* **Deploy to GCP** (Cloud Run, Artifact Registry, load balancing, Cloud SQL) with CI/CD.

## Suggested Repository Layout
```
WebDev_Course/
├── COURSE_STRUCTURE.md        # this file
├── module-00-setup/
├── module-01-html/
├── module-02-css/
├── module-03-javascript/
├── module-04-react-vite/
├── module-05-fastapi/
├── module-06-sqlite/
├── module-07-auth/
├── module-08-logging/
├── module-09-production/
├── capstone-taskflow/
│   ├── frontend/
│   └── backend/
└── bonus-track/
    ├── b1-git-strategy/
    ├── b2-gcp-cloud-run/
    └── b3-gcp-loadbalancing-cicd/
```

## How to Use Each Chunk
1. Read the **Lecture** section's concepts (I can generate full lecture notes per chunk).
2. Do the **Lab** (I can generate step-by-step lab instructions + starter code + solution).
3. Confirm the **Deliverable** exists and works.
4. Commit your work to Git before moving on.

---

*Next step: tell me which chunk to build out first (lecture notes + lab + starter code), or say "start from 0.1" and I'll generate the full materials chunk by chunk.*
