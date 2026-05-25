from flask import flash, redirect, render_template, request, url_for
from pymysql import MySQLError

from app.database import connection_scope, ensure_schema
from werkzeug.security import check_password_hash, generate_password_hash


class AuthController:
    def login(self):
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()

            if not email or not password:
                flash("Email and password are required.")
                return render_template("login.html", email=email), 400

            try:
                ensure_schema()
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT id, name, email, password_hash FROM users WHERE email = %s",
                            (email,),
                        )
                        user = cursor.fetchone()

                if user is None or not check_password_hash(user["password_hash"], password):
                    flash("Invalid email or password.")
                    return render_template("login.html", email=email), 401

                flash(f"Welcome back, {user['name']}.")
                return redirect(url_for("home"))
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("login.html", email=email), 500

        return render_template("login.html")
    
    def register(self):
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()

            if not name or not email or not password:
                flash("Name, email, and password are required.")
                return render_template("register.html", name=name, email=email), 400

            try:
                ensure_schema()
                password_hash = generate_password_hash(password)

                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
                        existing_user = cursor.fetchone()

                        if existing_user is not None:
                            flash("An account with that email already exists.")
                            return render_template("register.html", name=name, email=email), 409

                        cursor.execute(
                            "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s)",
                            (name, email, password_hash),
                        )
                    connection.commit()

                flash(f"Account created for {name}.")
                return redirect(url_for("auth.login"))
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("register.html", name=name, email=email), 500

        return render_template("register.html")

    def profile(self):
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()

            if not name or not email:
                flash("Name and email are required.")
                return render_template("profile.html", name=name, email=email), 400

            try:
                ensure_schema()
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE users SET name = %s WHERE email = %s",
                            (name, email),
                        )
                    connection.commit()

                flash("Profile updated.")
                return render_template("profile.html", name=name, email=email)
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("profile.html", name=name, email=email), 500

        return render_template("profile.html")

    def reset_password(self):
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            new_password = request.form.get("new_password", "").strip()
            confirm_password = request.form.get("confirm_password", "").strip()

            if not email or not new_password or not confirm_password:
                flash("Email and both password fields are required.")
                return render_template("reset_password.html", email=email), 400

            if new_password != confirm_password:
                flash("Passwords do not match.")
                return render_template("reset_password.html", email=email), 400

            try:
                ensure_schema()
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "UPDATE users SET password_hash = %s WHERE email = %s",
                            (generate_password_hash(new_password), email),
                        )
                    connection.commit()

                flash("Password updated.")
                return redirect(url_for("auth.login"))
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("reset_password.html", email=email), 500

        return render_template("reset_password.html")