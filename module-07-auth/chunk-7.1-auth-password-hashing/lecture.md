*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.1 — Auth Concepts & Password Hashing

**📖 LECTURE** · **⏱️ 60–90 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- The difference between **authentication** (who are you?) and **authorization** (what may you do?).
- How login actually works, and the two big approaches: **sessions** vs **tokens**.
- Why you must **never store plaintext passwords** — and why hashing (not encryption) is the answer.
- What **salts** and slow, adaptive hashes like **bcrypt** / **argon2** protect you from.
- How to hash and verify passwords in FastAPI with **passlib[bcrypt]**.

In the lab you'll add a `User` with a hashed password to the Tasks API and build secure `register` / `login` endpoints.

## 1. Authentication vs Authorization

People use these two words interchangeably, but they are different jobs and you'll build them in different chunks.

| Term | Question it answers | Example |
| --- | --- | --- |
| **Authentication** (authn) | "Who are you?" — proving identity. | Logging in with email + password. |
| **Authorization** (authz) | "What are you allowed to do?" — checking permissions. | Only the task's owner can delete it; only admins see all users. |

This chunk and 7.2 are about **authentication** (logging in, proving identity). Chunk 7.4 adds **authorization** (roles and ownership rules). You authenticate *first*, then authorize.

> **📝 Mnemonic**
>
> Auth
>
> N
>
> = who you are (i
>
> N
>
> dentity). Auth
>
> Z
>
> = what you can do (privilege
>
> Z
>
> ). You always do N before Z.

## 2. How login actually works

Here's the high-level flow you'll implement across 7.1–7.3. Don't worry about the JWT details yet — that's the next chunk. Just notice the shape:

>

The crucial insight: the server **never stores your real password**. It stores a one-way fingerprint of it (a *hash*) and only ever *compares*. We'll explain why that matters in section 4.

## 3. Sessions vs Tokens

HTTP is **stateless**: the server forgets you the instant a request finishes. So after you log in, every later request needs to re-prove who you are. There are two classic ways to do that.

### Sessions (server remembers)

On login the server creates a **session record** (stored server-side, e.g. in a database or Redis) and sends the browser a random **session ID** in a cookie. On each request the browser sends the cookie; the server looks the ID up in its session store to know who you are.

### Tokens (the token carries the info)

On login the server hands back a signed **token** (a JWT) that *contains* the user's identity and is cryptographically signed. The browser sends it on each request. The server just verifies the signature — **no lookup table required**. This is "stateless" auth.

|  | Sessions | Tokens (JWT) |
| --- | --- | --- |
| Where state lives | On the server (session store) | In the token itself (client holds it) |
| Scales across servers | Needs shared store / sticky sessions | Any server can verify — great for load balancing |
| Revoke instantly | Easy (delete the session) | Harder (token valid until it expires) |
| Typical transport | Cookie | `Authorization: Bearer` header |

We use **JWTs** in this course because they pair naturally with a separate React frontend and the load-balanced deployment you'll build in Module 9. You'll build them in **Chunk 7.2**. This chunk is the foundation that login depends on: **safely storing passwords**.

## 4. Why you must never store plaintext passwords

Imagine your `users` table has a `password` column with the literal text `"hunter2"`. The day your database leaks — and databases leak — every attacker instantly has every user's password.

That's worse than it sounds, because people **reuse passwords**. The password someone used on your little Tasks app is probably the same one they use on their email and bank. A plaintext leak from *you* becomes a break-in *everywhere*. Storing plaintext passwords is the single most damaging beginner mistake in web security.

> **⚠️ The rule**
>
> Never store a password you can read back.
>
> Not plaintext, and — as we'll see — not encrypted either. Store a one-way
>
> hash
>
> .

## 5. Hashing vs Encryption vs Encoding

These three get confused constantly. They are not the same thing.

| Technique | Reversible? | Purpose | Use for passwords? |
| --- | --- | --- | --- |
| **Encoding** (e.g. Base64) | Yes, trivially | Reformatting data for transport | ❌ No — it's not security at all |
| **Encryption** (e.g. AES) | Yes, with a key | Keep data secret but recoverable | ❌ No — if the key leaks, all passwords leak |
| **Hashing** (e.g. bcrypt) | **No** — one-way | Produce a fixed fingerprint you can only compare | ✅ **Yes** |

A **hash function** turns any input into a fixed-size string and **cannot be reversed**. Same input always gives the same hash, so to check a password at login you hash what the user typed and compare it to the stored hash. You never "decrypt" anything because there's nothing to decrypt.

```
hash("hunter2")  ->  "$2b$12$Nl2.../bVq9..."   (always the same for "hunter2")
hash("hunter3")  ->  "$2b$12$8aD...x0Lp..."    (completely different)
```

