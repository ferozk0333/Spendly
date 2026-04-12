# Spec: Registration

## Overview
Implement user registration so new users can create a Spendly account with their name, email, and password. This step wires up the `POST /register` route to write a new row into the `users` table, hash the password with Werkzeug, and redirect the user on success. The `register.html` template already exists and is fully built — only the route logic needs implementing.

## Depends on
- Step 01 — Database Setup (`database/db.py` with `get_db()`, `init_db()`, `users` table)

## Routes
- `GET /register` — render the registration form — public (already implemented, no changes needed)
- `POST /register` — validate form input, insert new user, redirect on success — public

## Database changes
No database changes. The `users` table already exists with the correct schema:
- `id`, `name`, `email` (UNIQUE), `password_hash`, `created_at`

## Templates
- **Modify:** `templates/register.html` — already has the form and `{{ error }}` block; no structural changes needed. Ensure `action="/register"` and `method="POST"` are present (they already are).

## Files to change
- `app.py` — convert the `register` route to accept both GET and POST; add form handling logic
- Add `from flask import session, redirect, url_for, request, flash` imports as needed

## Files to create
No new files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs — use raw `sqlite3` via `get_db()`
- Parameterised queries only — never string-format SQL
- Passwords hashed with `werkzeug.security.generate_password_hash` using `method="pbkdf2:sha256"`
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use `flask.session` to log the user in immediately after successful registration
- Set `app.secret_key` in `app.py` (required for sessions) — use a fixed dev string like `"spendly-dev-secret"`
- On duplicate email, catch the `sqlite3.IntegrityError` and re-render the form with an error message
- Validate server-side: name and email must be non-empty, password must be at least 8 characters
- After successful registration, redirect to `/expenses` (placeholder route for now) or `/` if that route does not yet exist
- Do not use `flash()` — pass `error` directly via `render_template`

## Definition of done
- [ ] Visiting `GET /register` renders the form without errors
- [ ] Submitting valid name, email, and password creates a new row in `users` with a hashed password
- [ ] After successful registration the user is redirected (not shown a blank page)
- [ ] `session["user_id"]` is set after registration
- [ ] Submitting a duplicate email re-renders the form with a visible error message (no crash)
- [ ] Submitting a password shorter than 8 characters re-renders the form with a visible error message
- [ ] Submitting with blank name or email re-renders the form with a visible error message
- [ ] Password is never stored in plain text — only `password_hash` is written to the DB
- [ ] App starts without errors (`python3 app.py`)
