import os
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import re
from datetime import datetime

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

        self.have_account_button = tk.Button(self.master, text="Нет аккаунта? Зарегистрируйтесь здесь", command=self.show_registration_window)
        self.have_account_button.pack(pady=5)

    def login_user(self):
        usermail = self.usermail_entry.get()
        password = self.password_entry.get()

        if self.registration_window and self.registration_window.user_exists(usermail) and self.check_user_password(usermail, password):
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
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM users WHERE usermail=? AND password=?", (usermail, hashed_password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def show_registration_window(self):
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

        if self.user_exists(usermail):
            messagebox.showinfo("Ошибка", "Пользователь с таким логином уже зарегистрирован.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.save_user_data(usermail, hashed_password, "some_phone_number")
        messagebox.showinfo("Успешно", "Регистрация успешна.")
        self.master.destroy()
        root = tk.Tk()
        MainApp(root, usermail, [])
        root.mainloop()

    def user_exists(self, usermail):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE usermail=?", (usermail,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def save_user_data(self, usermail, password, phone):
        try:
            conn = sqlite3.connect("user_data.db")
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   usermail TEXT,
                   password TEXT,
                   ''')

            conn.commit()
            cursor.execute("INSERT INTO users (usermail, password, phone) VALUES (?, ?, ?)", (usermail, password, phone))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при работе с базой данных: {e}")
        finally:
            if conn:
                conn.close()

    def show_authorization_window(self):
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

        if not re.match(r'\d{2}.\d{2}.\d{4}', end_date):
            messagebox.showinfo("Неверный ввод данных", "Пожалуйста введите дату окончания цели в формате дд.мм.гггг.")
            return

        if goal and end_date:
            self.save_goal_data(goal, end_date)
            self.update_current_goal_label(goal)
            messagebox.showinfo("Цель: ", f"Цель: {goal}\nДата окончания: {end_date}")
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
        self.delete_goal_button.config(state=tk.NORMAL, command=lambda: self.delete_goal(goal))
    
    def delete_goal(self, goal):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE usermail=? AND goal=?", (self.usermail, goal))
        conn.commit()
        conn.close()

        self.current_goal_label.config(text="Ваша текущая цель: Нет цели")
        self.delete_goal_button.config(state=tk.DISABLED)
        self.num_goals_added -= 1
    
    def show_purchase_window(self):
        purchase_window = tk.Toplevel(self.master)
        purchase_window.title("Покупка подписки")
        PurchaseSubscriptionWindow(purchase_window, self).create_widgets()
    
    def update_after_purchase(self):
        self.num_goals_limit = 5
        self.purchase_button.pack(pady=10)

    def set_goal(self):
        goal = self.goal_var.get()
        end_date = self.end_date_var.get()

        if goal and end_date:
            self.save_goal_data(goal, end_date)
            self.update_current_goal_label(goal)
            messagebox.showinfo("Цель: ", f"Цель: {goal}\nДата окончания: {end_date}")
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
        self.delete_goal_button.config(state=tk.NORMAL, command=lambda: self.delete_goal(goal))
    
    def delete_goal(self, goal):
        conn = sqlite3.connect("user_data.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE usermail=? AND goal=?", (self.usermail, goal))
        conn.commit()
        conn.close()

        self.current_goal_label.config(text="Ваша текущая цель: Нет цели")
        self.delete_goal_button.config(state=tk.DISABLED)
        self.num_goals_added -= 1
    
    def show_purchase_window(self):
        purchase_window = tk.Toplevel(self.master)
        purchase_window.title("Покупка подписки")
        PurchaseSubscriptionWindow(purchase_window, self).create_widgets()

class PurchaseSubscriptionWindow:
    def __init__(self, master, main_app):
        self.master = master
        self.master.title("Покупка подписки")
        self.main_app = main_app
        
    def create_widgets(self):
        self.label = tk.Label(self.master, text="Купите подписку для получения дополнительных функций.")
        self.label.pack(pady=10)
        
        self.purchase_button = tk.Button(self.master, text="Купить подписку", command=self.purchase_subscription)
        self.purchase_button.pack(pady=10)
        
        self.close_button = tk.Button(self.master, text="Закрыть", command=self.master.destroy)
        self.close_button.pack(pady=5)
        
    def purchase_subscription(self):
        # Здесь может быть логика для покупки подписки
        # После успешной покупки вызываем метод update_after_purchase() главного приложения
        self.main_app.update_after_purchase()
        messagebox.showinfo("Успешно", "Подписка успешно куплена.")
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    authorization_window = AuthorizationWindow(root, None)
    root.mainloop()