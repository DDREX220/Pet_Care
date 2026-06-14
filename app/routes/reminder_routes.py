from flask import Blueprint
from app.controllers.reminder_controller import ReminderController

class ReminderRoutes:
    def __init__(self):
        self.bp = Blueprint("reminders", __name__)
        self.controller = ReminderController()

    def register(self):
        self.bp.add_url_rule(
            "/reminders/add",
            view_func=self.controller.add_reminder,
            methods=["GET", "POST"]
        )
        self.bp.add_url_rule(
            "/reminders",
            view_func=self.controller.view_reminders,
            methods=["GET"]
        )
        self.bp.add_url_rule(
            "/reminders/delete/<int:reminder_id>",
            view_func=self.controller.delete_reminder,
            methods=["POST"]
        )
        return self.bp
    