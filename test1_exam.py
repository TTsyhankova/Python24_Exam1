import unittest
from exam4_3 import Resident  # Імпорт класy Resident

class TestResident(unittest.TestCase):
    def setUp(self):
        """
        Налаштування, яке виконується перед кожним тестом.
        """
        self.resident1 = Resident(
            name="Андрій",
            tax_id="123456789",
            birthdate="1990-01-01",
            phone="050-123-45-67",
            email="andre@gmail.com",
            additional_info="має авто",
            apartment="5"
        )

        self.resident2 = Resident(
            name="Тамара",
            tax_id="987654321",
            birthdate="1985-05-15",
            phone="050-987-65-43",
            email="tamara@gmail.com",
            additional_info="має кішку",
            apartment="6"
        )

    def test_init(self):
        """
        Перевірка ініціалізації об'єкта Resident.
        """
        self.assertEqual(self.resident1.name, "Андрій")
        self.assertEqual(self.resident1.tax_id, "123456789")
        self.assertEqual(self.resident1.birthdate, "1990-01-01")
        self.assertEqual(self.resident1.phone, "050-123-45-67")
        self.assertEqual(self.resident1.email, "andre@gmail.com")
        self.assertEqual(self.resident1.additional_info, "має авто")
        self.assertEqual(self.resident1.apartment, "5")

    def test_to_dict(self):
        """
        Перевірка методу to_dict.
        """
        expected_dict = {
            "name": "Андрій",
            "tax_id": "123456789",
            "birthdate": "1990-01-01",
            "phone": "050-123-45-67",
            "email": "andre@gmail.com",
            "additional_info": "має авто",
            "apartment": "5"
        }
        self.assertEqual(self.resident1.to_dict(), expected_dict)

    def test_eq(self):
        """
        Перевірка порівняння об'єктів Resident.
        """
        same_resident = Resident(
            name="Андрій",
            tax_id="123456789",
            birthdate="1990-01-01",
            phone="050-123-45-67",
            email="andre@gmail.com",
            additional_info="має авто",
            apartment="5"
        )
        self.assertEqual(self.resident1, same_resident)
        self.assertNotEqual(self.resident1, self.resident2)

    def test_eq_different_type(self):
        """
        Перевірка порівняння Resident з об'єктом іншого типу.
        """
        self.assertNotEqual(self.resident1, "Some string")


if __name__ == "__main__":
    unittest.main()