
import json
import re
from datetime import datetime

# Клас для роботи з файлами
class FileManager:
    """ FileManager відповідає за завантаження та збереження даних у файл. """
    def __init__(self, file_path):
        self.file_path = file_path  # Шлях до файлу для зберігання даних

    def load(self):
        """ Завантажує дані з файлу. Якщо файл не знайдено або він містить некоректний JSON,
        повертає порожній шаблон даних."""
        try:
            # Спроба завантажити дані з файлу
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)  # Читаємо JSON-дані з файлу
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Якщо файл не знайдено або не можна декодувати JSON, ініціалізуємо порожні дані
            print(f"Помилка завантаження даних: {e}")
            return {"residents": [], "apartments": []}  # Повертаємо порожні дані

    def save(self, data):
        """ Зберігає дані у файл у форматі JSON """
        try:
            # Спроба зберегти дані у файл
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)  # Записуємо дані у файл
        except OSError as e:
            # Обробка помилки при записі у файл
            print(f"Помилка запису до файлу: {e}")

# Клас Мешканця
class Resident:
    """
    Resident представляє мешканця із відповідними атрибутами.
    """
    def __init__(self, name, tax_id, birthdate, phone, email, additional_info, apartment=None):
        self.name = name  # Ім'я мешканця
        self.tax_id = tax_id  # ІПН мешканця
        self.birthdate = birthdate  # Дата народження
        self.phone = phone  # Номер телефону
        self.email = email  # Електронна пошта
        self.additional_info = additional_info  # Додаткова інформація
        self.apartment = apartment  # Номер квартири (необов'язково)

    def to_dict(self):
        """
        Перетворює об'єкт Resident на словник для серіалізації.
        """
        return {
            "name": self.name,
            "tax_id": self.tax_id,
            "birthdate": self.birthdate,
            "phone": self.phone,
            "email": self.email,
            "additional_info": self.additional_info,
            "apartment": self.apartment
        }
    def __eq__(self, other):
        if isinstance(other, Resident):
            return self.tax_id == other.tax_id  # ІПН унікальний
        return False

# Клас Квартири
class Apartment:
    """ Apartment представляє квартиру із відповідними атрибутами. """
    def __init__(self, number, entrance, floors, floor, rooms, residents=None):
        self.number = number
        self.entrance = entrance
        self.floors = floors
        self.floor = floor
        self.rooms = rooms
        self.residents = residents if residents is not None else []

    def add_resident(self, resident):
        if not any(r["tax_id"] == resident.tax_id for r in self.residents):
            self.residents.append(resident.to_dict())

    def remove_resident(self, tax_id):
        self.residents = [r for r in self.residents if r["tax_id"] != tax_id]

    def to_dict(self):
        return {
            "number": self.number,
            "entrance": self.entrance,
            "floors": self.floors,
            "floor": self.floor,
            "rooms": self.rooms,
            "residents": [resident.to_dict() if isinstance(resident, Resident) else resident
                          for resident in self.residents]
        }
    def __eq__(self, other):
        """Перевіряє (порівнює) квартири за номером."""
        return isinstance(other, Apartment) and self.number == other.number


