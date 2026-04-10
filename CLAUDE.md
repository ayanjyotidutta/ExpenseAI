# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

ExpenseAI is a lightweight personal expense tracker built with Flask and SQLite. The project is designed as a step-by-step implementation, with frontend pages mostly complete and backend routes scaffolded for incremental student/developer implementation.

---

## Architecture

```
expense-tracker/
├── app.py                  # All routes (single file, no blueprints)
├── database/
│   ├── __init__.py
│   └── db.py              # SQLite helpers: get_db(), init_db(), create_user(), get_user_by_email()
├── templates/
│   ├── base.html          # Shared layout — all pages extend this
│   ├── landing.html       # Home page with hero, features, CTA
│   ├── register.html      # User registration
│   ├── login.html         # User login
│   ├── terms.html         # Terms and conditions
│   └── privacy.html       # Privacy policy
├── static/
│   ├── css/
│   │   └── style.css      # All styles (global + page-specific)
│   └── js/
│       └── main.js        # Vanilla JS (theme toggle, modal handlers)
├── expense_tracker.db     # SQLite database (created at runtime)
├── requirements.txt
└── CLAUDE.md             # This file

```

**Database schema:**
- `users`: id, email, password
- `expenses`: id, user_id, category, amount, date, description

**Where things belong:**
- New routes → `app.py` only, no blueprints
- DB logic → `database/db.py` only, never inline in routes
- New pages → new `.html` file extending `base.html`
- Styles → `static/css/style.css` (no separate page-specific CSS files, no inline `<style>` tags)
- Frontend logic → `static/js/main.js` (vanilla JS only)

---

## Code style

- **Python**: PEP 8, snake_case for all variables and functions. Use parameterized queries with `?` placeholders—never f-strings in SQL.
- **Templates**: Jinja2 with `url_for()` for every internal link—never hardcode URLs.
- **Routes**: One responsibility per route function (fetch data, render template, done). Use `abort()` for HTTP errors, not bare `return "error string"`.
- **Frontend**: Vanilla JavaScript only. No frameworks, no jQuery, no npm packages.

---

## Tech constraints

- **Flask only** — no FastAPI, Django, or other web frameworks
- **SQLite only** — no ORMs, no external databases
- **Vanilla JS only** — no React, Vue, jQuery, or npm packages
- **No new pip packages** — work within `requirements.txt` unless explicitly instructed
- Python 3.10+ assumed — f-strings and `match` statements are fine

---

## Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run dev server (port 5001, hot reload enabled)
python app.py

# Run all tests
pytest

# Run tests with output visible
pytest -s

# Run a specific test file
pytest tests/test_foo.py

# Run tests matching a pattern
pytest -k "test_name"
```

---

## Route status

| Route | Status | Template |
|---|---|---|
| `GET /` | ✓ Implemented | landing.html |
| `GET /register` | ✓ Implemented | register.html |
| `GET /login` | ✓ Implemented | login.html |
| `GET /terms` | ✓ Implemented | terms.html |
| `GET /privacy` | ✓ Implemented | privacy.html |
| `GET /logout` | Stub — Step 3 | — |
| `GET /profile` | Stub — Step 4 | — |
| `GET /expenses/add` | Stub — Step 7 | — |
| `GET /expenses/<id>/edit` | Stub — Step 8 | — |
| `GET /expenses/<id>/delete` | Stub — Step 9 | — |

**Important**: Do not implement a stub route unless the active task explicitly targets that step.

---

## Key implementation details

**Database initialization:**
- `init_db()` creates tables (idempotent via `CREATE TABLE IF NOT EXISTS`)
- `get_db()` returns a connection with `row_factory = sqlite3.Row` and `PRAGMA foreign_keys = ON`
- `seed_db()` currently empty—populate with test data as needed
- Every route that queries the database must call `get_db()` to ensure foreign keys are enabled

**Authentication:**
- Passwords are hashed using werkzeug.security (`generate_password_hash`, `check_password_hash`)
- Sessions use Flask's built-in session management (session dictionary)
- `app.secret_key` is set to "dev-secret-key" (replace for production)

**Frontend:**
- All pages extend `base.html`, which includes navbar, footer, and global styles
- Theme toggle (light/dark mode) is implemented in `main.js` via `data-theme` attribute on `<html>`
- Modal for video is on landing page; handled by `main.js`

---

## Warnings and things to avoid

- **Never hardcode URLs** in templates — always use `url_for()`
- **Never put DB logic in route functions** — it belongs in `database/db.py`
- **Never install new packages** without flagging it—keep `requirements.txt` in sync
- **Never use JS frameworks** — vanilla JS only
- **Never use `GET` for state-changing operations** — use `POST`/`PUT`/`DELETE` for mutations
- Avoid returning raw strings from routes once a page is implemented — always render a template
- FK enforcement is manual in SQLite; `get_db()` handles this via `PRAGMA foreign_keys = ON`

