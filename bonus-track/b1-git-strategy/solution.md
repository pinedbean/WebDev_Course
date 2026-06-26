*Full-Stack Web Dev · ⭐ Bonus Track — Git Strategy & GCP*

# Chunk B.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Each step gives the exact commands, the files to create, expected output, and troubleshooting. Run everything from the root of your TaskFlow repo. Replace `YOUR-USER` and `taskflow` with your GitHub username and repo name.

> **📝 Interactive logins happen in your terminal**
>
> Anything that opens a browser (GitHub auth via
>
> gh auth login
>
> , approving a device code) happens in
>
> your own
>
> terminal/browser. Commands below assume you're already authenticated to push to GitHub.

### 1 Document the strategy in `CONTRIBUTING.md`

Make sure `main` is current, then create the file:

```bash
cd capstone-taskflow        # your repo root
git switch main
git pull origin main
```

Create `CONTRIBUTING.md`:

```
# Contributing to TaskFlow

## Branching strategy: GitHub Flow
- `main` is always deployable. Never push directly to it.
- Do all work on short-lived branches off `main`:
  - `feature/<name>` — new functionality
  - `fix/<name>`     — bug fixes
  - `chore/<name>`   — tooling, deps, config
- Open a Pull Request into `main`. Keep PRs small and focused.
- A PR merges only when: CI is green, the branch is up to date
  with `main`, and it has at least one approving review.
- We **squash-merge** so `main` has one clean commit per change.

## Commit messages: Conventional Commits
`<type>(scope): summary` — e.g. `feat(tasks): add due dates`.
Types: feat, fix, docs, refactor, test, chore.

## Releases: Semantic Versioning
Tags are `vMAJOR.MINOR.PATCH` (e.g. `v1.0.0`).
- feat → MINOR, fix → PATCH, breaking change → MAJOR.

## Secrets
Never commit `.env` or key files. Use `.env.example` for names only.
```

```bash
git add CONTRIBUTING.md
git commit -m "docs(repo): document GitHub Flow branching strategy"
```

### 2 `.gitignore` + PR template

Ensure `.gitignore` at the repo root covers secrets and junk (append if it already exists):

```bash
# secrets & env
.env
.env.*
!.env.example
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

Create the PR template at `.github/pull_request_template.md`:

```bash
mkdir -p .github
```

```
## What & why
<!-- What does this PR change, and why? -->

## How to test
1.

## Checklist
- [ ] Tests pass locally
- [ ] No secrets or .env files committed
- [ ] Updated docs if needed
```

```bash
git add .gitignore .github/pull_request_template.md
git commit -m "chore(repo): add gitignore rules and PR template"
git push origin main
```

### 2.5 Plant the conflict seed

Add a `## Status` line to `README.md` on `main` — this is the line we'll change differently on the branch:

```bash
# append to README.md, then:
git add README.md
git commit -m "docs(readme): add status section"
git push origin main
```

For example the new lines in `README.md`:

```
## Status
TaskFlow is in active development.
```

### 3 Feature branch & a real change

```bash
git switch -c feature/readme-badges
```

Make a real improvement (e.g. add a tech-stack section to the README) **and** change that same Status line to something different, so it conflicts with `main`:

```
## Status
TaskFlow v1 is ready for its first release. 🚀
```

Commit in small steps with conventional messages, then push and set upstream:

```bash
git add README.md
git commit -m "docs(readme): add tech stack section"
git commit -am "docs(readme): mark v1 ready in status"   # second small commit
git push -u origin feature/readme-badges
```

> **💡 `-am`**
>
> git commit -am "..."
>
> stages all
>
> tracked
>
> file changes and commits in one go. Use it once files already exist; new files still need
>
> git add
>
> first.

### 4 Open the PR, self-review, resolve the conflict

**Open the PR.** Either click the "Compare & pull request" banner GitHub shows after a push, or use the CLI:

```
gh pr create --base main --head feature/readme-badges \
  --title "docs: README tech stack + v1 status" \
  --body "Adds a tech-stack section and marks v1 ready."
```

**Self-review:** open the PR's "Files changed" tab and leave at least one comment on a line of your own diff (e.g. "Consider linking each tool to its docs"). This builds the review habit.

**Now resolve the conflict.** Bring your branch up to date with `main`. Using rebase (recommended for your own branch):

```bash
git fetch origin
git rebase origin/main
```

Git stops on the README conflict. Open `README.md` — you'll see:

