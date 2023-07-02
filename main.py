import tkinter as tk
from tkinter import ttk, messagebox
from mysql.connector import connect, Error


class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#ffffff")

        # Set transparent background
        self.root.attributes("-transparentcolor", "#ffffff")

        # Database connection
        try:
            self.connection = connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="studentms"
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print("Error connecting to database:", e)
            messagebox.showerror("Error", "Failed to connect to database")

        # Login Page
        self.login_frame = tk.Frame(self.root, bg="#ffffff")
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        login_label = tk.Label(self.login_frame, text="Login", font=("Arial", 20, "bold"), bg="#ffffff")
        login_label.pack(pady=20)

        username_label = tk.Label(self.login_frame, text="Username:", font=("Arial", 14), bg="#ffffff")
        username_label.pack()
        self.username_entry = tk.Entry(self.login_frame, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.login_frame, text="Password:", font=("Arial", 14), bg="#ffffff")
        password_label.pack()
        self.password_entry = tk.Entry(self.login_frame, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="Login", font=("Arial", 14), command=self.login,
                                 bd=0, relief=tk.RAISED, bg="#2ecc71", fg="#ffffff", padx=10, pady=5)
        login_button.pack(pady=10)

        create_account_button = tk.Button(self.login_frame, text="Create New Account", font=("Arial", 12),
                                          command=self.show_signup_page, bd=0, relief=tk.RAISED, bg="#3498db",
                                          fg="#ffffff", padx=10, pady=5)
        create_account_button.pack()

        # Signup Page
        self.signup_frame = tk.Frame(self.root, bg="#ffffff")

        name_label = tk.Label(self.signup_frame, text="Name:", font=("Arial", 14), bg="#ffffff")
        name_label.pack()
        self.name_entry = tk.Entry(self.signup_frame, font=("Arial", 14))
        self.name_entry.pack(pady=5)

        signup_username_label = tk.Label(self.signup_frame, text="Username:", font=("Arial", 14), bg="#ffffff")
        signup_username_label.pack()
        self.signup_username_entry = tk.Entry(self.signup_frame, font=("Arial", 14))
        self.signup_username_entry.pack(pady=5)

        signup_password_label = tk.Label(self.signup_frame, text="Password:", font=("Arial", 14), bg="#ffffff")
        signup_password_label.pack()
        self.signup_password_entry = tk.Entry(self.signup_frame, show="*", font=("Arial", 14))
        self.signup_password_entry.pack(pady=5)

        signup_button = tk.Button(self.signup_frame, text="Signup", font=("Arial", 14), command=self.signup,
                                  bd=0, relief=tk.RAISED, bg="#2ecc71", fg="#ffffff", padx=10, pady=5)
        signup_button.pack(pady=10)

        go_to_login_button = tk.Button(self.signup_frame, text="Go to Login Page", font=("Arial", 12),
                                       command=self.show_login_page, bd=0, relief=tk.RAISED, bg="#3498db",
                                       fg="#ffffff", padx=10, pady=5)
        go_to_login_button.pack()

        self.show_login_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            self.cursor.execute("SELECT * FROM login_Cred WHERE username=%s AND password=%s", (username, password))
            user = self.cursor.fetchone()
            if user:
                messagebox.showinfo("Success", "Login Successful")
                self.clear_login_fields()
            else:
                messagebox.showerror("Error", "Invalid username or password")
        except Error as e:
            print("Error executing query:", e)
            messagebox.showerror("Error", "Failed to execute query")

    def signup(self):
        name = self.name_entry.get()
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()

        try:
            self.cursor.execute("INSERT INTO login_Cred (name, username, password) VALUES (%s, %s, %s)",
                                (name, username, password))
            self.connection.commit()
            messagebox.showinfo("Success", "Signup Successful")
            self.show_login_page()
            self.clear_signup_fields()
        except Error as e:
            print("Error executing query:", e)
            messagebox.showerror("Error", "Failed to execute query")

    def show_signup_page(self):
        self.clear_login_fields()
        self.login_frame.pack_forget()
        self.signup_frame.pack(fill=tk.BOTH, expand=True)

    def show_login_page(self):
        self.clear_signup_fields()
        self.signup_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def clear_login_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def clear_signup_fields(self):
        self.name_entry.delete(0, tk.END)
        self.signup_username_entry.delete(0, tk.END)
        self.signup_password_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.overrideredirect(True)
    root.geometry("800x600")
    root.attributes("-transparentcolor", "#ffffff")
    root.configure(bg="#ffffff")
    app = StudentManagementSystem(root)
    root.mainloop()
