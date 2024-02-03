import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
import re  # Для работы с регулярными выражениями

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Darin - Motivatli")
        self.root.geometry("270x250")
        self.root.resizable(width=False, height=False)

        # Connect to database
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

    def show_login_window(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Авторизация")
        self.login_window.geometry("400x200")
        self.login_window.resizable(width=False, height=False)

        # Hide registration window
        self.root.withdraw()

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

    def return_to_registration(self):
        self.login_window.withdraw()
        self.root.deiconify()

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
                self.cursor.execute("INSERT INTO users (email, password, name, secret_question, secret_answer) VALUES (?, ?, ?, ?, ?)", (email, password, name, secret_question, secret_answer))
                self.conn.commit()
                messagebox.showinfo("Успешно", "Регистрация успешно пройдена!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Пользователь с такой почтой уже зарегистрирован.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста введите корректные данные.")

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
        self.cursor.execute("SELECT id, description, deadline FROM goals WHERE user_id = ?", (self.user[0],))
        goals = self.cursor.fetchall()
        for goal in goals:
            id, description, deadline = goal
            self.listbox.insert(tk.END, f"{id} - {description} - {deadline}")

    def add_goal(self):
        # Проверяем, не превысил ли пользователь лимит на количество целей
        description = simpledialog.askstring("Добавить цель", "Введите что нужно сделать для вашей цели:")
        deadline = simpledialog.askstring("Добавить цель", "Введите дату окончания (YYYY-MM-DD):")
        if description and deadline:
            try:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                self.cursor.execute("INSERT INTO goals (description, deadline, user_id) VALUES (?, ?, ?)", (description, deadline_date, self.user[0]))
                self.conn.commit()

                # Обновляем лимит целей для пользователя
                self.cursor.execute("UPDATE users SET goal_limit = goal_limit + 1 WHERE id = ?", (self.user[0],))
                self.conn.commit()

                messagebox.showinfo("Успешно", "Ваша цель была добавлена!")
                self.load_goals()
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат срока окончания. Пожалуйста, используйте ГГГГ-ММ-ДД.")
        else:
            messagebox.showerror("Ошибка", "Пожалуйста введите корректные данные.")
            
        self.cursor.execute("SELECT goal_limit FROM users WHERE id = ?", (self.user[0],))
        limit = self.cursor.fetchone()[0]
        if limit is not None and limit >= 2:
            messagebox.showerror("Ошибка", "Вы уже создали максимальное количество целей.")
            return

    def delete_goal(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            goal_id = self.listbox.get(selected_item).split(" - ")[0]
            self.cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
            self.conn.commit()
            messagebox.showinfo("Успешно", "Ваша цель удаленна!")
            self.load_goals()
        else:
            messagebox.showerror("Ошибка", "Пожалуйста, выберете цель для удаления ")

    def logout(self):
        self.profile_window.destroy()
        self.root.deiconify()
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Вы вышли", "Выход из аккаунта успешнно выполнен")

    def add_card_details(self):
        card_window = tk.Toplevel(self.profile_window)
        card_window.title("Оплата подписки")
        card_window.geometry("400x150")
        card_window.resizable(width=False, height=False)

        card_number_label = ttk.Label(card_window, text="16-ти значный номер карты:")
        card_number_entry = ttk.Entry(card_window)
        expiration_date_label = ttk.Label(card_window, text="Срок действия карты (MM/YY):")
        expiration_date_entry = ttk.Entry(card_window)
        cvv_label = ttk.Label(card_window, text="Код CVV:")
        cvv_entry = ttk.Entry(card_window)

        card_number_label.grid(row=0, column=0, padx=10, pady=5)
        card_number_entry.grid(row=0, column=1, padx=10, pady=5)
        expiration_date_label.grid(row=1, column=0, padx=10, pady=5)
        expiration_date_entry.grid(row=1, column=1, padx=10, pady=5)
        cvv_label.grid(row=2, column=0, padx=10, pady=5)
        cvv_entry.grid(row=2, column=1, padx=10, pady=5)

        save_button = ttk.Button(card_window, text="Купить", command=lambda: self.save_card_details(card_window, card_number_entry.get(), expiration_date_entry.get(), cvv_entry.get()))
        save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        self.cursor.execute("UPDATE users SET goal_limit = 10 WHERE id = ?", (self.user[0],))
        self.conn.commit()
        
        messagebox.showinfo("Успешно", "Покупка совершена! Теперь вы можете создавать до 10 целей.")

    def save_card_details(self, window, card_number, expiration_date, cvv):
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
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
