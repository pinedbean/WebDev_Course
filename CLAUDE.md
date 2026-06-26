# CLAUDE.md — Project Guide for This Course

This repository is a **self-paced full-stack web development course**, authored chunk by chunk.
This file tells Claude (and any contributor) how the course is built and how to keep it consistent.

## What this project is
A structured course that teaches: **HTML · CSS · JavaScript · React + Vite · FastAPI · SQLite · Auth · Logging · Load Balancing**, ending in a real-world capstone (**TaskFlow**) plus a bonus track (**Git strategy + GCP deployment**).

- Full curriculum: see [`COURSE_STRUCTURE.md`](./COURSE_STRUCTURE.md).
- Live progress: see [`course_progress_tracking.md`](./course_progress_tracking.md).
- The learner studies **1–2 hours/day**, one **chunk** per session.

## ✅ The Golden Rules (read before generating any chunk)

1. **Build ONE module at a time** (all of that module's chunks in a single pass). Never batch-generate multiple modules. Finish every chunk in the module completely, update the tracker, then stop and let the learner review before moving to the next module.
2. **Every chunk produces exactly three HTML files** (see below). Lecture and assignment **must be HTML**, and every lab gets an HTML **solution** with step-by-step instructions.
3. **After finishing a chunk, update `course_progress_tracking.md`** (mark Lecture / Assignment / Solution as ✅ and set the chunk status).
4. **Beginner-first.** Assume no prior knowledge unless an earlier chunk taught it. Explain the "why", not just the "how".
5. **macOS / zsh is the primary environment** (the learner is on macOS). Provide macOS commands first; add Windows/Linux notes where they differ.

## Per-chunk deliverables

Each chunk lives in its own folder and contains **three self-contained HTML files**:

```
module-XX-name/
└── chunk-X.Y-slug/
    ├── lecture.html      # 📖 The teaching material (concepts + worked examples)
    ├── assignment.html   # 🧪 The lab/assignment the learner does themselves
    └── solution.html     # ✅ Step-by-step solution to the assignment
```

### File responsibilities
- **`lecture.html`** — Concepts, diagrams, worked examples, "why it matters". Ends with a short recap and a pointer to the assignment.
- **`assignment.html`** — Clear objective, prerequisites, numbered tasks, an explicit **Deliverable / acceptance checklist**, and optional stretch goals. It does NOT give away the answers.
- **`solution.html`** — A complete **step-by-step** walkthrough: each step states what to do, the exact command/code, the expected result, and common troubleshooting. This is the answer key.

### Folder & naming conventions
- Module folders: `module-00-setup`, `module-01-html`, … `module-10-capstone`, `bonus-track`.
- Chunk folders: `chunk-<num>-<kebab-slug>` (e.g. `chunk-0.1-dev-environment`).
- Capstone code lives under `capstone-taskflow/{frontend,backend}`.
- Bonus chunks: `bonus-track/b1-git-strategy`, `b2-gcp-cloud-run`, `b3-gcp-loadbalancing-cicd`.

## HTML authoring conventions
- Each HTML file is **self-contained**: it embeds its own `<style>` so it renders correctly when double-clicked / opened directly in a browser (no build step, no external dependencies).
- Reuse the **same embedded stylesheet and page layout** across all files for a consistent look (header banner → content → footer nav). Copy the style block from an existing chunk (e.g. `module-00-setup/chunk-0.1-dev-environment/lecture.html`) when creating a new file.
- Standard structure of every file:
  - A header banner showing the **course name**, **module/chunk number**, and **file type** (Lecture / Assignment / Solution).
  - Semantic content (`<main>`, `<section>`, headings).
  - Callout boxes via CSS classes: `.note`, `.tip`, `.warning`, `.task`, `.deliverable`.
  - Code shown in `<pre><code>` blocks.
  - A footer with simple links to the sibling files (Lecture ↔ Assignment ↔ Solution).
- Keep it **accessible**: real headings, `alt` text, sufficient contrast, `lang="en"`, viewport meta.
- No external CDNs/fonts required — use a system font stack so files work offline.

## Workflow for creating a module (do this every time)
1. Confirm which module to build (the next module with ⬜ chunks in `course_progress_tracking.md`, unless told otherwise).
2. For **each chunk** in that module, in order:
   - Create the chunk folder.
   - Write `lecture.html`, then `assignment.html`, then `solution.html` — consistent style, beginner-friendly.
3. Keep continuity across the module: later chunks build on earlier ones, and each module ends with its 🏁 Checkpoint mini-project (per `COURSE_STRUCTURE.md`).
4. Update `course_progress_tracking.md` for every chunk built (Lecture/Assignment/Solution ✅, build status, completion date) and refresh the Summary counts.
5. Briefly summarize the whole module and **stop for review** before the next module.

## Tech versions to assume (teach current, stable tooling)
- Node.js LTS (20.x or newer), npm.
- Python 3.11+.
- Vite 5+, React 18+, React Router 6+.
- FastAPI + Uvicorn, Pydantic v2, SQLAlchemy 2.x, Alembic.
- Docker + Docker Compose, Nginx.
- GCP: `gcloud` CLI, Cloud Run, Artifact Registry, Cloud SQL, Cloud Build.

## What NOT to do
- ❌ Don't generate multiple modules in one pass (one module per pass is the unit; all chunks within it is expected).
- ❌ Don't put lecture/assignment content in Markdown — those must be HTML.
- ❌ Don't skip the solution file or leave it without step-by-step detail.
- ❌ Don't introduce a concept the learner hasn't been taught yet without explaining it.
- ❌ Don't forget to update the progress tracker.
