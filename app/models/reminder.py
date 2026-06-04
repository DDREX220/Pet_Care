from app.database import Database

class Reminder:

    @staticmethod
    def delete(reminder_id, user_id):
        """US15 - Remove a completed reminder."""
        db = Database()
        db.execute(
            "DELETE FROM reminders WHERE id = %s AND user_id = %s",
            (reminder_id, user_id)
        )
        db.close()
