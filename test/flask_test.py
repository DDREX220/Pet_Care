import unittest
from flask import Flask, Blueprint
from app.auth import login_required

class TestFlaskBasics(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = "secret_keyy"
        auth = Blueprint("auth", __name__)

        @auth.route("/login")
        def login():
            return "this is the login page"

        @auth.route("/home")
        @login_required
        def home():
            return "welcome home"

        self.app.register_blueprint(auth)
        self.client = self.app.test_client()

    def test_locked_page_redirects_a_guest(self):
        response = self.client.get('/home')
        self.assertEqual(response.status_code, 302)  # Redirect to login page
        self.assertIn('/login', response.location)  # Check if redirected to login page

if __name__ == '__main__':
    unittest.main()