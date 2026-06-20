from flask import Flask, current_app, flash, redirect, render_template, request, session, url_for
import os
import uuid

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

    @app.route("/lost-found", methods=["GET", "POST"])
    def lost_found():
        from .database import create_lost_found_report, get_recent_lost_found_reports
        from werkzeug.utils import secure_filename

        if request.method == "POST":
            if not session.get("user_id"):
                flash("Please sign in to report a lost or found pet.", "error")
                return redirect(url_for("auth.login"))

            report_type = request.form.get("report_type", "lost")
            if report_type not in {"lost", "found"}:
                report_type = "lost"

            pet_name = request.form.get("pet_name", "").strip()
            pet_type = request.form.get("pet_type", "").strip()
            breed = request.form.get("breed", "").strip()
            location = request.form.get("location", "").strip()
            event_date = request.form.get("event_date", "").strip()
            description = request.form.get("description", "").strip()
            contact_info = request.form.get("contact_info", "").strip()
            reward = request.form.get("reward", "").strip()
            photo_url = None

            photo = request.files.get("photo")
            if photo and photo.filename:
                uploads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
                os.makedirs(uploads_dir, exist_ok=True)
                filename = secure_filename(photo.filename)
                filename = f"lostfound_{session.get('user_id')}_{uuid.uuid4().hex}_{filename}"
                dest = os.path.join(uploads_dir, filename)
                photo.save(dest)
                photo_url = f"uploads/{filename}"

            if not pet_name or not pet_type or not location or not description or not contact_info:
                flash("Please complete the required report fields.", "error")
                return redirect(url_for("lost_found"))

            create_lost_found_report(
                session.get("user_id"),
                report_type,
                pet_name,
                pet_type,
                breed,
                location,
                event_date,
                description,
                contact_info,
                reward,
                photo_url,
                current_app.config.get("AUTH_DB_PATH"),
            )
            flash(f"Your {report_type} pet report was posted.", "success")
            return redirect(url_for("lost_found"))

        reports = get_recent_lost_found_reports(8, current_app.config.get("AUTH_DB_PATH"))
        return render_template("lost_found.html", reports=reports)


    @app.route("/lost-found/<int:report_id>/delete", methods=["POST"])
    def delete_report(report_id: int):
        from .database import get_lost_found_report, delete_lost_found_report

        if not session.get("user_id"):
            flash("Please sign in to manage reports.", "error")
            return redirect(url_for("auth.login"))

        report = get_lost_found_report(report_id, current_app.config.get("AUTH_DB_PATH"))
        if not report:
            flash("Report not found.", "error")
            return redirect(url_for("lost_found"))

        # Only the original reporter or an admin can delete
        allowed = session.get("user_id") == report["user_id"] or session.get("is_admin")
        if not allowed:
            flash("You don't have permission to delete this report.", "error")
            return redirect(url_for("lost_found"))

        # Remove uploaded photo file if present
        try:
            if report["photo_url"]:
                photo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", report["photo_url"].replace("/", os.sep))
                if os.path.exists(photo_path):
                    os.remove(photo_path)
        except Exception:
            pass

        delete_lost_found_report(report_id, current_app.config.get("AUTH_DB_PATH"))
        flash("Report deleted.", "success")
        return redirect(url_for("lost_found"))

    @app.route("/community", methods=["GET", "POST"])
    def community():
        from .database import create_community_post, get_recent_community_posts
        from werkzeug.utils import secure_filename

        if request.method == "POST":
            if not session.get("user_id"):
                flash("Please sign in to create a community post.", "error")
                return redirect(url_for("auth.login"))

            category = request.form.get("category", "adoption").strip().lower()
            if category not in {"adoption", "tips", "occasion", "question", "update"}:
                category = "adoption"

            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()
            location = request.form.get("location", "").strip()
            photo_url = None

            photo = request.files.get("photo")
            if photo and photo.filename:
                uploads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
                os.makedirs(uploads_dir, exist_ok=True)
                filename = secure_filename(photo.filename)
                filename = f"community_{session.get('user_id')}_{uuid.uuid4().hex}_{filename}"
                dest = os.path.join(uploads_dir, filename)
                photo.save(dest)
                photo_url = f"uploads/{filename}"

            if not title or not content:
                flash("Please add both a title and a post message.", "error")
                return redirect(url_for("community"))

            create_community_post(
                session.get("user_id"),
                category,
                title,
                content,
                location,
                photo_url,
                current_app.config.get("AUTH_DB_PATH"),
            )
            flash("Your community post was published.", "success")
            return redirect(url_for("community"))

        posts = get_recent_community_posts(12, current_app.config.get("AUTH_DB_PATH"))
        return render_template("community.html", posts=posts)


    @app.route("/community/<int:post_id>/delete", methods=["POST"])
    def delete_community_post(post_id: int):
        from .database import delete_community_post, get_community_post

        if not session.get("user_id"):
            flash("Please sign in to manage community posts.", "error")
            return redirect(url_for("auth.login"))

        post = get_community_post(post_id, current_app.config.get("AUTH_DB_PATH"))
        if not post:
            flash("Post not found.", "error")
            return redirect(url_for("community"))

        if int(session.get("user_id")) != int(post["user_id"]) and not session.get("is_admin"):
            flash("You can only delete your own post.", "error")
            return redirect(url_for("community"))

        try:
            if post["photo_url"]:
                photo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", post["photo_url"].replace("/", os.sep))
                if os.path.exists(photo_path):
                    os.remove(photo_path)
        except Exception:
            pass

        delete_community_post(post_id, current_app.config.get("AUTH_DB_PATH"))
        flash("Your post was deleted.", "success")
        return redirect(url_for("community"))

    @app.route("/pet-care-tips")
    def pet_care_tips():
        return render_template("pet_care_tips.html")

    @app.route("/my-note", methods=["GET", "POST"])
    def my_note():
        from .database import create_pet_note, get_pet_notes_by_user
        from werkzeug.utils import secure_filename

        if not session.get("user_id"):
            flash("Please sign in to view and save your pet notes.", "error")
            return redirect(url_for("auth.login"))

        if request.method == "POST":
            pet_name = request.form.get("pet_name", "").strip()
            species = request.form.get("species", "").strip()
            age = request.form.get("age", "").strip()
            vaccine_date = request.form.get("vaccine_date", "").strip()
            notes = request.form.get("notes", "").strip()
            photo_url = None

            photo = request.files.get("photo")
            if photo and photo.filename:
                uploads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
                os.makedirs(uploads_dir, exist_ok=True)
                filename = secure_filename(photo.filename)
                filename = f"petnote_{session.get('user_id')}_{uuid.uuid4().hex}_{filename}"
                dest = os.path.join(uploads_dir, filename)
                photo.save(dest)
                photo_url = f"uploads/{filename}"

            if not pet_name or not species or not age or not vaccine_date or not notes:
                flash("Please complete all required pet note fields.", "error")
                return redirect(url_for("my_note"))

            create_pet_note(
                session.get("user_id"),
                pet_name,
                species,
                age,
                vaccine_date,
                notes,
                photo_url,
                current_app.config.get("AUTH_DB_PATH"),
            )
            flash("Pet note saved to your account.", "success")
            return redirect(url_for("my_note"))

        notes = get_pet_notes_by_user(session.get("user_id"), current_app.config.get("AUTH_DB_PATH"))
        return render_template("my_note.html", notes=notes)

    @app.route("/my-note/<int:note_id>/delete", methods=["POST"])
    def delete_my_note(note_id: int):
        from .database import delete_pet_note, get_pet_note

        if not session.get("user_id"):
            flash("Please sign in to manage your pet notes.", "error")
            return redirect(url_for("auth.login"))

        note = get_pet_note(note_id, current_app.config.get("AUTH_DB_PATH"))
        if not note:
            flash("Pet note not found.", "error")
            return redirect(url_for("my_note"))

        if int(session.get("user_id")) != int(note["user_id"]):
            flash("You can only delete your own pet notes.", "error")
            return redirect(url_for("my_note"))

        try:
            if note["photo_url"]:
                photo_path = os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    "static",
                    note["photo_url"].replace("/", os.sep),
                )
                if os.path.exists(photo_path):
                    os.remove(photo_path)
        except Exception:
            pass

        delete_pet_note(note_id, current_app.config.get("AUTH_DB_PATH"))
        flash("Pet note deleted.", "success")
        return redirect(url_for("my_note"))

    @app.route("/dashboard", methods=["GET", "POST"])
    def dashboard():
        from flask import session, redirect, request, flash, current_app, url_for
        from .database import get_user_by_id, update_user_profile, get_all_users, get_user_activity_counts
        from werkzeug.utils import secure_filename
        import os

        if not session.get("user_id"):
            return redirect("/login")

        user = get_user_by_id(session.get("user_id"), current_app.config.get("AUTH_DB_PATH"))
        if not user:
            session.clear()
            flash("Your session expired. Please sign in again.", "error")
            return redirect(url_for("auth.login"))

        if request.method == "POST":
            if request.form.get("action") == "delete":
                from .database import delete_user

                if session.get("is_admin"):
                    flash("Admin accounts cannot be deleted from the dashboard.", "error")
                    return redirect(url_for("dashboard"))

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

            name = request.form.get("name", user["name"] if user else "")
            email = request.form.get("email", user["email"] if user else "")
            address = request.form.get("address", user["address"] if user else "")

            if email.strip().lower() == "admin@admin.com" and not session.get("is_admin"):
                flash("This email is reserved for administrators.", "error")
                return redirect(url_for("dashboard"))

            photo_filename = None
            photo = request.files.get("photo")
            if photo and photo.filename:
                uploads_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "uploads")
                os.makedirs(uploads_dir, exist_ok=True)
                filename = secure_filename(photo.filename)
                filename = f"user_{session.get('user_id')}_" + filename
                dest = os.path.join(uploads_dir, filename)
                photo.save(dest)
                photo_filename = f"uploads/{filename}"

            update_user_profile(session.get("user_id"), name, email, address, photo_filename, current_app.config.get("AUTH_DB_PATH"))
            session["user_name"] = name
            session["user_email"] = email
            flash("Profile updated successfully.", "success")
            return redirect(url_for("dashboard"))

        activity = get_user_activity_counts(session.get("user_id"), current_app.config.get("AUTH_DB_PATH"))
        all_users = get_all_users(current_app.config.get("AUTH_DB_PATH")) if session.get("is_admin") else None

        return render_template(
            "dashboard.html",
            user=user,
            activity=activity,
            all_users=all_users,
            is_admin=session.get("is_admin", False),
        )


    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been signed out.", "success")
        return redirect(url_for("home"))
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
