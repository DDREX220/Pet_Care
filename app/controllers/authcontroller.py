import secrets

from flask import current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import (
    create_password_reset_token,
    create_user,
    delete_password_reset_token,
    get_password_reset_token,
    get_user_by_email,
    update_user_password,
)
from app.email_utils import send_password_reset_email


class AuthController:
    def login(self):
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")

            user = get_user_by_email(email, current_app.config.get("AUTH_DB_PATH"))
            if user and check_password_hash(user["password_hash"], password):
                role = user["role"] if user["role"] else "user"
                session["user_id"] = user["id"]
                session["user_name"] = user["name"]
                session["user_email"] = user["email"]
                session["user_role"] = role
                session["is_admin"] = role == "admin"
                flash(f"Welcome back, {user['name']}!", "success")
                return redirect(url_for("dashboard"))

            flash("Invalid email or password.", "error")

        return render_template("login.html")
    
    def register(self):
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not name or not email or not password:
                flash("Please fill in all required fields.", "error")
                return render_template("register.html")

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return render_template("register.html")

            if email == "admin@admin.com":
                flash("This email is reserved for administrators.", "error")
                return render_template("register.html")

            existing_user = get_user_by_email(email, current_app.config.get("AUTH_DB_PATH"))
            if existing_user:
                flash("An account with that email already exists.", "error")
                return render_template("register.html")

            password_hash = generate_password_hash(password)
            create_user(name, email, password_hash, current_app.config.get("AUTH_DB_PATH"))
            flash("Account created successfully. Please sign in.", "success")
            return redirect(url_for("auth.login"))

        return render_template("register.html")

    def forgot_password(self):
        if request.method == "POST":
            email = request.form.get("email", "").strip().lower()
            if not email:
                flash("Please enter your email address.", "error")
                return render_template("forgot_password.html")

            db_path = current_app.config.get("AUTH_DB_PATH")
            user = get_user_by_email(email, db_path)
            if user:
                token = secrets.token_urlsafe(32)
                create_password_reset_token(user["id"], token, db_path)
                reset_url = url_for("auth.reset_password", token=token, _external=True)
                emailed = send_password_reset_email(user["email"], reset_url)
                if not emailed and current_app.debug:
                    flash(
                        f"Email is not configured. Use this reset link: {reset_url}",
                        "success",
                    )
                    return redirect(url_for("auth.login"))

            flash(
                "If an account exists for that email, password reset instructions have been sent.",
                "success",
            )
            return redirect(url_for("auth.login"))

        return render_template("forgot_password.html")

    def reset_password(self, token):
        db_path = current_app.config.get("AUTH_DB_PATH")
        record = get_password_reset_token(token, db_path)
        if not record:
            flash("This password reset link is invalid or has expired.", "error")
            return redirect(url_for("auth.forgot_password"))

        if request.method == "POST":
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not password:
                flash("Please enter a new password.", "error")
                return render_template("reset_password.html", token=token)

            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return render_template("reset_password.html", token=token)

            password_hash = generate_password_hash(password)
            update_user_password(record["user_id"], password_hash, db_path)
            delete_password_reset_token(token, db_path)
            flash("Your password has been reset. Please sign in.", "success")
            return redirect(url_for("auth.login"))

        return render_template("reset_password.html", token=token)