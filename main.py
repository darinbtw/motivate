import os
import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string

class AuthorizationWindow:
    def __init__(self, master, registration_window):
        self.master = master
        self.master.title("Авторизация")
        self.master.geometry("400x200")
        self.registration_window = registration_window
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Авторизация")
        self.label.pack(pady=10)

        self.usermail_label = tk.Label(self.master, text="Логин:")
        self.usermail_label.pack()
        self.usermail_entry = tk.Entry(self.master)
        self.usermail_entry.pack()

        self.password_label = tk.Label(self.master, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.master, text="Войти", command=self.login_user)
        self.login_button.pack(pady=10)

        self.have_account_button = tk.Button(self.master, text="Нет аккаунта? Зарегестрируйтесь здесь", command=self.show_registration_window)
        self.have_account_button.pack(pady=5)

    def login_user(self):
        usermail = self.usermail_entry.get()
        password = self.password_entry.get()

        if self.registration_window.user_exists(usermail) and self.check_user_password(usermail, password):
            messagebox.showinfo("Успешно", "Вход выполнен успешно.")
            self.master.destroy()
            root = tk.Tk()
            user_goals = self.load_user_goals(usermail)
            MainApp(root, usermail, user_goals)
            root.mainloop()
        else:
            messagebox.showinfo("Ошибка", "Неверная почта или пароль.")

    def load_user_goals(self, usermail):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM goals WHERE usermail=?", (usermail,))
        goals = cursor.fetchall()
        conn.close()
        return goals

    def check_user_password(self, usermail, password):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE usermail=? AND password=?", (usermail, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def show_registration_window(self):
        # При нажатии кнопки "Есть аккаунт? Авторизуйтесь здесь" открываем окно регистрации
        self.master.destroy()
        root = tk.Tk()
        RegistrationWindow(root)
        root.mainloop()


