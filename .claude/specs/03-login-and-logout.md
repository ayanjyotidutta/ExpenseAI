# Spec: Login and Logout

## Overview
This step implements session-based authentication for ExpenseAI. A registered user submits their email and password via the login form; the server looks up the user by email, verifies the password hash with werkzeug, and writes the user's `id` and `name` into Flask's signed session cookie. On success the user is redirected to `/profile` (the next step). Logout clears the session and redirects to `/`. This is the gateway that unlocks all authenticated routes in later steps.

## Depends on
- Step 01 — Database Setup (`get_db`, `init_db` must exist in `database/db.py`)
- Step 02 — Registration (`users` table and `get_user_by_email` must exist; a registered account must be present to test login)

## Routes
- `GET /login` — render the login form — public (already exists as stub, needs upgrade)
- `POST /login` — validate credentials, write session, redirect — public
- `GET /logout` — clear session, redirect to `/` — public (already exists as stub, needs implementation)

## Database changes
No database changes. The `users` table and `get_user_by_email(email)` helper already exist in `database/db.py`.

## Templates
- **Modify:** `templates/login.html`
  - Change the form `action` to `action="{{ url_for('login') }}"` with `method="post"`
  - Display flash messages via `get_flashed_messages()` — remove any hardcoded error block
  - Ensure the form has `email` and `password` input fields with matching `name` attributes
- **Modify:** `templates/base.html`
  - Add conditional nav links: show "Logout" when `session.user_id` is set, show "Login" and "Register" when it is not

## Files to change
- `app.py` — upgrade `login()` to handle `GET` and `POST`; implement `logout()`
- `templates/login.html` — fix form action, add flash message display
- `templates/base.html` — add session-aware nav links

## Files to create
No new files.

## New dependencies
No new dependencies. Uses `werkzeug.security.check_password_hash` (already installed) and Flask's built-in `session`, `flash`, `redirect`, `url_for`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never f-strings in SQL
- Passwords verified with `werkzeug.security.check_password_hash` — never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Write only `session['user_id']` and `session['user_name']` on successful login — no other keys
- Use `flash()` for all user-facing errors; display with `get_flashed_messages()` in templates
- `logout()` must call `session.clear()` before redirecting — not `session.pop`
- After successful login, redirect to `url_for('profile')` — do not render the login template
- After logout, redirect to `url_for('landing')`
- Never redirect to a URL taken from request args (open redirect risk)
- The `POST /login` handler must live in `app.py` — no helper route files

## Definition of done
- [ ] `GET /login` renders the login form without errors
- [ ] The form includes `email` and `password` fields with correct `name` attributes
- [ ] The form `action` uses `url_for('login')` — no hardcoded URL
- [ ] Flash messages are displayed via `get_flashed_messages()`, not via a passed variable
- [ ] Submitting with any empty field re-renders the form with a flash validation error and no session is written
- [ ] Submitting an email not in the database shows a flash error and re-renders the form
- [ ] Submitting a correct email with a wrong password shows a flash error and re-renders the form
- [ ] Submitting valid credentials writes `session['user_id']` and `session['user_name']`
- [ ] After successful login the user is redirected to `/profile`
- [ ] `GET /logout` clears the session entirely
- [ ] After logout the user is redirected to `/` and `session['user_id']` no longer exists
- [ ] `base.html` nav shows "Login" / "Register" when logged out and "Logout" when logged in
