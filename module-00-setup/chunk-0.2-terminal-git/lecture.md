*Full-Stack Web Dev · Module 0 — Setup & Tooling*

# Chunk 0.2 — Terminal & Git Basics

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- How to **navigate the filesystem** from the terminal (`pwd`, `ls`, `cd`, `mkdir`).
- The difference between **absolute** and **relative** paths.
- What **Git** is and the mental model: *working directory → staging → commit*.
- What **GitHub** is and how `push` connects your computer to the cloud.

In the lab you'll put your `webdev-course` folder under version control and push it to GitHub.

## 1. The terminal: talking to your computer with text

The terminal (a.k.a. the command line or shell) lets you tell the computer what to do by typing commands instead of clicking. Developers live here because it's fast, scriptable, and many tools *only* have a command-line interface.

Your shell on macOS is **zsh**. At all times you are "standing" in some folder — your **current working directory**. The core navigation commands:

| Command | Stands for | What it does |
| --- | --- | --- |
| `pwd` | print working directory | Shows the folder you're currently in. |
| `ls` | list | Lists files & folders here. `ls -la` shows hidden files too. |
| `cd folder` | change directory | Move into `folder`. |
| `cd ..` | — | Move *up* one level to the parent folder. |
| `mkdir name` | make directory | Create a new folder called `name`. |
| `touch file.txt` | — | Create an empty file. |
| `mv` / `cp` / `rm` | move / copy / remove | Move (or rename), copy, or delete files. |

> **⚠️ rm is forever**
>
> rm
>
> deletes immediately — there's no Trash/Recycle Bin to recover from. Double-check before you delete anything, especially with
>
> rm -r
>
> (which deletes a whole folder).

## 2. Paths: absolute vs relative

A **path** is an address for a file or folder.

- **Absolute path** — starts from the root of the disk. On macOS it begins with `/`, e.g. `/Users/you/Desktop/webdev-course`. `~` is shorthand for your home folder.
- **Relative path** — starts from wherever you currently are. `.` means "here", `..` means "one level up", and `subfolder/file.txt` means "into subfolder from here".

```
cd ~/Desktop/webdev-course   # absolute-ish (~ = home)
cd ..                        # go up one level
cd ./notes                   # relative: into "notes" from here
```

## 3. What is Git?

**Git** is a *version control system*. It takes snapshots of your project so you can: see exactly what changed and when, go back to an earlier working version, and collaborate without overwriting each other's work. Think of it as an infinite, organized "undo history" for your whole project.

The key idea is the **three areas** a file moves through:

> Working Directoryyour edited files  →  — git add →  →  Staging Areachanges to include  →  — git commit →  →  Repositorysaved snapshot

1. You edit files in your **working directory**.
2. `git add` moves the changes you choose into the **staging area** ("I want these in my next snapshot").
3. `git commit` permanently records the staged changes as a snapshot with a message.

The everyday Git commands:

| Command | What it does |
| --- | --- |
| `git init` | Start tracking the current folder with Git. |
| `git status` | Show what's changed / staged. Run this constantly. |
| `git add .` | Stage all changed files. |
| `git commit -m "message"` | Save a snapshot with a description. |
| `git log` | Show the history of commits. |

> **💡 Good commit messages**
>
> Write what the change does, in the present tense:
>
> "Add contact form"
>
> , not
>
> "stuff"
>
> . Your future self will thank you.

## 4. Branches (the mental model)

A **branch** is an independent line of work. The default branch is usually called `main`. You can create a branch to build a feature without disturbing `main`, then merge it back when it's ready. We'll keep it simple for now and work mostly on `main` — full branching strategy comes in the **Bonus Track (B.1)**. For today, just know branches exist and that `main` is your primary line.

## 5. GitHub: Git in the cloud

**Git** runs on your computer. **GitHub** is a website that hosts Git repositories online — a backup, a portfolio, and a place to collaborate. The link between them:

> Your computerlocal repo  →  — git push →  →  GitHubremote repo  →  ← git pull —  →  Your computer

- `git push` uploads your local commits to GitHub.
- `git pull` downloads commits from GitHub to your computer.
- A **remote** named `origin` is the connection to your GitHub repo.

> **📝 Note**
>
> GitHub no longer accepts your account password for pushing over HTTPS. You'll authenticate with a
>
> Personal Access Token
>
> or SSH key — the solution walks you through it.

## ✅ Recap

- Navigate with `pwd`, `ls`, `cd`, `mkdir`; understand absolute vs relative paths.
- Git tracks snapshots through three areas: **working dir → staging (`add`) → commit**.
- Daily flow: `git status` → `git add .` → `git commit -m "…"`.
- **GitHub** hosts your repo online; `git push` uploads, `git pull` downloads.

**Next:** open `assignment.html` and put your course folder on GitHub. Stuck? `solution.html` has every command.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
