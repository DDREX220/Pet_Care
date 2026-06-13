from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    @staticmethod
    def get(user_id):
        from .database import connection_scope
        with connection_scope() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, name, email FROM users WHERE id = %s", (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(user_data['id'], user_data['name'], user_data['email'])
        return None
