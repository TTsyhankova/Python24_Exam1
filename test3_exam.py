import unittest
from unittest.mock import MagicMock
from exam4_3 import HouseRepository, HouseManagementService, Validator, Resident

class TestHouseManagementService(unittest.TestCase):
    def setUp(self):
        # Мокаємо репозиторій, щоб не використовувати реальні дані
        self.repository = MagicMock(spec=HouseRepository)
        # Мокаємо data, щоб воно було доступне у репозиторії
        self.repository.data = {"residents": []}  # Підготовка порожнього списку для мешканців
        self.service = HouseManagementService(self.repository)

    def test_add_resident_success(self):
        """Перевірка додавання мешканця з правильними даними."""
        # Підготовка
        self.repository.add_resident = MagicMock()  # Мокаємо додавання мешканця

        # Дані для мешканця
        name = "John Doe"
        tax_id = "123456789"
        birthdate = "1985-05-15"
        phone = "050-123-45-67"
        email = "john.doe@example.com"
        additional_info = "Additional info"

        # Мокаємо метод generate_report_residents, щоб він не виконувався
        self.service.generate_report_residents = MagicMock()

        # Виклик методу
        self.service.add_resident(name, tax_id, birthdate, phone, email, additional_info)

        # Перевірка, чи був викликаний метод для додавання мешканця
        self.repository.add_resident.assert_called_once()

        # Перевірка, чи був викликаний метод для генерації звіту
        self.service.generate_report_residents.assert_called_once()

    def test_add_resident_invalid_tax_id(self):
        """Перевірка додавання мешканця з неправильним ІПН."""
        name = "John Doe"
        tax_id = "12345"  # Некоректний ІПН
        birthdate = "1985-05-15"
        phone = "050-123-45-67"
        email = "john.doe@example.com"
        additional_info = "Additional info"

        # Виклик методу
        self.service.add_resident(name, tax_id, birthdate, phone, email, additional_info)

        # Перевірка, чи не було додано мешканця (метод не повинен бути викликаний)
        self.repository.add_resident.assert_not_called()

    # Інші тести...

if __name__ == "__main__":
    unittest.main()