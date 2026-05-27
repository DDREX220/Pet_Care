from flask import Blueprint
from ..controllers.authcontroller import AuthController
class AuthRoutes:
    def __init__(self):
        self.bp = Blueprint("auth", __name__)
        self.controller = AuthController()

    def register(self):
        self.bp.route("/login", methods=["GET","POST"]) (
            self.controller.login
        )
        self.bp.route("/register", methods=["GET","POST"])(
            self.controller.register
        )
        self.bp.route("/profile", methods=["GET","POST"])(
            self.controller.profile
        )
        self.bp.route("/reset_password", methods=["GET","POST"])(
            self.controller.reset_password
        )
        return self.bp
    