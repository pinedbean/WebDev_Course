*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.1 — Lab: Your First SQLite Database

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Create a SQLite database file called `tasks.db`, build a `tasks` table that matches the Task entity from Module 5, fill it with sample data, and run every CRUD operation by hand from the terminal. By the end you'll have a real database file you could hand to anyone.

## Before you start

- Make a folder for this module, e.g. `~/Desktop/webdev-course/module-06-sqlite/sql-practice/`.
- Open a terminal in that folder (in VS Code: *Terminal → New Terminal*).
- Check SQLite is available — on macOS it's pre-installed: `sqlite3 --version` You should see a version number (3.x). *Windows/Linux notes are in the solution.*
- Prefer clicking over typing? Install [DB Browser for SQLite](https://sqlitebrowser.org) and do the same steps in its GUI.

> **⚠️ Try it yourself first**
>
> Write the SQL from memory and the lecture. Only open
>
> solution.html
>
> when you're stuck or to check your work at the end.

## Tasks

### 1 Open a new database

From your folder, start the SQLite prompt pointed at a new file. SQLite creates the file on first write:

```
sqlite3 tasks.db
```

Turn on friendlier output so results are readable:

```
.headers on
.mode column
```

### 2 Create the `tasks` table

Write a `CREATE TABLE tasks` statement with these columns (matching the Module 5 Task):

- `id` — integer, primary key, auto-increments
- `title` — text, required
- `description` — text, optional (allowed to be NULL)
- `completed` — integer, required, defaults to `0`
- `created_at` — text, required, defaults to the current time

Then confirm it exists with `.tables` and inspect it with `.schema tasks`.

### 3 Insert sample tasks (Create)

Add **at least four** tasks with `INSERT`. Give some a description and leave at least one description as `NULL`. Mark at least one task as completed (`completed = 1`).

### 4 Read your data (Read)

Run these `SELECT` queries and look at the output of each:

- All columns of all tasks.
- Only the `id` and `title` columns.
- Only the tasks that are **not** completed (`WHERE completed = 0`).
- All tasks sorted newest-first (`ORDER BY` on `created_at`, descending).

### 5 Update a task (Update)

Pick one unfinished task and mark it completed with an `UPDATE … SET completed = 1 WHERE id = …`. Then `SELECT` that one row to prove the change stuck.

### 6 Delete a task (Delete)

Remove one task by its `id` with `DELETE … WHERE id = …`. Run `SELECT * FROM tasks;` again to confirm it's gone.

### 7 Prove it persisted

Exit the prompt with `.quit`. Confirm the file exists on disk (`ls -l tasks.db`). Re-open it (`sqlite3 tasks.db`) and run `SELECT * FROM tasks;` — your data is still there. **That's persistence.**

## ✅ Deliverable — acceptance checklist

- A `tasks.db` file exists in your folder.
- It contains a `tasks` table with the 5 columns and correct constraints (visible via `.schema tasks`).
- The table has at least 4 rows, including at least one with a `NULL` description and at least one completed task.
- You ran each of `INSERT`, `SELECT` (with and without `WHERE`), `UPDATE`, and `DELETE` successfully.
- After quitting and re-opening, your data is still present.

## 🚀 Stretch goals (optional)

- Count your tasks: `SELECT COUNT(*) FROM tasks;` and count only completed ones with a `WHERE`.
- Use `LIKE` to find tasks whose title contains a word, e.g. `WHERE title LIKE '%report%'`.
- Combine conditions with `AND` / `OR` in a single query.
- Save your statements to a file `seed.sql` and run the whole thing at once with `sqlite3 tasks.db < seed.sql`.
- Open the same `tasks.db` in **DB Browser for SQLite** and browse your rows in the grid.

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
