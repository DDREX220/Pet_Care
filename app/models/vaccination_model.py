from app.database import Database

class Vaccination:
    def __init__(self, pet_id, vaccine_name, date_given, next_due_date=None, notes=None):
        self.pet_id = pet_id
        self.vaccine_name = vaccine_name
        self.date_given = date_given
        self.next_due_date = next_due_date
        self.notes = notes

    def save(self):
        db = Database()
        db.execute(
            """INSERT INTO vaccinations 
               (pet_id, vaccine_name, date_given, next_due_date, notes)
               VALUES (%s, %s, %s, %s, %s)""",
            (self.pet_id, self.vaccine_name, self.date_given, 
             self.next_due_date, self.notes)
        )
        db.close()

    @staticmethod
    def get_all_by_pet(pet_id):
        db = Database()
        vaccinations = db.fetch_all(
            "SELECT * FROM vaccinations WHERE pet_id = %s ORDER BY date_given DESC",
            (pet_id,)
        )
        db.close()
        return vaccinations

    @staticmethod
    def get_by_id(vaccination_id):
        db = Database()
        vaccination = db.fetch_one(
            "SELECT * FROM vaccinations WHERE id = %s",
            (vaccination_id,)
        )
        db.close()
        return vaccination

    @staticmethod
    def delete(vaccination_id):
        db = Database()
        db.execute(
            "DELETE FROM vaccinations WHERE id = %s",
            (vaccination_id,)
        )
        db.close()