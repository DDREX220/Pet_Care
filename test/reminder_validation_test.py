import unittest
from app.models.reminder import Reminder


class TestReminderValidation(unittest.TestCase):

    def test_empty_title_is_rejected(self):
        error = Reminder.validate("", "2026-06-25")
        self.assertEqual(error, "Title is required.")

    def test_invalid_date_format_is_rejected(self):
        error = Reminder.validate("Vet Appointment", "25-06-2026")
        self.assertEqual(error, "Invalid date format. Use YYYY-MM-DD.")

    def test_valid_reminder_passes(self):
        error = Reminder.validate("Vet Appointment", "2026-06-25")
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()