*Full-Stack Web Dev · Module 6 — Database with SQLite*

# Chunk 6.1 — SQL & SQLite Fundamentals

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- Why your Tasks API needs a **database** (and why in-memory data was never going to last).
- The **relational model**: tables, rows, columns, primary keys, data types.
- The four CRUD verbs in **SQL**: `INSERT`, `SELECT`, `UPDATE`, `DELETE` — plus `CREATE TABLE` and filtering with `WHERE`.
- What **SQLite** is, why it's perfect for this course, and how to drive it from the terminal.

In the lab you'll create a real `tasks.db` file, build a `tasks` table, and run every kind of query by hand.

## 1. The problem: your data disappears

In Module 5 you built a Tasks API with FastAPI. It worked — you could create, read, update, and delete tasks. But every task lived in a Python **list in memory**:

```
# Module 5 — the in-memory store
tasks: list[Task] = []
```

That list only exists while the server is running. The moment you stop Uvicorn (or it crashes, or you redeploy), **every task is gone**. Restart the server and you're back to an empty list. That's fine for a demo, useless for a real app.

We need **persistence**: a place to store data that survives restarts. That place is a **database**, and the data lives in a file on disk. This whole module is about giving the Tasks API a real, durable memory.

> **📝 Where this is going**
>
> 6.1 (today): learn SQL by hand. 6.2: talk to SQLite from Python with SQLAlchemy. 6.3: make the Tasks API itself persistent + migrations. 6.4: add a second table (Users) and connect them. Then Module 7 adds login.

## 2. The relational model

A **relational database** organizes data into **tables** — think of a spreadsheet, but with strict rules. A table for tasks might look like this:

| id | title | description | completed | created_at |
| --- | --- | --- | --- | --- |
| 1 | Buy milk | 2% organic | 0 | 2026-06-26 09:00:00 |
| 2 | Finish report | (null) | 1 | 2026-06-26 09:05:00 |
| 3 | Call dentist | Reschedule | 0 | 2026-06-26 09:10:00 |

- A **table** holds one kind of thing (here, tasks). Its name is plural by convention: `tasks`.
- A **row** (also called a *record*) is one item — one task.
- A **column** (also called a *field*) is one attribute every row has — `title`, `completed`, etc.
- A **primary key** is a column whose value uniquely identifies each row. Here it's `id`. No two rows share an `id`.

Notice this is *exactly* the shape of the `Task` entity from Module 5: `id`, `title`, `description`, `completed`, `created_at`. A database column maps cleanly onto a model field — that's the bridge we'll cross in 6.2.

### SQLite data types

Each column has a **type** that says what kind of value it stores. SQLite keeps this simple — it has just a handful of *storage classes*:

| Type | Stores | Used for our Task |
| --- | --- | --- |
| `INTEGER` | Whole numbers | `id`, and `completed` (0 = false, 1 = true) |
| `TEXT` | Strings of text | `title`, `description`, and dates (as ISO text) |
| `REAL` | Decimal numbers | (not needed here — e.g. prices) |
| `BLOB` | Raw bytes (files, images) | (not needed here) |
| `NULL` | "No value" / missing | a `description` that wasn't provided |

> **📝 No real boolean or date type**
>
> SQLite has no dedicated
>
> BOOLEAN
>
> or
>
> DATETIME
>
> type. Booleans are stored as
>
> INTEGER
>
> 0
>
> /
>
> 1
>
> , and dates/times are stored as
>
> TEXT
>
> in ISO format like
>
> 2026-06-26 09:00:00
>
> . SQLAlchemy will hide this from us later — it converts to/from Python
>
> bool
>
> and
>
> datetime
>
> automatically.

## 3. Why SQLite?

**SQLite** is a relational database that lives in a *single file*. There's no server to install, no port to open, no username/password to configure. Your whole database is one file (we'll call ours `tasks.db`) that you can copy, email, or delete like any other file.

