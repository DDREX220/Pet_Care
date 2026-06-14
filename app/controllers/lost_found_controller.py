from flask import render_template, request, redirect, url_for, flash, session
from app.models.lost_found_model import LostFound
from app.models.pet_model import Pet
from app.auth import login_required
import os

class LostFoundController:

    @login_required
    def report_lost(self):
        user_id = session.get("user_id")
        pets = Pet.get_all_by_user(user_id)

        if request.method == "POST":
            pet_id = request.form.get("pet_id")
            location = request.form.get("location")
            description = request.form.get("description")

            if not pet_id or not location:
                flash("Pet and location are required.", "danger")
                return render_template("lost_found/report_lost.html", 
                                       pets=pets)

            LostFound.report_lost(user_id, pet_id, location, description)
            flash("Lost pet reported successfully!", "success")
            return redirect(url_for("lost_found.view_lost"))

        return render_template("lost_found/report_lost.html", pets=pets)

    @login_required
    def report_found(self):
        if request.method == "POST":
            location = request.form.get("location")
            description = request.form.get("description")
            photo = None

            if not location or not description:
                flash("Location and description are required.", "danger")
                return render_template("lost_found/report_found.html")

            # Handle photo upload
            if "photo" in request.files:
                file = request.files["photo"]
                if file.filename != "":
                    upload_folder = "app/static/uploads"
                    os.makedirs(upload_folder, exist_ok=True)
                    photo_path = os.path.join(upload_folder, file.filename)
                    file.save(photo_path)
                    photo = file.filename

            user_id = session.get("user_id")
            LostFound.report_found(user_id, location, description, photo)
            flash("Found pet reported successfully!", "success")
            return redirect(url_for("lost_found.view_found"))

        return render_template("lost_found/report_found.html")

    def view_lost(self):
        location = request.args.get("location", "")
        if location:
            reports = LostFound.filter_by_location(location)
        else:
            reports = LostFound.get_all_lost()
        return render_template("lost_found/view_lost.html",
                               reports=reports, location=location)

    def view_found(self):
        reports = LostFound.get_all_found()
        return render_template("lost_found/view_found.html", 
                               reports=reports)

    @login_required
    def mark_as_found(self, report_id):
        user_id = session.get("user_id")
        LostFound.mark_as_found(report_id, user_id)
        flash("Pet marked as found!", "success")
        return redirect(url_for("lost_found.view_lost"))