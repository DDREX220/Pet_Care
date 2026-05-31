from flask import Flask, render_template
import os

from .database import init_db


def create_app():
    # Use project-level templates/static by default
    base = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(base, "templates")
    static_folder = os.path.join(base, "static")

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    app.secret_key = "petcare-development-secret-key"
    app.config["AUTH_DB_PATH"] = os.path.join(base, "petcare_auth.db")

    init_db(app.config["AUTH_DB_PATH"])

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

    @app.route("/dashboard", methods=["GET", "POST"])
    def dashboard():
        # Require sign-in for dashboard; redirect to login if not signed in
        from flask import session, redirect, request, flash, current_app, url_for
        from .database import get_user_by_id, update_user_profile
        from werkzeug.utils import secure_filename
        import os

        if not session.get("user_id"):
            return redirect("/login")

        user = get_user_by_id(session.get("user_id"), current_app.config.get("AUTH_DB_PATH"))

        if request.method == "POST":
            # If the user wants to delete their profile
            if request.form.get("action") == "delete":
                from .database import delete_user, get_user_by_id
                # remove user's uploaded photo file if present
                stored = get_user_by_id(session.get("user_id"), current_app.config.get("AUTH_DB_PATH"))
                if stored and stored["photo"]:
                    try:
                        photo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", stored["photo"].replace("/", os.sep))
                        if os.path.exists(photo_path):
                            os.remove(photo_path)
                    except Exception:
                        pass
                delete_user(session.get("user_id"), current_app.config.get("AUTH_DB_PATH"))
                session.clear()
                flash("Your profile has been deleted.", "success")
                return redirect(url_for("home"))

            # Handle profile update
            name = request.form.get("name", user["name"] if user else "")
            email = request.form.get("email", user["email"] if user else "")
            address = request.form.get("address", user["address"] if user else "")

            photo_filename = None
            photo = request.files.get("photo")
            if photo and photo.filename:
                uploads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
                os.makedirs(uploads_dir, exist_ok=True)
                filename = secure_filename(photo.filename)
                # Prepend user id to avoid collisions
                filename = f"user_{session.get('user_id')}_" + filename
                dest = os.path.join(uploads_dir, filename)
                photo.save(dest)
                photo_filename = f"uploads/{filename}"

            update_user_profile(session.get("user_id"), name, email, address, photo_filename, current_app.config.get("AUTH_DB_PATH"))
            # Refresh session name/email
            session["user_name"] = name
            session["user_email"] = email
            flash("Profile updated successfully.", "success")
            return redirect(url_for("dashboard"))

        return render_template("dashboard.html", user=user)
    # Register blueprints if present (defensive)
    try:
        from . import routes as _routes_pkg
        # petroute: prefer `pet_bp` if available
        try:
            petroute = __import__(f"{__name__}.routes.petroute", fromlist=["pet_bp"])  # type: ignore
            pet_bp = getattr(petroute, "pet_bp", None)
            if pet_bp:
                app.register_blueprint(pet_bp)
        except ModuleNotFoundError:
            pass
        except Exception as e:
            print("petroute load error:", e)

        # productroute: support either `product_bp` or a `ProductRoutes` class
        try:
            productroute = __import__(f"{__name__}.routes.productroute", fromlist=["product_bp", "ProductRoutes"])  # type: ignore
            if hasattr(productroute, "product_bp"):
                app.register_blueprint(getattr(productroute, "product_bp"))
            elif hasattr(productroute, "ProductRoutes"):
                app.register_blueprint(productroute.ProductRoutes().register())
        except ModuleNotFoundError:
            pass
        except Exception as e:
            print("productroute load error:", e)

        # authroute: prefer `auth_bp` if available
        try:
            authroute = __import__(f"{__name__}.routes.authroute", fromlist=["auth_bp"])  # type: ignore
            if hasattr(authroute, "auth_bp"):
                app.register_blueprint(getattr(authroute, "auth_bp"))
            elif hasattr(authroute, "AuthRoutes"):
                app.register_blueprint(authroute.AuthRoutes().register())
        except ModuleNotFoundError:
            pass
        except Exception as e:
            print("authroute load error:", e)
    except Exception:
        # If the routes package itself cannot be inspected, skip registration
        pass

    return app
