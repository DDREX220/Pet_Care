import os
from flask import render_template, request, redirect, url_for, flash, session
from app.models.pet_model import Pet
from app.auth import login_required

class PetController:

    @login_required
    def add_pet(self):
        if request.method == "POST":
            name = request.form.get("name")
            species = request.form.get("species")
            breed = request.form.get("breed")
            age = request.form.get("age")
            gender = request.form.get("gender")
            photo = None

            # Handle photo upload
            if "photo" in request.files:
                file = request.files["photo"]
                if file.filename != "":
                    upload_folder = "app/static/uploads"
                    os.makedirs(upload_folder, exist_ok=True)
                    photo_path = os.path.join(upload_folder, file.filename)
                    file.save(photo_path)
                    photo = file.filename

            # Validation
            if not name or not species:
                flash("Pet name and species are required.", "danger")
                return render_template("pets/add_pet.html")

            user_id = session.get("user_id")
            pet = Pet(user_id, name, species, breed, age, gender, photo)
            pet.save()

            flash("Pet added successfully!", "success")
            return redirect(url_for("pets.view_pets"))

        return render_template("pets/add_pet.html")

    @login_required
    def view_pets(self):
        user_id = session.get("user_id")
        pets = Pet.get_all_by_user(user_id)
        return render_template("pets/view_pets.html", pets=pets)

    @login_required
    def edit_pet(self, pet_id):
        pet = Pet.get_by_id(pet_id)

        if not pet:
            flash("Pet not found.", "danger")
            return redirect(url_for("pets.view_pets"))

        if request.method == "POST":
            name = request.form.get("name")
            species = request.form.get("species")
            breed = request.form.get("breed")
            age = request.form.get("age")
            gender = request.form.get("gender")
            photo = None

            if "photo" in request.files:
                file = request.files["photo"]
                if file.filename != "":
                    upload_folder = "app/static/uploads"
                    os.makedirs(upload_folder, exist_ok=True)
                    photo_path = os.path.join(upload_folder, file.filename)
                    file.save(photo_path)
                    photo = file.filename

            Pet.update(pet_id, name, species, breed, age, gender, photo)
            flash("Pet updated successfully!", "success")
            return redirect(url_for("pets.view_pets"))

        return render_template("pets/edit_pet.html", pet=pet)

    @login_required
    def delete_pet(self, pet_id):
        Pet.delete(pet_id)
        flash("Pet deleted successfully!", "success")
        return redirect(url_for("pets.view_pets"))