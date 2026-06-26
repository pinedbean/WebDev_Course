*Full-Stack Web Dev · Module 0 — Setup & Tooling*

# Chunk 0.2 — Solution (Step-by-Step)

**✅ SOLUTION** · **macOS-first, with Windows/Linux notes**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## Make sure Git is installed

```
git --version
```

```bash
git version 2.39.3 (Apple Git-145)
```

macOS If it's missing, macOS will prompt to install the Command Line Tools — accept it, or run `brew install git`.  
 Windows Install [Git for Windows](https://git-scm.com/download/win) and use **Git Bash**.  
 Linux `sudo apt install git`.

### 1 Warm up: navigate the filesystem

```bash
pwd                 # where am I?
ls -la ~            # list home folder, including hidden files
cd ~/Desktop/webdev-course
cd ..               # up one level (now in Desktop)
cd webdev-course    # back into the project
mkdir notes         # create the notes folder
ls                  # confirm "notes" and "versions.txt" are here
```

You should see `notes` and `versions.txt` listed.

### 2 Tell Git who you are

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Make "main" the default branch name for new repos:
git config --global init.defaultBranch main

# Verify:
git config --global --list
```

> **💡 Tip**
>
> Use the same email you'll register on GitHub — that way GitHub links your commits to your profile.

### 3 Initialize the repo & first commit

From inside `webdev-course`, create a README. You can do it in VS Code, or from the terminal:

```bash
# Create a README with a couple of lines
printf "# WebDev Course\n\nMy work for the full-stack web development course.\n" > README.md

git init
git status
```

`git status` shows untracked files (in red):

```
On branch main
No commits yet
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md
        notes/
        versions.txt
```

Now stage everything and commit:

```bash
git add .
git commit -m "Initial commit: add README, versions, notes folder"
```

```
[main (root-commit) a1b2c3d] Initial commit: add README, versions, notes folder
 3 files changed, 8 insertions(+)
```

> **📝 Note**
>
> An empty folder won't be tracked by Git on its own. If
>
> notes/
>
> doesn't show up, add a file inside it (e.g.
>
> touch notes/day1.md
>
> ) and it will.

### 4 Make at least 3 commits

```bash
# Commit 2 — add a .gitignore
printf ".DS_Store\nnode_modules/\n" > .gitignore
git add .gitignore
git commit -m "Add .gitignore for OS and node files"

# Commit 3 — add a learning note
printf "# Day 1\nFinished Module 0 setup.\n" > notes/day1.md
git add notes/day1.md
git commit -m "Add day 1 learning notes"

# Review the history
git log --oneline
```

`git log --oneline` shows three commits:

```
c3d4e5f Add day 1 learning notes
b2c3d4e Add .gitignore for OS and node files
a1b2c3d Initial commit: add README, versions, notes folder
```

### 5 Create the GitHub repo

1. Sign up / log in at `github.com`.
2. Click the **+** (top-right) → **New repository**.
3. Repository name: `webdev-course`.
4. Leave it **empty** — do NOT tick "Add a README", ".gitignore", or "license" (you already have these locally; adding them now causes a conflict).
5. Click **Create repository**.

GitHub shows you a page with a URL like `https://github.com/yourname/webdev-course.git`. Keep it handy.

### 6 Connect the remote & push

```bash
# Link your local repo to GitHub (use YOUR url)
git remote add origin https://github.com/yourname/webdev-course.git

# Push your "main" branch and remember the connection (-u)
git push -u origin main
```

The first push over HTTPS asks you to authenticate. Your account password will **not** work — use a **Personal Access Token**:

> **⚠️ Authenticating the push**
>
> On GitHub:
>
> Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
>
> . Give it
>
> repo
>
> scope, copy the token, and paste it when the terminal asks for your "password". (On macOS it's then saved in Keychain, so you won't be asked again.)

A successful push looks like:

```
Enumerating objects: 6, done.
...
To https://github.com/yourname/webdev-course.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

Refresh the GitHub repo page — your `README.md`, `versions.txt`, and `notes/` are now online. 🎉

## Stretch goal: use SSH instead of tokens (optional)

```bash
# Generate a key (press Enter through the prompts)
ssh-keygen -t ed25519 -C "you@example.com"

# Copy the PUBLIC key to your clipboard (macOS)
pbcopy < ~/.ssh/id_ed25519.pub
```

Then on GitHub: **Settings → SSH and GPG keys → New SSH key**, paste, save. Switch your remote to SSH:

```bash
git remote set-url origin git@github.com:yourname/webdev-course.git
git push
```

## 🎉 You're done — and Module 0 is complete!

- ✅ Comfortable navigating the terminal.
- ✅ Git configured; `webdev-course` is a repo with 3+ commits.
- ✅ Code pushed to a GitHub repo named `webdev-course`.

From now on, after finishing each chunk's lab: `git add .` → `git commit -m "Finish chunk X.Y"` → `git push`. Building this habit is half of being a professional developer.

**Up next → Module 1: HTML Foundations**, where you build your first real web pages.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
