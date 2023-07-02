import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1250x625")
        self.root.resizable(False, False)

        self.Roll_No_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.grade_section_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.dob_var = tk.StringVar()

        self.search_by = tk.StringVar()
        self.search_txt = tk.StringVar()

        self.title = tk.Label(root, text="Student Management System", font=("bold", 20))
        self.title.pack(pady=20)

        self.manage_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
        self.manage_frame.place(x=20, y=100, width=450, height=380)

        self.manage_title = tk.Label(self.manage_frame, text="Manage Students", font=("bold", 14))
        self.manage_title.pack(side=tk.TOP, pady=10)

        self.roll_label = tk.Label(self.manage_frame, text="Student ID", font=("bold", 12))
        self.roll_label.pack()
        self.roll_entry = tk.Entry(self.manage_frame, textvariable=self.Roll_No_var)
        self.roll_entry.pack()

        self.name_label = tk.Label(self.manage_frame, text="Name", font=("bold", 12))
        self.name_label.pack()
        self.name_entry = tk.Entry(self.manage_frame, textvariable=self.name_var)
        self.name_entry.pack()

        self.grade_section_label = tk.Label(self.manage_frame, text="Grade and Section", font=("bold", 12))
        self.grade_section_label.pack()
        self.grade_section_entry = tk.Entry(self.manage_frame, textvariable=self.grade_section_var)
        self.grade_section_entry.pack()

        self.email_label = tk.Label(self.manage_frame, text="Email", font=("bold", 12))
        self.email_label.pack()
        self.email_entry = tk.Entry(self.manage_frame, textvariable=self.email_var)
        self.email_entry.pack()

        self.gender_label = tk.Label(self.manage_frame, text="Gender", font=("bold", 12))
        self.gender_label.pack()
        self.gender_combo = ttk.Combobox(self.manage_frame, textvariable=self.gender_var, state='readonly')
        self.gender_combo['values'] = ('Male', 'Female', 'Other')
        self.gender_combo.pack()

        self.contact_label = tk.Label(self.manage_frame, text="Contact", font=("bold", 12))
        self.contact_label.pack()
        self.contact_entry = tk.Entry(self.manage_frame, textvariable=self.contact_var)
        self.contact_entry.pack()

        self.dob_label = tk.Label(self.manage_frame, text="D.O.B", font=("bold", 12))
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.manage_frame, textvariable=self.dob_var)
        self.dob_entry.pack()

        self.button_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
        self.button_frame.place(x=20, y=500, width=450)

        self.add_btn = tk.Button(self.button_frame, text="Add", command=self.add_student)
        self.add_btn.grid(row=0, column=0, padx=10, pady=10)

        self.update_btn = tk.Button(self.button_frame, text="Update", command=self.update_student)
        self.update_btn.grid(row=0, column=1, padx=10, pady=10)

        self.delete_btn = tk.Button(self.button_frame, text="Delete", command=self.delete_student)
        self.delete_btn.grid(row=0, column=2, padx=10, pady=10)

        self.clear_btn = tk.Button(self.button_frame, text="Clear", command=self.clear_fields)
        self.clear_btn.grid(row=0, column=3, padx=10, pady=10)

        self.search_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
        self.search_frame.place(x=500, y=100, width=700, height=380)

        self.search_label = tk.Label(self.search_frame, text="Search By", font=("bold", 12))
        self.search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.search_combo = ttk.Combobox(self.search_frame, textvariable=self.search_by, state='readonly')
        self.search_combo['values'] = ('Roll No', 'Name', 'Grade and Section')
        self.search_combo.grid(row=0, column=1, padx=10, pady=10)
        self.search_combo.current(0)

        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_txt)
        self.search_entry.grid(row=0, column=2, padx=10, pady=10)

        self.search_btn = tk.Button(self.search_frame, text="Search", command=self.search_students)
        self.search_btn.grid(row=0, column=3, padx=10, pady=10)

        self.showall_btn = tk.Button(self.search_frame, text="Show All", command=self.show_all)
        self.showall_btn.grid(row=0, column=4, padx=10, pady=10)

        self.result_frame = tk.Frame(root, bd=4, relief=tk.RIDGE)
        self.result_frame.place(x=500, y=500, width=700, height=150)

        self.result_label = tk.Label(self.result_frame, text="Search Results", font=("bold", 12))
        self.result_label.pack(side=tk.TOP, pady=10)

        self.scrollbar = tk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.students_table = ttk.Treeview(
            self.result_frame,
            column=("Roll No", "Name", "Grade and Section", "Email", "Gender", "Contact", "D.O.B"),
            yscrollcommand=self.scrollbar.set,
        )

        self.students_table.heading("Roll No", text="Roll No")
        self.students_table.heading("Name", text="Name")
        self.students_table.heading("Grade and Section", text="Grade and Section")
        self.students_table.heading("Email", text="Email")
        self.students_table.heading("Gender", text="Gender")
        self.students_table.heading("Contact", text="Contact")
        self.students_table.heading("D.O.B", text="D.O.B")

        self.students_table['show'] = 'headings'
        self.students_table.column("Roll No", width=100)
        self.students_table.column("Name", width=200)
        self.students_table.column("Grade and Section", width=150)
        self.students_table.column("Email", width=200)
        self.students_table.column("Gender", width=100)
        self.students_table.column("Contact", width=150)
        self.students_table.column("D.O.B", width=100)

        self.students_table.pack(fill=tk.BOTH, expand=1)
        self.scrollbar.config(command=self.students_table.yview)

        self.students_table.bind("<ButtonRelease-1>", self.get_selected_row)

        self.initialize_database()

    def add_student(self):
        roll_no = self.Roll_No_var.get()
        name = self.name_var.get()
        grade_section = self.grade_section_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        contact = self.contact_var.get()
        dob = self.dob_var.get()

        if roll_no == "" or name == "" or grade_section == "" or email == "" or gender == "" or contact == "" or dob == "":
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="your_username",
                    password="your_password",
                    database="student_management_system"
                )

                cursor = connection.cursor()

                insert_query = "INSERT INTO students (roll_no, name, grade_section, email, gender, contact, dob) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                student_data = (roll_no, name, grade_section, email, gender, contact, dob)

                cursor.execute(insert_query, student_data)

                connection.commit()

                self.show_all()
                self.clear_fields()
                connection.close()
                messagebox.showinfo("Success", "Student added successfully!")

            except Error as e:
                print(f"Error while connecting to MySQL: {e}")

    def update_student(self):
        roll_no = self.Roll_No_var.get()
        name = self.name_var.get()
        grade_section = self.grade_section_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        contact = self.contact_var.get()
        dob = self.dob_var.get()

        if roll_no == "" or name == "" or grade_section == "" or email == "" or gender == "" or contact == "" or dob == "":
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="your_username",
                    password="your_password",
                    database="student_management_system"
                )

                cursor = connection.cursor()

                update_query = "UPDATE students SET name=%s, grade_section=%s, email=%s, gender=%s, contact=%s, dob=%s WHERE roll_no=%s"
                student_data = (name, grade_section, email, gender, contact, dob, roll_no)

                cursor.execute(update_query, student_data)

                connection.commit()

                self.show_all()
                self.clear_fields()
                connection.close()
                messagebox.showinfo("Success", "Student updated successfully!")

            except Error as e:
                print(f"Error while connecting to MySQL: {e}")

    def delete_student(self):
        roll_no = self.Roll_No_var.get()

        if roll_no == "":
            messagebox.showerror("Error", "Please select a student!")
        else:
            try:
                connection = mysql.connector.connect(
                    host="localhost",
                    user="your_username",
                    password="your_password",
                    database="student_management_system"
                )

                cursor = connection.cursor()

                delete_query = "DELETE FROM students WHERE roll_no=%s"
                student_data = (roll_no,)

                cursor.execute(delete_query, student_data)

                connection.commit()

                self.show_all()
                self.clear_fields()
                connection.close()
                messagebox.showinfo("Success", "Student deleted successfully!")

            except Error as e:
                print(f"Error while connecting to MySQL: {e}")

    def clear_fields(self):
        self.Roll_No_var.set("")
        self.name_var.set("")
        self.grade_section_var.set("")
        self.email_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")
        self.dob_var.set("")

    def search_students(self):
        search_by = self.search_by.get()
        search_text = self.search_txt.get()

        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="student_management_system"
            )

            cursor = connection.cursor()

            if search_by == "Roll No":
                search_query = "SELECT * FROM students WHERE roll_no=%s"
            elif search_by == "Name":
                search_query = "SELECT * FROM students WHERE name=%s"
            elif search_by == "Grade and Section":
                search_query = "SELECT * FROM students WHERE grade_section=%s"

            search_data = (search_text,)

            cursor.execute(search_query, search_data)

            rows = cursor.fetchall()

            if len(rows) != 0:
                self.students_table.delete(*self.students_table.get_children())
                for row in rows:
                    self.students_table.insert("", tk.END, values=row)

                connection.close()
            else:
                connection.close()
                messagebox.showinfo("No Results", "No matching records found!")

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def show_all(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password",
                database="student_management_system"
            )

            cursor = connection.cursor()

            select_query = "SELECT * FROM students"

            cursor.execute(select_query)

            rows = cursor.fetchall()

            if len(rows) != 0:
                self.students_table.delete(*self.students_table.get_children())
                for row in rows:
                    self.students_table.insert("", tk.END, values=row)

                connection.close()

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def get_selected_row(self, event):
        selected_row = self.students_table.focus()
        data = self.students_table.item(selected_row)
        row = data['values']

        self.Roll_No_var.set(row[0])
        self.name_var.set(row[1])
        self.grade_section_var.set(row[2])
        self.email_var.set(row[3])
        self.gender_var.set(row[4])
        self.contact_var.set(row[5])
        self.dob_var.set(row[6])

    def initialize_database(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="your_username",
                password="your_password"
            )

            cursor = connection.cursor()

            create_db_query = "CREATE DATABASE IF NOT EXISTS student_management_system"
            use_db_query = "USE student_management_system"
            create_table_query = "CREATE TABLE IF NOT EXISTS students (roll_no INT PRIMARY KEY, name VARCHAR(255), grade_section VARCHAR(255), email VARCHAR(255), gender VARCHAR(255), contact VARCHAR(255), dob VARCHAR(255))"

            cursor.execute(create_db_query)
            cursor.execute(use_db_query)
            cursor.execute(create_table_query)

            connection.close()

        except Error as e:
            print(f"Error while connecting to MySQL: {e}")


root = tk.Tk()
student_management_system = StudentManagementSystem(root)
root.mainloop()
