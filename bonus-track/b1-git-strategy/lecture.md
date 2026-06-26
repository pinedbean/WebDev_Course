*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.1 — Git Strategy & Collaborative Workflows

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why teams need a **branching strategy** — not just "everyone pushes to main".
- The three strategies compared: **trunk-based**, **GitHub Flow**, and **Git Flow** — and when to pick each.
- Feature branches, **pull requests**, and code review the way real teams work.
- **Merge vs. rebase** — what each does and a sane default.
- Resolving merge conflicts calmly.
- **Conventional commits**, **SemVer** tags & releases.
- Protecting `main` with branch protection, and keeping secrets out of history.

In the lab you'll adopt **GitHub Flow** on your TaskFlow repo end-to-end: feature branch → PR → conflict → squash-merge → `v1.0.0` tag.

## 1. Why a strategy at all?

Back in Module 0 you learned the Git basics: `commit`, `branch`, `push`. That's enough when you work alone. But TaskFlow is the kind of app a *team* builds, and the moment two people touch the same code, "just push to `main`" stops working:

- Someone pushes a half-finished feature and breaks `main` for everyone.
- Two people edit the same file and overwrite each other's work.
- There's no moment to *review* code before it ships, so bugs and secrets leak in.
- You can't tell which commit is "the version we shipped to users".

A **branching strategy** is a shared agreement about *where work happens, how it gets reviewed, and how it reaches users*. It's the difference between a codebase that scales to a team and one that descends into chaos. The strategy is mostly social (a convention everyone follows), backed by a few technical guardrails (branch protection, CI).

> **📝 The one rule behind all strategies**
>
> main
>
> should
>
> always
>
> be deployable. Whatever lands there is, in principle, ready to ship. Everything risky happens on branches first.

## 2. The mental model: trunk, branches, PRs

Picture a tree. The **trunk** is your long-lived main line — the branch named `main`. A **feature branch** is a short twig that grows off the trunk while you build one thing, then merges back in. A **pull request (PR)** is the formal proposal: "here's my twig — please review and merge it into the trunk."

>

You branch off `main` (commit C), make commits D and E in isolation, open a PR, and once it's approved your work merges back as commit F. Nobody saw your broken intermediate states on `main`; `main` stayed green the whole time.

| Term | Meaning |
| --- | --- |
| **Trunk / `main`** | The single source of truth. Always releasable. |
| **Feature branch** | A short-lived branch for one unit of work (a feature, a fix). |
| **Remote** | The shared copy on GitHub everyone pushes to / pulls from (`origin`). |
| **Pull Request (PR)** | A request to merge a branch into another, with review & discussion attached. (GitLab calls it a Merge Request.) |
| **Code review** | A teammate reading your diff before it merges — catches bugs early. |

## 3. The three strategies, compared

There are three widely-used branching strategies. They differ mainly in *how many long-lived branches* exist and *how features reach production*.

### a) Trunk-Based Development

Everyone commits to `main` (the "trunk") in very small, frequent increments — often via tiny, short-lived branches that merge the same day. There are essentially no long-lived branches. Releases are cut straight from `main`. This requires strong automated testing and feature flags (to hide unfinished work). It's how high-velocity teams (and most big tech) operate.

### b) GitHub Flow

One long-lived branch (`main`) plus short-lived **feature branches**. The loop is simple: branch off `main` → commit → open a PR → review → merge → deploy. `main` is always deployable; you deploy after each merge. This is the sweet spot for small teams, web apps, and continuous deployment — and it's what we'll adopt for TaskFlow.

### c) Git Flow

Many long-lived branches: `main` (released code), `develop` (integration), plus `feature/*`, `release/*`, and `hotfix/*` branches. Powerful but heavy — designed for software with *scheduled, versioned releases* (e.g. desktop apps shipping v2.3 every few months). For a continuously-deployed web app it's usually overkill.

|  | Trunk-Based | GitHub Flow | Git Flow |
| --- | --- | --- | --- |
| Long-lived branches | `main` only | `main` only | `main` + `develop` |
| Branch lifetime | Hours | Hours–days | Days–weeks |
| Release model | Continuous | Continuous | Scheduled / versioned |
| Complexity | Low (needs flags + tests) | Low | High |
| Best for | High-velocity teams, big orgs | Web apps, small teams, SaaS | Released/installed software, mobile/desktop |

> **💡 A sane default**
>
> For almost any modern web app (including TaskFlow), start with
>
> GitHub Flow
>
> . It gives you isolation, review, and continuous deploys without ceremony. Reach for Git Flow only when you genuinely have scheduled versioned releases.

