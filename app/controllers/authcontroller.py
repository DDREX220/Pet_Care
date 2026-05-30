from flask import render_template, request, redirect, url_for, flash, session
from app.models.user_model import User
from app.auth import login_required

class AuthController:
    def login(self):
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")
            
            user = User.get_by_email(email)
            if user and User.check_password(user['password'], password):
                session['user_id'] = user['id']
                session['name'] = user['name']
                session['role'] = user['role']
                flash(f"Welcome back, {user['name']}!", "success")
                return redirect(url_for("pets.view_pets"))
            else:
                flash("Invalid email or password.", "danger")
        
        return render_template("login.html")

    def register(self):
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirm_password")
            
            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                return render_template("register.html")
            
            if User.get_by_email(email):
                flash("Email already registered.", "danger")
                return render_template("register.html")
            
            new_user = User(name, email, password)
            new_user.save()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))
            
        return render_template("register.html")

    def logout(self):
        session.clear()
        flash("You have been logged out.", "info")
        return redirect(url_for("auth.login"))

    @login_required
    def profile(self):
        user_id = session.get("user_id")
        user = User.get_by_id(user_id)
        
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            
            User.update_profile(user_id, name, email)
            session['name'] = name
            flash("Profile updated successfully!", "success")
            return redirect(url_for("auth.profile"))
            
        return render_template("profile.html", user=user)

    @login_required
    def reset_password(self):
        if request.method == "POST":
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")
            
            user_id = session.get("user_id")
            user = User.get_by_id(user_id)
            
            if not User.check_password(user['password'], old_password):
                flash("Incorrect old password.", "danger")
                return render_template("reset_password.html")
                
            if new_password != confirm_password:
                flash("New passwords do not match.", "danger")
                return render_template("reset_password.html")
            
            User.update_password(user_id, new_password)
            flash("Password updated successfully!", "success")
            return redirect(url_for("auth.profile"))
            
        return render_template("reset_password.html")

    @login_required
    def dashboard(self):
        return render_template("dashboard.html")