# Клас репозиторію для роботи з даними
class HouseRepository:
    """
       HouseRepository містить основну логіку роботи з даними про мешканців та квартири.
       """
    def __init__(self, file_path):
        self.file_path = file_path  # Шлях до файлу
        self.file_manager = FileManager(file_path)
        self.data = self.file_manager.load() # Завантажуємо дані з файлу

    def find_resident_by_tax_id(self, tax_id):
        """Повертає мешканця за його ІПН або None, якщо не знайдено."""
        return next((r for r in self.data["residents"] if r["tax_id"] == tax_id), None)

    def find_apartment_by_number(self, number):
        """Повертає квартиру за її номером або None, якщо не знайдено."""
        return next((a for a in self.data["apartments"] if a["number"] == number), None)

    def add_resident(self, resident):
        """Додає мешканця до списку."""
        if self.find_resident_by_tax_id(resident.tax_id):
            print(f"Мешканець із ІПН {resident.tax_id} вже існує.")
            return
        self.data["residents"].append(resident.to_dict()) # Додаємо мешканця у список
        self.file_manager.save(self.data) # Зберігаємо оновлені дані


    def remove_resident(self, tax_id):
        """ Видаляє мешканця за ІПН. """
        # Перевіряє мешканця за ІПН
        resident = self.find_resident_by_tax_id(tax_id)
        if not resident:
            print(f"Мешканця з ІПН {tax_id} не знайдено.")
            return

        # Видаляємо мешканця з усіх квартир
        for apartment in self.data["apartments"]:
            apartment["residents"] = [r for r in apartment["residents"] if r["tax_id"] != tax_id]

        # Видаляємо мешканця зі списку
        self.data["residents"] = [r for r in self.data["residents"] if r["tax_id"] != tax_id]
        self.file_manager.save(self.data)

    def add_apartment(self, apartment):
        """ Додає квартиру до списку. """
        if self.find_apartment_by_number(apartment.number):
            print(f"Квартира з номером {apartment.number} вже існує.")
            return
        self.data["apartments"].append(apartment.to_dict()) # Додаємо квартиру у список
        self.file_manager.save(self.data) # Зберігаємо оновлені дані

    def remove_apartment(self, number):
        """ Видаляє квартиру за номером. """
        # Перевіряє наявність квартири за номером
        apartment = self.find_apartment_by_number(number)
        if not apartment:
            print(f"Квартира з номером {number} не знайдена.")
            return

        # Видаляємо квартиру з усіх мешканців
        for resident in self.data["residents"]:
            if resident.get("apartment") == number:
                resident["apartment"] = None  # Відкріплюємо мешканця від квартири

        # Видаляємо квартиру зі списку
        self.data["apartments"] = [a for a in self.data["apartments"] if a["number"] != number]
        self.file_manager.save(self.data)

    def assign_resident_to_apartment(self, tax_id, apartment_number):
        """Закріплює мешканця за квартирою."""
        resident = self.find_resident_by_tax_id(tax_id)
        if not resident:
            print(f"Мешканця з ІПН {tax_id} не знайдено.")
            return

        apartment = self.find_apartment_by_number(apartment_number)
        if not apartment:
            print(f"Квартиру з номером {apartment_number} не знайдено.")
            return

        # Перевірка, чи вже мешканець не прив'язаний до цієї квартири
        if resident["apartment"] == apartment_number:
            print(f"Мешканець з ІПН {tax_id} вже прив'язаний до квартири з номером {apartment_number}.")
            return

        # Оновлюємо мешканця: додаємо квартиру
        resident['apartment'] = apartment_number

        # Створюємо об'єкти
        resident_obj = Resident(**resident)
        apartment_obj = Apartment(**apartment)
        # Додаємо мешканця до квартири
        apartment_obj.add_resident(resident_obj)

        self.data["apartments"] = [
            apartment_obj.to_dict() if a["number"] == apartment_number else a
            for a in self.data["apartments"]
        ]

        # Оновлюємо дані
        self.data["residents"] = [r if r != resident else resident_obj.__dict__ for r in self.data["residents"]]

        self.file_manager.save(self.data)


    def unassign_resident_from_apartment(self, tax_id):
        """Відкріплює мешканця від квартири і видаляє його зі списку мешканців цієї квартири."""
        resident = self.find_resident_by_tax_id(tax_id)
        if not resident:
            print(f"Мешканця з ІПН {tax_id} не знайдено.")
            return

        apartment_number = resident["apartment"]
        if apartment_number is None:
            print(f"Мешканець не закріплений за жодною квартирою.")
            return

        apartment = self.find_apartment_by_number(apartment_number)
        if apartment:
            apartment_obj = Apartment(**apartment)
            apartment_obj.remove_resident(tax_id)
            self.data["apartments"] = [
                apartment_obj.to_dict() if a["number"] == apartment_number else a
                for a in self.data["apartments"]
            ]

        # Відкріплюємо мешканця від квартири
        resident["apartment"] = None
        self.file_manager.save(self.data)



