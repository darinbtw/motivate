import tkinter as tk
from tkinter import messagebox
import phonenumbers
import random
import string

class RegistrationWindow:
    def __init__(self, master, app):
        self.master = master
        self.master.title("Registration")
        self.master.geometry("400x300")
        self.app = app

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Registration")
        self.label.pack(pady=10)

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master)
        self.username_entry.pack()

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.pack()

        self.phone_label = tk.Label(self.master, text="Phone:")
        self.phone_label.pack()
        self.phone_entry = tk.Entry(self.master)
        self.phone_entry.pack()

        self.register_button = tk.Button(self.master, text="Register", command=self.register)
        self.register_button.pack(pady=10)

    def validate_phone(self, phone):
        try:
            parsed_phone = phonenumbers.parse(phone, "RU")
            return phonenumbers.is_valid_number(parsed_phone)
        except phonenumbers.NumberParseException:
            return False

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        phone = self.phone_entry.get()

        if not self.validate_phone(phone):
            messagebox.showwarning("Error", "Invalid phone number format. Please enter a valid phone number.")
            return

        verification_code = ''.join(random.choice(string.digits) for _ in range(6))
        print(f"Verification Code for {phone}: {verification_code}")

        # Здесь можно реализовать отправку кода на телефон (например, через SMS)

        # Открываем новое окно для ввода кода подтверждения
        verify_window = tk.Toplevel(self.master)
        VerifyPhoneWindow(verify_window, self.app, phone)

        # Закрываем окно регистрации
        self.master.destroy()

class VerifyPhoneWindow:
    def __init__(self, master, app, phone):
        self.master = master
        self.master.title("Verify Phone")
        self.master.geometry("400x300")
        self.app = app
        self.phone = phone

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text=f"Verify Phone for {self.phone}")
        self.label.pack(pady=10)

        self.verify_code_label = tk.Label(self.master, text="Enter the verification code:")
        self.verify_code_label.pack()

        self.verify_code_entry = tk.Entry(self.master)
        self.verify_code_entry.pack()

        self.verify_button = tk.Button(self.master, text="Verify", command=self.verify)
        self.verify_button.pack(pady=10)

    def verify(self):
        entered_code = self.verify_code_entry.get()
        # Здесь можно реализовать проверку кода подтверждения
        # (например, сравнение с кодом, отправленным пользователю)

        # В данном примере просто выводим сообщение
        messagebox.showinfo("Verification", "Phone verified successfully!")

        # Закрываем окно подтверждения
        self.master.destroy()

        # Регистрация пользователя
        # (здесь можно добавить логику сохранения данных в базу данных)

        # Открываем новое окно после успешной регистрации
        self.app.open_dashboard()

class DashboardWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Меню мотивации")
        self.master.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Добро пожаловать в меню")
        self.label.pack()

        self.set_goal_button = tk.Button(self.master, text="Поставить цель", command=self.set_goal)
        self.set_goal_button.pack(pady=10)

        #self.set_input_goal = tk.Label(self.master, text=)

    def set_goal(self):
        # Здесь вы можете добавить логику установки цели
        # В данном примере, просто выводим сообщение
        messagebox.showinfo("Set Goal", "Goal set successfully!")

class MotivationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Motivation App")
        self.master.geometry("400x300")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Motivation App")
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

        self.register_button = tk.Button(self.master, text="Register", command=self.open_registration)
        self.register_button.pack(pady=10)

    def login(self):
        # Здесь вы можете добавить логику проверки логина и пароля в базе данных
        # В данном примере, просто открываем новое окно
        self.open_dashboard()

    def open_dashboard(self):
        self.dashboard_window = tk.Toplevel(self.master)
        DashboardWindow(self.dashboard_window)

    def open_registration(self):
        registration_window = tk.Toplevel(self.master)
        RegistrationWindow(registration_window, self)

if __name__ == "__main__":
    root = tk.Tk()
    app = MotivationApp(root)
    root.mainloop()
