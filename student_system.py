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
        self.root.resizable(False,False)
        self.root.configure(bg="#e6e6e6")


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

        self.manage_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="#f2f2f2")
        self.manage_frame.pack(side=tk.LEFT, padx=20)

        self.manage_title = tk.Label(self.manage_frame, text="Manage Students", font=("bold", 20), bg="#f2f2f2")
        self.manage_title.pack(side=tk.TOP, pady=10)

        self.roll_label = tk.Label(self.manage_frame, text="Student ID", font=("bold", 14))
        self.roll_label.pack()
        self.roll_entry = tk.Entry(self.manage_frame, textvariable=self.Roll_No_var)
        self.roll_entry.pack()

        self.name_label = tk.Label(self.manage_frame, text="Name", font=("bold", 14))
        self.name_label.pack()
        self.name_entry = tk.Entry(self.manage_frame, textvariable=self.name_var)
        self.name_entry.pack()

        self.grade_section_label = tk.Label(self.manage_frame, text="Grade and Section", font=("bold", 14))
        self.grade_section_label.pack()
        self.grade_section_entry = tk.Entry(self.manage_frame, textvariable=self.grade_section_var)
        self.grade_section_entry.pack()

        self.email_label = tk.Label(self.manage_frame, text="Email", font=("bold", 14))
        self.email_label.pack()
        self.email_entry = tk.Entry(self.manage_frame, textvariable=self.email_var)
        self.email_entry.pack()

        self.gender_label = tk.Label(self.manage_frame, text="Gender", font=("bold", 14))
        self.gender_label.pack()
        self.gender_combo = ttk.Combobox(self.manage_frame, textvariable=self.gender_var, state='readonly')
        self.gender_combo['values'] = ('Male', 'Female', 'Other')
        self.gender_combo.pack()

        self.contact_label = tk.Label(self.manage_frame, text="Contact", font=("bold", 14))
        self.contact_label.pack()
        self.contact_entry = tk.Entry(self.manage_frame, textvariable=self.contact_var)
        self.contact_entry.pack()

        self.dob_label = tk.Label(self.manage_frame, text="D.O.B", font=("bold", 14))
        self.dob_label.pack()
        self.dob_entry = tk.Entry(self.manage_frame, textvariable=self.dob_var, width=25)
        self.dob_entry.pack()

        self.button_frame = tk.Frame(self.manage_frame, bd=4, relief=tk.RIDGE)
        self.button_frame.pack(pady=20)

        self.add_button = tk.Button(self.button_frame, text="Add", font=("bold", 12), command=self.add_student)
        self.add_button.grid(row=0, column=0, padx=5, pady=10)
        self.update_button = tk.Button(self.button_frame, text="Update", font=("bold", 12), command=self.update_student)
        self.update_button.grid(row=0, column=1, padx=5, pady=10)
        self.delete_button = tk.Button(self.button_frame, text="Delete", font=("bold", 12), command=self.delete_student)
        self.delete_button.grid(row=0, column=2, padx=5, pady=10)
        self.clear_button = tk.Button(self.button_frame, text="Clear", font=("bold", 12), command=self.clear_entries)
        self.clear_button.grid(row=0, column=3, padx=5, pady=10)

        self.details_frame = tk.Frame(root, bd=4, relief=tk.RIDGE, bg="#f2f2f2")
        self.details_frame.pack(side=tk.TOP, padx=20,pady=100)

        self.search_frame = tk.Frame(self.details_frame, bd=4, relief=tk.RIDGE, bg="#f2f2f2")
        self.search_frame.pack(side=tk.TOP, pady=20)

        self.search_label = tk.Label(self.search_frame, text="Search By", font=("bold", 14))
        self.search_label.grid(row=0, column=0, padx=5)
        self.search_combo = ttk.Combobox(self.search_frame, textvariable=self.search_by, state='readonly')
        self.search_combo['values'] = ('Roll_No', 'Name', 'Grade_Section')
        self.search_combo.grid(row=0, column=1, padx=5)
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_txt)
        self.search_entry.grid(row=0, column=2, padx=5)
        self.search_button = tk.Button(self.search_frame, text="Search", font=("bold", 12), command=self.search_students)
        self.search_button.grid(row=0, column=3, padx=5)

        self.students_tree = ttk.Treeview(self.details_frame, columns=(
            'Roll_No', 'Name', 'Grade_Section', 'Email', 'Gender', 'Contact', 'D.O.B'))
        
        self.students_tree.heading('Roll_No', text='Student ID', anchor=tk.CENTER, foreground="black")
        self.students_tree.heading('Name', text='Name', anchor=tk.CENTER, foreground="black")
        self.students_tree.heading('Grade_Section', text='Grade and Section', anchor=tk.CENTER, foreground="black")
        self.students_tree.heading('Email', text='Email', anchor=tk.CENTER, foreground="black")
        self.students_tree.heading('Gender', text='Gender', anchor=tk.CENTER, foreground="black")
        self.students_tree.heading('Contact', text='Contact', anchor=tk.CENTER, foreground="black")
        self.students_tree.heading('D.O.B', text='D.O.B', anchor=tk.CENTER, foreground="black")

        self.students_tree['show'] = 'headings'
        self.students_tree.column('Roll_No', width=100, foreground="black")
        self.students_tree.column('Name', width=150, foreground="black")
        self.students_tree.column('Grade_Section', width=120, foreground="black")
        self.students_tree.column('Email', width=200, foreground="black")
        self.students_tree.column('Gender', width=100, foreground="black")
        self.students_tree.column('Contact', width=120, foreground="black")
        self.students_tree.column('D.O.B', width=100, foreground="black")

        self.students_tree.pack(fill=tk.BOTH, expand=1)
        self.students_tree.bind('<ButtonRelease-1>', self.get_selected_row)

        self.display_students()

    def add_student(self):
        if self.Roll_No_var.get() == '' or self.name_var.get() == '' or self.grade_section_var.get() == '':
            messagebox.showerror("Error", "Please fill in all required fields")
        else:
            try:
                connection = self.connect_to_database()
                cursor = connection.cursor()
                query = "INSERT INTO students (Roll_No, Name, Grade_Section, Email, Gender, Contact, DOB) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (self.Roll_No_var.get(), self.name_var.get(), self.grade_section_var.get(),
                          self.email_var.get(), self.gender_var.get(), self.contact_var.get(), self.dob_var.get())
                cursor.execute(query, values)
                connection.commit()
                connection.close()
                self.clear_entries()
                self.display_students()
                messagebox.showinfo("Success", "Student added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def update_student(self):
        if self.Roll_No_var.get() == '' or self.name_var.get() == '' or self.grade_section_var.get() == '':
            messagebox.showerror("Error", "Please select a student")
        else:
            try:
                connection = self.connect_to_database()
                cursor = connection.cursor()
                query = "UPDATE students SET Name=%s, Grade_Section=%s, Email=%s, Gender=%s, Contact=%s, DOB=%s " \
                        "WHERE Roll_No=%s"
                values = (self.name_var.get(), self.grade_section_var.get(), self.email_var.get(),
                          self.gender_var.get(), self.contact_var.get(), self.dob_var.get(), self.Roll_No_var.get())
                cursor.execute(query, values)
                connection.commit()
                connection.close()
                self.clear_entries()
                self.display_students()
                messagebox.showinfo("Success", "Student updated successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def delete_student(self):
        if self.Roll_No_var.get() == '':
            messagebox.showerror("Error", "Please select a student")
        else:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this student?")
            if confirmation == 1:
                try:
                    connection = self.connect_to_database()
                    cursor = connection.cursor()
                    query = "DELETE FROM students WHERE Roll_No=%s"
                    value = (self.Roll_No_var.get(),)
                    cursor.execute(query, value)
                    connection.commit()
                    connection.close()
                    self.clear_entries()
                    self.display_students()
                    messagebox.showinfo("Success", "Student deleted successfully")
                except Error as e:
                    messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def search_students(self):
        try:
            connection = self.connect_to_database()
            cursor = connection.cursor()
            query = ""
            value = ""
            if self.search_by.get() == 'Roll_No':
                query = "SELECT * FROM students WHERE Roll_No=%s"
                value = (self.search_txt.get(),)
            elif self.search_by.get() == 'Name':
                query = "SELECT * FROM students WHERE Name=%s"
                value = (self.search_txt.get(),)
            elif self.search_by.get() == 'Grade_Section':
                query = "SELECT * FROM students WHERE Grade_Section=%s"
                value = (self.search_txt.get(),)
            cursor.execute(query, value)
            rows = cursor.fetchall()
            self.students_tree.delete(*self.students_tree.get_children())
            for row in rows:
                self.students_tree.insert('', tk.END, values=row)
            connection.close()
        except Error as e:
            messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def display_students(self):
        try:
            connection = self.connect_to_database()
            cursor = connection.cursor()
            query = "SELECT * FROM students"
            cursor.execute(query)
            rows = cursor.fetchall()
            self.students_tree.delete(*self.students_tree.get_children())
            for row in rows:
                self.students_tree.insert('', tk.END, values=row)
            connection.close()
        except Error as e:
            messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def get_selected_row(self, event):
        try:
            selected_row = self.students_tree.focus()
            values = self.students_tree.item(selected_row, 'values')
            self.Roll_No_var.set(values[0])
            self.name_var.set(values[1])
            self.grade_section_var.set(values[2])
            self.email_var.set(values[3])
            self.gender_var.set(values[4])
            self.contact_var.set(values[5])
            self.dob_var.set(values[6])
        except IndexError:
            pass

    def clear_entries(self):
        self.Roll_No_var.set('')
        self.name_var.set('')
        self.grade_section_var.set('')
        self.email_var.set('')
        self.gender_var.set('')
        self.contact_var.set('')
        self.dob_var.set('')

    @staticmethod
    def connect_to_database():
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Rahul@5111",
            database="student_management_system"
        )
        return connection

def open_student_system(): 
    root = tk.Tk()
    sms = StudentManagementSystem(root)
    root.mainloop()
