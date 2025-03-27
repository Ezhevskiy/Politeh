
import datetime
import logging
from abc import ABC, abstractmethod

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Задание 1: Иерархия пользовательских исключений
class BaseLibraryException(Exception):
    """Базовое исключение для библиотеки."""
    def __init__(self, message="Ошибка библиотеки."):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"BaseLibraryException: {self.message}"




class BookError(BaseLibraryException):
    """Исключения, связанные с книгами."""
    pass

class BookNotFound(BookError):
    """Книга не найдена."""
    pass

class BookUnavailable(BookError):
    """Книга недоступна для выдачи."""
    pass

class InvalidBookData(BookError):
    """Некорректные данные книги."""
    pass


class ReaderError(BaseLibraryException):
    """Исключения, связанные с читателями."""
    pass

class ReaderNotFound(ReaderError):
    """Читатель не найден."""
    pass

# Класс, представляющий автора
class Author:
    """Представляет автора книги."""
    def __init__(self, first_name, last_name, biography=""):
        """
        Инициализирует объект Author.

        Args:
            first_name: Имя автора.
            last_name: Фамилия автора.
            biography: Биография автора (необязательное поле).
        """
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography

    def __str__(self):
        """Возвращает строковое представление автора (имя и фамилия)."""
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other):
        """Перегрузка оператора == для сравнения двух авторов."""
        if isinstance(other, Author):
            return (self.first_name == other.first_name and
                    self.last_name == other.last_name)
        return False

    def __hash__(self):
        """Возвращает хеш-значение для автора (необходимо для использования в set)."""
        return hash((self.first_name, self.last_name))

