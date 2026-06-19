import unittest
from app.models.pet_model import Pet


class TestPetValidation(unittest.TestCase):

    def test_empty_name_is_rejected(self):
        error = Pet.validate("", "Dog", 3)
        self.assertEqual(error, "Pet name is required.")

    def test_empty_species_is_rejected(self):
        error = Pet.validate("Buddy", "", 3)
        self.assertEqual(error, "Species is required.")

    def test_negative_age_is_rejected(self):
        error = Pet.validate("Buddy", "Dog", -1)
        self.assertEqual(error, "Age cannot be negative.")

    def test_non_numeric_age_is_rejected(self):
        error = Pet.validate("Buddy", "Dog", "abc")
        self.assertEqual(error, "Age must be a number.")

    def test_valid_pet_passes(self):
        error = Pet.validate("Buddy", "Dog", 3)
        self.assertIsNone(error)

    def test_valid_pet_with_no_age_passes(self):
        error = Pet.validate("Buddy", "Dog", None)
        self.assertIsNone(error)


if __name__ == "__main__":
    unittest.main()