class Validator:
    @staticmethod
    def validate_phone(phone):
        # Допускаються формати: +38-050-123-45-67 або 050-123-45-67
        pattern = re.compile(r"^(\+38-)?0\d{2}-\d{3}-\d{2}-\d{2}$")
        return bool(pattern.match(phone))

    @staticmethod
    def validate_email(email):
        # Перевірка на формат email
        pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return bool(pattern.match(email))

    @staticmethod
    def validate_tax_id(tax_id):
        # Перевірка на 9 цифр за допомогою патерну
        pattern = re.compile(r"^\d{9}$")
        return bool(pattern.match(tax_id))

    @staticmethod
    def validate_date(date):
        # Перетворення рядків у дати
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    @staticmethod
    def validate_apartment(apartment):
        # Перевірка, що квартира є числовим значенням
        return apartment.isdigit()


    # Клас сервісу для управління мешканцями і квартирами
class HouseManagementService:
    """HouseManagementService містить бізнес-логіку управління мешканцями та квартирами."""

    def __init__(self, repository):
        self.repository = repository  # Посилання на репозиторій даних

    def add_resident(self, name, tax_id, birthdate, phone, email, additional_info, apartment=None):
        """Додає нового мешканця п.1."""
        if not Validator.validate_tax_id(tax_id):
            print("ІПН повинен складатися з 9 цифр.")
            return
        if not Validator.validate_date(birthdate):
            print("Неправильний формат дати. Використовуйте формат 'YYYY-MM-DD'.")
            return
        if not Validator.validate_phone(phone):
            print("Неправильний формат телефону. Використовуйте формат '+38-050-123-45-67' або '050-123-45-67'.")
            return
        if not Validator.validate_email(email):
            print("Неправильний формат email.")
            return

        # Додаємо мешканця в репозиторій
        resident = Resident(name, tax_id, birthdate, phone, email, additional_info, apartment)
        self.repository.add_resident(resident)

        print(f"Мешканеця {name} успішно додано.")
        self.generate_report_residents()

    def remove_resident(self, tax_id):
        """Видаляє мешканця за ІПН п.2."""
        if not self.repository.find_resident_by_tax_id(tax_id):
            print(f"Мешканця з ІПН {tax_id} не знайдено.")
            return
        self.repository.remove_resident(tax_id)
        print(f"Мешканця з ІПН {tax_id} видалено успішно.")
        self.generate_report_residents()

    def add_apartment(self, number, entrance, floors, floor, rooms):
        """ Додає нову квартиру п.3. """

        if not number.isdigit() or not floors.isdigit() or not floor.isdigit() or not rooms.isdigit():
            print("Номер квартири, кількість поверхів, номер поверху та кількість кімнат повинні бути числами.")
            return

        # Додаємо квартиру в репозиторій
        apartment = Apartment(number, entrance, floors, floor, rooms)
        self.repository.add_apartment(apartment)

        # Сортуємо список квартир за номером
        self.repository.data["apartments"] = sorted(
            self.repository.data["apartments"],
            key=lambda x: int(x["number"])  # Сортування за числовим значенням номера
        )
        print(f"Квартира з номером {number} додана.")
        self.generate_report_apartments()

    def remove_apartment(self, number):
        """ Видаляє квартиру за номером п.4."""

        if not number.isdigit():
            print("Номер квартири повинен бути числом.")
            return
        if not self.repository.find_apartment_by_number(number):
            print(f"Квартира з номером {number} не знайдена.")
            return
        self.repository.remove_apartment(number)
        print(f"Квартира з номером {number} видалена.")
        self.generate_report_apartments()

    def assign_resident_to_apartment(self, tax_id, apartment_number):
        """Закріплює мешканця за квартирою п.5."""
        if not tax_id.isdigit():
            print("ІПН повинен складатися лише з цифр.")
            return
        if not apartment_number.isdigit():
            print("Номер квартири повинен бути числом.")
            return

        if not self.repository.find_resident_by_tax_id(tax_id):
            print(f"Мешканця з ІПН {tax_id} не знайдено.")
            return
        if not self.repository.find_apartment_by_number(apartment_number):
            print(f"Квартира з номером {apartment_number} не знайдена.")
            return
        self.repository.assign_resident_to_apartment(tax_id, apartment_number)
        # Сортуємо список мешканців за номером квартири
        self.repository.data["residents"] = sorted(
            self.repository.data["residents"],
            key=lambda x: int(x["apartment"]) if x["apartment"] else float('inf')  # Несортовані без номера квартири
        )
        print(f"Мешканця з ІПН {tax_id} успішно закріплено за квартирою {apartment_number}.")
        self.generate_report_residents()

    def unassign_resident_from_apartment(self, tax_id):
        """Відкріплює мешканця від квартири п.6. """
        if not tax_id.isdigit():
            print("ІПН повинен складатися лише з цифр.")
            return
        if not self.repository.find_resident_by_tax_id(tax_id):
            print(f"Мешканця з ІПН {tax_id} не знайдено.")
            return
        self.repository.unassign_resident_from_apartment(tax_id)
        print(f"Мешканця з ІПН {tax_id} успішно відкріплено.")
        self.generate_report_residents()

    def generate_report_residents(self):
        """ Виводить список усіх мешканців. """
        print("\nСписок мешканців:")
        for resident in self.repository.data["residents"]:
            print(
                f"Ім'я: {resident['name']}, ІПН: {resident['tax_id']}, Квартира: {resident.get('apartment', 'Не закріплена')}")

    def generate_report_apartments(self):
        """Виводить список усіх квартир."""
        print("\nСписок квартир (в порядку зростання номера):")
        for apartment in self.repository.data["apartments"]:
            print(
                f"Номер квартири: {apartment['number']}, Під'їзд: {apartment['entrance']}, Кіл-ть поверхів: {apartment['floors']}, "
                f"Поверх: {apartment['floor']}, Кілкість кімнат: {apartment['rooms']}, "
                f"Кіл-ть мешканців: {len(apartment['residents'])}")

    def report_residents_by_apartment(self):
        """ Виводить список усіх мешканців за квартирами. """
        print("\nСписок мешканців за квартирами:")
        for apartment in self.repository.data["apartments"]:
            print(f"Квартира {apartment['number']}:")
            for resident in self.repository.data["residents"]:
                if resident.get("apartment") == apartment["number"]:
                    print(f"  - {resident['name']}, ІПН: {resident['tax_id']}")

    def report_unassigned_residents(self):
        """ Виводить список усіх мешканців без квартир. """
        print("\nМешканці без закріпленої квартири:")
        for resident in self.repository.data["residents"]:
            if not resident.get("apartment"):
                print(f"  - {resident['name']}, ІПН: {resident['tax_id']}")