## 4. Feature branches in practice

A feature branch isolates one piece of work. Keep them **small and short-lived** — a branch that lives for three weeks drifts far from `main` and becomes a merge nightmare.

```bash
# start from an up-to-date main
git switch main
git pull origin main

# create and switch to a feature branch
git switch -c feature/task-due-dates

# ...edit files...
git add .
git commit -m "feat(tasks): add due-date field to task model"

# push the branch to GitHub (first push sets the upstream)
git push -u origin feature/task-due-dates
```

Notice the branch *name* describes the work: `feature/task-due-dates`, `fix/login-redirect`, `chore/bump-deps`. A consistent prefix convention makes the branch list readable.

> **📝 `git switch` vs `git checkout`**
>
> Modern Git split the overloaded
>
> checkout
>
> into
>
> git switch
>
> (change branches) and
>
> git restore
>
> (discard file changes). Both still work;
>
> switch
>
> is clearer.
>
> -c
>
> means "create".

## 5. Pull requests & code review

A **pull request** is where your branch is proposed for merging. It bundles: the diff, a description, automated checks (CI), and a conversation. Even solo, PRs are valuable — they give you a moment to re-read your own diff and a clean record of *why* a change happened.

A good PR:

- Is **small** and does *one* thing (easy to review).
- Has a clear title and a description: *what* changed and *why*.
- Passes CI (tests, linting) before anyone reviews it.
- Links the issue it closes (e.g. "Closes #42").

A good **review** is kind and specific: ask questions, suggest, praise good code, and block only on real problems. A **PR template** (a file at `.github/pull_request_template.md`) auto-fills the description box so every PR answers the same questions.

```
# .github/pull_request_template.md
## What & why
<!-- What does this PR change, and why? -->

## How to test
1.

## Checklist
- [ ] Tests pass locally
- [ ] No secrets or .env files committed
- [ ] Updated docs if needed
```

## 6. Merge vs. rebase

Both bring changes from one branch into another, but they shape history differently.

### Merge

A **merge** ties two histories together with a new *merge commit*. Nothing is rewritten — your branch's commits stay exactly as they were. History is truthful but can look like a tangle of merge commits.

>

### Rebase

A **rebase** *replays* your commits on top of the latest `main`, as if you'd branched from there just now. History becomes a clean straight line — but it **rewrites** your commits (new IDs).

>

|  | Merge | Rebase |
| --- | --- | --- |
| History | Preserved, with merge commits | Linear, rewritten |
| Safe on shared branches? | Yes | **No** — never rebase commits others have pulled |
| Good for | Integrating finished branches | Tidying *your own* branch before a PR |

> **⚠️ The golden rule of rebase**
>
> Never rebase commits that you've already pushed and others may have based work on. Rebasing rewrites history; rewriting
>
> shared
>
> history forces painful "force-push" recoveries. Rebase only your own un-shared feature branch.

### A sane default + squash merge

For GitHub Flow, a great default is: **rebase your feature branch onto `main`** to keep it current while you work, then **squash-merge the PR**. A "squash merge" collapses all the messy commits on your branch ("wip", "fix typo", "oops") into one clean commit on `main`. The result is a tidy, linear, one-commit-per-feature history.

```bash
# keep your branch current with main while working
git switch feature/task-due-dates
git fetch origin
git rebase origin/main
# (resolve any conflicts, then:)
git push --force-with-lease   # safe force-push of YOUR branch only
```

`--force-with-lease` is the polite force-push: it refuses to overwrite the remote if someone else pushed in the meantime.

## 7. Resolving merge conflicts

A **conflict** happens when two branches changed the *same lines* of the same file and Git can't decide which to keep. It's not an error — it's Git asking *you* to choose. Git marks the spot:

```javascript
<<<<<<< HEAD
const PAGE_SIZE = 20;        // your current branch's version
=======
const PAGE_SIZE = 50;        // the incoming branch's version
>>>>>>> main
```

To resolve: open the file, decide what the final lines should be, delete the `<<<` / `===` / `>>>` markers, then stage and continue:

```bash
# after editing the file to the version you want:
git add src/config.js
git rebase --continue      # if you were rebasing
# or
git commit                 # if you were merging
```

> **💡 Conflicts are routine**
>
> Conflicts feel scary the first time, but they're a normal part of collaboration. Small, frequent merges = small, easy conflicts. Long-lived branches = giant, painful ones. Keep branches short.

## 8. Conventional commits

A commit message is documentation. **Conventional Commits** is a simple, widely-adopted format that makes history readable and even *machine-readable* (tools can auto-generate changelogs and version bumps from it):

