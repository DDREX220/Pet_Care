from flask import Blueprint
from app.controllers.lost_found_controller import LostFoundController

class LostFoundRoutes:
    def __init__(self):
        self.bp = Blueprint("lost_found", __name__)
        self.controller = LostFoundController()

    def register(self):
        self.bp.add_url_rule(
            "/lost-pets/report",
            view_func=self.controller.report_lost,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/found-pets/report",
            view_func=self.controller.report_found,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/lost-pets",
            view_func=self.controller.view_lost,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/found-pets",
            view_func=self.controller.view_found,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/lost-pets/mark-found/<int:report_id>",
            view_func=self.controller.mark_as_found,
            methods=["POST"]
        )
        return self.bp