# Основна функція
def main():
    """
    Запускає інтерактивне меню для управління мешканцями та квартирами.
    """
    # Створення репозиторію, що завантажує дані з файлу або створює порожній репозиторій
    repository = HouseRepository('house_data1.json')
    # Створення сервісу для виконання дій над даними
    service = HouseManagementService(repository)

    while True:
        # Виведення головного меню
        print("\n--- Головне меню ---")
        print("1. Додати мешканця.")
        print("2. Видалити мешканця.")
        print("3. Додати квартиру.")
        print("4. Видалити квартиру.")
        print("5. Закріпити мешканця за квартирою.")
        print("6. Відкріпити мешканця від квартири.")
        print("7. Зберегти дані у файл.")
        print("8. Завантажити дані з файлу.")
        print("9. Звіти.")
        print("10. Вийти.")
        try:
            # Отримання вибору користувача
            choice = input("Виберіть дію: ")

            if choice == "1":
                # Додавання нового мешканця
                try:
                    name = input("Ім'я: ")
                    if not name.strip():
                        raise ValueError("Ім'я не може бути порожнім.")
                    tax_id = input("ІПН: ")
                    if not Validator.validate_tax_id(tax_id):
                        raise ValueError("ІПН має складатися з 9 цифр.")
                    birthdate = input("Дата народження (у форматі РРРР-ММ-ДД): ")
                    if not Validator.validate_date(birthdate):
                        raise ValueError("Некоректний формат дати. Використовуйте РРРР-ММ-ДД.")
                    phone = input("Телефон (у форматі: +38-050-123-45-67' або '050-123-45-67): ")
                    if not Validator.validate_phone(phone):
                        raise ValueError("Некоректний формат телефону.")
                    email = input("Email: ")
                    if not Validator.validate_email(email):
                        raise ValueError("Некоректний email.")
                    additional_info = input("Додаткова інформація: ")
                    apartment = None

                    # Виклик методу для додавання мешканця
                    service.add_resident(name, tax_id, birthdate, phone, email, additional_info, apartment)
                except ValueError as ve:
                    print(f"Помилка: {ve}. Спробуйте ще раз.")
                except Exception as e:
                    print(f"Помилка при додаванні мешканця: {e}")

            elif choice == "2":
                # Видалення мешканця
                try:
                    tax_id = input("ІПН мешканця: ")
                    if not tax_id.isdigit() or len(tax_id) != 9:
                        raise ValueError("ІПН має складатися з 9 цифр.")
                    service.remove_resident(tax_id)
                except Exception as e:
                    print(f"Помилка при додаванні мешканця: {e}")

            elif choice == "3":
                # Додавання нової квартири
                try:
                    number = input("Номер квартири: ")
                    if not number.isdigit():
                        print("Некоректний ввід номера квартири. Введіть число.")
                        continue
                    entrance = input("Під'їзд: ")
                    if not entrance.isdigit():
                        print("Некоректний ввід номера під'їзду. Введіть число.")
                        continue
                    floors = input("Кількість поверхів: ")
                    if not floors.isdigit():
                        print("Некоректний ввід для кількості поверхів. Введіть число.")
                        continue
                    floor = input("Поверх: ")
                    if not floor.isdigit():
                        print("Некоректний ввід для поверху. Введіть число.")
                        continue
                    rooms = input("Кількість кімнат: ")
                    if not rooms.isdigit():
                        print("Некоректний ввід для кількості кімнат. Введіть число.")
                        continue
                    service.add_apartment(number, entrance, floors, floor, rooms)

                except ValueError:
                    print("Некоректний ввід числових даних для квартири.")
                except Exception as e:
                    print(f"Помилка при додаванні квартири: {e}")

            elif choice == "4":
                # Видалення квартири
                try:
                    number = input("Номер квартири: ")
                    service.remove_apartment(number)
                except ValueError:
                    print("Некоректний номер квартири.")
                except Exception as e:
                    print(f"Помилка при видаленні квартири: {e}")

            elif choice == "5":
                # Закріплення мешканця за квартирою
                try:
                    tax_id = input("ІПН мешканця: ")
                    apartment_number = input("Номер квартири: ")
                    service.assign_resident_to_apartment(tax_id, apartment_number)
                except Exception as e:
                    print(f"Помилка при закріпленні мешканця: {e}")

            elif choice == "6":
                # Відкріплення мешканця від квартири
                try:
                    tax_id = input("ІПН мешканця: ")
                    service.unassign_resident_from_apartment(tax_id)
                except Exception as e:
                    print(f"Помилка при відкріпленні мешканця: {e}")

            elif choice == "7":
                # Зберегти дані у файл
                try:
                    persistence = FileManager('house_data.json')
                    persistence.save(repository.data)
                    print("Дані успішно збережено.")
                except Exception as e:
                    print(f"Помилка при збереженні даних: {e}")

            elif choice == "8":
                # Завантажити дані з файлу
                try:
                    repository.data = FileManager('house_data.json').load()
                    print("Дані успішно завантажено.")
                except Exception as e:
                    print(f"Помилка при завантаженні даних: {e}")

            elif choice == "9":
                while True:    # Звіти
                    print("\n--- Звіти ---")
                    print("1. Звіт про мешканців.")
                    print("2. Звіт про квартири.")
                    print("3. Звіт мешканців за квартирами.")
                    print("4. Звіт мешканців без закріпленої квартири.")
                    print("5. Повернення до головного меню")
                    report_choice = input("Виберіть дію: ")

                    try:
                        if report_choice == "1":
                            # Генерація звіту про всіх мешканців
                            service.generate_report_residents()

                        elif report_choice == "2":
                            # Генерація звіту про всі квартири
                            service.generate_report_apartments()

                        elif report_choice == "3":
                            # Звіт про мешканців, закріплених за квартирами
                            service.report_residents_by_apartment()

                        elif report_choice == "4":
                            # Звіт про мешканців без квартир
                            service.report_unassigned_residents()

                        elif report_choice == "5":
                            break
                        else:
                            print("Некоректний вибір у розділі звітів.")
                    except Exception as e:
                        print(f"Помилка при генерації звіту: {e}")

            elif choice == "10":
                # Завершення роботи програми
                print("До побачення!")
                break

            else:
                # Обробка некоректного вибору
                print("Некоректний вибір, спробуйте знову.")

        except Exception as e:
            print(f"Сталася непередбачена помилка: {e}")

# Перевірка, чи скрипт виконується безпосередньо
if __name__ == "__main__":
    main()