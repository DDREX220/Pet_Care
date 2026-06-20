import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Optional

from werkzeug.security import generate_password_hash

ADMIN_EMAIL = "admin@admin.com"
ADMIN_PASSWORD = "admin1122"


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
        if "role" not in cols:
            connection.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")

        ensure_admin_user(db_path)

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS lost_found_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                report_type TEXT NOT NULL,
                pet_name TEXT NOT NULL,
                pet_type TEXT NOT NULL,
                breed TEXT,
                location TEXT NOT NULL,
                event_date TEXT,
                description TEXT NOT NULL,
                contact_info TEXT NOT NULL,
                reward TEXT,
                photo_url TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT NOT NULL UNIQUE,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pet_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pet_name TEXT NOT NULL,
                species TEXT NOT NULL,
                age TEXT NOT NULL,
                vaccine_date TEXT NOT NULL,
                notes TEXT NOT NULL,
                photo_url TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )

        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS community_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                location TEXT,
                photo_url TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )


def ensure_admin_user(db_path: Optional[str] = None) -> None:
    email = ADMIN_EMAIL.lower()
    password_hash = generate_password_hash(ADMIN_PASSWORD)
    with connect(db_path) as connection:
        row = connection.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            connection.execute(
                "UPDATE users SET role = 'admin', password_hash = ?, name = 'Admin' WHERE email = ?",
                (password_hash, email),
            )
        else:
            connection.execute(
                "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
                ("Admin", email, password_hash, "admin"),
            )


def get_user_by_email(email: str, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT id, name, email, password_hash, address, photo, role, created_at FROM users WHERE email = ?",
            (email.strip().lower(),),
        ).fetchone()


def create_user(name: str, email: str, password_hash: str, role: str = "user", db_path: Optional[str] = None):
    with connect(db_path) as connection:
        cursor = connection.execute(
            "INSERT INTO users (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            (name.strip(), email.strip().lower(), password_hash, role),
        )
        return cursor.lastrowid


def get_user_by_id(user_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT id, name, email, address, photo, role, created_at FROM users WHERE id = ?",
            (int(user_id),),
        ).fetchone()


def get_all_users(db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            """
            SELECT id, name, email, address, photo, role, created_at
            FROM users
            ORDER BY created_at DESC, id DESC
            """
        ).fetchall()