# Класс, представляющий книгу
class Book:
    """Представляет книгу."""
    def __init__(self, title, author, isbn, genre, quantity):
        """
        Инициализирует объект Book.

        Args:
            title: Название книги.
            author: Автор книги (объект класса Author).
            isbn: ISBN книги.
            genre: Жанр книги.
            quantity: Количество экземпляров книги в библиотеке.
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.quantity = quantity

    def __str__(self):
        """Возвращает строковое представление книги."""
        return f"{self.title} от {self.author} (ISBN: {self.isbn})"

    def __repr__(self):
        """Возвращает строковое представление книги (repr)."""
        return f"Book('{self.title}', {repr(self.author)}, '{self.isbn}', '{self.genre}', {self.quantity})"

    def __lt__(self, other):
        """Перегрузка оператора < (меньше) для сравнения книг по названию."""
        return self.title < other.title

    def __gt__(self, other):
        """Перегрузка оператора > (больше) для сравнения книг по названию."""
        return self.title > other.title

    def __eq__(self, other):
        """Перегрузка оператора == (равно) для сравнения книг по ISBN."""
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __hash__(self):
        """Возвращает хеш-значение для книги (по ISBN)."""
        return hash(self.isbn)

# Абстрактный класс для представления активов библиотеки
class LibraryAsset(ABC):
    """Абстрактный класс, представляющий активы библиотеки."""
    @abstractmethod
    def display_asset_info(self):
        """Абстрактный метод для отображения информации об активе."""
        pass

# Базовый класс для библиотеки (Задание 3: Наследование)
class BaseLibrary(LibraryAsset):
    """Базовый класс для библиотеки."""
    def __init__(self, name, address):
        """
        Инициализирует объект BaseLibrary.

        Args:
            name: Название библиотеки.
            address: Адрес библиотеки.
        """
        self.name = name
        self.address = address
        # Задание 4: Защищенные атрибуты
        self._catalog = {}  # Защищенный каталог книг (ISBN: Book)
        self._reader_database = {} # Защищенная база данных читателей (reader_id: Reader)

    def display_asset_info(self):
        """Выводит информацию об активе (название и адрес библиотеки)."""
        print(f"Название: {self.name}, Адрес: {self.address}")

    def _base_method(self): # Дополнительный метод для демонстрации наследования
        """Пример метода базового класса."""
        return "Base Library Method"

# Производный класс (Задание 3: Наследование)
class Library(BaseLibrary):
    """Производный класс для библиотеки."""

    # Статическое поле для хранения общего количества библиотек
    total_libraries = 0

    def __init__(self, name, address, library_type="Public"): # Задание 5: Конструкторы и наследование
        """
        Инициализирует объект Library.

        Args:
            name: Название библиотеки.
            address: Адрес библиотеки.
            library_type: Тип библиотеки (по умолчанию "Public").
        """
        super().__init__(name, address) # Вызов конструктора базового класса
        self.library_type = library_type # Дополнительный атрибут для производного класса
        # Множество книг в библиотеке (используется set для уникальности)
        self.books = set()
        # Список выданных книг (объекты Loan)
        self.loans = []
        # Увеличиваем счетчик библиотек при создании новой библиотеки
        Library.total_libraries += 1

    def add_book(self, book):
        """
        Добавляет книгу в библиотеку.

        Args:
            book: Объект Book, который нужно добавить.
        """
        try:
            if not isinstance(book.quantity, int) or book.quantity < 0:
                raise InvalidBookData("Количество экземпляров книги должно быть целым числом больше или равно 0.")
            if not isinstance(book.isbn, str) or len(book.isbn) == 0:
                raise InvalidBookData("ISBN должен быть строкой.")

            if book.isbn in self._catalog:
                raise BookError(f"Книга с ISBN {book.isbn} уже есть в каталоге.")  # Использовать BookError
            self._catalog[book.isbn] = book
            self.books.add(book)
            logging.info(f"Книга '{book.title}' добавлена в библиотеку.")
        except BookError as e:  # Ловить BookError
            logging.error(f"Ошибка при добавлении книги: {e}")
            print(f"Ошибка при добавлении книги: {e}")  # Вывод в консоль
        except InvalidBookData as e:
            logging.error(f"Ошибка при добавлении книги: {e}")
            print(f"Ошибка при добавлении книги: {e}")
        except Exception as e:
            logging.exception(f"Неожиданная ошибка при добавлении книги: {e}")
        finally:
            logging.debug("Завершение операции добавления книги.")

    def remove_book(self, book):
        """
        Удаляет книгу из библиотеки.

        Args:
            book: Объект Book, который нужно удалить.
        """
        try:
            if book.isbn not in self._catalog:
                raise BookNotFound(f"Книга '{book.title}' не найдена в каталоге.")
            del self._catalog[book.isbn]
            self.books.remove(book)
            logging.info(f"Книга '{book.title}' удалена из библиотеки.")
        except BookNotFound as e:
            logging.error(f"Ошибка при удалении книги: {e}")
            print(f"Ошибка при удалении книги: {e}")  # Вывод в консоль
        except KeyError:
            logging.error(f"Книга '{book.title}' не найдена в библиотеке.")
            print(f"Книга '{book.title}' не найдена в библиотеке.") # Вывод в консоль
        except Exception as e:
            logging.exception(f"Неожиданная ошибка при удалении книги: {e}")
        finally:
            logging.debug("Завершение операции удаления книги.")

    def add_reader(self, reader):
        """
        Добавляет читателя в библиотеку.

        Args:
            reader: Объект Reader, который нужно добавить.
        """
        try:
            if reader.reader_id in self._reader_database:
                raise ReaderError(f"Читатель с ID {reader.reader_id} уже зарегистрирован.") # Использовать ReaderError
            self._reader_database[reader.reader_id] = reader
            logging.info(f"Читатель '{reader.first_name} {reader.last_name}' добавлен в библиотеку.")
        except ReaderError as e: # Ловить ReaderError
            logging.error(f"Ошибка при добавлении читателя: {e}")
            print(f"Ошибка при добавлении читателя: {e}") # Вывод в консоль
        except Exception as e:
            logging.exception(f"Неожиданная ошибка при добавлении читателя: {e}")
        finally:
            logging.debug("Завершение операции добавления читателя.")

    def remove_reader(self, reader):
        """
        Удаляет читателя из библиотеки.

        Args:
            reader: Объект Reader, который нужно удалить.
        """
        try:
            if reader.reader_id not in self._reader_database:
                raise ReaderNotFound(f"Читатель '{reader.first_name} {reader.last_name}' не найден в библиотеке.")
            del self._reader_database[reader.reader_id]
            logging.info(f"Читатель '{reader.first_name} {reader.last_name}' удален из библиотеки.")
        except ReaderNotFound as e:
            logging.error(f"Ошибка при удалении читателя: {e}")
            print(f"Ошибка при удалении читателя: {e}")  # Вывод в консоль
        except KeyError:
            logging.error(f"Читатель '{reader.first_name} {reader.last_name}' не найден в библиотеке.")
            print(f"Читатель '{reader.first_name} {reader.last_name}' не найден в библиотеке.") # Вывод в консоль
        except Exception as e:
            logging.exception(f"Неожиданная ошибка при удалении читателя: {e}")
        finally:
            logging.debug("Завершение операции удаления читателя.")

    def display_books(self):
        """Выводит список книг в библиотеке."""
        if not self.books:
            print("В библиотеке нет книг.")
        else:
            print("Книги в библиотеке:")
            for book in sorted(self.books): # Сортировка книг по названию
                print(book)

    def display_readers(self):
        """Выводит список читателей в библиотеке."""
        if not self._reader_database: # Используем защищенный атрибут
            print("В библиотеке нет читателей.")
        else:
            print("Читатели в библиотеке:")
            for reader_id, reader in self._reader_database.items():
                print(reader)

    def lend_book(self, book, reader, due_date):
        """
        Выдает книгу читателю.

        Args:
            book: Объект Book, который нужно выдать.
            reader: Объект Reader, которому выдается книга.
            due_date: Дата возврата книги.
        """
        try:
            if book not in self.books:
                raise BookNotFound(f"Книга '{book.title}' не найдена в библиотеке.")
            if reader.reader_id not in self._reader_database:
                raise ReaderNotFound(f"Читатель '{reader.first_name} {reader.last_name}' не найден в библиотеке.")
            if book.quantity <= 0:
                raise BookUnavailable(f"Книга '{book.title}' недоступна для выдачи.")

            book.quantity -= 1
            loan = Loan(book, reader, datetime.date.today(), due_date)
            self.loans.append(loan)
            logging.info(f"Книга '{book.title}' выдана читателю '{reader.first_name} {reader.last_name}'.")
        except BookNotFound as e:
            logging.error(f"Ошибка: {e}")
            print(f"Ошибка: {e}") # Вывод в консоль
        except ReaderNotFound as e:
            logging.error(f"Ошибка: {e}")
            print(f"Ошибка: {e}") # Вывод в консоль
        except BookUnavailable as e:
            logging.error(f"Ошибка: {e}")
            print(f"Ошибка: {e}") # Вывод в консоль
        except Exception as e:
            logging.exception(f"Неожиданная ошибка: {e}")
        finally:
             logging.debug("Завершение операции выдачи книги.")

    def return_book(self, book, reader):
        """
        Возвращает книгу в библиотеку.

        Args:
            book: Объект Book, который возвращается.
            reader: Объект Reader, который возвращает книгу.
        """
        try:
            # Ищем запись о выдаче, соответствующую книге и читателю
            for i, loan in enumerate(self.loans):
                if loan.book == book and loan.reader == reader:
                    book.quantity += 1
                    del self.loans[i]  # Удаляем запись о выдаче по индексу
                    logging.info(f"Книга '{book.title}' возвращена читателем '{reader.first_name} {reader.last_name}'.")
                    return

            # Если запись о выдаче не найдена, выбрасываем исключение
            raise ValueError("Данная книга не была выдана этому читателю.")

        except ValueError as e:
            logging.error(f"Ошибка при возврате книги: {e}")
            print(f"Ошибка при возврате книги: {e}") # Вывод в консоль
        except Exception as e:
            logging.exception(f"Неожиданная ошибка при возврате книги: {e}")
        finally:
            logging.debug("Завершение операции возврата книги.")

    @staticmethod
    def get_library_count():
        """Возвращает общее количество библиотек."""
        return Library.total_libraries

    def display_asset_info(self):
        """Выводит информацию о библиотеке (название, адрес, тип, количество книг)."""
        print(f"Название библиотеки: {self.name}, Адрес: {self.address}, Тип: {self.library_type}")
        # Задание 4: Доступ к защищенным атрибутам
        print(f"Количество книг в каталоге: {len(self._catalog)}")

    # Задание 3: Переопределение и вызов метода базового класса
    def display_library_info(self):
        """Выводит информацию о библиотеке, используя метод базового класса."""
        super().display_asset_info()  # Вызов метода базового класса
        print(f"Тип библиотеки: {self.library_type}")

    def combined_method(self, condition): # Дополнительный метод для наследования.
        """Пример комбинированного метода для демонстрации наследования."""
        if condition:
            print("Производный метод сначала:")
            self.display_library_info() # Вызываем переопределенный метод
            print(self._base_method()) # Вызываем метод базового класса
        else:
            print("Базовый метод сначала:")
            print(self._base_method()) # Вызываем метод базового класса
            self.display_library_info() # Вызываем переопределенный метод

# Класс, представляющий читателя
class Reader:
    """Представляет читателя."""
    def __init__(self, first_name, last_name, reader_id):
        """
        Инициализирует объект Reader.

        Args:
            first_name: Имя читателя.
            last_name: Фамилия читателя.
            reader_id: Уникальный идентификатор читателя.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.reader_id = reader_id
        # Словарь взятых книг (ключ - Book, значение - дата выдачи)
        self.borrowed_books = {}

    def __str__(self):
        """Возвращает строковое представление читателя."""
        return f"{self.first_name} {self.last_name} (ID: {self.reader_id})"

    def __hash__(self):
        """Возвращает хеш-значение для читателя (по ID)."""
        return hash(self.reader_id)

