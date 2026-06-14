from flask import Blueprint
from app.controllers.admin_controller import AdminController

class AdminRoutes:
    def __init__(self):
        self.bp = Blueprint("admin", __name__)
        self.controller = AdminController()

    def register(self):
        self.bp.add_url_rule(
            "/admin/users",
            view_func=self.controller.view_users,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/admin/users/delete/<int:user_id>",
            view_func=self.controller.delete_user,
            methods=["POST"]
        )
        self.bp.add_url_rule(
            "/admin/lost-reports",
            view_func=self.controller.view_lost_reports,
            methods=["GET"]
        )
        return self.bp