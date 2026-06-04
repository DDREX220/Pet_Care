from app.database import Database

class MedicalNote:
    def __init__(self, pet_id, title, description, date):
        self.pet_id = pet_id
        self.title = title
        self.description = description
        self.date = date

    def save(self):
        db = Database()
        db.execute(
            """INSERT INTO medical_notes 
               (pet_id, title, description, date)
               VALUES (%s, %s, %s, %s)""",
            (self.pet_id, self.title, self.description, self.date)
        )
        db.close()

    @staticmethod
    def get_all_by_pet(pet_id):
        db = Database()
        notes = db.fetch_all(
            """SELECT * FROM medical_notes 
               WHERE pet_id = %s ORDER BY date DESC""",
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