```
<type>(optional scope): <short summary>

feat(tasks): add due-date field to tasks
fix(auth): reject expired JWTs with 401
docs(readme): add local setup instructions
chore(deps): bump fastapi to 0.115
refactor(api): extract pagination helper
test(projects): cover membership permission checks
```

| Type | Use for |
| --- | --- |
| `feat` | A new feature (user-visible). |
| `fix` | A bug fix. |
| `docs` | Documentation only. |
| `refactor` | Code change that neither fixes a bug nor adds a feature. |
| `test` | Adding or fixing tests. |
| `chore` | Tooling, deps, config — no production code change. |

The summary is imperative ("add", not "added"), lowercase, and under ~50 characters. A `!` after the type (e.g. `feat!:`) or a `BREAKING CHANGE:` footer flags a breaking change — which matters for versioning, next.

## 9. Tags & SemVer releases

A **tag** is a permanent label on a specific commit — usually marking a release. Unlike a branch, a tag never moves. **Semantic Versioning (SemVer)** gives tags meaning with three numbers: `MAJOR.MINOR.PATCH`.

| Part | Bump when… | Example |
| --- | --- | --- |
| **MAJOR** | You make a breaking change. | 1.4.2 → **2**.0.0 |
| **MINOR** | You add a feature, backward-compatible. | 1.4.2 → 1.**5**.0 |
| **PATCH** | You fix a bug, backward-compatible. | 1.4.2 → 1.4.**3** |

Your first stable release is `v1.0.0`. Create an **annotated** tag (it stores a message, author, and date — better than a lightweight tag):

```bash
git tag -a v1.0.0 -m "TaskFlow 1.0.0 — first public release"
git push origin v1.0.0      # tags aren't pushed by default
```

On GitHub, a tag can be turned into a **Release** with notes and downloadable artifacts. Notice how conventional commits feed this: `feat` commits → MINOR bump, `fix` → PATCH, `feat!` → MAJOR.

## 10. Branch protection

The strategy is a social agreement — **branch protection rules** are the technical enforcement. On GitHub (Settings → Branches → Add rule for `main`) you can require that:

- Changes to `main` arrive **only through a PR** — no direct pushes.
- The PR has at least one **approving review**.
- **Status checks pass** (CI green) before merging.
- The branch is **up to date** with `main` before merging.
- Even admins follow the rules ("Do not allow bypassing").

This is what guarantees "`main` is always deployable" isn't just a hope. In B.3 you'll wire CI/CD so that a green `main` auto-deploys — branch protection is what keeps that pipeline safe.

## 11. `.gitignore` hygiene & keeping secrets out of history

Some files must **never** be committed: secrets (`.env`, API keys, service-account JSON), dependency folders (`node_modules`), build output (`dist/`), and local databases (`*.db`). A `.gitignore` file tells Git to ignore them:

```bash
# .gitignore — TaskFlow
# secrets & env
.env
.env.*
*-key.json
service-account*.json

# python
__pycache__/
.venv/
*.db

# node / vite
node_modules/
dist/

# os
.DS_Store
```

> **⚠️ Git never forgets**
>
> If you commit a secret, deleting it in a
>
> later
>
> commit does
>
> not
>
> remove it — it lives forever in history and anyone with the repo can recover it. The only real fixes are: (1)
>
> rotate the secret immediately
>
> (assume it's burned), and (2) rewrite history with a tool like
>
> git filter-repo
>
> or BFG. Prevention beats cure: ignore secrets
>
> before
>
> the first commit, and consider a pre-commit secret scanner.

The pattern you'll use everywhere: commit a `.env.example` with the *names* of the variables (no values), so teammates know what to set, while the real `.env` stays ignored.

## ✅ Recap

- A **branching strategy** keeps `main` always-deployable while many people work in parallel.
- **GitHub Flow** (one `main` + short feature branches + PRs) is the sane default for web apps like TaskFlow.
- **PRs + code review** catch problems early; a PR template keeps them consistent.
- **Merge** preserves history; **rebase** linearizes it but rewrites commits — never rebase shared history. Squash-merge for a clean trunk.
- Conflicts are normal; resolve by choosing the final lines and removing the markers.
- **Conventional commits** + **SemVer** tags make history meaningful; `v1.0.0` is your first stable release.
- **Branch protection** enforces the strategy; `.gitignore` keeps secrets out — and rotate any secret that slips in.

**Next:** open `assignment.html` and adopt GitHub Flow on your TaskFlow repo for real.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