```
<<<<<<< HEAD
TaskFlow is in active development.
=======
TaskFlow v1 is ready for its first release. 🚀
>>>>>>> (your commit)
```

Edit it to the final version you want (keep the v1 line), delete all three marker lines, then continue:

```bash
git add README.md
git rebase --continue
git push --force-with-lease     # update the PR with the rebased branch
```

> **⚠️ During a rebase**
>
> Rebase replays each commit, so a conflict can appear more than once. Resolve,
>
> git add
>
> ,
>
> git rebase --continue
>
> each time. To bail out entirely:
>
> git rebase --abort
>
> . Prefer rebase only because this is
>
> your own
>
> un-shared branch.

Prefer merge instead of rebase? This also works and avoids force-push:

```bash
git merge origin/main      # resolve the same conflict, then:
git add README.md
git commit                 # completes the merge
git push
```

### 5 Branch protection, then squash-merge

**Branch protection** (GitHub UI): repo → *Settings → Branches → Add branch ruleset* (or "Add rule") targeting `main`. Enable:

- ✅ Require a pull request before merging
- ✅ Require branches to be up to date before merging
- ✅ Require status checks to pass *(once you add CI — stretch goal)*
- ✅ Require approvals: 1 *(see note below for solo repos)*

> **📝 Solo personal repo**
>
> GitHub won't let you approve your own PR. Either: leave "Require approvals"
>
> off
>
> (keep "Require a PR" on — you still can't push directly to
>
> main
>
> ), or set the repo to an Organization where a second account can approve. The point of the exercise is that
>
> main
>
> is no longer directly pushable.

**Squash-merge** the PR. In the UI, click the merge dropdown → "Squash and merge" → confirm → "Delete branch". Or via CLI:

```
gh pr merge --squash --delete-branch
```

Expected: the PR shows "Merged", your branch is gone, and `main` has *one* new commit containing the whole feature.

### 6 Cut the `v1.0.0` release tag

Sync local `main`, then create and push an annotated tag:

```bash
git switch main
git pull origin main
git tag -a v1.0.0 -m "TaskFlow 1.0.0 — first public release"
git push origin v1.0.0
```

Verify:

```bash
git tag                    # lists v1.0.0
git show v1.0.0 --stat     # shows the tag message + the commit it points to
```

Optionally publish a GitHub Release from the tag:

```
gh release create v1.0.0 --title "TaskFlow v1.0.0" \
  --notes "First public release: auth, projects, tasks, load-balanced Docker stack."
```

## 📄 Quick reference — the whole flow

```bash
# once, on main
git switch main && git pull origin main

# per change
git switch -c feature/my-change
# ...edit, commit with conventional messages...
git push -u origin feature/my-change
gh pr create --base main --fill          # open PR

# keep current with main (resolve conflicts if any)
git fetch origin && git rebase origin/main
git push --force-with-lease

# merge + clean up
gh pr merge --squash --delete-branch

# release
git switch main && git pull origin main
git tag -a v1.0.0 -m "..." && git push origin v1.0.0
```

## 🛠️ Troubleshooting

| Symptom | Fix |
| --- | --- |
| `! [rejected] ... (fetch first)` on push | Remote moved on. `git fetch origin` then rebase/merge before pushing. |
| `--force-with-lease` rejected | Someone (or you, elsewhere) pushed to the branch. Re-fetch, re-rebase, then push again. Never use plain `--force`. |
| Accidentally committed `.env` | Rotate the secret immediately. Then remove it from history with `git filter-repo` / BFG and add it to `.gitignore`. |
| Can't merge — "branch out of date" | That's branch protection working. Update the branch (rebase/merge `main`), push, then merge. |
| Tag pushed to wrong commit | `git tag -d v1.0.0`, `git push origin :refs/tags/v1.0.0` to delete remotely, re-tag the right commit, push again. |
| `gh: command not found` | Install GitHub CLI (`brew install gh`) and run `gh auth login` in your terminal — or just use the GitHub web UI. |

## 🎉 You're done

Your TaskFlow repo now works like a real team's: a documented strategy in `CONTRIBUTING.md`, a PR template, protected `main`, a clean squash-merged history, and a tagged `v1.0.0` release.

This is the backbone B.3 will build on: when you add CI/CD, *every merge to a protected, green `main` auto-deploys to GCP*. The discipline you set up here is what makes that safe.

**Up next → Chunk B.2: Deploy the Capstone to GCP (Cloud Run).**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
