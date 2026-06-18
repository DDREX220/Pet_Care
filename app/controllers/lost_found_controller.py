from flask import render_template, request, redirect, url_for, flash, session
from app.models.lost_found_model import LostFound
from app.models.pet_model import Pet
from app.auth import login_required
import os

class LostFoundController:

    @login_required
    def report_lost_found(self):
        """Unified report method to match the frontend form."""
        if request.method == "POST":
            status = request.form.get("status") # 'lost' or 'found'
            name = request.form.get("name")
            animal_type = request.form.get("type")
            breed = request.form.get("breed")
            age = request.form.get("age")
            location = request.form.get("location")
            contact_info = request.form.get("contact_info")
            description = request.form.get("description")

            user_id = session.get("user_id")
            
            # Since the model expects pet_id for lost, but form gives name, 
            # we adapt the model or simplify the storage.
            # For now, we use report_found even for lost if pet_id is not known.
            LostFound.report_found(user_id, location, f"{status.upper()} | Name: {name} | Type: {animal_type} | Contact: {contact_info} | {description}")
            
            flash(f"{status.capitalize()} report submitted successfully!", "success")
            return redirect(url_for("lost_found.view_lost"))

        return render_template("lost_found/report_lost.html")

    def view_lost(self):
        reports = LostFound.get_all_lost()
        # Also getting 'found' reports for the same page
        found_reports = LostFound.get_all_found()
        return render_template("lost_found/view_lost.html",
                               reports=reports, found_reports=found_reports)

    @login_required
    def mark_as_found(self, report_id):
        user_id = session.get("user_id")
        LostFound.mark_as_found(report_id, user_id)
        flash("Report marked as resolved!", "success")
        return redirect(url_for("lost_found.view_lost"))
