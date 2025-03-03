
import datetime
from abc import ABC, abstractmethod

# Класс, представляющий автора
class Author:
    def __init__(self, first_name, last_name, biography=""):
        # Имя автора
        self.first_name = first_name
        # Фамилия автора
        self.last_name = last_name
        # Биография автора (необязательное поле)
        self.biography = biography

    def __str__(self):
        # Возвращает строковое представление автора (имя и фамилия)
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other):
        # Перегрузка оператора == для сравнения двух авторов
        if isinstance(other, Author):
            return (self.first_name == other.first_name and
                    self.last_name == other.last_name)
        return False

    def __hash__(self):
        # Возвращает хеш-значение для автора (необходимо для использования в set)
        return hash((self.first_name, self.last_name))

# Класс, представляющий книгу
class Book:
    def __init__(self, title, author, isbn, genre, quantity):
        # Название книги
        self.title = title
        # Автор книги (объект класса Author)
        self.author = author
        # ISBN книги
        self.isbn = isbn
        # Жанр книги
        self.genre = genre
        # Количество экземпляров книги в библиотеке
        self.quantity = quantity

    def __str__(self):
        # Возвращает строковое представление книги
        return f"{self.title} от {self.author} (ISBN: {self.isbn})"

    def __lt__(self, other):
        # Перегрузка оператора < (меньше) для сравнения книг по названию
        return self.title < other.title

    def __gt__(self, other):
        # Перегрузка оператора > (больше) для сравнения книг по названию
        return self.title > other.title

    def __eq__(self, other):
        # Перегрузка оператора == (равно) для сравнения книг по ISBN
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __hash__(self):
        # Возвращает хеш-значение для книги (по ISBN)
        return hash(self.isbn)

# Абстрактный класс для представления активов библиотеки
class LibraryAsset(ABC):
    @abstractmethod
    # Абстрактный метод для отображения информации об активе
    def display_asset_info(self):
        pass

# Класс, представляющий библиотеку (наследуется от LibraryAsset)
class Library(LibraryAsset):

    # Статическое поле для хранения общего количества библиотек
    total_libraries = 0

    def __init__(self, name, address):
        # Название библиотеки
        self.name = name
        # Адрес библиотеки
        self.address = address
        # Множество книг в библиотеке (используется set для уникальности)
        self.books = set()
        # Словарь читателей в библиотеке (ключ - reader_id, значение - объект Reader)
        self.readers = {}
        # Список выданных книг (объекты Loan)
        self.loans = []
        # Увеличиваем счетчик библиотек при создании новой библиотеки
        Library.total_libraries += 1

    def add_book(self, book):
        # Добавляет книгу в библиотеку
        self.books.add(book)

    def remove_book(self, book):
        # Удаляет книгу из библиотеки
        try:
            self.books.remove(book)
        except KeyError:
            # Обработка исключения, если книга не найдена
            print(f"Книга '{book.title}' не найдена в библиотеке.")

    def add_reader(self, reader):
        # Добавляет читателя в библиотеку
        self.readers[reader.reader_id] = reader

    def remove_reader(self, reader):
        # Удаляет читателя из библиотеки
        try:
            del self.readers[reader.reader_id]
        except KeyError:
            # Обработка исключения, если читатель не найден
            print(f"Читатель '{reader.first_name} {reader.last_name}' не найден в библиотеке.")

    def display_books(self):
        # Выводит список книг в библиотеке
        if not self.books:
            print("В библиотеке нет книг.")
        else:
            print("Книги в библиотеке:")
            for book in sorted(self.books): # Сортировка книг по названию
                print(book)

    def display_readers(self):
        # Выводит список читателей в библиотеке
        if not self.readers:
            print("В библиотеке нет читателей.")
        else:
            print("Читатели в библиотеке:")
            for reader_id, reader in self.readers.items():
                print(reader)

    def lend_book(self, book, reader, due_date):
        # Выдает книгу читателю
        if book in self.books and reader.reader_id in self.readers and book.quantity > 0:
            book.quantity -= 1
            loan = Loan(book, reader, datetime.date.today(), due_date)
            self.loans.append(loan)
            print(f"Книга '{book.title}' выдана читателю '{reader.first_name} {reader.last_name}'.")
        else:
            print("Невозможно выдать книгу.")

    def return_book(self, book, reader):
        # Возвращает книгу в библиотеку
        for loan in self.loans:
            if loan.book == book and loan.reader == reader:
                book.quantity += 1
                self.loans.remove(loan)
                print(f"Книга '{book.title}' возвращена читателем '{reader.first_name} {reader.last_name}'.")
                return
        print("Данная книга не была выдана этому читателю.")

    @staticmethod
    def get_library_count():
        # Статический метод для получения общего количества библиотек
        return Library.total_libraries

    def display_asset_info(self):
        # Реализация абстрактного метода для отображения информации о библиотеке
        print(f"Название библиотеки: {self.name}, Адрес: {self.address}")

