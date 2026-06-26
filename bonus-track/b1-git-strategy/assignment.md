*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.1 — Lab: Adopt GitHub Flow on TaskFlow

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Turn your TaskFlow repo into one that follows a real team workflow. You'll document a branching strategy in `CONTRIBUTING.md`, do a full **GitHub Flow** cycle (feature branch → PR → self-review → deliberately resolve a conflict → squash-merge), protect `main`, add a PR template, and cut a **v1.0.0** release tag.

## Prerequisites

- You finished **Module 9** and have a containerized **TaskFlow** repo (`capstone-taskflow/` with backend + frontend).
- The repo is on **GitHub** (push it if it's only local). A free personal account is fine.
- Git installed and configured (`git --version`, `git config user.name` set).
- You read the lecture — you know merge vs. rebase, conventional commits, and SemVer.

> **⚠️ Try it yourself first**
>
> Work through the steps from the lecture and your own knowledge. Only open
>
> solution.html
>
> when you're stuck or to compare at the end.

## Tasks

### 1 Document the strategy in `CONTRIBUTING.md`

On `main`, add a `CONTRIBUTING.md` to your repo root that states: you use **GitHub Flow**; branch naming (`feature/*`, `fix/*`, `chore/*`); that all changes go through a PR with one approval and green CI; that commits follow **Conventional Commits**; and that releases use **SemVer** tags. Commit it with a conventional message.

### 2 Add a `.gitignore` + PR template

Make sure `.gitignore` excludes secrets and junk (`.env`, `__pycache__/`, `node_modules/`, `dist/`, `*.db`, `.DS_Store`). Add `.github/pull_request_template.md` with "What & why / How to test / Checklist" sections. Commit and push to `main` (this is your last direct push — see step 5).

### 2.5 Plant a conflict seed (so step 4 has a conflict to resolve)

Add a line to your `README.md` on `main` — e.g. a `## Status` heading with a sentence. Commit and push to `main`. You'll edit the *same* line differently on your feature branch to create a deliberate conflict.

### 3 Create a feature branch & make a change

Branch off an up-to-date `main` as `feature/<something-real>` (e.g. `feature/readme-badges`). Make a small, real improvement and **edit the same README line** from step 2.5 to a different value. Make 2–3 commits with conventional messages, then push the branch with `-u`.

### 4 Open a PR, self-review, and resolve the conflict

On GitHub, open a Pull Request from your feature branch into `main`. Fill in the template. Read your own diff line by line and leave at least one review comment on yourself. Bring your branch up to date with `main` (rebase or merge) — you'll hit the conflict on the README line. Resolve it locally, finish, and push.

### 5 Turn on branch protection, then squash-merge

In repo Settings → Branches, add a protection rule for `main`: require a PR before merging, require it be up to date, and (if available on your plan) require an approving review. Then **squash-merge** your PR and delete the branch.

> **📝 Solo-account note**
>
> On a free personal repo you can't "approve" your own PR. That's fine — require the PR + up-to-date checks, and still do the self-review in comments. The solution explains the exact toggles.

### 6 Cut the `v1.0.0` release tag

Back on an updated local `main`, create an **annotated** tag `v1.0.0` with a message, push the tag, and (optional) publish a GitHub Release from it with short notes.

## ✅ Deliverable — acceptance checklist

- `CONTRIBUTING.md` documents GitHub Flow, branch naming, PR rules, conventional commits, and SemVer.
- `.gitignore` excludes secrets/junk and `.github/pull_request_template.md` exists.
- A feature branch was created and pushed to GitHub.
- A PR was opened with the template filled in and at least one self-review comment.
- A real merge conflict was created and **resolved** (markers removed, change kept intentionally).
- The PR was **squash-merged** into `main` and the branch deleted.
- **Branch protection** is enabled on `main` (PR required before merge).
- An annotated `v1.0.0` tag exists on `main` and is pushed to GitHub.

## 🚀 Stretch goals (optional)

- Add a tiny **GitHub Actions CI** workflow (lint/test) and make it a *required status check* in branch protection.
- Add a `CODEOWNERS` file so PRs request review automatically.
- Install a pre-commit secret scanner (e.g. `gitleaks`) and run it once over your repo.
- Practice an interactive rebase to squash your branch's commits *before* opening the PR.
- Write release notes that group changes by conventional-commit type (Features / Fixes / Chores).

> **💡 Where this is going**
>
> The branch protection + green-
>
> main
>
> habit you build here is exactly what B.3's CI/CD pipeline relies on: every merge to
>
> main
>
> will auto-deploy to GCP. Get the workflow solid now.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
