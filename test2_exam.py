import unittest
from unittest.mock import MagicMock, patch
from exam4_3 import HouseRepository  # Імпортуємо клас з основного файлу


class TestHouseRepository(unittest.TestCase):

    @patch('exam4_3.FileManager')  # Патчимо клас FileManager
    def setUp(self, MockFileManager):
        # Створюємо мок для FileManager
        self.mock_file_manager = MagicMock()
        MockFileManager.return_value = self.mock_file_manager

        # Підготовка тестових даних
        self.mock_file_manager.load.return_value = {
            "residents": [
                {"tax_id": "123456789", "name": "John Doe", "email": "john.doe@example.com"},
                {"tax_id": "987654321", "name": "Jane Doe", "email": "jane.doe@example.com"}
            ],
            "apartments": [
                {"number": 101, "residents": [{"tax_id": "123456789"}]},
                {"number": 102, "residents": [{"tax_id": "987654321"}]}
            ]
        }

        # Ініціалізація HouseRepository
        self.repository = HouseRepository("test_file_path.json")

    def test_find_resident_by_tax_id(self):
        # Тест на пошук мешканця за ІПН
        resident = self.repository.find_resident_by_tax_id("123456789")
        self.assertIsNotNone(resident)
        self.assertEqual(resident["name"], "John Doe")

        # Тест на пошук неіснуючого мешканця
        resident = self.repository.find_resident_by_tax_id("111111111")
        self.assertIsNone(resident)

    def test_add_resident(self):
        # Тест на додавання мешканця
        new_resident = MagicMock()
        new_resident.tax_id = "1122334455"
        new_resident.to_dict.return_value = {"tax_id": "1122334455", "name": "New Resident"}

        self.repository.add_resident(new_resident)

        # Перевіряємо, чи викликано метод збереження
        self.mock_file_manager.save.assert_called_once()
        self.assertIn({"tax_id": "1122334455", "name": "New Resident"},
                      self.mock_file_manager.save.call_args[0][0]["residents"])

    def test_remove_resident(self):
        # Тест на видалення мешканця
        self.repository.remove_resident("123456789")

        # Перевіряємо, чи викликано метод збереження
        self.mock_file_manager.save.assert_called_once()
        # Перевіряємо, чи мешканець більше не присутній у списку
        residents = self.mock_file_manager.save.call_args[0][0]["residents"]
        self.assertNotIn({"tax_id": "123456789", "name": "John Doe"}, residents)

    def test_remove_non_existent_resident(self):
        # Тест на видалення неіснуючого мешканця
        self.repository.remove_resident("000000000")
        # Перевіряємо, що метод save не був викликаний
        self.mock_file_manager.save.assert_not_called()


if __name__ == '__main__':
    unittest.main()