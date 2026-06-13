from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..database import connection_scope
from pymysql import MySQLError


class PetController:
    @login_required
    def pets(self):
        try:
            with connection_scope() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM pets WHERE user_id = %s AND status = 'owned' ORDER BY created_at DESC",
                        (current_user.id,)
                    )
                    pets_list = cursor.fetchall()
            return render_template("pet.html", title="My Pets | Pet Care", pets=pets_list)
        except MySQLError as error:
            flash(f"Database error: {error}")
            return render_template("pet.html", title="My Pets | Pet Care", pets=[])

    @login_required
    def save_pet(self):
        pet_id = request.form.get("pet_id")
        name = request.form.get("name")
        pet_type = request.form.get("type")
        breed = request.form.get("breed")
        age = request.form.get("age")
        notes = request.form.get("notes")

        try:
            with connection_scope() as connection:
                with connection.cursor() as cursor:
                    if pet_id:
                        cursor.execute(
                            """UPDATE pets SET name=%s, type=%s, breed=%s, age=%s, description=%s 
                               WHERE id=%s AND user_id=%s""",
                            (name, pet_type, breed, age, notes, pet_id, current_user.id)
                        )
                        flash("Pet updated successfully!")
                    else:
                        cursor.execute(
                            """INSERT INTO pets (user_id, name, type, breed, age, description, status) 
                               VALUES (%s, %s, %s, %s, %s, %s, 'owned')""",
                            (current_user.id, name, pet_type, breed, age, notes)
                        )
                        flash("Pet added successfully!")
                connection.commit()
            return redirect(url_for("pet.pets"))
        except MySQLError as error:
            flash(f"Database error: {error}")
            return redirect(url_for("pet.pets"))

    @login_required
    def delete_pet(self, pet_id):
        try:
            with connection_scope() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM pets WHERE id=%s AND user_id=%s", (pet_id, current_user.id))
                connection.commit()
            flash("Pet removed.")
            return redirect(url_for("pet.pets"))
        except MySQLError as error:
            flash(f"Database error: {error}")
            return redirect(url_for("pet.pets"))

    def lost_found(self):
        status_filter = request.args.get("status", "")
        location_filter = request.args.get("location", "")
        
        query = "SELECT * FROM pets WHERE status IN ('lost', 'found')"
        params = []
        
        if status_filter:
            query += " AND status = %s"
            params.append(status_filter)
        
        if location_filter:
            query += " AND location LIKE %s"
            params.append(f"%{location_filter}%")
            
        query += " ORDER BY created_at DESC"

        try:
            with connection_scope() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, tuple(params))
                    pets_list = cursor.fetchall()
            return render_template("lost_found.html", title="Lost & Found | Pet Care", pets=pets_list, 
                                 status_filter=status_filter, location_filter=location_filter)
        except MySQLError as error:
            flash(f"Database error: {error}")
            return render_template("lost_found.html", title="Lost & Found | Pet Care", pets=[])

    def report_lost_found(self):
        if request.method == "POST":
            name = request.form.get("name")
            pet_type = request.form.get("type")
            breed = request.form.get("breed")
            age = request.form.get("age")
            description = request.form.get("description")
            status = request.form.get("status") # 'lost' or 'found'
            location = request.form.get("location")
            contact_info = request.form.get("contact_info")
            user_id = current_user.id if current_user.is_authenticated else None

            try:
                with connection_scope() as connection:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO pets (user_id, name, type, breed, age, description, status, location, contact_info) 
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                            (user_id, name, pet_type, breed, age, description, status, location, contact_info)
                        )
                    connection.commit()
                flash(f"Report for {status} pet submitted!")
                return redirect(url_for("pet.lost_found"))
            except MySQLError as error:
                flash(f"Database error: {error}")
                return render_template("report_lost_found.html")

        return render_template("report_lost_found.html", title="Report Lost/Found Pet | Pet Care")

    @login_required
    def mark_as_found(self, pet_id):
        try:
            with connection_scope() as connection:
                with connection.cursor() as cursor:
                    # Only the person who reported it can mark it as found, or if it's their pet
                    cursor.execute(
                        "UPDATE pets SET status = 'owned' WHERE id = %s AND (user_id = %s OR status = 'found')",
                        (pet_id, current_user.id)
                    )
                connection.commit()
            flash("Pet marked as found/reunited!")
            return redirect(url_for("pet.lost_found"))
        except MySQLError as error:
            flash(f"Database error: {error}")
            return redirect(url_for("pet.lost_found"))