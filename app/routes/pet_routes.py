from flask import Blueprint
from app.controllers.pet_controller import PetController

class PetRoutes:
    def __init__(self):
        self.bp = Blueprint("pets", __name__)
        self.controller = PetController()

    def register(self):
        self.bp.add_url_rule(
            "/pets",
            view_func=self.controller.view_pets,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/pets/save",
            view_func=self.controller.save_pet,
            methods=["POST"]
        )
        self.bp.add_url_rule(
            "/pets/delete/<int:pet_id>",
            view_func=self.controller.delete_pet,
            methods=["POST"]
        )
        self.bp.add_url_rule(
            "/pets/search",
            view_func=self.controller.search_pets,
            methods=["GET"]
        )
        return self.bpgit