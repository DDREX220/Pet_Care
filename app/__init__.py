import os
from flask import Flask, render_template, session, request, abort
import config
from app.database import Database

def create_app():
    app = Flask(__name__)
    app.secret_key = config.SECRET_KEY

    # Create database tables automatically
    with app.app_context():
        Database.create_tables()

    # Register blueprints
    from app.routes.authroute import AuthRoutes
    from app.routes.pet_routes import PetRoutes
    from app.routes.vaccination_routes import VaccinationRoutes
    from app.routes.medical_routes import MedicalRoutes
    from app.routes.reminder_routes import ReminderRoutes
    from app.routes.tip_routes import TipRoutes
    from app.routes.lost_found_routes import LostFoundRoutes
    from app.routes.admin_routes import AdminRoutes

    auth_routes = AuthRoutes()
    pet_routes = PetRoutes()
    vaccination_routes = VaccinationRoutes()
    medical_routes = MedicalRoutes()
    reminder_routes = ReminderRoutes()
    tip_routes = TipRoutes()
    lost_found_routes = LostFoundRoutes()
    admin_routes = AdminRoutes()

    app.register_blueprint(auth_routes.register())
    app.register_blueprint(pet_routes.register())
    app.register_blueprint(vaccination_routes.register())
    app.register_blueprint(medical_routes.register())
    app.register_blueprint(reminder_routes.register())
    app.register_blueprint(tip_routes.register())
    app.register_blueprint(lost_found_routes.register())
    app.register_blueprint(admin_routes.register())

    # Static routes
    @app.route("/community")
    def community():
        return render_template("community.html")

    @app.route("/services")
    def services():
        return render_template("services.html")

    @app.route("/my-note")
    def my_note():
        return render_template("my_note.html")
    @app.route("/")
    def home():
        from app.models.lost_found_model import LostFound

        lost_pets = LostFound.get_all_lost()
        found_pets = LostFound.get_all_found()

        return render_template("home.html", lost_pets=lost_pets, found_pets=found_pets)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    return app
