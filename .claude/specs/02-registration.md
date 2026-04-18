# Spec: Registration

## Overview
This step implements user registration — the first point of account creation in ExpenseAI. A visitor fills out a form with their name, email, and password. The server validates the input, hashes the password with werkzeug, and inserts the new user into the `users` table. Duplicate emails and mismatched passwords are rejected with flash messages. On success the user is redirected to `/login` to sign in. This is the entry point for all authenticated features that follow.

## Depends on
- Step 01 — Database Setup (`get_db`, `init_db`, `create_user`, `get_user_by_email` must exist in `database/db.py`)

## Routes
- `GET /register` — render the registration form — public (already exists as stub, needs no change)
- `POST /register` — process form submission, create user, start session — public

## Database changes
No database changes. The `users` table and `create_user(name, email, password_hash)` / `get_user_by_email(email)` helpers already exist in `database/db.py`. Password hashing happens in `app.py` before calling `create_user`.

## Templates
- **Modify**: `templates/register.html`
  - Change the hardcoded `action="/register"` to `action="{{ url_for('register') }}"` with `method="post"`
  - Add a `confirm_password` input field (type `password`, name `confirm_password`) below the password field
  - Replace the `{% if error %}` block with Flask's `get_flashed_messages()` loop to display flash messages
  - Keep all existing visual design

## Files to change
- `app.py` — upgrade `register()` to handle `GET` and `POST`; add flash + redirect logic
- `database/db.py` — add `create_user()` helper
- `templates/register.html` — fix hardcoded action URL, add `confirm_password` field, replace `{{ error }}` with `get_flashed_messages()`

## Files to create
No new files.

## New dependencies
No new dependencies. Uses `werkzeug.security` (already installed) and Flask's built-in `flash` / `redirect` / `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` before insert
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `flash()` for user-facing errors and success messages; display them in templates with `get_flashed_messages()` — never pass an `error` variable directly to `render_template`
- Use `abort(400)` only for truly malformed requests; prefer `flash` + re-render for validation errors
- After successful registration, do NOT write to session — redirect to `url_for('login')` with a success flash message
- The `POST /register` handler must live in `app.py` — no helper route files
- Call `get_user_by_email` before insert to check for duplicate email; do not rely solely on catching `IntegrityError`

## Definition of done
- [ ] `GET /register` renders the registration form without errors
- [ ] The form includes `name`, `email`, `password`, and `confirm_password` fields
- [ ] The form `action` uses `url_for('register')` — no hardcoded URL
- [ ] Flash messages are displayed via `get_flashed_messages()`, not via a passed `error` variable
- [ ] Submitting with any empty field re-renders the form with a flash validation error
- [ ] Submitting with mismatched passwords re-renders the form with a flash error; no DB insert occurs
- [ ] Submitting with an already-registered email shows a flash error and re-renders the form; no duplicate row inserted
- [ ] Submitting valid data creates a new row in the `users` table
- [ ] Password is stored as a werkzeug hash — never plaintext — verifiable by inspecting `expense_tracker.db`
- [ ] After successful registration the user is redirected to `/login` with a success flash message
- [ ] No session is written during registration
