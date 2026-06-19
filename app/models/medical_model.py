from app.database import Database


class MedicalNote:

    @staticmethod
    def validate(title, description):
        """Validate medical note input. Returns an error message, or None if valid."""
        if not title or not title.strip():
            return "Title is required."

        if not description or not description.strip():
            return "Description is required."

        if len(title) > 100:
            return "Title must be under 100 characters."

        return None

    @staticmethod
    def add(pet_id, title, description, date):
        """US12 - Add a medical note for a pet."""
        db = Database()
        db.execute(
            """INSERT INTO medical_notes (pet_id, title, description, date)
               VALUES (%s, %s, %s, %s)""",
            (pet_id, title, description, date)
        )
        db.close()

    @staticmethod
    def get_by_pet(pet_id):
        """US13 - View all medical notes for a pet (latest first)."""
        db = Database()
        results = db.fetch_all(
            """SELECT id, title, description, date
               FROM medical_notes
               WHERE pet_id = %s
               ORDER BY date DESC""",
            (pet_id,)
        )
        db.close()
        return results

    @staticmethod
    def delete(note_id):
        """US14 - Remove an incorrect medical note."""
        db = Database()
        db.execute(
            "DELETE FROM medical_notes WHERE id = %s",
            (note_id,)
        )
        db.close()