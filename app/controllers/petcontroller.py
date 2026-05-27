from flask import render_template


class PetController:
    def pets(self):
        return render_template("pet.html", title="Pets | Pet Care")