import os
from flask import render_template, request, redirect, url_for, flash, session
from app.models.pet_model import Pet
from app.auth import login_required

class PetController:

    @login_required
    def view_pets(self):
        user_id = session.get("user_id")
        pets = Pet.get_all_by_user(user_id)
        return render_template("pets/view_pets.html", pets=pets)

    @login_required
    def save_pet(self):
        """Combined Add and Update method to match the single-page frontend."""
        if request.method == "POST":
            pet_id = request.form.get("pet_id")
            name = request.form.get("name")
            species = request.form.get("type")  # Template uses 'type', model uses 'species'
            breed = request.form.get("breed")
            age = request.form.get("age")
            age = int(age) if age and age.strip().isdigit() else None
            description = request.form.get("notes")  # Template uses 'notes'

            user_id = session.get("user_id")

            if pet_id:
                # Update existing pet
                Pet.update(pet_id, name, species, breed, age, "Not Set")
                flash("Pet updated successfully!", "success")
            else:
                # Add new pet
                pet = Pet(user_id, name, species, breed, age, "Not Set")
                pet.save()
                flash("Pet added successfully!", "success")

            return redirect(url_for("pets.view_pets"))

        return redirect(url_for("pets.view_pets"))

    @login_required
    def delete_pet(self, pet_id):
        Pet.delete(pet_id)
        flash("Pet deleted successfully!", "success")
        return redirect(url_for("pets.view_pets"))

    @login_required
    def search_pets(self):
        user_id = session.get("user_id")
        keyword = request.args.get("name", "")

        if keyword:
            pets = Pet.search_pets_by_name(user_id, keyword)
        else:
            pets = Pet.get_all_by_user(user_id)

        return render_template("pets/view_pets.html", pets=pets, search_keyword=keyword)