# Класс, представляющий информацию о выдаче книги
class Loan:
    """Представляет информацию о выдаче книги."""
    def __init__(self, book, reader, loan_date, due_date):
        """
        Инициализирует объект Loan.

        Args:
            book: Книга, которая была выдана.
            reader: Читатель, которому выдали книгу.
            loan_date: Дата выдачи книги.
            due_date: Дата возврата книги.
        """
        self.book = book
        self.reader = reader
        self.loan_date = loan_date
        self.due_date = due_date

    def __str__(self):
        """Возвращает строковое представление информации о выдаче книги."""
        return f"Книга: {self.book.title}, Читатель: {self.reader.first_name} {self.reader.last_name}, Дата выдачи: {self.loan_date}, Дата возврата: {self.due_date}"

    def is_overdue(self):
        """Проверяет, просрочена ли книга."""
        return self.due_date < datetime.date.today()

# Задание 2: Класс для работы с массивами объектов
class Item:
    """Представляет элемент с именем и значением."""
    def __init__(self, name, value):
        """
        Инициализирует объект Item.

        Args:
            name: Имя элемента.
            value: Значение элемента.
        """
        self.name = name
        self.value = value

    def __str__(self):
        """Возвращает строковое представление элемента."""
        return f"Item: {self.name}, Value: {self.value}"

