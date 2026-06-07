import os

from flask import Flask, render_template

from .database import DEFAULTS
from .routes.authroute import AuthRoutes
from .routes.productroute import ProductRoutes
from .routes.petroute import PetRoutes


def create_app():
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
        static_url_path="/static",
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        MYSQL_HOST=os.environ.get("MYSQL_HOST", DEFAULTS["MYSQL_HOST"]),
        MYSQL_PORT=int(os.environ.get("MYSQL_PORT", DEFAULTS["MYSQL_PORT"])),
        MYSQL_USER=os.environ.get("MYSQL_USER", DEFAULTS["MYSQL_USER"]),
        MYSQL_PASSWORD=os.environ.get("MYSQL_PASSWORD", DEFAULTS["MYSQL_PASSWORD"]),
        MYSQL_DATABASE=os.environ.get("MYSQL_DATABASE", DEFAULTS["MYSQL_DATABASE"]),
    )

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    app.register_blueprint(AuthRoutes().register())
    app.register_blueprint(ProductRoutes().register())
    app.register_blueprint(PetRoutes().register())

    return app