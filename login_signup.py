import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import student_system as s_system
from student_system import open_student_system
import time

class LoginSignupSystem:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('925x500+300+200')
        self.root.configure(bg="#fff")
        self.root.resizable(False, False)
        self.img = tk.PhotoImage(file='bg_images/login.png')
        tk.Label(root, image=self.img, bg='white').place(x=50, y=50)
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "dark")
        self.login_frame()

    def login_frame(self):
        self.frame = tk.Frame(self.root, width=350, height=350, bg="white")
        self.frame.place(x=480, y=70)
        heading = tk.Label(self.frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.user = tk.Entry(self.frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Username')
        self.user.bind('<FocusIn>', self.on_enter)
        self.user.bind('<FocusOut>', self.on_leave)
        tk.Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=107)

        self.passw = tk.Entry(self.frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.passw.place(x=30, y=150)
        self.passw.insert(0, 'Password')
        self.passw.bind('<FocusIn>', self.on_enter_1)
        self.passw.bind('<FocusOut>', self.on_leave_1)
        tk.Frame(self.frame, width=295, height=2, bg='black').place(x=25, y=177)

        ttk.Button(self.frame, width=38, text='Sign In', style="Accent.TButton", command=self.login_process).place(x=30, y=204)
        label = tk.Label(self.frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft Yahei UI Light', 9))
        label.place(x=75, y=250)
        sign_up = tk.Button(self.frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=self.signup)
        sign_up.place(x=224, y=250)

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
                    name VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)

            return connection

        except Error as e:
            print("Error connecting to MySQL:", e)
            messagebox.showerror("Error", "Failed to connect to MySQL")
            return None

    def on_enter(self, e):
        self.user.delete(0, 'end')

    def on_leave(self, e):
        username = self.user.get()
        if username == '':
            self.user.insert(0, 'Username')

    def on_enter_1(self, e):
        self.passw.delete(0, 'end')

    def on_leave_1(self, e):
        password = self.passw.get()
        if password == '':
            self.passw.insert(0, 'Password')




    def login_process(self):
        username = self.user.get()
        password = self.passw.get()

        if username == '' or username == 'Username' or password == '' or password == 'Password':
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
                    print("Initializing Database Portal")
                    s_system.open_student_system()  # Replace this line with your student system code

                else:
                    messagebox.showerror("Error", "Invalid username or password")
                    self.progress_window.destroy()

            except Error as e:
                print("Error occurred while logging in:", e)
                messagebox.showerror("Error", "Failed to login")
                self.progress_window.destroy()


    def signup(self):
        self.frame.pack_forget()
        self.frame1 = tk.Frame(self.root, width=350, height=350, bg="white")
        self.frame1.place(x=480, y=70)
        heading = tk.Label(self.frame1, text='Sign Up', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100, y=5)

        self.name = tk.Entry(self.frame1, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.name.place(x=30, y=80)
        self.name.insert(0, 'Name')
        self.name.bind('<FocusIn>', self.on_enter_2)
        self.name.bind('<FocusOut>', self.on_leave_2)
        tk.Frame(self.frame1, width=295, height=2, bg='black').place(x=25, y=107)

        self.username = tk.Entry(self.frame1, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.username.place(x=30, y=150)
        self.username.insert(0, 'Username')
        self.username.bind('<FocusIn>', self.on_enter_3)
        self.username.bind('<FocusOut>', self.on_leave_3)
        tk.Frame(self.frame1, width=295, height=2, bg='black').place(x=25, y=177)

        self.password = tk.Entry(self.frame1, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
        self.password.place(x=30, y=220)
        self.password.insert(0, 'Password')
        self.password.bind('<FocusIn>', self.on_enter_4)
        self.password.bind('<FocusOut>', self.on_leave_4)
        tk.Frame(self.frame1, width=295, height=2, bg='black').place(x=25, y=247)

        ttk.Button(self.frame1, width=38, text='Sign Up',style="Accent.TButton", command=self.confirm_signup).place(x=30, y=270)
        label = tk.Label(self.frame1, text="Already have an Account?", fg='black', bg='white', font=('Microsoft Yahei UI Light', 9))
        label.place(x=75, y=320)
        sign_in = tk.Button(self.frame1, width=6, text='Sign In', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=self.login_frame)
        sign_in.place(x=224, y=319)

    def on_enter_2(self, e):
        self.name.delete(0, 'end')

    def on_leave_2(self, e):
        name_entry = self.name.get()
        if name_entry == '':
            self.name.insert(0, 'Name')

    def on_enter_3(self, e):
        self.username.delete(0, 'end')

    def on_leave_3(self, e):
        username = self.username.get()
        if username == '':
            self.username.insert(0, 'Username')

    def on_enter_4(self, e):
        self.password.delete(0, 'end')

    def on_leave_4(self, e):
        password = self.password.get()
        if password == '':
            self.password.insert(0, 'Password')

    def confirm_signup(self):
        name = self.name.get()
        username = self.username.get()
        password = self.password.get()


        try:
                
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO users (name, username, password) VALUES (%s,%s,%s)", (name, username, password))
            self.connection.commit()
            messagebox.showinfo("Success", "Signup successful")

            self.frame1.destroy()
            self.frame.place(x=480, y=70)

                    
                

        except Error as e:
            print("Error occurred while signing up:", e)
            messagebox.showerror("Error", "Failed to signup")


def open_login_signup_system():
    root = tk.Tk()
    obj = LoginSignupSystem(root)
    root.mainloop()


open_login_signup_system()
