from app.database import Database

class Reminder:

    @staticmethod
    def add(user_id, title, description, reminder_date):
        """US24 - Add a reminder."""
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
        """US25 - View all reminders for a user."""
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
        """US15 - Remove a completed reminder."""
        db = Database()
        db.execute(
            "DELETE FROM reminders WHERE id = %s AND user_id = %s",
            (reminder_id, user_id)
        )
        db.close()