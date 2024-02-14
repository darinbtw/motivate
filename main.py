import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkinter import messagebox as msgbox
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import webbrowser
import threading
import webbrowser
import time

class App:
    logo_photo = None  # Static variable to store logo photo

    def __init__(self, root):
        self.user_blocked = False  # Флаг блокировки пользователя
        self.blocked_until = None  # Время, до которого пользователь заблокирован
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)  # Обработчик события закрытия окна
        self.running = True  

        # Load background image
        background_image = Image.open("C:/Users/Vlad/Documents/GitHub/motivate/background.jpg")
        background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(root, image=background_photo)
        background_label.place(relwidth=1, relheight=1)

        # Display background image
        background_label = tk.Label(root, image=background_photo)
        background_label.place(relwidth=1, relheight=1)
        
        # Путь к файлу с логотипом
        logo_path = "logo.ico"

        # Загрузка изображения и создание объекта PhotoImage
        if not App.logo_photo:
            logo_img = Image.open(logo_path)
            App.logo_photo = ImageTk.PhotoImage(logo_img)

        # Установка иконки приложения
        root.iconphoto(False, App.logo_photo) 

        # Connect to database, initialize cursor
        self.conn = sqlite3.connect("motivation.db")
        self.cursor = self.conn.cursor()

        # Create users table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    email TEXT UNIQUE,
                                    password TEXT,
                                    name TEXT,
                                    secret_question TEXT,
                                    secret_answer TEXT,
                                    goal_limit INTEGER DEFAULT 2
                                    )''')

        # Create goals table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                                    id INTEGER PRIMARY KEY,
                                    description TEXT,
                                    deadline DATE,
                                    user_id INTEGER,
                                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )''')

        # Create card details table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS card_details (
                                    id INTEGER PRIMARY KEY,
                                    card_number TEXT,
                                    expiration_date TEXT,
                                    cvv TEXT,
                                    user_id INTEGER,
                                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )''')

        # Create widgets for registration
        self.email_label = ttk.Label(self.root, text="Email:")
        self.email_entry = ttk.Entry(self.root)
        self.password_label = ttk.Label(self.root, text="Пароль:")
        self.password_entry = ttk.Entry(self.root, show="*")
        self.name_label = ttk.Label(self.root, text="Имя(Настоящее):")
        self.name_entry = ttk.Entry(self.root)
        self.secret_question_label = ttk.Label(self.root, text="Секретный вопрос:")
        self.secret_question_entry = ttk.Entry(self.root)
        self.secret_answer_label = ttk.Label(self.root, text="Секретный ответ:")
        self.secret_answer_entry = ttk.Entry(self.root)

        self.register_button = ttk.Button(self.root, text="Зарегестрироваться", command=self.register)
        self.login_button = ttk.Button(self.root, text="Есть аккаунт? Жмите сюда!", command=self.show_login_window)

        # Layout widgets for registration
        self.email_label.grid(row=0, column=0, padx=10, pady=5)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.name_label.grid(row=2, column=0, padx=10, pady=5)
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)
        self.secret_question_label.grid(row=3, column=0, padx=10, pady=5)
        self.secret_question_entry.grid(row=3, column=1, padx=10, pady=5)
        self.secret_answer_label.grid(row=4, column=0, padx=10, pady=5)
        self.secret_answer_entry.grid(row=4, column=1, padx=10, pady=5)
        self.register_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.login_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="we")

        # Apply custom style
        self.apply_custom_style()  

    def apply_custom_style(self):
        # Apply custom style to ttk widgets
        style = ttk.Style()
        style.theme_create('sber_style', parent='clam', settings={
            "TButton": {
                "configure": {
                    "background": "#67b83b",  # Зеленый цвет СберБанка
                    "foreground": "white",
                    "padding": 5,
                    "font": ("Helvetica", 10),
                    "highlightthickness": 0  # Убираем прозрачный фон
                },
                "map": {
                    "background": [("active", "#ff8f1c")]  # Оранжевый цвет СберБанка при наведении
                }
            }
        })
        style.theme_use('sber_style')

    def show_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Авторизация")
        self.login_window.geometry("280x260")
        self.login_window.resizable(width=False, height=False)

        self.login_window.iconphoto(False, App.logo_photo)
        # Hide registration window
        self.root.withdraw()

        # Показать другое окно
        self.login_window.deiconify()

        self.login_email_label = ttk.Label(self.login_window, text="Email:")
        self.login_email_entry = ttk.Entry(self.login_window)
        self.login_password_label = ttk.Label(self.login_window, text="Пароль:")
        self.login_password_entry = ttk.Entry(self.login_window, show="*")

        self.login_submit_button = ttk.Button(self.login_window, text="Залогиниться", command=self.login)
        self.forgot_password_button = ttk.Button(self.login_window, text="Забыли пароль?", command=self.forgot_password)
        self.return_button = ttk.Button(self.login_window, text="Вернуться к регестриации", command=self.return_to_registration)

        self.login_email_label.grid(row=0, column=0, padx=10, pady=5)
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=5)
        self.login_password_label.grid(row=1, column=0, padx=10, pady=5)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.login_submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.forgot_password_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.return_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    
    def return_to_registration(self):
        self.login_window.withdraw()
        self.root.deiconify()

    def forgot_password(self):
        self.forgot_password_window = tk.Toplevel(self.login_window)
        self.forgot_password_window.title("Забыл/а пароль")
        self.forgot_password_window.geometry("300x150")
        self.forgot_password_window.resizable(width=False, height=False)
        self.login_window.iconphoto(False, App.logo_photo)

        self.forgot_email_label = ttk.Label(self.forgot_password_window, text="Email:")
        self.forgot_email_entry = ttk.Entry(self.forgot_password_window)
        self.forgot_name_label = ttk.Label(self.forgot_password_window, text="Ваше имя:")
        self.forgot_name_entry = ttk.Entry(self.forgot_password_window)
        self.forgot_question_label = ttk.Label(self.forgot_password_window, text="Секретный вопрос:")
        self.forgot_question_entry = ttk.Entry(self.forgot_password_window)

        self.forgot_submit_button = ttk.Button(self.forgot_password_window, text="Отправить", command=self.check_secret_answer)

        self.forgot_email_label.grid(row=0, column=0, padx=10, pady=5)
        self.forgot_email_entry.grid(row=0, column=1, padx=10, pady=5)
        self.forgot_name_label.grid(row=1, column=0, padx=10, pady=5)
        self.forgot_name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.forgot_question_label.grid(row=2, column=0, padx=10, pady=5)
        self.forgot_question_entry.grid(row=2, column=1, padx=10, pady=5)
        self.forgot_submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    def check_secret_answer(self):
        email = self.forgot_email_entry.get()
        name = self.forgot_name_entry.get()
        question = self.forgot_question_entry.get()

        if email and name and question:
            self.cursor.execute("SELECT * FROM users WHERE email = ? AND name = ? AND secret_question = ?", (email, name, question))
            user = self.cursor.fetchone()
            if user:
                secret_answer = simpledialog.askstring("Секретный вопрос", "Введите свой ответ на вопрос:")
                if secret_answer == user[5]:
                    messagebox.showinfo("Успешно", f"Ваш пароль: {user[2]}")
                    self.forgot_password_window.destroy()
                else:
                    messagebox.showerror("Ошибка", "Неверный ответ на вопрос.")
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите данные.")
    
    
    def check_goal_deadline(self):
        while True:
            # Проверяем, если пользователь не выполнил цель и блокировка еще не установлена
            if not self.user_blocked and not self.goal_completed():
                self.set_block()  # Устанавливаем блокировку
                # Сообщаем пользователю о блокировке
                self.show_message("Блокировка", f"Вы не выполнили цель в срок. Вы заблокированы на YouTube на 30 минут.")
            time.sleep(60)  # Проверяем цель каждую минуту
    
    
    def check_goal_deadline(self):
        while True:
            # Проверяем, если пользователь не выполнил цель и блокировка еще не установлена
            if not self.user_blocked and not self.goal_completed():
                self.set_block()  # Устанавливаем блокировку
                # Сообщаем пользователю о блокировке
                self.show_message("Блокировка", f"Вы не выполнили цель в срок. Вы заблокированы на YouTube на 30 минут.")
            time.sleep(60)  # Проверяем цель каждую минуту

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        secret_question = self.secret_question_entry.get()
        secret_answer = self.secret_answer_entry.get()

        # Проверка наличия корректного домена в адресе электронной почты
        valid_domains = ['@gmail.com', '@yandex.ru', '@mail.ru', '@bk.ru', '@phystech.pro']
        if not any(domain in email for domain in valid_domains):
            messagebox.showerror("Ошибка", "Неподдерживаемый домен электронной почты.")
            return

        if email and password and name and secret_question and secret_answer:
            try:
                self.cursor.execute("INSERT INTO users (email, password, name, secret_question, secret_answer, goal_limit) VALUES (?, ?, ?, ?, ?, ?)", (email, password, name, secret_question, secret_answer, 2))
                self.conn.commit()
                messagebox.showinfo("Успешно", "Регистрация успешно пройдена!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Пользователь с такой почтой уже зарегистрирован.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    def login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        if email and password:
            self.cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = self.cursor.fetchone()
            if user:
                messagebox.showinfo("Успешно", f"Добро пожаловать, {user[3]}!")
                self.show_profile_window(user)
            else:
                messagebox.showerror("Ошибка", "Неверная почта/пароль комбинация.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    def show_profile_window(self, user):
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title("Профиль")
        self.profile_window.geometry("470x425")
        self.profile_window.resizable(width=False, height=False)

        # Hide both registration and login windows
        self.root.withdraw()
        self.login_window.withdraw()

        self.user = user

        self.welcome_label = ttk.Label(self.profile_window, text=f"Здравствуйте, {self.user[3]}!")
        self.welcome_label.pack(pady=10)

        self.goals_label = ttk.Label(self.profile_window, text="Ваши цели:")
        self.goals_label.pack()

        self.listbox = tk.Listbox(self.profile_window, width=50)
        self.listbox.pack(pady=5)

        self.load_goals()

        self.add_goal_button = ttk.Button(self.profile_window, text="Добавить цель", command=self.add_goal)
        self.add_goal_button.pack(pady=5)

        self.delete_goal_button = ttk.Button(self.profile_window, text="Удалить выбранную цель", command=self.delete_goal)
        self.delete_goal_button.pack(pady=5)

        self.logout_button = ttk.Button(self.profile_window, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=5)

        self.add_card_details_button = ttk.Button(self.profile_window, text="Купить подписку", command=self.add_card_details)
        self.add_card_details_button.pack(pady=5)

    def load_goals(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT description, deadline FROM goals WHERE user_id = ?", (self.user[0],))
        goals = self.cursor.fetchall()
        for goal in goals:
            description, deadline = goal
            self.listbox.insert(tk.END, f"{description} - {deadline}")

    def add_goal(self):
        description = simpledialog.askstring("Добавить цель", "Введите, что нужно сделать для вашей цели:")
        deadline = simpledialog.askstring("Добавить цель", "Введите дату окончания (YYYY-MM-DD):")

        if description and deadline:
            try:
                # Получаем текущее количество целей пользователя
                self.cursor.execute("SELECT COUNT(*) FROM goals WHERE user_id = ?", (self.user[0],))
                current_goals_count = self.cursor.fetchone()[0]

                # Получаем текущий лимит целей пользователя
                self.cursor.execute("SELECT goal_limit FROM users WHERE id = ?", (self.user[0],))
                goal_limit = self.cursor.fetchone()[0]

                if current_goals_count < goal_limit:
                    self.cursor.execute("INSERT INTO goals (description, deadline, user_id) VALUES (?, ?, ?)", (description, deadline, self.user[0]))
                    self.conn.commit()
                    self.load_goals()
                else:
                    messagebox.showerror("Ошибка", f"Вы достигли лимита целей ({goal_limit})!")
            except sqlite3.Error as e:
                print("Ошибка при добавлении цели:", e)
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите данные для цели.")

    def delete_goal(self):
        selected_index = self.listbox.curselection()  # Получаем индекс выбранного элемента
        if selected_index:
            goal_info = self.listbox.get(selected_index)  # Получаем информацию о выбранной цели
            goal_description = goal_info.split(" - ")[0]  # Получаем описание цели
            self.cursor.execute("DELETE FROM goals WHERE description = ? AND user_id = ?", (goal_description, self.user[0]))
            self.conn.commit()
            messagebox.showinfo("Успешно", "Ваша цель удалена!")
            self.load_goals()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите цель для удаления")

    def add_card_details(self):
        self.card_details_window = tk.Toplevel(self.profile_window)
        self.card_details_window.title("Подписка")
        self.card_details_window.geometry("400x200")
        self.card_details_window.resizable(width=False, height=False)

        self.card_number_label = ttk.Label(self.card_details_window, text="Номер карты:")
        self.card_number_entry = ttk.Entry(self.card_details_window)
        self.expiration_date_label = ttk.Label(self.card_details_window, text="Дата окончания:")
        self.expiration_date_entry = ttk.Entry(self.card_details_window)
        self.cvv_label = ttk.Label(self.card_details_window, text="CVV:")
        self.cvv_entry = ttk.Entry(self.card_details_window)

        self.card_submit_button = ttk.Button(self.card_details_window, text="Подтвердить", command=self.save_card_details)

        self.card_number_label.grid(row=0, column=0, padx=10, pady=5)
        self.card_number_entry.grid(row=0, column=1, padx=10, pady=5)
        self.expiration_date_label.grid(row=1, column=0, padx=10, pady=5)
        self.expiration_date_entry.grid(row=1, column=1, padx=10, pady=5)
        self.cvv_label.grid(row=2, column=0, padx=10, pady=5)
        self.cvv_entry.grid(row=2, column=1, padx=10, pady=5)
        self.card_submit_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    def save_card_details(self):
        card_number = self.card_number_entry.get()
        expiration_date = self.expiration_date_entry.get()
        cvv = self.cvv_entry.get()

        if len(card_number) != 16:
            messagebox.showerror("Ошибка", "Номер карты должен состоять из 16-ти чисел.")
            return
        if len(expiration_date) != 5 or expiration_date[2] != '/':
            messagebox.showerror("Ошибка", "Срок истечения должен состоять из (2 цифр) месяца /дня (2 цифр).")
            return
        if len(cvv) != 3:
            messagebox.showerror("Ошибка", "CVV должен состоять из 3 цифр вашей карты.")
            return

        try:
            expiration_month, expiration_year = expiration_date.split('/')
            expiration_month = int(expiration_month)
            expiration_year = int(expiration_year)
            cvv = int(cvv)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ввод даты истечения срока действия или CVV.")
            return

        if expiration_month < 1 or expiration_month > 12 or expiration_year < 0:
            messagebox.showerror("Ошибка", "Недействительный срок годности.")
            return

        self.cursor.execute("INSERT INTO card_details (card_number, expiration_date, cvv, user_id) VALUES (?, ?, ?, ?)",
                            (card_number, expiration_date, cvv, self.user[0]))
        self.conn.commit()
        messagebox.showinfo("Успешно", "Покупка совершенна!")
        self.card_details_window.destroy()

    def user_has_subscription(self):
        # Проверка подписки пользователя
        self.cursor.execute("SELECT * FROM card_details WHERE user_id = ?", (self.user[0],))
        return self.cursor.fetchone() is not None

    def set_block(self):
        self.user_blocked = True
        self.blocked_until = datetime.now() + timedelta(minutes=30)  # Устанавливаем время снятия блокировки

    def check_block(self):
        while True:
            if self.user_blocked:
                if datetime.now() >= self.blocked_until:
                    self.remove_block()  # Снимаем блокировку
                    # Сообщаем пользователю о снятии блокировки
                    self.show_message("Блокировка снята", "Ваша блокировка на YouTube снята!")
            time.sleep(60)  # Проверяем блокировку каждую минуту

    def remove_block(self):
        self.user_blocked = False

    def show_message(self, title, message):
        root = tk.Tk()
        root.withdraw()  # Скрыть основное окно
        messagebox.showinfo(title, message)

    def open_youtube(self):
        if self.user_blocked:
            self.show_message("Блокировка", f"У вас блокировка на YouTube до {self.blocked_until}.")
        else:
            webbrowser.open("https://www.youtube.com")

    def logout(self):
        self.profile_window.destroy()
        self.root.deiconify()
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Вы вышли", "Выход из аккаунта успешнно выполнен")
    
    def on_close(self):
        self.root.destroy()  # Закрыть основное окно
        try:
            self.login_window.destroy()  # Закрыть окно авторизации
        except AttributeError:
            pass
        try:
            self.profile_window.destroy()  # Закрыть окно профиля
        except AttributeError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
