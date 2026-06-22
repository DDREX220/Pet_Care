import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, Blueprint, session, get_flashed_messages
from app.controllers.authcontroller import AuthController


def make_test_app():
    app = Flask(__name__)
    app.secret_key = "test-secret-key"

    bp = Blueprint("auth", __name__)
    bp.route("/", endpoint="home")(lambda: "home")
    bp.route("/login", endpoint="login")(lambda: "login")
    bp.route("/dashboard", endpoint="dashboard")(lambda: "dashboard")
    bp.route("/register", endpoint="register")(lambda: "register")

    pets_bp = Blueprint("pets", __name__)
    pets_bp.route("/pets", endpoint="view_pets")(lambda: "pets")

    app.register_blueprint(bp)
    app.register_blueprint(pets_bp)
    return app


class TestRegister(unittest.TestCase):
    def setUp(self):
        self.app = make_test_app()
        self.controller = AuthController()

    @patch("app.controllers.authcontroller.render_template")
    def test_register_get_shows_form(self, mock_render):
        """Visiting register with GET should show the register form."""
        mock_render.return_value = "register_page"
        with self.app.test_request_context(method="GET"):
            result = self.controller.register()
            self.assertEqual(result, "register_page")
            mock_render.assert_called_once_with("register.html")

    @patch("app.controllers.authcontroller.render_template")
    def test_register_password_mismatch_is_rejected(self, mock_render):
        """If password and confirm_password do not match, registration is refused."""
        mock_render.return_value = "register_page"
        with self.app.test_request_context(
            method="POST",
            data={"name": "Bob", "email": "bob@example.com",
                  "password": "secret1", "confirm_password": "different"},
        ):
            self.controller.register()
            flashes = get_flashed_messages(with_categories=True)
            self.assertIn(("danger", "Passwords do not match."), flashes)

    @patch("app.controllers.authcontroller.User")
    @patch("app.controllers.authcontroller.render_template")
    def test_register_duplicate_email_is_rejected(self, mock_render, mock_user_class):
        """If the email already exists, registration is refused."""
        mock_render.return_value = "register_page"
        mock_user_class.get_by_email.return_value = {"id": 1, "email": "taken@example.com"}

        with self.app.test_request_context(
            method="POST",
            data={"name": "Bob", "email": "taken@example.com",
                  "password": "secret1", "confirm_password": "secret1"},
        ):
            self.controller.register()
            flashes = get_flashed_messages(with_categories=True)
            self.assertIn(("danger", "Email already registered."), flashes)
            mock_user_class.assert_not_called()

    @patch("app.controllers.authcontroller.User")
    def test_register_success_saves_user_and_redirects(self, mock_user_class):
        """A valid new user is saved and sent to the login page."""
        mock_user_class.get_by_email.return_value = None
        fake_user = MagicMock()
        mock_user_class.return_value = fake_user

        with self.app.test_request_context(
            method="POST",
            data={"name": "Alice", "email": "alice@example.com",
                  "password": "secret1", "confirm_password": "secret1"},
        ):
            response = self.controller.register()
            fake_user.save.assert_called_once()
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login", response.location)
            flashes = get_flashed_messages(with_categories=True)
            self.assertIn(
                ("success", "Registration successful! Please login."), flashes
            )


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = make_test_app()
        self.controller = AuthController()

    @patch("app.controllers.authcontroller.render_template")
    def test_login_get_shows_form(self, mock_render):
        """Visiting login with GET should show the login form."""
        mock_render.return_value = "login_page"
        with self.app.test_request_context(method="GET"):
            result = self.controller.login()
            self.assertEqual(result, "login_page")
            mock_render.assert_called_once_with("login.html")

    @patch("app.controllers.authcontroller.User")
    @patch("app.controllers.authcontroller.render_template")
    def test_login_wrong_password_is_rejected(self, mock_render, mock_user_class):
        """A correct email but wrong password is refused."""
        mock_render.return_value = "login_page"
        mock_user_class.get_by_email.return_value = {
            "id": 1, "name": "Bob", "email": "bob@example.com",
            "role": "user", "password": "hashed_pw",
        }
        mock_user_class.check_password.return_value = False

        with self.app.test_request_context(
            method="POST",
            data={"email": "bob@example.com", "password": "wrongpass"},
        ):
            self.controller.login()
            flashes = get_flashed_messages(with_categories=True)
            self.assertIn(("danger", "Invalid email or password."), flashes)
            self.assertNotIn("user_id", session)

    @patch("app.controllers.authcontroller.User")
    def test_login_success_sets_session_and_redirects(self, mock_user_class):
        """A correct login stores the user in the session and redirects."""
        mock_user_class.get_by_email.return_value = {
            "id": 2, "name": "Bob", "email": "bob@example.com",
            "role": "user", "password": "hashed_pw",
        }
        mock_user_class.check_password.return_value = True

        with self.app.test_request_context(
            method="POST",
            data={"email": "bob@example.com", "password": "secret1"},
        ):
            response = self.controller.login()
            self.assertEqual(session["user_id"], 2)
            self.assertEqual(session["name"], "Bob")
            self.assertEqual(session["role"], "user")
            self.assertEqual(response.status_code, 302)
            flashes = get_flashed_messages(with_categories=True)
            self.assertIn(("success", "Welcome back, Bob!"), flashes)


class TestLogout(unittest.TestCase):
    def setUp(self):
        self.app = make_test_app()
        self.controller = AuthController()

    def test_logout_clears_session_and_redirects(self):
        """Logging out wipes the session and returns to the login page."""
        with self.app.test_request_context():
            session["user_id"] = 99
            session["name"] = "Alice"
            session["role"] = "user"

            response = self.controller.logout()

            self.assertNotIn("user_id", session)
            self.assertNotIn("name", session)
            self.assertNotIn("role", session)
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login", response.location)
            flashes = get_flashed_messages(with_categories=True)
            self.assertIn(("info", "You have been logged out."), flashes)


if __name__ == "__main__":
    unittest.main()