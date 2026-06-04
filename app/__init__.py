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

    auth_routes = AuthRoutes()
    pet_routes = PetRoutes()
    vaccination_routes = VaccinationRoutes()
    medical_routes = MedicalRoutes()
    app.register_blueprint(auth_routes.register())
    app.register_blueprint(pet_routes.register())
    app.register_blueprint(vaccination_routes.register())
    app.register_blueprint(medical_routes.register())

    # Static routes
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/services")
    def services():
        return render_template("services.html")

    @app.route("/lost-found")
    def lost_found():
        return render_template("lost_found.html")

    @app.route("/community")
    def community():
        return render_template("community.html")

    @app.route("/pet-care-tips")
    def pet_care_tips():
        return render_template("pet_care_tips.html")

    @app.route("/my-note")
    def my_note():
        return render_template("my_note.html")

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    return app
