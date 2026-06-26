*Full-Stack Web Dev · Module 0 — Setup & Tooling*

# Chunk 0.1 — Solution (Step-by-Step)

**✅ SOLUTION** · **macOS-first, with Windows/Linux notes**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Follow the steps in order. Each step shows the **command to run**, the **expected output** (in green), and **troubleshooting** if it goes wrong. Your version numbers will differ slightly — that's fine, as long as they meet the minimums.

> **💡 Open a terminal**
>
> macOS
>
> Press
>
> ⌘ + Space
>
> , type "Terminal", press Enter. (Your shell is
>
> zsh
>
> .)
>
> Windows
>
> Open
>
> PowerShell
>
> or
>
> Windows Terminal
>
> from the Start menu.
>
> Linux
>
> Open your
>
> Terminal
>
> app.

### 1 Install Node.js (LTS)

macOS The simplest route is the official installer, but if you have **Homebrew** it's one command. To install Homebrew first (optional):

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then install Node LTS:

```bash
# With Homebrew:
brew install node

# Or download the macOS "LTS" .pkg installer from:
# https://nodejs.org  → run it → click through
```

Windows Download the **LTS** Windows Installer (.msi) from `https://nodejs.org` and run it (keep all defaults — it adds Node to your PATH).

Linux Use [nvm](https://github.com/nvm-sh/nvm): `nvm install --lts`, or your distro's package manager.

Verify:

```bash
node --version
npm --version
```

```
v20.11.1
10.2.4
```

> **⚠️ "command not found: node"**
>
> Close and reopen the terminal so it picks up the new PATH. Still failing on macOS after a .pkg install? Try
>
> brew install node
>
> instead, or reopen Terminal.

### 2 Install Python 3.11+

macOS macOS ships with an old Python. Install a fresh one:

```bash
# With Homebrew:
brew install python@3.12

# Or download the macOS installer from:
# https://www.python.org/downloads/  → run it
```

Windows Download from `https://www.python.org/downloads/` and run the installer. **Important:** tick *"Add python.exe to PATH"* on the first screen.

Linux `sudo apt install python3 python3-pip` (Debian/Ubuntu) or your distro's equivalent.

Verify:

```bash
python3 --version
pip3 --version
```

```bash
Python 3.12.2
pip 24.0 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

> **📝 Note (Windows)**
>
> On Windows the commands are often
>
> python --version
>
> and
>
> pip --version
>
> (no "3"). Both are fine.

### 3 Install VS Code + 3 extensions

Download VS Code from `https://code.visualstudio.com` and install it.

macOS Drag **Visual Studio Code** into your **Applications** folder, then open it.

**Add the extensions:** click the Extensions icon in the left sidebar (□ stacked icon, or `⌘ + Shift + X`). Search and install each:

- **Prettier - Code formatter** (by Prettier)
- **ESLint** (by Microsoft)
- **Python** (by Microsoft)

**Enable the `code` terminal command** (very handy): open the Command Palette with `⌘ + Shift + P`, type *"Shell Command: Install 'code' command in PATH"*, and select it. Now you can run:

```
code .
```

…from any folder to open it in VS Code.

### 4 Browser + DevTools

Install **Chrome** (`https://www.google.com/chrome`) or use Firefox. Open any website, then:

- macOS Open DevTools with `⌥ + ⌘ + I`, or right-click → **Inspect**.
- Windows / Linux Press `F12`, or right-click → **Inspect**.

Click through the three tabs you'll use most:

| Tab | What it's for |
| --- | --- |
| **Elements** | Inspect & tweak the HTML/CSS of the page live. |
| **Console** | See errors and run JavaScript. Try typing `2 + 2` and Enter. |
| **Network** | Watch the requests the page makes (you'll use this for APIs). |

### 5 Create your project folder

From the terminal, create the folder and open it in VS Code:

```bash
# macOS / Linux
mkdir -p ~/Desktop/webdev-course
cd ~/Desktop/webdev-course
code .
```

```bash
# Windows (PowerShell)
mkdir $HOME\Desktop\webdev-course
cd $HOME\Desktop\webdev-course
code .
```

> **💡 Tip**
>
> mkdir
>
> makes a directory,
>
> cd
>
> changes into it, and
>
> code .
>
> opens the current folder ("
>
> .
>
> ") in VS Code. You'll use this trio constantly.

### 6 Create `versions.txt`

Easiest way: create the file in VS Code (File → New File → save as `versions.txt`) and paste your version outputs. Or generate it from the terminal in one go:

```
# macOS / Linux — writes everything into versions.txt
{
  echo "Node.js: $(node --version)"
  echo "npm: $(npm --version)"
  echo "Python: $(python3 --version)"
  echo "pip: $(pip3 --version)"
} > versions.txt

cat versions.txt
```

Expected contents of `versions.txt`:

```bash
Node.js: v20.11.1
npm: 10.2.4
Python: Python 3.12.2
pip: pip 24.0 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)
```

Then add two manual lines for your editor and browser:

```
VS Code: 1.89.0
Browser: Chrome 125
```

> **📝 Note**
>
> The
>
> { … } > versions.txt
>
> trick runs several commands and writes their combined output into the file. The
>
> >
>
> means "send output to this file (overwrite)". You'll learn more shell in Chunk 0.2.

## 🎉 You're done

Re-check the acceptance list from the assignment — every box should now be tickable:

- ✅ Node, npm, Python, pip all print versions that meet the minimums.
- ✅ VS Code installed with Prettier, ESLint, Python extensions.
- ✅ DevTools opened; Elements / Console / Network located.
- ✅ `versions.txt` exists in `~/Desktop/webdev-course`.

**Up next → Chunk 0.2: Terminal & Git Basics.** You'll learn to navigate the filesystem and start version-controlling this exact folder with Git.

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
