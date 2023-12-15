import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime, timedelta

class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Регистрация")
        self.master.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Регистрация")
        self.label.pack(pady=10)

        self.usermail_label = tk.Label(self.master, text="Почта:")
        self.usermail_label.pack()
        self.usermail_entry = tk.Entry(self.master)
        self.usermail_entry.pack()

        self.password_label = tk.Label(self.master, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.phone_label = tk.Label(self.master, text="Телефон:")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self.master)
        self.phone_entry.pack()

        self.register_button = tk.Button(self.master, text="Регистрация", command=self.register)
        self.register_button.pack(pady=10)

    def register(self):
        usermail = self.usermail_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()

        # Проверяем, что телефонный номер содержит ровно 10 цифр
        if len(phone) == 11 and phone.isdigit():
            # Сохраняем данные в базе данных
            self.save_user_data(usermail, password, phone)

            # Открываем главное окно приложения
            self.open_main_app(usermail)
        else:
            messagebox.showinfo("Не правильно введено", "Пожалуйста, введите 11-ти значное значение телефонного номера.")

    def save_user_data(self, usermail, password, phone):
        # Создаем подключение к базе данных
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        # Создаем таблицу, если она еще не создана
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           usermail TEXT,
                           password TEXT,
                           phone TEXT)''')
        conn.commit()

        # Вставляем данные пользователя
        cursor.execute("INSERT INTO users (username, password, phone) VALUES (?, ?, ?)", (usermail, password, phone))
        conn.commit()

        # Закрываем соединение
        conn.close()

    def open_main_app(self, username):
        # Закрываем окно регистрации
        self.master.destroy()

        # Открываем главное окно приложения
        root = tk.Tk()
        MainApp(root, username)
        root.mainloop()

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Логин")
        self.master.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Почта")
        self.label.pack(pady=10)

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.master, text="Register", command=self.show_registration_window)
        self.register_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Проверяем, существует ли пользователь с такими данными в базе данных
        if self.check_user_credentials(username, password):
            # Закрываем окно входа
            self.master.destroy()

            # Открываем главное окно приложения
            root = tk.Tk()
            MainApp(root, username)
            root.mainloop()
        else:
            messagebox.showinfo("Invalid Credentials", "Incorrect username or password.")

    def check_user_credentials(self, username, password):
        # Создаем подключение к базе данных
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()

        # Выполняем запрос к базе данных
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        # Закрываем соединение
        conn.close()

        return user is not None

    def show_registration_window(self):
        # Закрываем окно входа
        self.master.destroy()

        # Открываем окно регистрации
        registration_window = tk.Tk()
        RegistrationWindow(registration_window)

class MainApp:
    def __init__(self, master, username):
        self.master = master
        self.master.title("Main App")
        self.master.geometry("400x300")
        self.username = username

        # Добавляем переменные для цели и времени выполнения
        self.goal_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text=f"Main App - Welcome, {self.username}!")
        self.label.pack(pady=10)

        # Добавляем текстовое поле для ввода цели
        self.goal_label = tk.Label(self.master, text="Set your goal:")
        self.goal_label.pack()
        self.goal_entry = tk.Entry(self.master, textvariable=self.goal_var)
        self.goal_entry.pack()

        # Добавляем текстовое поле для ввода времени выполнения
        self.end_date_label = tk.Label(self.master, text="Set the end date (format: dd.mm.yyyy):")
        self.end_date_label.pack()
        self.end_date_entry = tk.Entry(self.master, textvariable=self.end_date_var)
        self.end_date_entry.pack()

        # Добавляем кнопку для установки цели и времени выполнения
        self.set_goal_button = tk.Button(self.master, text="Set Goal", command=self.set_goal)
        self.set_goal_button.pack(pady=10)

        # Добавляем кнопку для перехода к окну покупки подписки
        self.purchase_button = tk.Button(self.master, text="Purchase Subscription", command=self.show_purchase_window)
        self.purchase_button.pack(pady=10)

    def set_goal(self):
        goal = self.goal_var.get()
        end_date = self.end_date_var.get()

        # Проверяем, что цель и дата введены
        if goal and end_date:
            # Обработка логики установки цели и времени выполнения
            # Здесь вы можете добавить логику сохранения данных в базе данных или другие действия

            # Пример: выводим сообщение
            messagebox.showinfo("Goal Set", f"Goal: {goal}\nEnd Date: {end_date}")
        else:
            messagebox.showinfo("Invalid Input", "Please enter both goal and end date.")

    def show_purchase_window(self):
        # Открываем окно покупки подписки
        purchase_window = tk.Toplevel(self.master)
        PurchaseSubscriptionWindow(purchase_window)

class PurchaseSubscriptionWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Попкупка подписки")
        self.master.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Покупка подписки")
        self.label.pack(pady=10)

        self.card_number_label = tk.Label(self.master, text="Введите вашу карту (16 цифр):")
        self.card_number_label.pack()
        self.card_number_entry = tk.Entry(self.master, show="*")
        self.card_number_entry.pack()

        self.cvv_label = tk.Label(self.master, text="Введите CVV (3 цифр):")
        self.cvv_label.pack()
        self.cvv_entry = tk.Entry(self.master, show="*")
        self.cvv_entry.pack()

        self.purchase_button = tk.Button(self.master, text="Purchase", command=self.purchase_subscription)
        self.purchase_button.pack(pady=10)

    def purchase_subscription(self):
        card_number = self.card_number_entry.get()
        cvv = self.cvv_entry.get()

        # Проверяем, что введены корректные данные
        if len(card_number) == 16 and card_number.isdigit() and len(cvv) == 3 and cvv.isdigit():
            # Обработка логики покупки подписки
            # Здесь вы можете добавить логику сохранения данных в базе данных или другие действия

            # Пример: выводим сообщение
            messagebox.showinfo("Purchase Successful", "Subscription purchased successfully!")
        else:
            messagebox.showinfo("Invalid Input", "Please enter valid card number and CVV.")

if __name__ == "__main__":
    root = tk.Tk()
    login_window = LoginWindow(root)
    root.mainloop()
