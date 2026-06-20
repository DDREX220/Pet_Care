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
                session['user_name'] = user['name']
                session['role'] = user['role']
                session['is_admin'] = (user['role'] == 'admin')
                flash(f"Welcome back, {user['name']}!", "success")
                return redirect(url_for("auth.dashboard"))
            else:
                flash("Invalid email or password.", "danger")
        
        return render_template("login.html")

    def register(self):
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            
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
        return redirect(url_for("auth.dashboard"))

    @login_required
    def reset_password(self):
        if request.method == "POST":
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")
            
            user_id = session.get("user_id")
            user = User.get_by_id(user_id)
            
            if not User.check_password(user['password'], current_password):
                flash("Current password is incorrect.", "danger")
                return redirect(url_for("auth.dashboard", pwd_error=1))
                
            if new_password != confirm_password:
                flash("New passwords do not match.", "danger")
                return redirect(url_for("auth.dashboard"))
            
            User.update_password(user_id, new_password)
            flash("Password updated successfully!", "success")
            return redirect(url_for("auth.dashboard"))
            
        return redirect(url_for("auth.dashboard"))

    @login_required
    def dashboard(self):
        from app.models.pet_model import Pet
        from app.models.reminder import Reminder

        user_id = session.get("user_id")
        is_admin = session.get("is_admin", False)

        if request.method == "POST":
            if request.form.get("action") == "delete":
                User.delete(user_id)
                session.clear()
                flash("Your account has been deleted.", "info")
                return redirect(url_for("auth.login"))

            name = request.form.get("name")
            email = request.form.get("email")
            address = request.form.get("address")
            try:
                User.update_profile(user_id, name, email, address)
                session['name'] = name
                session['user_name'] = name
                flash("Profile updated successfully!", "success")
            except Exception:
                flash("Error updating profile. Email might already be in use.", "danger")
            return redirect(url_for("auth.dashboard"))

        pwd_error = request.args.get("pwd_error")

        user = User.get_by_id(user_id)
        pets = Pet.get_all_by_user(user_id)
        reminders = Reminder.get_all_by_user(user_id)

        activity = {
            "posts": 0,
            "reports": 0,
        }

        all_users = User.get_all() if is_admin else None

        return render_template(
            "dashboard.html",
            user=user,
            is_admin=is_admin,
            activity=activity,
            all_users=all_users,
            total_pets=len(pets),
            total_reminders=len(reminders),
            pwd_error=pwd_error
        )