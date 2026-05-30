from flask import Blueprint
from app.controllers.vaccination_controller import VaccinationController

class VaccinationRoutes:
    def __init__(self):
        self.bp = Blueprint("vaccinations", __name__)
        self.controller = VaccinationController()

    def register(self):
        self.bp.add_url_rule(
            "/vaccinations/add/<int:pet_id>",
            view_func=self.controller.add_vaccination,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/vaccinations/<int:pet_id>",
            view_func=self.controller.view_vaccinations,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/vaccinations/delete/<int:vaccination_id>",
            view_func=self.controller.delete_vaccination,
            methods=["POST"]
        )
        return self.bp