def get_user_activity_counts(user_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        posts = connection.execute(
            "SELECT COUNT(*) AS count FROM community_posts WHERE user_id = ?",
            (int(user_id),),
        ).fetchone()["count"]
        reports = connection.execute(
            "SELECT COUNT(*) AS count FROM lost_found_reports WHERE user_id = ?",
            (int(user_id),),
        ).fetchone()["count"]
        return {"posts": posts, "reports": reports}


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


def update_user_password(user_id: int, password_hash: str, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        connection.execute(
            "UPDATE users SET password_hash = ? WHERE id = ?",
            (password_hash, int(user_id)),
        )
        return True


def create_password_reset_token(user_id: int, token: str, db_path: Optional[str] = None, hours_valid: int = 1):
    expires_at = (datetime.utcnow() + timedelta(hours=hours_valid)).isoformat()
    with connect(db_path) as connection:
        connection.execute(
            "DELETE FROM password_reset_tokens WHERE user_id = ?",
            (int(user_id),),
        )
        cursor = connection.execute(
            "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (?, ?, ?)",
            (int(user_id), token, expires_at),
        )
        return cursor.lastrowid


def get_password_reset_token(token: str, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        row = connection.execute(
            "SELECT id, user_id, token, expires_at FROM password_reset_tokens WHERE token = ?",
            (token,),
        ).fetchone()
        if not row:
            return None
        expires = datetime.fromisoformat(row["expires_at"])
        if expires < datetime.utcnow():
            connection.execute("DELETE FROM password_reset_tokens WHERE id = ?", (row["id"],))
            return None
        return row


def delete_password_reset_token(token: str, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        connection.execute("DELETE FROM password_reset_tokens WHERE token = ?", (token,))
        return True


def create_lost_found_report(
    user_id: int,
    report_type: str,
    pet_name: str,
    pet_type: str,
    breed: str,
    location: str,
    event_date: str,
    description: str,
    contact_info: str,
    reward: str = None,
    photo_url: str = None,
    db_path: Optional[str] = None,
):
    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO lost_found_reports (
                user_id, report_type, pet_name, pet_type, breed, location,
                event_date, description, contact_info, reward, photo_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(user_id),
                report_type,
                pet_name.strip(),
                pet_type.strip(),
                breed.strip() if breed else None,
                location.strip(),
                event_date.strip() if event_date else None,
                description.strip(),
                contact_info.strip(),
                reward.strip() if reward else None,
                photo_url.strip() if photo_url else None,
            ),
        )
        return cursor.lastrowid


def get_recent_lost_found_reports(limit: int = 6, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            """
            SELECT
                r.id, r.user_id, r.report_type, r.pet_name, r.pet_type, r.breed, r.location,
                r.event_date, r.description, r.contact_info, r.reward, r.photo_url,
                r.created_at, u.name AS reporter_name
            FROM lost_found_reports AS r
            JOIN users AS u ON u.id = r.user_id
            ORDER BY r.created_at DESC, r.id DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()


def get_lost_found_report(report_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT * FROM lost_found_reports WHERE id = ?",
            (int(report_id),),
        ).fetchone()


def delete_lost_found_report(report_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        connection.execute(
            "DELETE FROM lost_found_reports WHERE id = ?",
            (int(report_id),),
        )
        return True


def create_community_post(
    user_id: int,
    category: str,
    title: str,
    content: str,
    location: str = None,
    photo_url: str = None,
    db_path: Optional[str] = None,
):
    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO community_posts (
                user_id, category, title, content, location, photo_url
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                int(user_id),
                category,
                title.strip(),
                content.strip(),
                location.strip() if location else None,
                photo_url.strip() if photo_url else None,
            ),
        )
        return cursor.lastrowid


def get_recent_community_posts(limit: int = 10, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            """
            SELECT
                p.id, p.user_id, p.category, p.title, p.content, p.location, p.photo_url,
                p.created_at, u.name AS author_name, u.photo AS author_photo
            FROM community_posts AS p
            JOIN users AS u ON u.id = p.user_id
            ORDER BY p.created_at DESC, p.id DESC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()


def get_community_post(post_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT * FROM community_posts WHERE id = ?",
            (int(post_id),),
        ).fetchone()


def delete_community_post(post_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        connection.execute(
            "DELETE FROM community_posts WHERE id = ?",
            (int(post_id),),
        )
        return True


def create_pet_note(
    user_id: int,
    pet_name: str,
    species: str,
    age: str,
    vaccine_date: str,
    notes: str,
    photo_url: str = None,
    db_path: Optional[str] = None,
):
    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO pet_notes (
                user_id, pet_name, species, age, vaccine_date, notes, photo_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                int(user_id),
                pet_name.strip(),
                species.strip(),
                age.strip(),
                vaccine_date.strip(),
                notes.strip(),
                photo_url.strip() if photo_url else None,
            ),
        )
        return cursor.lastrowid


def get_pet_notes_by_user(user_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            """
            SELECT id, user_id, pet_name, species, age, vaccine_date, notes, photo_url, created_at
            FROM pet_notes
            WHERE user_id = ?
            ORDER BY created_at DESC, id DESC
            """,
            (int(user_id),),
        ).fetchall()


def get_pet_note(note_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        return connection.execute(
            "SELECT * FROM pet_notes WHERE id = ?",
            (int(note_id),),
        ).fetchone()


def delete_pet_note(note_id: int, db_path: Optional[str] = None):
    with connect(db_path) as connection:
        connection.execute(
            "DELETE FROM pet_notes WHERE id = ?",
            (int(note_id),),
        )
        return True
