from flask import render_template, request, redirect, url_for, flash
from app.models.medical_model import MedicalNote
from app.models.pet_model import Pet
from app.auth import login_required

class MedicalController:

    @login_required
    def add_medical_note(self, pet_id):
        pet = Pet.get_by_id(pet_id)

        if not pet:
            flash("Pet not found.", "danger")
            return redirect(url_for("pets.view_pets"))

        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            date = request.form.get("date")

            # Validation
            if not title or not description or not date:
                flash("All fields are required.", "danger")
                return render_template("medical/add_medical_note.html", pet=pet)

            note = MedicalNote(pet_id, title, description, date)
            note.save()

            flash("Medical note added successfully!", "success")
            return redirect(url_for("medical.view_medical_notes", pet_id=pet_id))

        return render_template("medical/add_medical_note.html", pet=pet)

    @login_required
    def view_medical_notes(self, pet_id):
        pet = Pet.get_by_id(pet_id)

        if not pet:
            flash("Pet not found.", "danger")
            return redirect(url_for("pets.view_pets"))

        notes = MedicalNote.get_all_by_pet(pet_id)
        return render_template("medical/view_medical_notes.html",
                                pet=pet, notes=notes)

    @login_required
    def delete_medical_note(self, note_id):
        MedicalNote.delete(note_id)
        flash("Medical note deleted successfully!", "success")
        return redirect(request.referrer or url_for("pets.view_pets"))
    