class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Регистрация")
        self.master.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Регистрация")
        self.label.pack(pady=10)

        self.usermail_label = tk.Label(self.master, text="Логин:")
        self.usermail_label.pack()
        self.usermail_entry = tk.Entry(self.master)
        self.usermail_entry.pack()

        self.password_label = tk.Label(self.master, text="Пароль:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self.master, text="Зарегистрироваться", command=self.register_user)
        self.register_button.pack(pady=10)

        self.have_account_button = tk.Button(self.master, text="Есть аккаунт? Авторизуйтесь здесь", command=self.show_authorization_window)
        self.have_account_button.pack(pady=5)

    def register_user(self):
        usermail = self.usermail_entry.get()
        password = self.password_entry.get()

        # Проверяем, существует ли пользователь с таким же логином
        if self.user_exists(usermail):
            messagebox.showinfo("Ошибка", "Пользователь с таким логином уже зарегистрирован.")
            return

        # Сохраняем пользователя в базе данных
        self.save_user_data(usermail, password, "some_phone_number")  # Замените на свои данные
        messagebox.showinfo("Успешно", "Регистрация успешна.")
        self.master.destroy()
        root = tk.Tk()
        MainApp(root, usermail)
        root.mainloop()

    def user_exists(self, usermail):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE usermail=?", (usermail,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def save_user_data(self, usermail, password, phone):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           usermail TEXT,
                           password TEXT,
                           phone TEXT)''')
        conn.commit()
        cursor.execute("INSERT INTO users (usermail, password, phone) VALUES (?, ?, ?)", (usermail, password, phone))
        conn.commit()
        conn.close()

    def show_authorization_window(self):
        # При нажатии кнопки "Есть аккаунт? Авторизуйтесь здесь" открываем окно авторизации
        self.master.destroy()
        root = tk.Tk()
        AuthorizationWindow(root, self)
        root.mainloop()

class MainApp:
    def __init__(self, master, usermail, user_goals):
        self.master = master
        self.master.title("Меню")
        self.master.geometry("400x300")
        self.usermail = usermail

        self.num_goals_limit = 2
        self.num_goals_added = len(user_goals)

        self.create_widgets()

        if user_goals:
            first_goal = user_goals[0]
            self.update_current_goal_label(first_goal[2])

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text=f"Меню - Добро пожаловать!, {self.usermail}!")
        self.label.pack(pady=10)

        self.goal_var = tk.StringVar()
        self.end_date_var = tk.StringVar()

        self.goal_label = tk.Label(self.master, text="Поставьте свою цель:")
        self.goal_label.pack()
        self.goal_entry = tk.Entry(self.master, textvariable=self.goal_var)
        self.goal_entry.pack()

        self.end_date_label = tk.Label(self.master, text="Поставить срок оканчания цели (Формат: дд.мм.гггг):")
        self.end_date_label.pack()
        self.end_date_entry = tk.Entry(self.master, textvariable=self.end_date_var)
        self.end_date_entry.pack()

        self.set_goal_button = tk.Button(self.master, text="Поставить цель", command=self.set_goal)
        self.set_goal_button.pack(pady=10)

        self.purchase_button = tk.Button(self.master, text="Купить подписку", command=self.show_purchase_window)
        self.purchase_button.pack(pady=10)
        
        self.current_goal_label = tk.Label(self.master, text="Ваша текущая цель: Нет цели")
        self.current_goal_label.pack(side=tk.TOP, padx=10, pady=5)
        
        self.delete_goal_button = tk.Button(self.master, text="Удалить цель", command=self.delete_goal)
        self.delete_goal_button.pack(side=tk.TOP, padx=10, pady=5)

        if self.num_goals_added < self.num_goals_limit:
            self.add_goal_button = tk.Button(self.master, text="Добавить цель", command=self.add_goal)
            self.add_goal_button.pack(pady=10)

    def set_goal(self):
        goal = self.goal_var.get()
        end_date = self.end_date_var.get()

        if goal and end_date:
            self.save_goal_data(goal, end_date)
            self.update_current_goal_label(goal)  # Обновляем отображение текущей цели
            messagebox.showinfo("Цель: ", f"Цель: {goal}\nДата оканчания: {end_date}")
        else:
            messagebox.showinfo("Неверный ввод данных", "Пожалуйста введите правильные значения.")

    def add_goal(self):
        goal = self.goal_var.get()
        end_date = self.end_date_var.get()

        if goal and end_date:
            if self.num_goals_added < self.num_goals_limit:
                self.save_goal_data(goal, end_date)
                messagebox.showinfo("Цель добавлена", f"Цель: {goal}\nДата оканчания: {end_date}")
                self.num_goals_added += 1
            else:
                messagebox.showinfo("Лимит целей", "У вас достигнут лимит целей. Купите подписку для добавления больше целей.")
        else:
            messagebox.showinfo("Неверный ввод данных", "Пожалуйста введите верные значения.")

    def save_goal_data(self, goal, end_date):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS goals 
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           usermail TEXT,
                           goal TEXT,
                           end_date TEXT)''')
        conn.commit()
        cursor.execute("INSERT INTO goals (usermail, goal, end_date) VALUES (?, ?, ?)", (self.usermail, goal, end_date))
        conn.commit()
        conn.close()
    
    def update_current_goal_label(self, goal):
        self.current_goal_label.config(text=f"Ваша текущая цель: {goal}")
        self.delete_goal_button.config(state=tk.NORMAL, command=lambda: self.delete_goal(goal))

        # Добавляем кнопку для удаления цели
        self.delete_goal_button.config(state=tk.NORMAL, command=lambda: self.delete_goal(goal))
    def delete_goal(self, goal):
        # Пример SQL-запроса для удаления цели
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE usermail=? AND goal=?", (self.usermail, goal))
        conn.commit()
        conn.close()

        self.current_goal_label.config(text="Ваша текущая цель: Нет цели")
        self.delete_goal_button.config(state=tk.DISABLED)  # Делаем кнопку недоступной
        self.num_goals_added -= 1
    
    def show_purchase_window(self):
        purchase_window = tk.Toplevel(self.master)
        purchase_window.title("Покупка подписки")
        PurchaseSubscriptionWindow(purchase_window, self).create_widgets()
    
    def update_after_purchase(self):
        # Добавьте здесь логику для обновления данных после успешной покупки
        # Например, изменение лимита целей или что-то еще
        self.num_goals_limit = 5  # Пример: увеличиваем лимит целей после покупки

class PurchaseSubscriptionWindow:
    def __init__(self, master, main_app):
        self.master = master
        self.master.title("Покупка подписки")
        self.master.geometry("400x200")
        self.main_app = main_app  # Сохраняем ссылку на главное приложение

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Покупка подписки")
        self.label.pack(pady=10)

        self.card_number_label = tk.Label(self.master, text="Введите вашу карту (16 цифр):")
        self.card_number_label.pack()
        self.card_number_entry = tk.Entry(self.master, show="*")
        self.card_number_entry.pack()

        self.cvv_label = tk.Label(self.master, text="Введите CVV (3 цифры):")
        self.cvv_label.pack()
        self.cvv_entry = tk.Entry(self.master, show="*")
        self.cvv_entry.pack()

        self.purchase_button = tk.Button(self.master, text="Купить", command=self.purchase_subscription)
        self.purchase_button.pack(pady=10)

    def purchase_subscription(self):
        card_number = self.card_number_entry.get()
        cvv = self.cvv_entry.get()

        if len(card_number) == 16 and card_number.isdigit() and len(cvv) == 3 and cvv.isdigit():
            messagebox.showinfo("Покупка совершена успешно", "Подписка успешно куплена!")
            # Добавьте здесь логику обработки успешной покупки
            # Например, обновление данных в базе данных или что-то еще
            self.main_app.update_after_purchase()  # Вызываем метод для обновления данных в главном приложении
            self.master.destroy()
        else:
            messagebox.showinfo("Неверный ввод данных", "Пожалуйста введите верные данные карты.")
        
root = tk.Tk()
AuthorizationWindow(root, None)
root.mainloop()
