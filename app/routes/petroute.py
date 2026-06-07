from flask import Blueprint

from ..controllers.petcontroller import PetController


class PetRoutes:
    def __init__(self):
        self.bp = Blueprint("pet", __name__)
        self.controller = PetController()

    def register(self):
        self.bp.route("/pets", methods=["GET"])(self.controller.pets)
        return self.bp