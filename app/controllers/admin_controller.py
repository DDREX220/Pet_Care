from flask import render_template, redirect, url_for, flash, session
from app.models.user_model import User
from app.models.lost_found_model import LostFound
from app.auth import admin_required

class AdminController:

    @admin_required
    def view_users(self):
        db_users = User.get_all()
        return render_template("admin/view_users.html", users=db_users)

    @admin_required
    def delete_user(self, user_id):
        current_user_id = session.get("user_id")

        if user_id == current_user_id:
            flash("You cannot delete yourself!", "danger")
            return redirect(url_for("admin.view_users"))

        User.delete(user_id)
        flash("User deleted successfully!", "success")
        return redirect(url_for("admin.view_users"))

    @admin_required
    def view_lost_reports(self):
        reports = LostFound.get_all_lost()
        return render_template("admin/view_lost_reports.html", 
                               reports=reports)