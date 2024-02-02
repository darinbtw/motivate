import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Motivation App")
        self.root.geometry("600x400")

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
                                    secret_answer TEXT
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
        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_entry = ttk.Entry(self.root, show="*")
        self.name_label = ttk.Label(self.root, text="Name:")
        self.name_entry = ttk.Entry(self.root)
        self.secret_question_label = ttk.Label(self.root, text="Secret Question:")
        self.secret_question_entry = ttk.Entry(self.root)
        self.secret_answer_label = ttk.Label(self.root, text="Secret Answer:")
        self.secret_answer_entry = ttk.Entry(self.root)

        self.register_button = ttk.Button(self.root, text="Register", command=self.register)
        self.login_button = ttk.Button(self.root, text="Login", command=self.show_login_window)

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
        self.login_window.title("Login")
        self.login_window.geometry("400x200")

        # Hide registration window
        self.root.withdraw()

        self.login_email_label = ttk.Label(self.login_window, text="Email:")
        self.login_email_entry = ttk.Entry(self.login_window)
        self.login_password_label = ttk.Label(self.login_window, text="Password:")
        self.login_password_entry = ttk.Entry(self.login_window, show="*")

        self.login_submit_button = ttk.Button(self.login_window, text="Login", command=self.login)
        self.forgot_password_button = ttk.Button(self.login_window, text="Forgot Password?", command=self.forgot_password)
        self.return_button = ttk.Button(self.login_window, text="Return to Registration", command=self.return_to_registration)

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
        self.forgot_password_window.title("Forgot Password")
        self.forgot_password_window.geometry("300x150")

        self.forgot_email_label = ttk.Label(self.forgot_password_window, text="Email:")
        self.forgot_email_entry = ttk.Entry(self.forgot_password_window)
        self.forgot_name_label = ttk.Label(self.forgot_password_window, text="Name:")
        self.forgot_name_entry = ttk.Entry(self.forgot_password_window)
        self.forgot_question_label = ttk.Label(self.forgot_password_window, text="Secret Question:")
        self.forgot_question_entry = ttk.Entry(self.forgot_password_window)

        self.forgot_submit_button = ttk.Button(self.forgot_password_window, text="Submit", command=self.check_secret_answer)

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
                secret_answer = simpledialog.askstring("Secret Answer", "Enter your secret answer:")
                if secret_answer == user[5]:
                    messagebox.showinfo("Success", f"Your password is: {user[2]}")
                    self.forgot_password_window.destroy()
                else:
                    messagebox.showerror("Error", "Incorrect secret answer.")
            else:
                messagebox.showerror("Error", "User not found.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def return_to_registration(self):
        self.login_window.withdraw()
        self.root.deiconify()

    def register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        secret_question = self.secret_question_entry.get()
        secret_answer = self.secret_answer_entry.get()

        if email and password and name and secret_question and secret_answer:
            try:
                self.cursor.execute("INSERT INTO users (email, password, name, secret_question, secret_answer) VALUES (?, ?, ?, ?, ?)", (email, password, name, secret_question, secret_answer))
                self.conn.commit()
                messagebox.showinfo("Success", "Registration successful!")
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "User with this email already exists.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def login(self):
        email = self.login_email_entry.get()
        password = self.login_password_entry.get()

        if email and password:
            self.cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
            user = self.cursor.fetchone()
            if user:
                messagebox.showinfo("Success", f"Welcome back, {user[3]}!")
                self.show_profile_window(user)
            else:
                messagebox.showerror("Error", "Invalid email/password combination.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def show_profile_window(self, user):
        self.profile_window = tk.Toplevel(self.root)
        self.profile_window.title("Profile")
        self.profile_window.geometry("470x425")

        # Hide both registration and login windows
        self.root.withdraw()
        self.login_window.withdraw()

        self.user = user

        self.welcome_label = ttk.Label(self.profile_window, text=f"Welcome, {self.user[3]}!")
        self.welcome_label.pack(pady=10)

        self.goals_label = ttk.Label(self.profile_window, text="Your Goals:")
        self.goals_label.pack()

        self.listbox = tk.Listbox(self.profile_window, width=50)
        self.listbox.pack(pady=5)

        self.load_goals()

        self.add_goal_button = ttk.Button(self.profile_window, text="Add Goal", command=self.add_goal)
        self.add_goal_button.pack(pady=5)

        self.delete_goal_button = ttk.Button(self.profile_window, text="Delete Selected Goal", command=self.delete_goal)
        self.delete_goal_button.pack(pady=5)

        self.logout_button = ttk.Button(self.profile_window, text="Logout", command=self.logout)
        self.logout_button.pack(pady=5)

        self.add_card_details_button = ttk.Button(self.profile_window, text="Add Card Details", command=self.add_card_details)
        self.add_card_details_button.pack(pady=5)

    def load_goals(self):
        self.listbox.delete(0, tk.END)
        self.cursor.execute("SELECT id, description, deadline FROM goals WHERE user_id = ?", (self.user[0],))
        goals = self.cursor.fetchall()
        for goal in goals:
            id, description, deadline = goal
            self.listbox.insert(tk.END, f"{id} - {description} - {deadline}")

    def add_goal(self):
        description = simpledialog.askstring("Add Goal", "Enter goal description:")
        deadline = simpledialog.askstring("Add Goal", "Enter deadline (YYYY-MM-DD):")
        if description and deadline:
            try:
                deadline_date = datetime.strptime(deadline, '%Y-%m-%d')
                self.cursor.execute("INSERT INTO goals (description, deadline, user_id) VALUES (?, ?, ?)", (description, deadline_date, self.user[0]))
                self.conn.commit()
                messagebox.showinfo("Success", "Goal added successfully!")
                self.load_goals()
            except ValueError:
                messagebox.showerror("Error", "Invalid deadline format. Please use YYYY-MM-DD.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def delete_goal(self):
        selected_item = self.listbox.curselection()
        if selected_item:
            goal_id = self.listbox.get(selected_item).split(" - ")[0]
            self.cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Goal deleted successfully!")
            self.load_goals()
        else:
            messagebox.showerror("Error", "Please select a goal to delete.")

    def logout(self):
        self.profile_window.destroy()
        self.root.deiconify()
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        messagebox.showinfo("Logout", "Logged out successfully!")

    def add_card_details(self):
        card_window = tk.Toplevel(self.profile_window)
        card_window.title("Add Card Details")
        card_window.geometry("300x200")

        card_number_label = ttk.Label(card_window, text="Card Number:")
        card_number_entry = ttk.Entry(card_window)
        expiration_date_label = ttk.Label(card_window, text="Expiration Date (MM/YY):")
        expiration_date_entry = ttk.Entry(card_window)
        cvv_label = ttk.Label(card_window, text="CVV:")
        cvv_entry = ttk.Entry(card_window)

        card_number_label.grid(row=0, column=0, padx=10, pady=5)
        card_number_entry.grid(row=0, column=1, padx=10, pady=5)
        expiration_date_label.grid(row=1, column=0, padx=10, pady=5)
        expiration_date_entry.grid(row=1, column=1, padx=10, pady=5)
        cvv_label.grid(row=2, column=0, padx=10, pady=5)
        cvv_entry.grid(row=2, column=1, padx=10, pady=5)

        save_button = ttk.Button(card_window, text="Save", command=lambda: self.save_card_details(card_window, card_number_entry.get(), expiration_date_entry.get(), cvv_entry.get()))
        save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

    def save_card_details(self, window, card_number, expiration_date, cvv):
        if len(card_number) != 16:
            messagebox.showerror("Error", "Card number must be 16 digits.")
            return
        if len(expiration_date) != 5 or expiration_date[2] != '/':
            messagebox.showerror("Error", "Expiration date must be in format MM/YY.")
            return
        if len(cvv) != 3:
            messagebox.showerror("Error", "CVV must be 3 digits.")
            return

        try:
            expiration_month, expiration_year = expiration_date.split('/')
            expiration_month = int(expiration_month)
            expiration_year = int(expiration_year)
            cvv = int(cvv)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for expiration date or CVV.")
            return

        if expiration_month < 1 or expiration_month > 12 or expiration_year < 0:
            messagebox.showerror("Error", "Invalid expiration date.")
            return

        self.cursor.execute("INSERT INTO card_details (card_number, expiration_date, cvv, user_id) VALUES (?, ?, ?, ?)",
                            (card_number, expiration_date, cvv, self.user[0]))
        self.conn.commit()
        messagebox.showinfo("Success", "Card details saved successfully!")
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
