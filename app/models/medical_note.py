from app.database import Database

class MedicalNote:

    @staticmethod
    def add(pet_id, note, condition, note_date):
        """US12 - Add a medical note for a pet."""
        db = Database()
        db.execute(
            """INSERT INTO medical_notes (pet_id, note, condition, note_date)
               VALUES (%s, %s, %s, %s)""",
            (pet_id, note, condition, note_date)
        )
        db.close()

    @staticmethod
    def get_by_pet(pet_id):
        """US13 - View all medical notes for a pet (latest first)."""
        db = Database()
        results = db.fetch_all(
            """SELECT id, note, condition, note_date
               FROM medical_notes
               WHERE pet_id = %s
               ORDER BY note_date DESC""",
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
