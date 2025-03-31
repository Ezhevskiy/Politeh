
import tkinter as tk
from tkinter import ttk, messagebox
import re
import datetime
import logging

class BugReportApp:
    """
    Приложение для отправки отчетов об ошибках с логированием в текстовый файл (Tkinter версия).
    """

    def __init__(self, root):
        """
        Инициализирует приложение, создает пользовательский интерфейс и настраивает логирование.
        """
        self.root = root
        self.root.title('Отчет об ошибке')
        self.log_file = "bug_reports.log"  # Имя файла журнала
        self.setup_logging() # Настройка логирования
        self.reports = [] # Список для хранения отчетов
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

        # --- Стиль ---
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="raised")
        style.configure("TLabel", padding=3)
        style.configure("TEntry", padding=3)

        # Создаем стиль для синих кнопок
        style.configure("Blue.TButton",
                        background="blue",
                        foreground="blue",
                        padding=6)

        # Labels and Input Fields
        # Метки и поля ввода
        self.label_name = ttk.Label(self.root, text="Имя:")
        self.input_name = ttk.Entry(self.root, width=40)

        self.label_email = ttk.Label(self.root, text="Почта:")
        self.input_email = ttk.Entry(self.root, width=40)

        self.label_priority = ttk.Label(self.root, text="Приоритет:")
        self.dropdown_priority = ttk.Combobox(self.root, values=["Низкий", "Средний", "Высокий", "Критический"], state="readonly")
        self.dropdown_priority.set("Средний") # Значение по умолчанию

        self.label_description = ttk.Label(self.root, text="Описание ошибки:")
        self.text_description = tk.Text(self.root, height=10, width=50)


        self.output_area = tk.Text(self.root, height=10, width=60, state="disabled")


        self.button_submit = ttk.Button(self.root, text="Отправить отчет", command=self.submit_report, style="Blue.TButton")
        self.button_clear = ttk.Button(self.root, text="Очистить форму", command=self.clear_form, style="Blue.TButton")
        self.button_show_reports = ttk.Button(self.root, text="Показать отчеты", command=self.show_reports, style="Blue.TButton") # Кнопка для отображения отчетов

        row = 0
        self.label_name.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_name.grid(row=row, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
        row += 1
        self.label_email.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.input_email.grid(row=row, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
        row += 1
        self.label_priority.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.dropdown_priority.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        row += 1
        self.label_description.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.text_description.grid(row=row, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
        row += 1
        self.output_area.grid(row=row, column=0, columnspan=2, sticky=tk.E + tk.W, padx=5, pady=5)
        row += 1
        self.button_submit.grid(row=row, column=0, sticky=tk.W, padx=5, pady=10)
        self.button_show_reports.grid(row=row, column=1, sticky=tk.W, padx=5, pady=10)
        self.button_clear.grid(row=row, column=2, sticky=tk.W, padx=5, pady=10)


        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(2, weight=1)

        for i in range(row + 1):
            self.root.rowconfigure(i, weight=0)

    def submit_report(self):
        """
        Обрабатывает отправку отчета.  Проверяет ввод, собирает данные,
        логирует их в файл и отображает подтверждение.  Сохраняет отчет в списке.
        """
        name = self.input_name.get()
        email = self.input_email.get()
        priority = self.dropdown_priority.get()
        description = self.text_description.get("1.0", tk.END)

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
        self.output_area.config(state="normal")  # Разрешить редактирование
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, report_text)
        self.output_area.config(state="disabled") # Запретить редактирование

        self.log_report(name, email, priority, description) # Логирование отчета

        # Отображение сообщения об успехе
        messagebox.showinfo("Отчет отправлен", "Ваш отчет об ошибке успешно отправлен!")


    def clear_form(self):
        """
        Очищает все поля ввода и область вывода.
        """
        self.input_name.delete(0, tk.END)
        self.input_email.delete(0, tk.END)
        self.text_description.delete("1.0", tk.END)
        self.output_area.config(state="normal")
        self.output_area.delete("1.0", tk.END)
        self.output_area.config(state="disabled")

    def validate_input(self, name, email, description):
        """
        Проверяет ввод имени, электронной почты и описания.  Отображает сообщения об ошибках, если ввод недействителен.
        """
        if not name:
            messagebox.warning("Ошибка ввода", "Пожалуйста, введите ваше имя.")
            return False

        if not email:
            messagebox.warning("Ошибка ввода", "Пожалуйста, введите ваш адрес электронной почты.")
            return False

        if not self.is_valid_email(email):
            messagebox.warning("Ошибка ввода", "Пожалуйста, введите действующий адрес электронной почты.")
            return False

        if not description:
            messagebox.warning("Ошибка ввода", "Пожалуйста, введите описание ошибки.")
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
            messagebox.showinfo("Отчеты", "Нет отчетов для отображения.")
            return

        # Собирает все отформатированные отчеты в одну строку
        formatted_reports = "".join(map(format_report, reports_to_display))

        # Отображает отчеты в текстовом поле
        self.output_area.config(state="normal")  # Разрешить редактирование
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, formatted_reports)
        self.output_area.config(state="disabled")  # Запретить редактирование


if __name__ == '__main__':
    root = tk.Tk()
    app = BugReportApp(root)
    root.mainloop()
