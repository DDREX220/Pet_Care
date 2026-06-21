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
            status = request.form.get("report_type")
            name = request.form.get("pet_name")
            animal_type = request.form.get("pet_type")
            breed = request.form.get("breed")
            age = request.form.get("age")
            location = request.form.get("location")
            contact_info = request.form.get("contact_info")
            description = request.form.get("description")

            user_id = session.get("user_id")

            # Handle photo upload
            photo_filename = None
            photo_file = request.files.get("photo")
            if photo_file and photo_file.filename:
                from werkzeug.utils import secure_filename

                filename = secure_filename(f"lf_{user_id}_{photo_file.filename}")
                upload_folder = os.path.join("app", "static", "uploads")
                os.makedirs(upload_folder, exist_ok=True)
                photo_file.save(os.path.join(upload_folder, filename))
                photo_filename = f"uploads/{filename}"

            full_description = f"{status.upper()} | Name: {name} | Type: {animal_type} | Contact: {contact_info} | {description}"
            if status == "lost":
                LostFound.report_lost(user_id, None, location, full_description, contact_info, photo_filename)
            else:
                LostFound.report_found(user_id, location, full_description, contact_info, photo_filename)
            flash(f"{status.capitalize()} report submitted successfully!", "success")
            return redirect(url_for("lost_found.view_lost"))

        return render_template("lost_found/report_lost.html")

    def view_lost(self):
        raw_reports = list(LostFound.get_all_lost() or [])
        raw_found = list(LostFound.get_all_found() or [])

        reports = []
        for r in raw_reports + raw_found:
            reports.append({
                'id': r.get('id'),
                'user_id': r.get('user_id'),
                'pet_name': r.get('pet_name') or 'Unknown',
                'pet_type': r.get('species') or '',
                'breed': r.get('breed') or '',
                'location': r.get('location') or '',
                'description': r.get('description') or '',
                'photo_url': r.get('photo') or '',
                'report_type': r.get('type') or '',
                'reporter_name': r.get('owner_name') or r.get('reporter_name') or 'Unknown',
                'event_date': r.get('created_at') or '',
                'reward': r.get('reward') or '',
                'contact_info': r.get('contact_info') or '',
            })

        return render_template("lost_found.html", reports=reports)

    @login_required
    def mark_as_found(self, report_id):
        user_id = session.get("user_id")
        LostFound.mark_as_found(report_id, user_id)
        flash("Report marked as resolved!", "success")
        return redirect(url_for("lost_found.view_lost"))