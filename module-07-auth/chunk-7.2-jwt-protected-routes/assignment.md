*Full-Stack Web Dev · Module 7 — Authentication & Security*

# Chunk 7.2 — Lab: Issue JWTs & Protect Your Routes

**🧪 ASSIGNMENT** · **⏱️ 45–75 min**

> 📄 **Prefer the styled version?** Open [`assignment.html`](assignment.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 Your mission

Turn last chunk's "Login successful" into a real **token-based** system. Your `/auth/login` will return a JWT, you'll build a reusable `get_current_user` dependency, add `GET /auth/me`, and lock down all task routes so each user only sees and edits their **own** tasks.

## Before you start

- Chunk 7.1 complete: `security.py` with bcrypt, `/auth/register` + `/auth/login`, and the `User` model with `hashed_password` + `role`.
- venv active; server runs with `uvicorn app.main:app --reload`; docs at `/docs`.
- Your `Task` model has an `owner_id` FK to `users.id` (from Module 6).

> **⚠️ Try it yourself first**
>
> Work from the lecture. Only open
>
> solution.html
>
> when stuck or to compare.

## Tasks

### 1 Install python-jose & set a SECRET_KEY

```bash
pip install "python-jose[cryptography]"
pip freeze > requirements.txt
```

Generate a strong secret and set it as an environment variable for this terminal session:

```python
python -c "import secrets; print(secrets.token_hex(32))"
export SECRET_KEY="paste-the-value-here"     # Windows PowerShell: $env:SECRET_KEY="..."
```

(In 7.4 you'll move this to a `.env` file. For now an env var is fine — just don't hard-code it.)

### 2 Add token functions to `security.py`

Add `create_access_token(subject)` and `decode_access_token(token)` using `jose.jwt`, plus constants `SECRET_KEY` (from env), `ALGORITHM = "HS256"`, and `ACCESS_TOKEN_EXPIRE_MINUTES = 30`. The token's `sub` claim should be the user id as a string, and it must include an `exp`.

### 3 Add a `Token` schema & return it from login

Add a `Token` Pydantic model (`access_token`, `token_type`). Update `/auth/login` to verify the password and return a freshly signed token.

> **💡 Switch login to the OAuth2 form**
>
> Change login to accept
>
> form_data: OAuth2PasswordRequestForm = Depends()
>
> instead of a JSON body, and read the email from
>
> form_data.username
>
> . This makes the
>
> /docs
>
> "Authorize" button work and matches what your React frontend will send in 7.3.

### 4 Build `app/deps.py`

Create the dependencies module with:

- `oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")`.
- `get_current_user(token, db)` — decode the token, load the user from the DB, raise `401` ("Could not validate credentials", with a `WWW-Authenticate: Bearer` header) if anything fails.

### 5 Add `GET /auth/me`

A protected endpoint that depends on `get_current_user` and returns the current user as `UserOut`.

### 6 Scope every task route to the owner

Add `current_user: models.User = Depends(get_current_user)` to all task endpoints, then:

- **list**: filter by `owner_id == current_user.id`.
- **create**: set `owner_id = current_user.id`.
- **get one / update / delete**: load the task and return `404` if it's missing *or* not owned by the current user.

### 7 Test the whole flow in `/docs`

1. Register two users (e.g. `a@x.com` and `b@x.com`).
2. Click **Authorize**, log in as user A.
3. Create a couple of tasks — confirm `GET /tasks` shows only A's tasks.
4. Authorize as user B; confirm B sees none of A's tasks, and trying to `GET /tasks/{A's id}` returns `404`.
5. Call `GET /tasks` with the Authorize logged out → expect `401`.

## ✅ Deliverable — acceptance checklist

- `python-jose[cryptography]` installed; `SECRET_KEY` read from the environment (not hard-coded).
- `/auth/login` returns `{access_token, token_type}` and works via the docs Authorize button.
- `get_current_user` in `deps.py` decodes the token and loads the user; bad/missing tokens give `401`.
- `GET /auth/me` returns the logged-in user and is `401` without a token.
- All task routes require a token; `GET /tasks` shows only the current user's tasks.
- Accessing another user's task by id returns `404` (not the task, not `403`).

## 🚀 Stretch goals (optional)

- Paste your access token into [jwt.io](https://jwt.io) and read the decoded `sub` and `exp`. Confirm you cannot see the password anywhere — and that editing the payload breaks the signature.
- Set `ACCESS_TOKEN_EXPIRE_MINUTES = 1`, log in, wait, then call `/auth/me` and watch it return `401` once the token expires.
- Extract the ownership check into a reusable `get_owned_task` dependency and use it in get/update/delete.
- Add the user's `role` as a claim in the token payload (you'll use it in 7.4).

---

**Navigate:** [📖 Lecture](lecture.md) · **🧪 Assignment** · [✅ Solution](solution.md)
