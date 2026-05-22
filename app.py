from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World! This is my first Flask website."

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

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)