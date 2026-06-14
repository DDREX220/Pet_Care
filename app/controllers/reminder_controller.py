from flask import render_template, redirect, url_for, flash, session, request
from app.models.reminder import Reminder
from app.auth import login_required

class ReminderController:

    @login_required
    def add_reminder(self):
        if request.method == "POST":
            title = request.form.get("title")
            reminder_date = request.form.get("reminder_date")
            description = request.form.get("description")
            user_id = session.get("user_id")

            if not title or not reminder_date:
                flash("Title and date are required.", "danger")
                return render_template("reminders/add_reminder.html")

            Reminder.add(user_id, title, description, reminder_date)
            flash("Reminder added successfully!", "success")
            return redirect(url_for("reminders.view_reminders"))

        return render_template("reminders/add_reminder.html")

    @login_required
    def view_reminders(self):
        user_id = session.get("user_id")
        reminders = Reminder.get_all_by_user(user_id)
        return render_template("reminders/view_reminders.html", 
                               reminders=reminders)

    @login_required
    def delete_reminder(self, reminder_id):
        user_id = session.get("user_id")
        Reminder.delete(reminder_id, user_id)
        flash("Reminder removed successfully!", "success")
        return redirect(url_for("reminders.view_reminders"))