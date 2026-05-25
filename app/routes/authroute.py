from flask import Blueprint
from app.controllers.authcontroller import AuthController


class AuthRoutes:
    def __init__(self):
        self.bp = Blueprint("auth", __name__)
        self.controller = AuthController()

    def register(self):
        self.bp.add_url_rule("/login", view_func=self.controller.login, methods=["GET", "POST"])
        self.bp.add_url_rule("/register", view_func=self.controller.register, methods=["GET", "POST"])
        self.bp.add_url_rule("/profile", view_func=self.controller.profile, methods=["GET", "POST"])
        self.bp.add_url_rule("/reset-password", view_func=self.controller.reset_password, methods=["GET", "POST"])
        return self.bp
    