from app.database import Database

class Pet:
    def __init__(self, user_id, name, species, breed, age, gender, photo=None):
        self.user_id = user_id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.gender = gender
        self.photo = photo

    def save(self):
        db = Database()
        db.execute(
            """INSERT INTO pets (user_id, name, species, breed, age, gender, photo)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (self.user_id, self.name, self.species, self.breed, self.age, self.gender, self.photo)
        )
        db.close()

    @staticmethod
    def get_all_by_user(user_id):
        db = Database()
        pets = db.fetch_all("SELECT * FROM pets WHERE user_id = %s", (user_id,))
        db.close()
        return pets

    @staticmethod
    def get_by_id(pet_id):
        db = Database()
        pet = db.fetch_one("SELECT * FROM pets WHERE id = %s", (pet_id,))
        db.close()
        return pet

    @staticmethod
    def update(pet_id, name, species, breed, age, gender, photo=None):
        db = Database()
        if photo:
            db.execute(
                """UPDATE pets SET name=%s, species=%s, breed=%s, 
                   age=%s, gender=%s, photo=%s WHERE id=%s""",
                (name, species, breed, age, gender, photo, pet_id)
            )
        else:
            db.execute(
                """UPDATE pets SET name=%s, species=%s, breed=%s, 
                   age=%s, gender=%s WHERE id=%s""",
                (name, species, breed, age, gender, pet_id)
            )
        db.close()

    @staticmethod
    def delete(pet_id):
        db = Database()
        db.execute("DELETE FROM pets WHERE id = %s", (pet_id,))
        db.close()