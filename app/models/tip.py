from app.database import Database

class Tip:

    @staticmethod
    def get_all():
        """US16 - View all pet care tips."""
        db = Database()
        results = db.fetch_all(
            """SELECT id, title, category, created_at
               FROM tips
               ORDER BY created_at DESC"""
        )
        db.close()
        return results

    @staticmethod
    def get_by_id(tip_id):
        """US16 - Read full tip details."""
        db = Database()
        result = db.fetch_one(
            "SELECT id, title, content, category FROM tips WHERE id = %s",
            (tip_id,)
        )
        db.close()
        return result

    @staticmethod
    def search(keyword):
        """US17 - Search tips by keyword."""
        db = Database()
        results = db.fetch_all(
            """SELECT id, title, category
               FROM tips
               WHERE title LIKE %s OR content LIKE %s""",
            (f"%{keyword}%", f"%{keyword}%")
        )
        db.close()
        return results
