import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import student_system as s_system


class LoginSignupSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Signup System")
        self.root.geometry("300x200")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.username_label = tk.Label(root, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root, textvariable=self.username_var)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, textvariable=self.password_var, show="*")
        self.password_entry.pack()

        self.login_btn = tk.Button(root, text="Login", command=self.login)
        self.login_btn.pack()

        self.signup_btn = tk.Button(root, text="Signup", command=self.signup)
        self.signup_btn.pack()

        self.connection = self.connect_to_database()

    def connect_to_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Rahul@5111"
            )
            print("Connected to MySQL")

            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS student_management_system")
            cursor.execute("USE student_management_system")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)

            return connection

        except Error as e:
            print("Error connecting to MySQL:", e)
            messagebox.showerror("Error", "Failed to connect to MySQL")
            return None

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username and password are required fields")
        else:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                user = cursor.fetchone()

                if user:
                    messagebox.showinfo("Success", "Login successful")
                    self.root.destroy()
                    # Call the function to open the student management system
                    print("Initialising Database Portal")
                    s_system.open_student_system()
                else:
                    messagebox.showerror("Error", "Invalid username or password")

            except Error as e:
                print("Error occurred while logging in:", e)
                messagebox.showerror("Error", "Failed to login")

    def signup(self):
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_btn.pack_forget()
        self.signup_btn.pack_forget()

        self.signup_username_label = tk.Label(self.root, text="Username:")
        self.signup_username_label.pack()
        self.signup_username_entry = tk.Entry(self.root, textvariable=self.username_var)
        self.signup_username_entry.pack()

        self.signup_password_label = tk.Label(self.root, text="Password:")
        self.signup_password_label.pack()
        self.signup_password_entry = tk.Entry(self.root, textvariable=self.password_var, show="*")
        self.signup_password_entry.pack()

        self.signup_confirm_btn = tk.Button(self.root, text="Signup", command=self.confirm_signup)
        self.signup_confirm_btn.pack()

    def confirm_signup(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "Username and password are required fields")
        else:
            try:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                self.connection.commit()
                messagebox.showinfo("Success", "Signup successful")

                self.signup_username_label.pack_forget()
                self.signup_username_entry.pack_forget()
                self.signup_password_label.pack_forget()
                self.signup_password_entry.pack_forget()
                self.signup_confirm_btn.pack_forget()

                self.username_label.pack()
                self.username_entry.pack()
                self.password_label.pack()
                self.password_entry.pack()
                self.login_btn.pack()
                self.signup_btn.pack()

            except Error as e:
                print("Error occurred while signing up:", e)
                messagebox.showerror("Error", "Failed to signup")




def open_login_signup_system():
    root = tk.Tk()
    obj = LoginSignupSystem(root)
    root.mainloop()


