import os
import sqlite3
from contextlib import contextmanager
from typing import Optional


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_DB_PATH = os.path.join(BASE_DIR, "petcare_auth.db")


@contextmanager
def connect(db_path: Optional[str] = None):
    connection = sqlite3.connect(db_path or DEFAULT_DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db(db_path: Optional[str] = None) -> None:
    with connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        # Ensure profile columns exist (SQLite allows ADD COLUMN)
        cols = [r[1] for r in connection.execute("PRAGMA table_info(users)")]
        if "address" not in cols:
            connection.execute("ALTER TABLE users ADD COLUMN address TEXT")
        if "photo" not in cols:
            connection.execute("ALTER TABLE users ADD COLUMN photo TEXT")


def get_user_by_email(email: str, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT id, name, email, password_hash, address, photo, created_at FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()


def create_user(name: str, email: str, password_hash: str, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name.strip(), email.strip().lower(), password_hash),
        )
        return cursor.lastrowid


def get_user_by_id(user_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT id, name, email, address, photo, created_at FROM users WHERE id = ?",
            (int(user_id),),
        ).fetchone()


def update_user_profile(user_id: int, name: str, email: str, address: str = None, photo: str = None, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        # Update provided fields; avoid overwriting password
        connection.execute(
            "UPDATE users SET name = ?, email = ?, address = ?, photo = ? WHERE id = ?",
            (name.strip(), email.strip().lower(), address or None, photo or None, int(user_id)),
        )
        return True


def delete_user(user_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (int(user_id),),
        )
        return True
