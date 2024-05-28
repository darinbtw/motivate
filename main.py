import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import psycopg2
import psutil
import time
from datetime import datetime
import bcrypt
import logging

# Конфигурация базы данных
DB_NAME = "motivatly"
DB_USER = "postgres"
DB_PASS = "123srmax"
DB_HOST = "localhost"
DB_PORT = "5432"

# Настройка логирования
logging.basicConfig(filename='app.log', level=logging.INFO)

def log_event(message):
    logging.info(message)

class GoalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Goal Tracker")
        self.conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
        )
        self.user_id = None
        self.create_widgets()
        
    def create_widgets(self):
        self.username_label = ttk.Label(self.root, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        self.password_label = ttk.Label(self.root, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = ttk.Button(self.root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)

        self.register_button = ttk.Button(self.root, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2)

        self.goal_listbox = tk.Listbox(self.root)
        self.goal_listbox.grid(row=4, column=0, columnspan=2)

        self.goal_entry = ttk.Entry(self.root)
        self.goal_entry.grid(row=5, column=0)
        self.deadline_entry = ttk.Entry(self.root)
        self.deadline_entry.grid(row=5, column=1)

        self.add_goal_button = ttk.Button(self.root, text="Add Goal", command=self.add_goal)
        self.add_goal_button.grid(row=6, column=0, columnspan=2)

        self.edit_goal_button = ttk.Button(self.root, text="Edit Goal", command=self.edit_goal)
        self.edit_goal_button.grid(row=7, column=0, columnspan=2)

        self.delete_goal_button = ttk.Button(self.root, text="Delete Goal", command=self.delete_goal)
        self.delete_goal_button.grid(row=8, column=0, columnspan=2)

        self.mark_completed_button = ttk.Button(self.root, text="Mark Completed", command=self.mark_goal_completed)
        self.mark_completed_button.grid(row=9, column=0, columnspan=2)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        if not username or not password:
            log_event("Username and password are required for registration")
            return
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            self.conn.commit()
            cur.close()
            log_event(f"User registered: {username}")
        except psycopg2.Error as e:
            log_event(f"Database error during registration: {e}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode('utf-8')
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if user and bcrypt.checkpw(password, user[1].encode('utf-8')):
                self.user_id = user[0]
                self.load_goals()
                log_event(f"User logged in: {username}")
            else:
                log_event("Invalid credentials during login")
                messagebox.showerror("Login Error", "Invalid username or password")
            cur.close()
        except psycopg2.Error as e:
            log_event(f"Database error during login: {e}")

    def load_goals(self):
        self.goal_listbox.delete(0, tk.END)
        cur = self.conn.cursor()
        cur.execute("SELECT goal, deadline FROM goals WHERE user_id = %s", (self.user_id,))
        for goal, deadline in cur.fetchall():
            self.goal_listbox.insert(tk.END, f"{goal} - {deadline}")
        cur.close()

    def add_goal(self):
        goal = self.goal_entry.get()
        deadline = self.deadline_entry.get()
        if not goal or not deadline:
            log_event("Goal or deadline is missing")
            return
        deadline_dt = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO goals (user_id, goal, deadline) VALUES (%s, %s, %s)", (self.user_id, goal, deadline_dt))
            self.conn.commit()
            cur.close()
            self.load_goals()
            log_event(f"Goal added: {goal} - {deadline}")
        except psycopg2.Error as e:
            log_event(f"Database error during goal addition: {e}")

    def edit_goal(self):
        selected_goal_index = self.goal_listbox.curselection()
        if selected_goal_index:
            goal_text = self.goal_listbox.get(selected_goal_index)
            goal, deadline = goal_text.rsplit(' - ', 1)
            new_goal = self.goal_entry.get()
            new_deadline = self.deadline_entry.get()
            if not new_goal or not new_deadline:
                log_event("New goal or new deadline is missing")
                return
            deadline_dt = datetime.strptime(new_deadline, '%Y-%m-%d %H:%M:%S')
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE goals SET goal = %s, deadline = %s WHERE user_id = %s AND goal = %s AND deadline = %s",
                            (new_goal, deadline_dt, self.user_id, goal, deadline))
                self.conn.commit()
                cur.close()
                self.load_goals()
                log_event(f"Goal edited: {new_goal} - {new_deadline}")
            except psycopg2.Error as e:
                log_event(f"Database error during goal editing: {e}")

    def delete_goal(self):
        selected_goal_index = self.goal_listbox.curselection()
        if selected_goal_index:
            goal_text = self.goal_listbox.get(selected_goal_index)
            goal, deadline = goal_text.rsplit(' - ', 1)
            try:
                cur = self.conn.cursor()
                cur.execute("DELETE FROM goals WHERE user_id = %s AND goal = %s AND deadline = %s", (self.user_id, goal, deadline))
                self.conn.commit()
                cur.close()
                self.load_goals()
                log_event(f"Goal deleted: {goal} - {deadline}")
            except psycopg2.Error as e:
                log_event(f"Database error during goal deletion: {e}")

    def mark_goal_completed(self):
        selected_goal_index = self.goal_listbox.curselection()
        if selected_goal_index:
            goal_text = self.goal_listbox.get(selected_goal_index)
            goal, deadline = goal_text.rsplit(' - ', 1)
            try:
                cur = self.conn.cursor()
                cur.execute("UPDATE goals SET completed = TRUE WHERE user_id = %s AND goal = %s AND deadline = %s",
                            (self.user_id, goal, deadline))
                self.conn.commit()
                cur.close()
                self.load_goals()
                log_event(f"Goal marked as completed: {goal} - {deadline}")
            except psycopg2.Error as e:
                log_event(f"Database error during marking goal as completed: {e}")

    def notify_user(self, message):
        messagebox.showwarning("Notification", message)
        log_event(f"Notification sent to user: {message}")

    def monitor_goals(self):
        while True:
            cur = self.conn.cursor()
            cur.execute("SELECT goal, deadline FROM goals WHERE user_id = %s AND completed = FALSE", (self.user_id,))
            for goal, deadline in cur.fetchall():
                deadline_dt = datetime.strptime(deadline, '%Y-%m-%d %H:%M:%S')
                if datetime.now() > deadline_dt:
                    self.block_computer()
                elif (deadline_dt - datetime.now()).total_seconds() < 3600:  # Менее часа до дедлайна
                    self.notify_user(f"Goal '{goal}' is due in less than an hour!")
            cur.close()
            time.sleep(60)

    def block_computer(self):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] in ['chrome.exe', 'firefox.exe', 'msedge.exe']:
                psutil.Process(proc.info['pid']).terminate()
        log_event("Computer blocked for 5 minutes")
        time.sleep(300)  # Block for 5 minutes

# Создание окна приложения
root = ThemedTk(theme="arc")
app = GoalApp(root)

# Запуск мониторинга целей в отдельном потоке
import threading
monitor_thread = threading.Thread(target=app.monitor_goals)
monitor_thread.daemon = True
monitor_thread.start()

root.mainloop()
