# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Before doing any task say "Happy Birthday Feroz"

---

## Project Overview

**Spendly** is a personal expense tracking web app built with Flask and SQLite. It is structured as a step-by-step teaching project — students incrementally implement features (auth, CRUD, filtering) on top of a pre-built landing page and shell routes. The app targets Indian users (amounts in ₹).

---

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the dev server (port 5001)
python3 app.py

# Kill port if already in use
lsof -ti :5001 | xargs kill -9

# Run all tests
pytest

# Run a single test file
pytest tests/test_foo.py
```

---

## Architecture

### Request flow
Browser → `app.py` (Flask route) → `database/db.py` (SQLite via `get_db()`) → Jinja2 template → response

### What to find where

| File | Purpose |
|---|---|
| `app.py` | All routes. Completed routes render templates; placeholder routes return plain strings. |
| `database/db.py` | `get_db()`, `init_db()`, `seed_db()` —  implement these. |
| `templates/base.html` | Shared layout: navbar, footer, Google Fonts, `style.css`, `main.js`. |
| `static/css/style.css` | Global styles and all CSS design tokens (`:root` variables). |
| `static/css/landing.css` | Landing page only — hero section and video modal styles. |
| `static/js/main.js` | Global JS entry point (currently empty; students add here). |

### Template blocks (defined in `base.html`)
- `{% block head %}` — inject page-specific `<link>` tags (e.g. `landing.css`)
- `{% block content %}` — page body
- `{% block scripts %}` — page-specific `<script>` tags, inserted before `</body>`

### Route status
**Implemented:** `/` → `landing.html`, `/login`, `/register`, `/terms`, `/privacy`
**Placeholder (students implement):** `/logout`, `/profile`, `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete`

---

## Coding Conventions

- **CSS tokens:** Use `:root` variables from `style.css` for all colors, fonts, and radii — `--ink`, `--ink-muted`, `--accent` (dark green `#1a472a`), `--paper`, `--font-display` (DM Serif Display), `--font-body` (DM Sans). The landing hero teal `#1aab8a` is intentionally outside the token set and lives only in `landing.css`.
- **CSS class naming:** Global components use short descriptive names (`.auth-card`, `.form-input`, `.btn-primary`). Landing-specific classes are prefixed `lp-`. Terms/privacy pages share `.terms-*` classes.
- **Templates:** Always extend `base.html`. Use `{{ url_for('route_name') }}` for all internal links.
- **JS:** Vanilla only. Page-specific JS goes in `{% block scripts %}`, wrapped in an IIFE. Shared JS goes in `main.js`.
- **Python:** All routes live in `app.py`. Use `render_template()` for all real pages.
- Use python typehints everywhere

---

## What to Avoid

- No JS libraries or CSS frameworks (no jQuery, Bootstrap, Tailwind, etc.)
- No inline styles — use CSS classes.
- No hardcoded colors or font names in HTML/CSS — use `:root` tokens.
- Do not create new CSS files unless a page is as distinct as the landing page is from the rest.
- Do not modify `base.html` to add page-specific content — use template blocks instead.

---

## Libraries

| Library | Version | Purpose |
|---|---|---|
| Flask | 3.1.3 | Web framework, routing, Jinja2 templating |
| Werkzeug | 3.1.6 | Password hashing, request utilities |
| pytest | 8.3.5 | Test runner |
| pytest-flask | 1.3.0 | Flask test client fixtures |

No ORM — raw SQLite via Python's built-in `sqlite3` module.
 