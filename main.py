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
import subprocess
import platform
import psutil
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageTk
import random
import pygame

class App:
    logo_photo = None
    def __init__(self, root):
        self.root = root
        self.root.title("Motivatly - Регистрация")  
        self.user_blocked = False
        self.browser_close_thread = threading.Thread(target=self.close_browsers_thread_func)
        self.browser_close_thread.daemon = True
        self.browser_close_thread.start()
        self.root.resizable(width=False, height=False)

        # Загрузка рандомного изображения фона для главного окна
        self.load_random_background(self.root)

        background_image = Image.open("background.jpg")  # Загружаем изображение только один раз
        background_photo = ImageTk.PhotoImage(background_image)

        # Создание фонового элемента
        background_label = tk.Label(root, image=background_photo)
        background_label.image = background_photo  # Сохраняем ссылку на изображение, чтобы избежать удаления из памяти

        # Размещение фонового элемента на главном окне
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        logo_path = "logo.ico"
        if not App.logo_photo:
            logo_img = Image.open(logo_path)
            App.logo_photo = ImageTk.PhotoImage(logo_img)
        root.iconphoto(False, App.logo_photo)
        self.conn = sqlite3.connect("motivation.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                    id INTEGER PRIMARY KEY,
                                    email TEXT UNIQUE,
                                    password TEXT,
                                    name TEXT,
                                    secret_question TEXT,
                                    secret_answer TEXT,
                                    goal_limit INTEGER DEFAULT 2
                                    )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
                                    id INTEGER PRIMARY KEY,
                                    description TEXT,
                                    deadline DATE,
                                    user_id INTEGER,
                                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS card_details (
                                    id INTEGER PRIMARY KEY,
                                    card_number TEXT,
                                    expiration_date TEXT,
                                    cvv TEXT,
                                    user_id INTEGER,
                                    FOREIGN KEY (user_id) REFERENCES users(id)
                                    )''')
        # Стили для кнопок
        self.style = ttk.Style()
        self.style.configure("Green.TButton", foreground="white", background="#67b83b", font=("Helvetica", 10))
        self.style.map("Green.TButton", background=[("active", "#ff8f1c")])
        
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
        self.show_login_window()
        self.apply_custom_style()
    
    def load_random_background(self, window):
        # Пути к вашим изображениям фонов
        backgrounds = ['background4.png', "background.jpg", "background3.jpg", "background2.png",'background3.png', ]
        random_background_path = random.choice(backgrounds)
        
        # Загружаем изображение
        background_image = Image.open(random_background_path)

        # Устанавливаем фоновое изображение
        photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(window, image=photo)
        background_label.image = photo
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def apply_custom_style(self):
        style = ttk.Style()
        self.root.tk.call('source', 'azure-dark.tcl')  # Подключаем файл стиля (azure-dark.tcl)
        self.style.theme_use('clam')  # Используем стандартную тему Tkinter
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
        style.theme_use('sber_style')  # Используем созданную тему
        
    def show_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Авторизация")
        self.login_window.geometry("240x200")
        self.login_window.resizable(width=False, height=False)
        self.login_window.iconphoto(False, App.logo_photo)
        self.load_random_background(self.login_window)
        self.root.withdraw()
        self.login_window.deiconify()
        self.login_email_label = ttk.Label(self.login_window, text="Email:")
        self.login_email_entry = ttk.Entry(self.login_window)
        self.login_password_label = ttk.Label(self.login_window, text="Пароль:")
        self.login_password_entry = ttk.Entry(self.login_window, show="*")
        self.login_submit_button = ttk.Button(self.login_window, text="Войти", command=self.login, style="Green.TButton")
        self.forgot_password_button = ttk.Button(self.login_window, text="Забыли пароль?", command=self.forgot_password, style="Green.TButton")
        self.return_button = ttk.Button(self.login_window, text="Вернуться к регистрации", command=self.return_to_registration, style="Green.TButton")
        self.login_email_label.grid(row=0, column=0, padx=10, pady=5)
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=5)
        self.login_password_label.grid(row=1, column=0, padx=10, pady=5)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.login_submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.forgot_password_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.return_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="we")
    
    def on_close(self):
        self.root.destroy()
    
    def return_to_registration(self):
        self.login_window.withdraw()
        self.root.deiconify()

    def forgot_password(self):
        self.forgot_password_window = tk.Toplevel(self.login_window)
        self.load_random_background(self.forgot_password_window)
        self.forgot_password_window.title("Забыл/а пароль")
        self.forgot_password_window.geometry("300x150")
        self.forgot_password_window.resizable(width=False, height=False)
        self.forgot_password_window.iconphoto(False, App.logo_photo)
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

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        secret_question = self.secret_question_entry.get()
        secret_answer = self.secret_answer_entry.get()
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
                self.show_profile_window(user)  # Передаем пользователя в show_profile_window
            else:
                messagebox.showerror("Ошибка", "Неверная почта/пароль комбинация.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные данные.")

    def close_browser_tabs_in_thread(self):
        thread = threading.Thread(target=self.close_browser_tabs)
        thread.start()
    
    def start_browser_close_thread(self):
        self.browser_close_thread.start()
    
    def close_browser_thread_func(self):
        while True:
            if self.user_blocked:
                self.close_browser_tabs()
            time.sleep(10)
        
    def show_profile_window(self, user):
        # Открываем аудиофайл
        pygame.init()
        pygame.mixer.init()
        sound = pygame.mixer.Sound("sound.wav")  # Замените "sound.wav" на путь к вашему аудиофайлу

        # Воспроизводим звук
        sound.play()

        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title("Профиль")
        self.profile_window.geometry("600x470")
        self.profile_window.resizable(width=False, height=False)
        self.profile_window.iconphoto(False, App.logo_photo)
        self.root.withdraw()
        self.login_window.withdraw()
        self.user = user

        # Load the background image
        background_image1 = Image.open("background2.jpg")
        background_photo1 = ImageTk.PhotoImage(background_image1)

        # Create a label to display the background image
        background_label1 = tk.Label(self.profile_window, image=background_photo1)
        background_label1.image = background_photo1  # Keep a reference to the image to prevent garbage collection
        background_label1.place(x=0, y=0, relwidth=1, relheight=1)  # Place the background label

        # Apply style to the profile window
        style = ttk.Style()
        style.theme_use('sber_style')

        self.welcome_label = ttk.Label(self.profile_window, text=f"Здравствуйте, {self.user[3]}!")
        self.welcome_label.pack(pady=10)

        self.goals_label = ttk.Label(self.profile_window, text="Ваши цели:")
        self.goals_label.pack()

        self.listbox = tk.Listbox(self.profile_window, width=50)
        self.listbox.pack(pady=5)

        self.load_goals(user)

        # Apply style to the buttons
        self.add_goal_button = ttk.Button(self.profile_window, text="Добавить цель", command=self.add_goal)
        self.add_goal_button.pack(pady=5)

        self.delete_goal_button = ttk.Button(self.profile_window, text="Удалить выбранную цель", command=self.delete_goal)
        self.delete_goal_button.pack(pady=5)

        self.logout_button = ttk.Button(self.profile_window, text="Выйти", command=self.logout)
        self.logout_button.pack(pady=5)

        self.add_card_details_button = ttk.Button(self.profile_window, text="Купить подписку", command=self.add_card_details)
        self.add_card_details_button.pack(pady=5)

    def load_goals(self, user):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT description, deadline FROM goals WHERE user_id = ?", (user[0],))
        goals = self.cursor.fetchall()
        for goal in goals:
            description, deadline = goal
            self.listbox.insert(tk.END, f"{description} - {deadline}")
            if datetime.strptime(deadline, '%Y-%m-%d') < datetime.now():
                self.set_block()
                
    def add_goal(self):
        description = simpledialog.askstring("Добавить цель", "Введите, что нужно сделать для вашей цели:")
        deadline = simpledialog.askstring("Добавить цель", "Введите дату окончания (YYYY-MM-DD):")
        if description and deadline:
            try:
                self.cursor.execute("SELECT COUNT(*) FROM goals WHERE user_id = ?", (self.user[0],))
                current_goals_count = self.cursor.fetchone()[0]
                self.cursor.execute("SELECT goal_limit FROM users WHERE id = ?", (self.user[0],))
                goal_limit = self.cursor.fetchone()[0]
                if current_goals_count < goal_limit:
                    self.cursor.execute("INSERT INTO goals (description, deadline, user_id) VALUES (?, ?, ?)", (description, deadline, self.user[0]))
                    self.conn.commit()
                    self.load_goals(self.user)  # Pass the user argument here
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
            self.load_goals(self.user)  # Передайте объект пользователя в load_goals()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите цель для удаления")

    def add_card_details(self):
        self.card_details_window = tk.Toplevel(self.profile_window)
        self.load_random_background(self.card_details_window)
        self.card_details_window.title("Подписка")
        self.card_details_window.geometry("250x150")
        self.card_details_window.iconphoto(False, App.logo_photo)
        self.card_details_window.resizable(width=False, height=False)
        self.card_number_label = ttk.Label(self.card_details_window, text="Номер карты:")
        self.card_number_entry = ttk.Entry(self.card_details_window)

        # Добавляем валидатор для ввода номера карты, чтобы вставлять пробел после каждых 4 цифр
        self.card_number_entry.config(validate="key", validatecommand=(self.root.register(self.validate_card_number), "%P"))
        
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

    def validate_card_number(self, new_value):
        # Валидатор для номера карты: вставляет пробел после каждых 4 цифр
        # new_value - новое значение вводимое в поле
        
        # Удаляем пробелы из введенной строки
        new_value = new_value.replace(" ", "")
        
        # Вставляем пробел после каждых 4 цифр
        formatted_value = " ".join([new_value[i:i+4] for i in range(0, len(new_value), 4)])
        
        # Возвращаем отформатированную строку, которая будет отображаться в поле ввода
        return formatted_value

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

        # После успешного сохранения данных карты, обновляем лимит целей пользователя до 10
        self.cursor.execute("UPDATE users SET goal_limit = ? WHERE id = ?", (10, self.user[0]))
        self.conn.commit()
        # Обновляем информацию о текущем пользователе в памяти
        self.user = (self.user[0], self.user[1], self.user[2], self.user[3], self.user[4], self.user[5], 10)

        self.cursor.execute("INSERT INTO card_details (card_number, expiration_date, cvv, user_id) VALUES (?, ?, ?, ?)",
                            (card_number, expiration_date, cvv, self.user[0]))
        self.conn.commit()
        messagebox.showinfo("Успешно", "Покупка совершенна!")
        self.card_details_window.destroy()

    def user_has_subscription(self):
        self.cursor.execute("SELECT * FROM card_details WHERE user_id = ?", (self.user[0],))
        return self.cursor.fetchone() is not None
    
    def close_browsers_thread_func(self):
        browsers = ["chrome",'browser', "msedge", "firefox"]
        while True:
            if self.user_blocked and self.goal_overdue():
                for proc in psutil.process_iter():
                    try:
                        for browser in browsers:
                            if browser in proc.name().lower():
                                proc.kill()
                    except psutil.NoSuchProcess:
                        # Процесс уже завершился, продолжаем выполнение
                        pass
            time.sleep(15)

    def goal_completed(self):
        return datetime.now() <= self.goal_deadline

    def set_block(self):
        self.user_blocked = True
        self.blocked_until = datetime.now() + timedelta(minutes=30)

    def remove_block(self):
        self.user_blocked = False

    def show_message(self, title, message):
        if title == "Блокировка":
            self.close_browsers_thread_func()
    
    def check_goal_deadline(self):
        while True:
            if not self.user_blocked and not self.goal_completed():
                self.set_block()
                self.show_message("Блокировка", f"Вы не выполнили цель в срок. Вы заблокированы на YouTube на 30 минут.")
                self.close_browsers_thread_func()
            time.sleep(10)

    def open_youtube(self):
        if self.user_blocked:
            while datetime.now() < self.blocked_until:
                remaining_time = self.blocked_until - datetime.now()
                remaining_minutes = remaining_time.seconds // 60
                self.show_message("Блокировка", f"У вас блокировка на YouTube до {self.blocked_until}. Осталось {remaining_minutes} минут.")
                time.sleep(10)
            self.remove_block()
            self.show_message("Блокировка снята", "Ваша блокировка на YouTube снята!")
        else:
            if self.goal_overdue():
                self.show_message("Блокировка", "Вы просрочили одну из целей. Вы заблокированы на YouTube на 30 минут.")
                self.set_block()
                self.close_browsers_thread_func()
            else:
                webbrowser.open("https://www.youtube.com")

    def close_youtube_window(self):
        if platform.system() == "Windows":
            subprocess.run(["taskkill", "/f", "/im", "chrome.exe"], shell=True)
        elif platform.system() == "Linux":
            subprocess.run(["pkill", "chrome"], shell=True)
        elif platform.system() == "Darwin":
            subprocess.run(["pkill", "Google Chrome"], shell=True)
        else:
            self.show_message("Ошибка", "Ваша операционная система не поддерживается.")

    def logout(self):
        self.profile_window.destroy()
        self.root.deiconify()
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Вы вышли", "Выход из аккаунта успешнно выполнен")
        
    def on_close(self):
        self.conn.close()
        self.running = False
        self.root.destroy()
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
