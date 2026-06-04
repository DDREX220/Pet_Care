from flask import Blueprint
from app.controllers.pet_controller import PetController

class PetRoutes:
    def __init__(self):
        self.bp = Blueprint("pets", __name__)
        self.controller = PetController()

    def register(self):
        self.bp.add_url_rule(
            "/pets/add",
            view_func=self.controller.add_pet,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/pets",
            view_func=self.controller.view_pets,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/pets/edit/<int:pet_id>",
            view_func=self.controller.edit_pet,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/pets/delete/<int:pet_id>",
            view_func=self.controller.delete_pet,
            methods=["POST"]
        )
        return self.bp