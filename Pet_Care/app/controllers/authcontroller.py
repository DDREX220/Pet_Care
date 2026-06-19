from flask import current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import create_user, get_user_by_email


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