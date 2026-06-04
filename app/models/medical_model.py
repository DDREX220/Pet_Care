from app.database import Database

class MedicalNote:
    def __init__(self, pet_id, title=None, description=None, date=None, note=None, condition=None, note_date=None, id=None):
        self.id = id
        self.pet_id = pet_id
        self.title = title
        self.description = description
        self.date = date
        self.note = note
        self.condition = condition
        self.note_date = note_date

    def save(self):
        db = Database()
        db.execute(
            """INSERT INTO medical_notes 
               (pet_id, title, description, date, note, `condition`, note_date)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (self.pet_id, self.title, self.description, self.date, self.note, self.condition, self.note_date)
        )
        db.close()

    @staticmethod
    def get_all_by_pet(pet_id):
        db = Database()
        notes = db.fetch_all(
            """SELECT * FROM medical_notes 
               WHERE pet_id = %s ORDER BY created_at DESC""",
            (pet_id,)
        )
        db.close()
        return notes

    @staticmethod
    def get_by_id(note_id):
        db = Database()
        note = db.fetch_one(
            "SELECT * FROM medical_notes WHERE id = %s",
            (note_id,)
        )
        db.close()
        return note

    @staticmethod
    def delete(note_id):
        db = Database()
        db.execute(
            "DELETE FROM medical_notes WHERE id = %s",
            (note_id,)
        )
        db.close()

    # Methods from Sprint 3's medical_note.py for backward compatibility
    @staticmethod
    def add(pet_id, note, condition, note_date):
        """US12 - Add a medical note for a pet."""
        db = Database()
        db.execute(
            """INSERT INTO medical_notes (pet_id, note, `condition`, note_date)
               VALUES (%s, %s, %s, %s)""",
            (pet_id, note, condition, note_date)
        )
        db.close()

    @staticmethod
    def get_by_pet(pet_id):
        """US13 - View all medical notes for a pet (latest first)."""
        db = Database()
        results = db.fetch_all(
            """SELECT id, note, `condition`, note_date
               FROM medical_notes
               WHERE pet_id = %s
               ORDER BY note_date DESC""",
            (pet_id,)
        )
        db.close()
        return results
