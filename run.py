from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from functools import wraps
import jwt
from flask import request, jsonify

from functools import wraps
import jwt
from flask import request, jsonify

SECRET_KEY = "mysecretkey"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token missing"}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["user_id"]
        except:
            return jsonify({"message": "Invalid token"}), 403

        return f(current_user_id, *args, **kwargs)

    return decorated

app = Flask(__name__)

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="deeparshan@123",
    database="petcare_db"
)

# -------------------------
# REGISTER API
# -------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # basic validation
    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    hashed_password = generate_password_hash(password)

    try:
        cursor = db.cursor()

        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        values = (name, email, hashed_password)

        cursor.execute(sql, values)
        db.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except mysql.connector.IntegrityError:
        return jsonify({"message": "Email already exists"}), 409
    
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user["password"], password):
        return jsonify({"message": "Incorrect password"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }), 200

@app.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT id, name, email, created_at FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify(user), 200



@app.route("/dashboard", methods=["GET"])
@token_required
def dashboard(current_user_id):

    cursor = db.cursor(dictionary=True)

    # Get total users
    cursor.execute("SELECT COUNT(*) AS total_users FROM users")
    total_users = cursor.fetchone()["total_users"]

    # Get current user info
    cursor.execute(
        "SELECT id, name, email FROM users WHERE id = %s",
        (current_user_id,)
    )
    user = cursor.fetchone()

    return jsonify({
        "message": "Dashboard loaded successfully",
        "total_users": total_users,
        "current_user": user
    }), 200

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
      