
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel,
                             QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox,
                             QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt
import re
import datetime
import logging

class BugReportApp(QWidget):
    """
    Приложение для отправки отчетов об ошибках с логированием в текстовый файл (PyQt5 версия).
    """

    def __init__(self):
        """
        Инициализирует приложение, задает заголовок, положение и размеры окна,
        инициализирует пользовательский интерфейс и настраивает логирование.
        """
        super().__init__()
        self.title = 'Отчет об ошибке'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.log_file = "bug_reports.log"  # Имя файла журнала
        self.reports = []  # Список для хранения отчетов
        self.setup_logging()
        self.initUI()

    def setup_logging(self):
        """Настраивает базовую конфигурацию логирования."""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)  # Логгер для текущего модуля


    def initUI(self):
        """
        Создает и размещает элементы управления в пользовательском интерфейсе.
        Включает метки, поля ввода, выпадающий список, текстовое поле и кнопки.
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Labels and Input Fields
        # Метки и поля ввода
        self.label_name = QLabel("Имя:")
        self.input_name = QLineEdit()

        self.label_email = QLabel("Почта:")
        self.input_email = QLineEdit()

        self.label_priority = QLabel("Приоритет:")
        self.dropdown_priority = QComboBox()
        self.dropdown_priority.addItems(["Низкий", "Средний", "Высокий", "Критический"])

        self.label_description = QLabel("Описание ошибки:")
        self.text_description = QTextEdit()

        # Output Area
        # Область вывода
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)

        # Buttons
        # Кнопки
        self.button_submit = QPushButton("Отправить отчет")
        self.button_clear = QPushButton("Очистить форму")
        self.button_show_reports = QPushButton("Показать отчеты")  # Кнопка для отображения отчетов

        # Connect buttons to functions
        # Связываем кнопки с функциями
        self.button_submit.clicked.connect(self.submit_report)
        self.button_clear.clicked.connect(self.clear_form)
        self.button_show_reports.clicked.connect(self.show_reports)  # Связываем с методом show_reports

        # Layout
        # Разметка
        form_layout = QVBoxLayout()
        form_layout.addWidget(self.label_name)
        form_layout.addWidget(self.input_name)
        form_layout.addWidget(self.label_email)
        form_layout.addWidget(self.input_email)
        form_layout.addWidget(self.label_priority)
        form_layout.addWidget(self.dropdown_priority)
        form_layout.addWidget(self.label_description)
        form_layout.addWidget(self.text_description)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_submit)
        button_layout.addWidget(self.button_clear)
        button_layout.addWidget(self.button_show_reports)  # Добавляем кнопку в разметку

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.output_area)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Styling using CSS-like syntax
        # Стилизация с использованием CSS-подобного синтаксиса
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: sans-serif;
                font-size: 11pt;
            }

            QLabel {
                color: #333;
                margin-bottom: 5px;
            }

            QLineEdit, QComboBox, QTextEdit {
                border: 1px solid #ccc;
                padding: 8px;
                border-radius: 5px;
                background-color: #fff;
                selection-background-color: #a0c4ff;
            }

            QPushButton {
                background-color: #0077cc;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12pt;
                margin: 5px 2px;
                cursor: pointer;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #005ea3;
            }

            QTextEdit {
                min-height: 100px;
            }
        """)

        self.show()


    def submit_report(self):
        """
        Обрабатывает отправку отчета.  Проверяет ввод, собирает данные,
        логирует их в файл и отображает подтверждение.  Сохраняет отчет в списке.
        """
        name = self.input_name.text()
        email = self.input_email.text()
        priority = self.dropdown_priority.currentText()
        description = self.text_description.toPlainText()

        if not self.validate_input(name, email, description):
            return  # Прекратить отправку, если проверка не пройдена

        report = {
            "name": name,
            "email": email,
            "priority": priority,
            "description": description
        }
        self.reports.append(report) # Сохраняем отчет в списке

        report_text = (f"Имя: {name}\n"
                       f"Почта: {email}\n"
                       f"Приоритет: {priority}\n"
                       f"Описание: {description}")
        self.output_area.setText(report_text)

        self.log_report(name, email, priority, description) # Логирование отчета

        # Show a success message
        # Отображение сообщения об успехе
        QMessageBox.information(self, "Отчет отправлен", "Ваш отчет об ошибке успешно отправлен!")


    def clear_form(self):
        """
        Очищает все поля ввода и область вывода.
        """
        self.input_name.clear()
        self.input_email.clear()
        self.text_description.clear()
        self.output_area.clear()

    def validate_input(self, name, email, description):
        """
        Проверяет ввод имени, электронной почты и описания.  Отображает сообщения об ошибках, если ввод недействителен.
        """
        if not name:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите ваше имя.")
            return False

        if not email:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите ваш адрес электронной почты.")
            return False

        if not self.is_valid_email(email):
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите действующий адрес электронной почты.")
            return False

        if not description:
            QMessageBox.warning(self, "Ошибка ввода", "Пожалуйста, введите описание ошибки.")
            return False

        return True  # Все проверки пройдены

    def is_valid_email(self, email):
        """
        Проверяет, является ли данный адрес электронной почты действительным.
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email) is not None

    def log_report(self, name, email, priority, description):
        """
        Логирует данные отчета об ошибке в текстовый файл.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (f"[{timestamp}] Отчет об ошибке:\n"
                     f"  Имя: {name}\n"
                     f"  Email: {email}\n"
                     f"  Приоритет: {priority}\n"
                     f"  Описание: {description}\n"
                     f"--------------------------------------\n")

        try:
            with open(self.log_file, "a", encoding="utf-8") as log: # Открываем файл для добавления
                log.write(log_entry)
            self.logger.info(f"Отчет об ошибке записан в {self.log_file}")  # Используем логгер
        except Exception as e:
            self.logger.error(f"Ошибка при записи в файл журнала: {e}")

    def show_reports(self):
        """Отображает отчёты, используя лямбда-выражения для форматирования и фильтрации."""

        # 1. Форматирование отчета для отображения (лямбда)
        format_report = lambda report: (
            f"Имя: {report['name']}\n"
            f"Почта: {report['email']}\n"
            f"Приоритет: {report['priority']}\n"
            f"Описание: {report['description']}\n"
            f"--------------------------------------\n"
        )

        # 2. Фильтрация отчетов по приоритету (лямбда)
        priority_filter = lambda priority: lambda report: report['priority'] == priority
        high_priority_reports = list(filter(priority_filter("Высокий"), self.reports))

        # 3. Вывод всех отчетов или отчетов с высоким приоритетом
        reports_to_display = high_priority_reports if high_priority_reports else self.reports #Показывать high priority reports, если они есть, иначе показать все

        if not reports_to_display:
            QMessageBox.information(self, "Отчеты", "Нет отчетов для отображения.")
            return

        # Собираем все отформатированные отчеты в одну строку
        formatted_reports = "".join(map(format_report, reports_to_display))

        # Отображаем отчеты в текстовом поле
        self.output_area.setText(formatted_reports)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BugReportApp()
    sys.exit(app.exec_())
