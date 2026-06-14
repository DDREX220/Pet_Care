from app.database import Database

class LostFound:

    @staticmethod
    def report_lost(user_id, pet_id, location, description):
        """US18 - Report a lost pet."""
        db = Database()
        db.execute(
            """INSERT INTO lost_found 
               (user_id, pet_id, type, location, description, status)
               VALUES (%s, %s, 'lost', %s, %s, 'active')""",
            (user_id, pet_id, location, description)
        )
        db.close()

    @staticmethod
    def report_found(user_id, location, description, photo=None):
        """US20 - Report a found pet."""
        db = Database()
        db.execute(
            """INSERT INTO lost_found 
               (user_id, type, location, description, photo, status)
               VALUES (%s, 'found', %s, %s, %s, 'active')""",
            (user_id, location, description, photo)
        )
        db.close()

    @staticmethod
    def get_all_lost():
        """US19 - View all lost pets."""
        db = Database()
        results = db.fetch_all(
            """SELECT lf.*, p.name as pet_name, p.species, 
               p.photo, u.name as owner_name
               FROM lost_found lf
               LEFT JOIN pets p ON lf.pet_id = p.id
               LEFT JOIN users u ON lf.user_id = u.id
               WHERE lf.type = 'lost' AND lf.status = 'active'
               ORDER BY lf.created_at DESC"""
        )
        db.close()
        return results

    @staticmethod
    def get_all_found():
        """US21 - View all found pets."""
        db = Database()
        results = db.fetch_all(
            """SELECT lf.*, u.name as reporter_name
               FROM lost_found lf
               LEFT JOIN users u ON lf.user_id = u.id
               WHERE lf.type = 'found' AND lf.status = 'active'
               ORDER BY lf.created_at DESC"""
        )
        db.close()
        return results

    @staticmethod
    def mark_as_found(report_id, user_id):
        """US22 - Mark lost pet as found."""
        db = Database()
        db.execute(
            """UPDATE lost_found SET status = 'resolved'
               WHERE id = %s AND user_id = %s""",
            (report_id, user_id)
        )
        db.close()

    @staticmethod
    def filter_by_location(location):
        """US23 - Filter lost pets by location."""
        db = Database()
        results = db.fetch_all(
            """SELECT lf.*, p.name as pet_name, p.species,
               p.photo, u.name as owner_name
               FROM lost_found lf
               LEFT JOIN pets p ON lf.pet_id = p.id
               LEFT JOIN users u ON lf.user_id = u.id
               WHERE lf.type = 'lost' 
               AND lf.status = 'active'
               AND lf.location LIKE %s
               ORDER BY lf.created_at DESC""",
            (f"%{location}%",)
        )
        db.close()
        return results

    @staticmethod
    def get_by_id(report_id):
        db = Database()
        result = db.fetch_one(
            "SELECT * FROM lost_found WHERE id = %s",
            (report_id,)
        )
        db.close()
        return result