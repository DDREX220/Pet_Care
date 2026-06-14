from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


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