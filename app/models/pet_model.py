from app.database import Database

class Pet:
    def __init__(self, user_id, name, species, breed, age, gender, photo=None, id=None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.gender = gender
        self.photo = photo

    @staticmethod
    def validate(name, species, age):
        """Validate pet input. Returns an error message, or None if valid."""
        if not name or not name.strip():
            return "Pet name is required."

        if not species or not species.strip():
            return "Species is required."

        if age is not None:
            try:
                age_val = int(age)
                if age_val < 0:
                    return "Age cannot be negative."
            except (ValueError, TypeError):
                return "Age must be a number."

        return None    

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

    @staticmethod
    def search_pets_by_name(user_id, name):
        """US17 - Search pets by name for a logged in user."""
        db = Database()
        results = db.fetch_all(
            """SELECT id, name, species, breed, photo
               FROM pets
               WHERE user_id = %s AND name LIKE %s""",
            (user_id, f"%{name}%")
        )
        db.close()
        return results