> **📝 Why not encryption?**
>
> Encryption is
>
> designed
>
> to be reversed (that's the point). To store passwords encrypted, your server must hold the decryption key — so a breach that grabs the database usually grabs the key too. Hashing has no key to steal. Encryption is for data you genuinely need to read back later (rare for passwords — you never do).

## 6. Salts and slow hashes (bcrypt / argon2)

Plain hashing isn't quite enough by itself. Two problems, two fixes.

### Problem A: identical passwords → identical hashes

If two users both pick `"password123"`, a naive hash gives them the *same* stored value. Attackers exploit this with precomputed **rainbow tables** (giant lookups of common-password → hash). The fix is a **salt**: a unique random value mixed in before hashing, so every hash is different even for identical passwords. This defeats rainbow tables entirely.

### Problem B: fast hashes are easy to brute-force

General-purpose hashes (MD5, SHA-256) are built to be *fast* — a GPU can try billions per second. Great for checksums, terrible for passwords. The fix is a **deliberately slow** hash with an adjustable **work factor** (cost) you can crank up over the years as hardware improves. **bcrypt** and **argon2** are the standard choices.

> **💡 bcrypt does all of this for you**
>
> bcrypt
>
> generates a random salt automatically
>
> and stores it
>
> inside
>
> the hash string, along with the cost factor. You don't manage salts manually. That's why two hashes of the same password look different — the salt differs each time.

Reading a bcrypt hash:

```
$2b$12$eImiTXuWVxfM37uY4JANjQ./9f7e8s3...
 │   │  └── salt + hash (the rest)
 │   └───── cost factor: 12  (2^12 = 4096 rounds; higher = slower = safer)
 └───────── algorithm identifier: bcrypt
```

## 7. Hashing in FastAPI with passlib

We use **passlib** with the **bcrypt** backend. Install both:

```bash
pip install "passlib[bcrypt]"
```

Set up a single `CryptContext` for your whole app (this is the heart of the `security.py` module you'll write in the lab):

```python
# app/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain: str) -> str:
    """Turn a plaintext password into a salted bcrypt hash for storage."""
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    """Check a login attempt against the stored hash. Never decrypts."""
    return pwd_context.verify(plain, hashed)
```

That's the entire password layer. `hash_password` runs at **register**, `verify_password` runs at **login**:

```
>>> h = hash_password("hunter2")
>>> h
'$2b$12$Nl2.../bVq9...'          # store THIS in the database
>>> verify_password("hunter2", h)
True                             # correct password
>>> verify_password("wrong", h)
False                            # wrong password
```

> **📝 deprecated="auto"**
>
> This lets passlib transparently upgrade old hashes to a stronger scheme over time. For now it just means "use the current best settings for bcrypt."

## 8. Putting it into endpoints

Here's the shape of the two endpoints you'll build. (In 7.2 the login endpoint will return a real JWT; for now it confirms the password is correct.) Notice we hash on register and verify on login — and we **never put the password (or the hash) in any response**.

```python
# app/routers/auth.py  (simplified preview)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.security import hash_password, verify_password
from app import models, schemas

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut,
             status_code=status.HTTP_201_CREATED)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(
        email=data.email,
        hashed_password=hash_password(data.password),   # hash here
    )
    db.add(user); db.commit(); db.refresh(user)
    return user                                         # UserOut hides the hash

@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        # Same vague message for "no such user" AND "wrong password"
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}              # 7.2: return a JWT here
```

> **⚠️ Don't leak which part was wrong**
>
> Return the
>
> same
>
> "Invalid credentials" error whether the email doesn't exist or the password is wrong. If you say "no such user" vs "wrong password," you let attackers discover which emails are registered (account enumeration).

> **💡 Keep passwords out of responses**
>
> Your
>
> UserOut
>
> Pydantic schema should expose
>
> id
>
> ,
>
> email
>
> ,
>
> role
>
> — and
>
> never
>
> hashed_password
>
> . Use a separate
>
> UserCreate
>
> schema for the incoming password. Shaping schemas this way makes accidental leaks structurally impossible.

## ✅ Recap

- **AuthN** = who you are; **AuthZ** = what you can do. Authenticate first.
- HTTP is stateless; you re-prove identity each request via **sessions** (server-side) or **tokens** (we use JWTs, in 7.2).
- **Never store plaintext** — and not encryption either. Store a one-way **hash**.
- **Salts** defeat rainbow tables; **slow, adaptive hashes** (bcrypt/argon2) defeat brute force. bcrypt handles the salt for you.
- In FastAPI: one `CryptContext`, `hash_password` on register, `verify_password` on login. Use a vague error and keep the hash out of responses.

**Next:** open `assignment.html` and add secure register/login endpoints to the Tasks API.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
