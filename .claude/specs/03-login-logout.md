# Spec: Login and Logout

## Overview
Implement login and logout so registered users can authenticate into Spendly and end their session. This step wires up `POST /login` to verify credentials against the `users` table using Werkzeug's `check_password_hash`, sets `session["user_id"]` on success, and implements `GET /logout` to clear the session and redirect to the landing page. The `login.html` template already exists — only the route logic needs implementing.

## Depends on
- Step 01 — Database Setup (`database/db.py` with `get_db()`, `users` table)
- Step 02 — Registration (users must exist in the database to log in)

## Routes
- `GET /login` — render the login form — public (already implemented, convert to accept POST too)
- `POST /login` — validate credentials, set session on success, redirect — public
- `GET /logout` — clear the session, redirect to landing page — logged-in (currently a placeholder)

## Database changes
No database changes. The `users` table already has all required columns: `id`, `email`, `password_hash`.

## Templates
- **Modify:** `templates/login.html` — ensure `action="/login"` and `method="POST"` are present on the form; ensure an `{{ error }}` block is rendered when the `error` variable is passed. No structural changes expected.

## Files to change
- `app.py` — convert `login` route to accept GET and POST; implement credential verification logic; implement `logout` route to clear session and redirect

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never string-format SQL
- Verify passwords with `werkzeug.security.check_password_hash` — import it alongside `generate_password_hash`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `flask.session` to store `session["user_id"]` after successful login
- On invalid email or wrong password, re-render the form with a generic error message: `"Invalid email or password."` — do not reveal which field was wrong
- Do not use `flash()` — pass `error` directly via `render_template`
- `logout` must call `session.clear()` (not just `session.pop`) then redirect to `url_for("landing")`
- If the user is already logged in and visits `GET /login`, redirect them to `url_for("landing")`

## Definition of done
- [ ] Visiting `GET /login` renders the login form without errors
- [ ] Submitting a valid email and password sets `session["user_id"]` and redirects away from the login page
- [ ] Submitting an email that does not exist re-renders the form with the error `"Invalid email or password."`
- [ ] Submitting a correct email with a wrong password re-renders the form with the same generic error (no crash)
- [ ] Visiting `GET /logout` clears the session and redirects to the landing page
- [ ] After logout, `session["user_id"]` is no longer set
- [ ] A logged-in user visiting `GET /login` is redirected rather than shown the form
- [ ] App starts without errors (`python3 app.py`)
