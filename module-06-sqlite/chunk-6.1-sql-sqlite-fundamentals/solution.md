*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.1 — Solution (Step-by-Step)

**✅ SOLUTION**

> 📄 **Prefer the styled version?** Open [`solution.html`](solution.html) in your browser for the formatted page with colors and live demos.

---

## How to use this page

Follow the steps to build `tasks.db` from an empty folder. Each step gives the exact command/SQL and the output you should see. A complete, runnable `seed.sql` script is at the bottom.

> **📝 Platform note**
>
> macOS ships with
>
> sqlite3
>
> . On
>
> Linux
>
> :
>
> sudo apt install sqlite3
>
> . On
>
> Windows
>
> : download the "command-line tools" bundle from
>
> sqlite.org/download
>
> and run
>
> sqlite3.exe
>
> , or just use
>
> DB Browser for SQLite
>
> on any OS.

### 1 Open a new database

In your project folder, launch the prompt. Passing a filename that doesn't exist yet is fine — SQLite creates it the first time you write data.

```
sqlite3 tasks.db
```

You'll drop into the interactive shell:

```
SQLite version 3.43.2 2023-10-10
Enter ".help" for usage hints.
sqlite>
```

Turn on readable output (these settings last for this session):

```
.headers on
.mode column
```

### 2 Create the `tasks` table

Paste this at the `sqlite>` prompt. It must end with a semicolon:

```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    completed   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

Confirm it exists and inspect its definition:

```sql
.tables
-- tasks

.schema tasks
-- CREATE TABLE tasks (
--     id          INTEGER PRIMARY KEY AUTOINCREMENT,
--     ...
-- );
```

### 3 Insert sample tasks (Create)

Add several rows. We provide `title` (and sometimes `description`/`completed`); `id` and `created_at` fill in automatically:

```sql
INSERT INTO tasks (title, description) VALUES
    ('Buy milk', '2% organic'),
    ('Call dentist', 'Reschedule cleaning'),
    ('Water plants', NULL),
    ('Read SQL chapter', 'Module 6 lecture');

INSERT INTO tasks (title, description, completed)
VALUES ('Finish report', 'Q2 summary', 1);
```

### 4 Read your data (Read)

**All rows, all columns:**

```sql
SELECT * FROM tasks;
```

```
id  title             description          completed  created_at
--  ----------------  -------------------  ---------  -------------------
1   Buy milk          2% organic           0          2026-06-26 09:00:00
2   Call dentist      Reschedule cleaning  0          2026-06-26 09:00:01
3   Water plants                           0          2026-06-26 09:00:01
4   Read SQL chapter  Module 6 lecture     0          2026-06-26 09:00:01
5   Finish report     Q2 summary           1          2026-06-26 09:00:02
```

**Just two columns:**

```sql
SELECT id, title FROM tasks;
```

**Only unfinished tasks:**

```sql
SELECT * FROM tasks WHERE completed = 0;
```

**Newest first:**

```sql
SELECT * FROM tasks ORDER BY created_at DESC;
```

### 5 Update a task (Update)

Mark "Buy milk" (id 1) as done, then read it back:

```sql
UPDATE tasks SET completed = 1 WHERE id = 1;

SELECT id, title, completed FROM tasks WHERE id = 1;
```

```
id  title     completed
--  --------  ---------
1   Buy milk  1
```

### 6 Delete a task (Delete)

Remove "Water plants" (id 3) and confirm:

```sql
DELETE FROM tasks WHERE id = 3;

SELECT id, title FROM tasks;
```

Row 3 is gone. Note that `id` values are *not* renumbered — gaps are normal and expected.

### 7 Prove it persisted

```
.quit
```

```sql
ls -l tasks.db
# -rw-r--r--  1 you  staff  12288 Jun 26 09:01 tasks.db

sqlite3 tasks.db
sqlite> .mode column
sqlite> .headers on
sqlite> SELECT * FROM tasks;
# your rows are still here 🎉
```

The data lived on disk through a full restart of the program. That is exactly the durability your Tasks API has been missing.

## 📄 Complete `seed.sql`

You can keep every statement in one file and run it all at once with `sqlite3 tasks.db < seed.sql`. (Delete `tasks.db` first if you want a clean slate.)

```sql
-- seed.sql — create and populate the tasks table

CREATE TABLE IF NOT EXISTS tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    completed   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

INSERT INTO tasks (title, description) VALUES
    ('Buy milk', '2% organic'),
    ('Call dentist', 'Reschedule cleaning'),
    ('Water plants', NULL),
    ('Read SQL chapter', 'Module 6 lecture');

INSERT INTO tasks (title, description, completed)
VALUES ('Finish report', 'Q2 summary', 1);

-- read it back
SELECT id, title, completed FROM tasks ORDER BY id;
```

## 🛠 Troubleshooting

| Symptom | Fix |
| --- | --- |
| `command not found: sqlite3` | On macOS it should exist; reopen your terminal. On Linux `sudo apt install sqlite3`; on Windows download the CLI tools from sqlite.org or use DB Browser. |
| Nothing happens after a statement | You probably forgot the trailing `;`. SQLite waits (the prompt becomes `...>`) until it sees a semicolon. Type `;` and Enter. |
| Results are cramped / no headers | Run `.mode column` and `.headers on` (dot-commands need no semicolon). |
| `Error: no such table: tasks` | You're in a different/empty database file. Make sure you opened the same `tasks.db` and that the `CREATE TABLE` succeeded. |
| An `UPDATE`/`DELETE` changed everything | You forgot the `WHERE`. Re-run `seed.sql` on a fresh file to reset, and always check the `WHERE` first. |
| Stuck at a `...>` continuation prompt | SQLite is waiting for you to finish the statement. Type `;` or press Enter after the closing quote/paren. |

## 🎉 You're done

You created a real database file, defined a table, and ran the full CRUD cycle in raw SQL — the foundation under every persistent app you'll ever build.

**Keep `tasks.db`** nearby. In the next chunk you'll stop typing SQL by hand: you'll point Python at a SQLite file and let **SQLAlchemy** generate these exact statements for you, wiring a database session into your FastAPI Tasks API.

**Up next → Chunk 6.2: SQLAlchemy ORM with FastAPI.**

---

**Navigate:** [📖 Lecture](lecture.md) · [🧪 Assignment](assignment.md) · **✅ Solution**
