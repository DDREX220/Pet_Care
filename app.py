from flask import Flask, render_template, request

app = Flask(__name__)

# Home Page (Figma Homepage)

@app.route("/")
def home():
    return render_template("home.html")


# Register Page

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        return f"""
        Name: {name}<br>
        Email: {email}<br>
        Password: {password}
        """

    return render_template("register.html")


# Login Page

@app.route("/login")
def login():
    return render_template("login.html")


# Dashboard Page

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# Pets Page

@app.route("/pets")
def pets():
    return render_template("pet.html", title="Pets | Pet Care")


# Profile Page

@app.route("/profile")
def profile():
    return render_template("profile.html")


# Reset Password Page

@app.route("/reset_password")
def reset_password():
    return render_template("reset_password.html")


if __name__ == "__main__":
    app.run(debug=True)