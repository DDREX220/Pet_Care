import unittest
from app.models.medical_model import MedicalNote


class TestMedicalNoteValidation(unittest.TestCase):

    def test_empty_title_is_rejected(self):
        error = MedicalNote.validate("", "Pet is healthy")
        self.assertEqual(error, "Title is required.")

    def test_empty_description_is_rejected(self):
        error = MedicalNote.validate("Checkup", "")
        self.assertEqual(error, "Description is required.")

    def test_long_title_is_rejected(self):
        long_title = "A" * 101
        error = MedicalNote.validate(long_title, "Some notes")
        self.assertEqual(error, "Title must be under 100 characters.")

    def test_valid_note_passes(self):
        error = MedicalNote.validate("Checkup", "Pet is healthy, weight normal.")
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()