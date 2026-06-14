from flask import Blueprint
from app.controllers.tip_controller import TipController

class TipRoutes:
    def __init__(self):
        self.bp = Blueprint("tips", __name__)
        self.controller = TipController()

    def register(self):
        self.bp.add_url_rule(
            "/tips",
            view_func=self.controller.view_tips,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/tips/<int:tip_id>",
            view_func=self.controller.view_tip_detail,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/tips/search",
            view_func=self.controller.search_tips,
            methods=["GET"]
        )
        return self.bp
    