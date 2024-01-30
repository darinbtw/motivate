import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import sqlite3
import threading

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
        self.login_window.geometry("300x150")

        # Hide registration window
        self.root.withdraw()

        self.login_email_label = ttk.Label(self.login_window, text="Email:")
        self.login_email_entry = ttk.Entry(self.login_window)
        self.login_password_label = ttk.Label(self.login_window, text="Password:")
        self.login_password_entry = ttk.Entry(self.login_window, show="*")

        self.login_submit_button = ttk.Button(self.login_window, text="Login", command=self.login)
        self.return_button = ttk.Button(self.login_window, text="Return to Registration", command=self.return_to_registration)

        self.login_email_label.grid(row=0, column=0, padx=10, pady=5)
        self.login_email_entry.grid(row=0, column=1, padx=10, pady=5)
        self.login_password_label.grid(row=1, column=0, padx=10, pady=5)
        self.login_password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.login_submit_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        self.return_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")

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
        self.profile_window.geometry("400x300")

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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.run()
