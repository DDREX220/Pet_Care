from flask import Blueprint

from ..controllers.petcontroller import PetController


class PetRoutes:
    def __init__(self):
        self.bp = Blueprint("pet", __name__)
        self.controller = PetController()

    def register(self):
        self.bp.route("/pets", methods=["GET"])(self.controller.pets)
        self.bp.route("/pets/save", methods=["POST"])(self.controller.save_pet)
        self.bp.route("/pets/delete/<int:pet_id>", methods=["POST"])(self.controller.delete_pet)
        self.bp.route("/lost-found", methods=["GET"])(self.controller.lost_found)
        self.bp.route("/lost-found/report", methods=["GET", "POST"])(self.controller.report_lost_found)
        self.bp.route("/lost-found/mark-found/<int:pet_id>", methods=["POST"])(self.controller.mark_as_found)
        return self.bp