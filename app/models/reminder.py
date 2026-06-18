from app.database import Database

class Reminder:

    @staticmethod
    def add(user_id, title, description, reminder_date):
        """US24 - Add a new reminder for a user."""
        db = Database()
        db.execute(
            """INSERT INTO reminders 
               (user_id, title, description, reminder_date)
               VALUES (%s, %s, %s, %s)""",
            (user_id, title, description, reminder_date)
        )
        db.close()

    @staticmethod
    def get_all_by_user(user_id):
        """US25 - View all reminders for a user ordered by date."""
        db = Database()
        results = db.fetch_all(
            """SELECT * FROM reminders 
               WHERE user_id = %s 
               ORDER BY reminder_date ASC""",
            (user_id,)
        )
        db.close()
        return results

    @staticmethod
    def delete(reminder_id, user_id):
        """US15 - Remove a completed reminder by id and user_id."""
        db = Database()
        db.execute(
            "DELETE FROM reminders WHERE id = %s AND user_id = %s",
            (reminder_id, user_id)
        )
        db.close()

    @staticmethod
    def get_by_id(reminder_id, user_id):
        """Get a single reminder by id for a specific user."""
        db = Database()
        result = db.fetch_one(
            "SELECT * FROM reminders WHERE id = %s AND user_id = %s",
            (reminder_id, user_id)
        )
        db.close()
        return result