*Full-Stack Web Dev · Module 0 — Setup & Tooling*

# Chunk 0.2 — Lab: Version-Control Your Course Folder

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Practice navigating the terminal, then put your `webdev-course` folder under Git, make several commits, create a GitHub repository, and push your work online.

## Before you start — prerequisites

- You completed Chunk 0.1 and have a `webdev-course` folder with `versions.txt` in it.
- Git installed. Check with `git --version` — if it's missing, the solution shows how to install it.
- An email you can use to sign up for GitHub.

## Tasks

### 1 Warm up: navigate the filesystem

Using only the terminal, do each of these and observe the output:

- Print where you are with `pwd`.
- List the contents of your home folder, including hidden files.
- `cd` into your `webdev-course` folder, then go up one level, then back in.
- Create a folder called `notes` inside `webdev-course`.

### 2 Tell Git who you are (first-time setup)

Configure your name and email so your commits are attributed to you. (You only do this once per machine.)

### 3 Initialize a repository & make your first commit

Inside `webdev-course`:

- Add a `README.md` file describing what this repo is.
- Run `git init`.
- Check `git status` — notice your files are "untracked".
- Stage everything and commit it with a clear message.

### 4 Make at least 3 commits total

Make a couple more small changes, committing after each, so your history has **3 or more commits**. Ideas: add a line to the README, create a `.gitignore`, add a note in the `notes` folder. Confirm with `git log`.

### 5 Create a GitHub account & an empty repo

Sign up at `github.com` (if you haven't), then create a **new repository** named `webdev-course`. Don't add a README from GitHub's side (you already have one locally).

### 6 Connect the remote & push

Link your local repo to the GitHub repo (the `origin` remote) and `git push` your commits. Refresh the GitHub page — your files should appear.

## ✅ Deliverable — acceptance checklist

- You can navigate with `pwd`, `ls -la`, and `cd` confidently.
- `git config` shows your name and email set.
- Your `webdev-course` folder is a Git repo with a `README.md`.
- `git log` shows **3 or more** commits with meaningful messages.
- A GitHub repo named `webdev-course` exists and shows your files.
- `git push` succeeded and the latest commit is visible on GitHub.

## 🚀 Stretch goals (optional)

- Add a `.gitignore` that ignores OS junk like `.DS_Store` and `node_modules/`.
- Set up an **SSH key** so you don't have to enter a token every push.
- Create a branch with `git switch -c experiment`, make a commit, then merge it back into `main`.
- Edit the README on GitHub's website, then `git pull` the change down to your computer.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