| Why it's great for us | What to know |
| --- | --- |
| **Zero setup** | It's built into Python and macOS. Nothing to install to get started. |
| **Serverless** | No separate database process — your app reads/writes the file directly. |
| **Portable** | The entire database is one file you can version, back up, or move. |
| **Real SQL** | The SQL you learn here works in Postgres, MySQL, etc. with minor tweaks. |

> **⚠️ When NOT to use SQLite**
>
> SQLite is fantastic for development, small apps, and learning. But because it's a single file, it struggles with
>
> many simultaneous writers
>
> (high-traffic production with lots of concurrent writes). For that you'd reach for a client/server database like
>
> PostgreSQL
>
> . The Bonus Track shows how to migrate. For everything in this course, SQLite is the right call.

## 4. SQL: the language of databases

**SQL** (Structured Query Language) is how you talk to a relational database. You write *statements* that describe what you want, and the database figures out how to do it. The four operations you'll use constantly map directly onto **CRUD**:

| CRUD | SQL keyword | Meaning |
| --- | --- | --- |
| Create | `INSERT` | Add new rows |
| Read | `SELECT` | Fetch rows |
| Update | `UPDATE` | Change existing rows |
| Delete | `DELETE` | Remove rows |

And before you can do any of that, you define the table's shape with `CREATE TABLE`. SQL keywords are usually written in UPPERCASE (just a convention — it makes statements easier to read). Every statement ends with a semicolon `;`.

## 5. CREATE TABLE — defining the shape

This creates our `tasks` table. Read it top to bottom: each line is a column name, its type, and optional **constraints** (rules the database enforces):

```sql
CREATE TABLE tasks (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT    NOT NULL,
    description TEXT,
    completed   INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);
```

| Constraint | What it does |
| --- | --- |
| `PRIMARY KEY` | Marks this column as the unique row identifier. |
| `AUTOINCREMENT` | The database fills in `id` for you (1, 2, 3, …) so you never repeat one. |
| `NOT NULL` | This column is required — you can't leave it empty. |
| `DEFAULT 0` | If you don't supply a value, use this one. New tasks default to "not completed". |
| `DEFAULT (datetime('now'))` | Auto-stamp the current UTC time when a row is created. |

> **💡 INTEGER PRIMARY KEY is special**
>
> In SQLite, a column declared
>
> INTEGER PRIMARY KEY
>
> automatically becomes an alias for the row's built-in
>
> ROWID
>
> , so it auto-assigns ascending numbers even without
>
> AUTOINCREMENT
>
> . Adding
>
> AUTOINCREMENT
>
> just guarantees ids are never reused after deletion.

## 6. INSERT — adding rows (Create)

You list the columns you're providing, then the matching values. Columns you skip (`id`, `completed`, `created_at`) fall back to their defaults:

```sql
INSERT INTO tasks (title, description)
VALUES ('Buy milk', '2% organic');

INSERT INTO tasks (title, description, completed)
VALUES ('Finish report', NULL, 1);
```

Text values go in **single quotes** `'like this'`. To insert several rows at once, separate value groups with commas:

```sql
INSERT INTO tasks (title, description) VALUES
    ('Call dentist', 'Reschedule cleaning'),
    ('Water plants', NULL),
    ('Read SQL chapter', 'Module 6');
```

## 7. SELECT — reading rows (Read)

`SELECT` fetches data. The simplest form grabs every column of every row (`*` means "all columns"):

```sql
SELECT * FROM tasks;
```

Ask for only the columns you need:

```sql
SELECT id, title FROM tasks;
```

### WHERE — filtering

`WHERE` keeps only the rows that match a condition. This is the most important clause in SQL:

```sql
-- only tasks that aren't done yet (completed = 0)
SELECT * FROM tasks WHERE completed = 0;

-- one specific task by id
SELECT * FROM tasks WHERE id = 2;
```

Comparison operators inside `WHERE`:

