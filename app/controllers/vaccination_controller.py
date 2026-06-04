from flask import render_template, request, redirect, url_for, flash, session
from app.models.vaccination_model import Vaccination
from app.models.pet_model import Pet
from app.auth import login_required

class VaccinationController:

    @login_required
    def add_vaccination(self, pet_id):
        pet = Pet.get_by_id(pet_id)

        if not pet:
            flash("Pet not found.", "danger")
            return redirect(url_for("pets.view_pets"))

        if request.method == "POST":
            vaccine_name = request.form.get("vaccine_name")
            date_given = request.form.get("date_given")
            next_due_date = request.form.get("next_due_date")
            notes = request.form.get("notes")

            # Validation
            if not vaccine_name or not date_given:
                flash("Vaccine name and date are required.", "danger")
                return render_template("vaccinations/add_vaccination.html", pet=pet)

            vaccination = Vaccination(pet_id, vaccine_name, date_given, next_due_date, notes)
            vaccination.save()

            flash("Vaccination record added successfully!", "success")
            return redirect(url_for("vaccinations.view_vaccinations", pet_id=pet_id))

        return render_template("vaccinations/add_vaccination.html", pet=pet)

    @login_required
    def view_vaccinations(self, pet_id):
        pet = Pet.get_by_id(pet_id)

        if not pet:
            flash("Pet not found.", "danger")
            return redirect(url_for("pets.view_pets"))

        vaccinations = Vaccination.get_all_by_pet(pet_id)
        return render_template("vaccinations/view_vaccinations.html", 
                                pet=pet, vaccinations=vaccinations)

    @login_required
    def delete_vaccination(self, vaccination_id):
        Vaccination.delete(vaccination_id)
        flash("Vaccination record deleted successfully!", "success")
        return redirect(request.referrer or url_for("pets.view_pets"))