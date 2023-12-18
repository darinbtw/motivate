import tkinter as tk
from tkinter import messagebox
import sqlite3
import smtplib
import random
from email.mime.text import MIMEText

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

        self.verify_code_label = tk.Label(self.master, text="Введите код подтверждения:")
        self.verify_code_label.pack()
        self.verify_code_entry = tk.Entry(self.master)
        self.verify_code_entry.pack()

        self.get_code_button = tk.Button(self.master, text="Получить код", command=self.send_verification_email)
        self.get_code_button.pack(pady=10)

        self.verify_button = tk.Button(self.master, text="Подтвердить", command=self.verify_email, state=tk.DISABLED)
        self.verify_button.pack(pady=10)

    def send_verification_email(self):
        usermail = self.usermail_entry.get()
        if not usermail:
            messagebox.showinfo("Ошибка", "Пожалуйста, введите вашу почту.")
            return

        self.verification_code = self.generate_verification_code()
        self.send_email(usermail, self.verification_code)
        messagebox.showinfo("Успешно", "Код подтверждения отправлен на вашу почту.")
        self.verify_button.config(state=tk.NORMAL)

    def generate_verification_code(self):
        return str(random.randint(100000, 999999))

    def send_email(self, usermail, verification_code):
        sender_email = "artemdenisovichdn4@gmail.com"  # Замените на вашу почту
        sender_password = "Xi5-P2Z-ezV-gAX"  # Замените на ваш пароль

        subject = "Код подтверждения регистрации"
        body = f"Ваш код подтверждения: {verification_code}"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = usermail

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, usermail, msg.as_string().encode('utf-8'))

    def verify_email(self):
        entered_code = self.verify_code_entry.get()
        if entered_code == self.verification_code:
            messagebox.showinfo("Успешно", "Почта успешно подтверждена.")
            # Теперь можно продолжить с регистрацией пользователя
        else:
            messagebox.showinfo("Неверный код", "Пожалуйста, введите правильный код подтверждения.")

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

    def open_main_app(self, usermail):
        self.master.destroy()
        root = tk.Tk()
        MainApp(root, usermail)
        root.mainloop()

class MainApp:
    def __init__(self, master, usermail):
        self.master = master
        self.master.title("Меню")
        self.master.geometry("400x300")
        self.usermail = usermail

        self.num_goals_limit = 2
        self.num_goals_added = 0

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

        # Добавляем кнопку для удаления цели
        self.delete_goal_button.config(state=tk.NORMAL, command=lambda: self.delete_goal(goal))

        
    def delete_goal(self, goal):
        # Добавьте здесь логику удаления цели из базы данных
        # Например, используйте SQL-запрос DELETE
        # Затем обновите отображение текущей цели и счетчик целей пользователя

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
        else:
            messagebox.showinfo("Неверный ввод данных", "Пожалуйста введите верные данные карты.")

if __name__ == "__main__":
    root = tk.Tk()
    login_window = RegistrationWindow(root)
    root.mainloop()