| Operator | Means | Example |
| --- | --- | --- |
| `=` | equals | `WHERE completed = 1` |
| `!=` or `<>` | not equal | `WHERE completed != 1` |
| `>` `<` `>=` `<=` | greater / less than | `WHERE id > 2` |
| `LIKE` | pattern match (`%` = any text) | `WHERE title LIKE 'Buy%'` |
| `IS NULL` | has no value | `WHERE description IS NULL` |

Combine conditions with `AND` / `OR`:

```sql
SELECT * FROM tasks
WHERE completed = 0 AND title LIKE '%report%';
```

### ORDER BY and LIMIT

Sort results, and cap how many come back:

```sql
-- newest tasks first
SELECT * FROM tasks ORDER BY created_at DESC;

-- the 3 lowest ids
SELECT * FROM tasks ORDER BY id ASC LIMIT 3;
```

`ASC` = ascending (default), `DESC` = descending.

## 8. UPDATE — changing rows (Update)

`UPDATE` modifies existing rows. `SET` assigns new values; `WHERE` chooses which rows to touch:

```sql
-- mark task #1 as completed
UPDATE tasks
SET completed = 1
WHERE id = 1;
```

You can change several columns at once:

```sql
UPDATE tasks
SET title = 'Buy oat milk', description = 'Switched brands'
WHERE id = 1;
```

> **⚠️ Never forget the WHERE**
>
> An
>
> UPDATE
>
> (or
>
> DELETE
>
> )
>
> without a
>
> WHERE
>
> applies to
>
> every row in the table
>
> .
>
> UPDATE tasks SET completed = 1;
>
> would mark
>
> all
>
> tasks done. Always double-check your
>
> WHERE
>
> before running it.

## 9. DELETE — removing rows (Delete)

`DELETE` removes rows that match the `WHERE` condition:

```sql
-- delete a single task
DELETE FROM tasks WHERE id = 3;

-- delete all completed tasks
DELETE FROM tasks WHERE completed = 1;
```

Same warning applies: `DELETE FROM tasks;` empties the entire table. There's no undo.

## 10. The tools: SQLite CLI & DB Browser

You can run all of this SQL by hand using one of two tools:

### Option A — the SQLite CLI (terminal)

macOS ships with the `sqlite3` command built in. Open a database file (it's created if it doesn't exist) and you get an interactive prompt:

```
sqlite3 tasks.db
```

Inside it you type SQL, plus a few special **dot-commands** (they start with `.` and don't need a semicolon):

| Dot-command | What it does |
| --- | --- |
| `.tables` | List the tables in the database |
| `.schema tasks` | Show the `CREATE TABLE` that defines a table |
| `.headers on` | Show column names above results |
| `.mode column` | Print results as neat aligned columns |
| `.quit` | Exit the SQLite prompt |

### Option B — DB Browser for SQLite (graphical)

[DB Browser for SQLite](https://sqlitebrowser.org) is a free desktop app that lets you click through tables, run SQL in a tab, and see results in a grid. Great for visual learners. The CLI is faster once you're comfortable; we'll use the CLI as primary in the lab and mention the GUI as an alternative.

> **💡 You will rarely write SQL by hand later**
>
> From Chunk 6.2 onward, an
>
> ORM
>
> (SQLAlchemy) writes the SQL for you from Python. So why learn raw SQL? Because when something breaks, you need to read the SQL the ORM generates, and inspect the database directly to see what really got stored. SQL is the ground truth.

## ✅ Recap

- In-memory data dies on restart; a **database** persists data to a file on disk.
- Relational databases store data in **tables** of **rows** and **columns**, with a **primary key** identifying each row.
- **SQLite** is a serverless, single-file database — zero setup, perfect for this course.
- **SQL** CRUD: `CREATE TABLE` defines shape; `INSERT`/`SELECT`/`UPDATE`/`DELETE` are Create/Read/Update/Delete.
- `WHERE` filters rows — and an `UPDATE`/`DELETE` without it hits every row.
- Drive SQLite from the terminal (`sqlite3`) or with DB Browser for SQLite.

**Next:** open `assignment.html` and build a real `tasks.db` with sample data and queries.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
