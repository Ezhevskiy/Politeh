import datetime

class Author:
    def __init__(self, first_name, last_name, biography=""):
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book:
    def __init__(self, title, author, isbn, genre, quantity):
        self.title = title
        self.author = author  # Ссылка на объект Author
        self.isbn = isbn
        self.genre = genre
        self.quantity = quantity

    def __str__(self):
        return f"{self.title} от {self.author} (ISBN: {self.isbn})"

class Library:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.books = []
        self.readers = []
        self.loans = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
        else:
            print(f"Книга '{book.title}' не найдена в библиотеке.")

    def add_reader(self, reader):
        self.readers.append(reader)

    def remove_reader(self, reader):
        if reader in self.readers:
            self.readers.remove(reader)
        else:
            print(f"Читатель '{reader.first_name} {reader.last_name}' не найден в библиотеке.")

    def display_books(self):
        if not self.books:
            print("В библиотеке нет книг.")
        else:
            print("Книги в библиотеке:")
            for book in self.books:
                print(book)

    def display_readers(self):
        if not self.readers:
            print("В библиотеке нет читателей.")
        else:
            print("Читатели в библиотеке:")
            for reader in self.readers:
                print(reader)

    def lend_book(self, book, reader, due_date):
        if book in self.books and reader in self.readers and book.quantity > 0:
            book.quantity -= 1
            loan = Loan(book, reader, datetime.date.today(), due_date)
            self.loans.append(loan)
            print(f"Книга '{book.title}' выдана читателю '{reader.first_name} {reader.last_name}'.")
        else:
            print("Невозможно выдать книгу.")

    def return_book(self, book, reader):
        for loan in self.loans:
            if loan.book == book and loan.reader == reader:
                book.quantity += 1
                self.loans.remove(loan)
                print(f"Книга '{book.title}' возвращена читателем '{reader.first_name} {reader.last_name}'.")
                return
        print("Данная книга не была выдана этому читателю.")


class Reader:
    def __init__(self, first_name, last_name, reader_id):
        self.first_name = first_name
        self.last_name = last_name
        self.reader_id = reader_id
        self.borrowed_books = {} # Use dictionary for easier book management. Key: Book, Value: Loan date

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.reader_id})"

    # The borrow_book and return_book logic moved into the Library class

class Loan:
    def __init__(self, book, reader, loan_date, due_date):
        self.book = book
        self.reader = reader
        self.loan_date = loan_date
        self.due_date = due_date

    def __str__(self):
        return f"Книга: {self.book.title}, Читатель: {self.reader.first_name} {self.reader.last_name}, Дата выдачи: {self.loan_date}, Дата возврата: {self.due_date}"

# Основная функция
if __name__ == "__main__":
    # Создание авторов
    author1 = Author("Джон", "Толкин")
    author2 = Author("Агата", "Кристи")

    # Создание книг
    book1 = Book("Властелин колец", author1, "978-0618260264", "Фэнтези", 5)
    book2 = Book("Убийство в Восточном экспрессе", author2, "978-0062073481", "Детектив", 3)

    # Создание библиотеки
    library = Library("Главная библиотека", "Улица Пушкина, дом Колотушкина")

    # Добавление книг в библиотеку
    library.add_book(book1)
    library.add_book(book2)

    # Создание читателей
    reader1 = Reader("Иван", "Иванов", "12345")
    reader2 = Reader("Мария", "Петрова", "67890")

    # Добавление читателей в библиотеку
    library.add_reader(reader1)
    library.add_reader(reader2)

    # Вывод информации о книгах и читателях в библиотеке
    library.display_books()
    library.display_readers()

    # Библиотека выдает книгу читателю
    library.lend_book(book1, reader1, datetime.date(2025, 2, 1))
    library.lend_book(book2, reader2, datetime.date(2025, 2, 8))
    library.lend_book(book2, reader1, datetime.date(2025, 2, 8))  # Попытка выдать книгу, когда она уже отсутствует

    # Библиотека принимает книгу обратно
    library.return_book(book1, reader1)

    # Библиотека удаляет книгу и читателя
    library.remove_book(book2)
    library.remove_reader(reader2)

    library.display_books()
    library.display_readers()

    # Пример использования класса Loan (выдача книги и информация о ней)
    loan1 = Loan(book1, reader1, datetime.date(2025, 1, 16), datetime.date(2025, 2, 16))
    print(loan1)
