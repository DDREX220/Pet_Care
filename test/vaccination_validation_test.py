import unittest
from datetime import date, timedelta
from app.models.vaccination_model import Vaccination


class TestVaccinationValidation(unittest.TestCase):

    def test_empty_vaccine_name_is_rejected(self):
        error = Vaccination.validate("", "2026-01-01")
        self.assertEqual(error, "Vaccine name is required.")

    def test_invalid_date_format_is_rejected(self):
        error = Vaccination.validate("Rabies", "01-01-2026")
        self.assertEqual(error, "Invalid date format. Use YYYY-MM-DD.")

    def test_future_date_is_rejected(self):
        future_date = (date.today() + timedelta(days=10)).strftime("%Y-%m-%d")
        error = Vaccination.validate("Rabies", future_date)
        self.assertEqual(error, "Vaccination date cannot be in the future.")

    def test_valid_vaccination_passes(self):
        error = Vaccination.validate("Rabies", "2026-01-01")
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()