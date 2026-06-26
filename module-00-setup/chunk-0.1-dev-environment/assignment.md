*Full-Stack Web Dev · Module 0 — Setup & Tooling*

# Chunk 0.1 — Lab: Set Up Your Environment

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Install every tool you'll use in this course, confirm each one works from the terminal, and record the versions in a file called `versions.txt`. By the end you'll have a developer machine that's ready to build.

## Before you start — prerequisites

- A computer you can install software on (admin rights).
- An internet connection.
- About 45–75 minutes. Downloads can take a while — that's normal.

> **⚠️ Don't peek yet**
>
> Try each task on your own first. Only open
>
> solution.html
>
> if you get stuck — that's where the exact commands and troubleshooting live.

## Tasks

### 1 Install Node.js (LTS)

Install the **LTS** version of Node.js (20.x or newer). This also installs `npm`.

**Verify it:** open a terminal and confirm both commands print a version number.

```bash
node --version
npm --version
```

### 2 Install Python 3.11+

Install Python version **3.11 or newer**. Confirm it runs from the terminal.

```bash
python3 --version
pip3 --version
```

### 3 Install VS Code + 3 extensions

Install **Visual Studio Code**, then add these extensions from the Extensions panel:

- **Prettier** – Code formatter
- **ESLint**
- **Python** (by Microsoft)

**Bonus:** enable the `code` command so you can open folders from the terminal with `code .`

### 4 Set up a browser with DevTools

Make sure you have **Chrome** or **Firefox** installed. Open any website, right-click anywhere, and choose **Inspect**. Find these three tabs and click each one: **Elements**, **Console**, **Network**.

### 5 Create your project folder

Create a folder for your course work somewhere sensible (e.g. your Desktop), and open it in VS Code.

### 6 Record your versions in `versions.txt`

Inside your project folder, create a file named `versions.txt`. Paste the output of each version command from Tasks 1 & 2, plus a line noting your VS Code version (Code → About) and your browser. It should look roughly like this:

```bash
Node.js: v20.11.1
npm: 10.2.4
Python: 3.12.2
pip: 24.0
VS Code: 1.89.0
Browser: Chrome 125
```

## ✅ Deliverable — acceptance checklist

You're done when **all** of these are true:

- `node --version` prints v20 or newer.
- `npm --version` prints a version.
- `python3 --version` prints 3.11 or newer.
- `pip3 --version` prints a version.
- VS Code is installed with Prettier, ESLint, and Python extensions enabled.
- You opened DevTools and found the Elements, Console, and Network tabs.
- A `versions.txt` file exists in your project folder with all versions recorded.

## 🚀 Stretch goals (optional)

- Install a Node version manager (**nvm**) so you can switch Node versions later.
- Set Prettier as your *default formatter* and turn on *Format On Save* in VS Code settings.
- Change your terminal prompt or install a nicer shell theme (e.g. Oh My Zsh).
- Explore the DevTools **Console**: type `2 + 2` and press Enter — you just ran JavaScript.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
