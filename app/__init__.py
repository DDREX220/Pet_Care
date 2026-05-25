import os

from flask import Flask, render_template

from app.database import DEFAULTS
from app.routes.authroute import AuthRoutes
from app.routes.productroute import ProductRoutes


def create_app():
    app = Flask(__name__, template_folder="../templates")
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
        return render_template("dashboard.html")

    app.register_blueprint(AuthRoutes().register())
    app.register_blueprint(ProductRoutes().register())

    return app