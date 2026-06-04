from flask import Blueprint
from app.controllers.medical_controller import MedicalController

class MedicalRoutes:
    def __init__(self):
        self.bp = Blueprint("medical", __name__)
        self.controller = MedicalController()

    def register(self):
        self.bp.add_url_rule(
            "/medical/add/<int:pet_id>",
            view_func=self.controller.add_medical_note,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/medical/<int:pet_id>",
            view_func=self.controller.view_medical_notes,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/medical/delete/<int:note_id>",
            view_func=self.controller.delete_medical_note,
            methods=["POST"]
        )
        return self.bp