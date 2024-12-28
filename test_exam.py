import unittest
from datetime import datetime
import re

from exam4_3 import Validator  # Імпорт класу Validator з файлу коду


class TestValidator(unittest.TestCase):

    def test_validate_phone(self):
        self.assertTrue(Validator.validate_phone("+38-050-123-45-67"))
        self.assertTrue(Validator.validate_phone("050-123-45-67"))
        self.assertFalse(Validator.validate_phone("+38-050-1234567"))
        self.assertFalse(Validator.validate_phone("123-456-7890"))

    def test_validate_email(self):
        self.assertTrue(Validator.validate_email("test@example.com"))
        self.assertTrue(Validator.validate_email("user.name+tag@domain.co.uk"))
        self.assertFalse(Validator.validate_email("invalid-email"))
        self.assertFalse(Validator.validate_email("user@domain"))

    def test_validate_tax_id(self):
        self.assertTrue(Validator.validate_tax_id("123456789"))
        self.assertFalse(Validator.validate_tax_id("12345"))
        self.assertFalse(Validator.validate_tax_id("1234567890"))
        self.assertFalse(Validator.validate_tax_id("abc123456"))

    def test_validate_date(self):
        self.assertTrue(Validator.validate_date("2023-12-28"))
        self.assertFalse(Validator.validate_date("28-12-2023"))
        self.assertFalse(Validator.validate_date("2023/12/28"))
        self.assertFalse(Validator.validate_date("invalid-date"))

    def test_validate_apartment(self):
        self.assertTrue(Validator.validate_apartment("123"))
        self.assertFalse(Validator.validate_apartment("A123"))
        self.assertFalse(Validator.validate_apartment("Apartment1"))
        self.assertFalse(Validator.validate_apartment(""))

if __name__ == "__main__":
    unittest.main()

