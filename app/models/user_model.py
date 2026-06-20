from app.database import Database
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, password, role='user', id=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def save(self):
        db = Database()
        hashed_password = generate_password_hash(self.password)
        db.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (self.name, self.email, hashed_password, self.role)
        )
        db.close()

    @staticmethod
    def get_by_email(email):
        db = Database()
        user_data = db.fetch_one("SELECT * FROM users WHERE email = %s", (email,))
        db.close()
        return user_data

    @staticmethod
    def get_by_id(user_id):
        db = Database()
        user_data = db.fetch_one("SELECT * FROM users WHERE id = %s", (user_id,))
        db.close()
        return user_data

    @staticmethod
    def update_profile(user_id, name, email, address=None):
        db = Database()
        db.execute(
            "UPDATE users SET name = %s, email = %s, address = %s WHERE id = %s",
            (name, email, address, user_id)
        )
        db.close()

    @staticmethod
    def update_password(user_id, new_password):
        db = Database()
        hashed_password = generate_password_hash(new_password)
        db.execute(
            "UPDATE users SET password = %s WHERE id = %s",
            (hashed_password, user_id)
        )
        db.close()

    @staticmethod
    def check_password(hashed_password, password):
        return check_password_hash(hashed_password, password)

    @staticmethod
    def get_all():
        """Admin - Get all users."""
        db = Database()
        users = db.fetch_all(
            "SELECT id, name, email, role, created_at FROM users ORDER BY id"
        )
        db.close()
        return users

    @staticmethod
    def delete(user_id):
        """Admin - Delete a user."""
        db = Database()
        db.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )
    @staticmethod
    def set_reset_token(email, token, expiry):
        db = Database()
        db.execute(
            "UPDATE users SET reset_token = %s, reset_token_expiry = %s WHERE email = %s",
            (token, expiry, email)
        )
        db.close()

    @staticmethod
    def get_by_reset_token(token):
        db = Database()
        user_data = db.fetch_one("SELECT * FROM users WHERE reset_token = %s", (token,))
        db.close()
        return user_data

    @staticmethod
    def clear_reset_token(user_id):
        db = Database()
        db.execute(
            "UPDATE users SET reset_token = NULL, reset_token_expiry = NULL WHERE id = %s",
            (user_id,)
        )
    @staticmethod
    def update_photo(user_id, photo_path):
        db = Database()
        db.execute(
        "UPDATE users SET photo = %s WHERE id = %s",
        (photo_path, user_id)
    )
    
        db.close()
        