def find_max_item(matrix):
    """
    Находит объект с максимальным значением value в двумерном списке.

    Args:
        matrix: Двумерный список объектов Item.

    Returns:
        Объект Item с максимальным значением value или None, если список пуст.
    """
    if not matrix:
        return None  # Обработка пустого списка

    max_item = None
    for row in matrix:
        if not row:
            continue  # Пропуск пустых строк

        for item in row:
            if max_item is None or item.value > max_item.value:
                max_item = item
    return max_item

# Основная функция
if __name__ == "__main__":

    # Создание авторов
    author1 = Author("Джон", "Толкин")
    author2 = Author("Агата", "Кристи")
    author3 = Author("Джон", "Толкин") # Создаем еще одного автора Толкина, чтобы проверить сравнение

    print(f"Автор1 равен Автору2: {author1 == author2}")
    print(f"Автор1 равен Автору3: {author1 == author3}")

    # Создание книг
    book1 = Book("Властелин колец", author1, "978-0618260264", "Фэнтези", 5)
    book2 = Book("Убийство в Восточном экспрессе", author2, "978-0062073481", "Детектив", 3)
    book3 = Book("Десять негритят", author2, "978-0062073481", "Детектив", 0) # Создаем книгу с тем же ISBN, что и book2, кол-во = 0
    book4 = Book("Некорректная книга", author1, 123, "Фантастика", "много");

    print(f"Книга1 меньше Книги2: {book1 < book2}")
    print(f"Книга2 больше Книги1: {book2 > book1}")
    print(f"Книга2 равна Книге3: {book2 == book3}")

    # Создание библиотеки
    library = Library("Главная библиотека", "Улица Пушкина, дом Колотушкина", "Научная")

    # Добавление книг в библиотеку
    library.add_book(book1)
    library.add_book(book2)
    try:
        library.add_book(book2) # Повторное добавление книги для демонстрации BookError
    except Exception as e:
        print(f"Поймано исключение при повторном добавлении книги: {e}")
    try:
        library.add_book(book4) # Добавление книги с некорректными данными
    except InvalidBookData as e:
        print(f"Ошибка при добавлении книги book4: {e}")


    # Создание читателей
    reader1 = Reader("Иван", "Иванов", "12345")
    reader2 = Reader("Мария", "Петрова", "67890")

    # Добавление читателей в библиотеку
    library.add_reader(reader1)
    library.add_reader(reader2)
    try:
        library.add_reader(reader1) # Повторное добавление читателя для демонстрации ReaderError
    except Exception as e:
        print(f"Поймано исключение при повторном добавлении читателя: {e}")


    # Вывод информации о книгах и читателях в библиотеке
    library.display_books()
    library.display_readers()

    # Выдача книги читателю
    try:
        library.lend_book(book1, reader1, datetime.date(2025, 2, 1))
        library.lend_book(book2, reader2, datetime.date(2025, 2, 8))
        library.lend_book(book2, reader1, datetime.date(2025, 2, 8))  # Попытка выдать отсутствующую книгу
        library.lend_book(book3, reader1, datetime.date(2025, 2, 8))  # Попытка выдать книгу, которой нет в наличии.
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    # Возврат книги
    library.return_book(book1, reader1)

    # Удаление книги и читателя
    library.remove_book(book2)
    library.remove_reader(reader2)

    library.display_books()
    library.display_readers()

    # Использование статического метода
    print(f"Всего библиотек: {Library.get_library_count()}")

    # Использование абстрактного класса и наследования
    library.display_asset_info() #Вызываем метод из класса Library,
    library.combined_method(True)
    # Демонстрация доступа к защищенным атрибутам
    print(f"Тип библиотеки: {library.library_type}")
    #  print(f"Книги: {library.books}") # AttributeError: 'Library' object has no attribute 'books'
    print(f"Читатели: {library._reader_database}")  # Доступ к защищенному атрибуту (словарь читателей)

    # Демонстрация работы со строками
    book_description = f"Эта книга - {book1.genre}, ее название '{book1.title}', а автор - {book1.author}."
    print(book_description)

    # Пример проверки статуса выдачи
    loan1 = Loan(book1, reader1, datetime.date(2025, 1, 16), datetime.date(2025, 2, 16))
    print(f"Выдача просрочена: {loan1.is_overdue()}")

    # Задание 2: Работа с массивами объектов
    item1 = Item("A", 10)
    item2 = Item("B", 5)
    item3 = Item("C", 15)
    item4 = Item("D", 7)
    item5 = Item("E", 20)

    # Одномерный список
    item_list = [item1, item2, item3]
    for item in item_list:
        print(item)

    # Двумерный список
    item_matrix = [
        [item1, item2],
        [item3, item4, item5],
    ]

    max_item = find_max_item(item_matrix)
    if max_item:
        print(f"Максимальный элемент в матрице: {max_item}")
    else:
        print("Матрица пуста.")