# Класс, представляющий читателя
class Reader:
    def __init__(self, first_name, last_name, reader_id):
        # Имя читателя
        self.first_name = first_name
        # Фамилия читателя
        self.last_name = last_name
        # Уникальный идентификатор читателя
        self.reader_id = reader_id
        # Словарь взятых книг (ключ - Book, значение - дата выдачи)
        self.borrowed_books = {}

    def __str__(self):
        # Возвращает строковое представление читателя
        return f"{self.first_name} {self.last_name} (ID: {self.reader_id})"

    def __hash__(self):
        # Возвращает хеш-значение для читателя (по ID)
        return hash(self.reader_id)

# Класс, представляющий информацию о выдаче книги
class Loan:
    def __init__(self, book, reader, loan_date, due_date):
        # Книга, которая была выдана
        self.book = book
        # Читатель, которому выдали книгу
        self.reader = reader
        # Дата выдачи книги
        self.loan_date = loan_date
        # Дата возврата книги
        self.due_date = due_date

    def __str__(self):
        # Возвращает строковое представление информации о выдаче книги
        return f"Книга: {self.book.title}, Читатель: {self.reader.first_name} {self.reader.last_name}, Дата выдачи: {self.loan_date}, Дата возврата: {self.due_date}"

    def is_overdue(self):
        # Проверяет, просрочена ли книга
        return self.due_date < datetime.date.today()

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
    book3 = Book("Десять негритят", author2, "978-0062073481", "Детектив", 3) # Создаем книгу с тем же ISBN, что и book2

    print(f"Книга1 меньше Книги2: {book1 < book2}")
    print(f"Книга2 больше Книги1: {book2 > book1}")
    print(f"Книга2 равна Книге3: {book2 == book3}")

    # Создание библиотеки
    library = Library("Главная библиотека", "Улица Пушкина, дом Колотушкина")

    # Добавление книг в библиотеку
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)  # Книга с дублирующимся ISBN не будет добавлена из-за set

    # Создание читателей
    reader1 = Reader("Иван", "Иванов", "12345")
    reader2 = Reader("Мария", "Петрова", "67890")

    # Добавление читателей в библиотеку
    library.add_reader(reader1)
    library.add_reader(reader2)

    # Вывод информации о книгах и читателях в библиотеке
    library.display_books()
    library.display_readers()

    # Выдача книги читателю
    try:
        library.lend_book(book1, reader1, datetime.date(2025, 2, 1))
        library.lend_book(book2, reader2, datetime.date(2025, 2, 8))
        library.lend_book(book2, reader1, datetime.date(2025, 2, 8))  # Попытка выдать отсутствующую книгу
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

    # Использование абстрактного класса
    library.display_asset_info()

    # Демонстрация работы со строками
    book_description = f"Эта книга - {book1.genre}, ее название '{book1.title}', а автор - {book1.author}."
    print(book_description)

    # Пример проверки статуса выдачи
    loan1 = Loan(book1, reader1, datetime.date(2025, 1, 16), datetime.date(2025, 2, 16))
    print(f"Выдача просрочена: {loan1.is_overdue()}")
