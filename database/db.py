import os
import sqlite3

from werkzeug.security import generate_password_hash

_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "spendly.db")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()


def seed_db() -> None:
    conn = get_db()

    existing = conn.execute(
        "SELECT id FROM users WHERE email = ?", ("demo@spendly.com",)
    ).fetchone()

    if existing:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123", method="pbkdf2:sha256")),
    )
    user_id = cursor.lastrowid

    expenses = [
        (user_id, 450.00,  "Food",          "2026-04-01", "Lunch at office canteen"),
        (user_id, 120.00,  "Transport",     "2026-04-03", "Auto rickshaw fare"),
        (user_id, 2500.00, "Bills",         "2026-04-05", "Electricity bill"),
        (user_id, 800.00,  "Health",        "2026-04-07", "Pharmacy — vitamins"),
        (user_id, 350.00,  "Entertainment", "2026-04-09", "Movie tickets"),
        (user_id, 1200.00, "Shopping",      "2026-04-10", "Grocery run"),
        (user_id, 600.00,  "Food",          "2026-04-11", "Dinner with family"),
        (user_id, 250.00,  "Other",         "2026-04-11", "Stationery supplies"),
    ]

    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        expenses,
    )
    conn.commit()
    conn.close()
