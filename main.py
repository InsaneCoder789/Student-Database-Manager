import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")

        # Database Connection
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Your_Password",
                database="studentms"
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print("Error occurred while connecting to database:", e)
            messagebox.showerror("Error", "Failed to connect to database")
            root.destroy()

        # Student Management System UI
        self.Roll_No_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.dob_var = tk.StringVar()

        title_label = tk.Label(self.root, text="Student Management System", font=("Arial", 20, "bold"), bg="yellow", fg="black")
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Student Details Frame
        details_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="light blue")  # Change background color here
        details_frame.place(x=20, y=60, width=750, height=300)

        details_label = tk.Label(details_frame, text="Student Details", font=("Arial", 14, "bold"), bg="light blue", fg="blue")  # Change background and foreground color here
        details_label.grid(row=0, columnspan=2, pady=10)

        roll_no_label = tk.Label(details_frame, text="Roll No.", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        roll_no_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        roll_no_entry = tk.Entry(details_frame, textvariable=self.Roll_No_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        roll_no_entry.grid(row=1, column=1, padx=10, pady=5)

        name_label = tk.Label(details_frame, text="Name", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        name_entry = tk.Entry(details_frame, textvariable=self.name_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        name_entry.grid(row=2, column=1, padx=10, pady=5)

        email_label = tk.Label(details_frame, text="Email", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        email_entry = tk.Entry(details_frame, textvariable=self.email_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        email_entry.grid(row=3, column=1, padx=10, pady=5)

        gender_label = tk.Label(details_frame, text="Gender", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        gender_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        gender_combo = ttk.Combobox(details_frame, textvariable=self.gender_var, font=("Arial", 12), state="readonly")
        gender_combo["values"] = ("Male", "Female", "Other")
        gender_combo.grid(row=4, column=1, padx=10, pady=5)

        contact_label = tk.Label(details_frame, text="Contact", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        contact_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        contact_entry = tk.Entry(details_frame, textvariable=self.contact_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        contact_entry.grid(row=1, column=3, padx=10, pady=5)

        dob_label = tk.Label(details_frame, text="Date of Birth", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        dob_entry = tk.Entry(details_frame, textvariable=self.dob_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        dob_entry.grid(row=2, column=3, padx=10, pady=5)

        add_btn = tk.Button(details_frame, text="Add", font=("Arial", 12, "bold"), bg="green", fg="white", command=self.add_students)  # Change background and foreground color here
        add_btn.grid(row=5, column=0, padx=10, pady=5)

        update_btn = tk.Button(details_frame, text="Update", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.update_students)  # Change background and foreground color here
        update_btn.grid(row=5, column=1, padx=10, pady=5)

        delete_btn = tk.Button(details_frame, text="Delete", font=("Arial", 12, "bold"), bg="red", fg="white", command=self.delete_students)  # Change background and foreground color here
        delete_btn.grid(row=5, column=2, padx=10, pady=5)

        clear_btn = tk.Button(details_frame, text="Clear", font=("Arial", 12, "bold"), bg="orange", fg="black", command=self.clear_entries)  # Change background and foreground color here
        clear_btn.grid(row=5, column=3, padx=10, pady=5)

        # Student Table Frame
        table_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE)
        table_frame.place(x=20, y=370, width=750, height=200)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.student_table = ttk.Treeview(table_frame, columns=("Roll No.", "Name", "Email", "Gender", "Contact", "DOB"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("Roll No.", text="Roll No.")
        self.student_table.heading("Name", text="Name")
        self.student_table.heading("Email", text="Email")
        self.student_table.heading("Gender", text="Gender")
        self.student_table.heading("Contact", text="Contact")
        self.student_table.heading("DOB", text="DOB")
        self.student_table["show"] = "headings"

        self.student_table.column("Roll No.", width=100)
        self.student_table.column("Name", width=150)
        self.student_table.column("Email", width=200)
        self.student_table.column("Gender", width=100)
        self.student_table.column("Contact", width=100)
        self.student_table.column("DOB", width=100)

        self.student_table.pack(fill=tk.BOTH, expand=1)
        self.student_table.bind("<ButtonRelease-1>", self.get_selected_row)

        self.display_students()

    def add_students(self):
        roll_no = self.Roll_No_var.get()
        name = self.name_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        contact = self.contact_var.get()
        dob = self.dob_var.get()

        if roll_no == "" or name == "":
            messagebox.showerror("Error", "Roll No. and Name are required fields")
        else:
            try:
                self.cursor.execute("INSERT INTO students (roll_no, name, email, gender, contact, dob) VALUES (%s, %s, %s, %s, %s, %s)",
                                    (roll_no, name, email, gender, contact, dob))
                self.connection.commit()
                messagebox.showinfo("Success", "Record added successfully")
                self.clear_entries()
                self.display_students()
            except Error as e:
                print("Error occurred while adding student:", e)
                messagebox.showerror("Error", "Failed to add student")

    def update_students(self):
        roll_no = self.Roll_No_var.get()
        name = self.name_var.get()
        email = self.email_var.get()
        gender = self.gender_var.get()
        contact = self.contact_var.get()
        dob = self.dob_var.get()

        if roll_no == "":
            messagebox.showerror("Error", "Please select a student from the table to update")
        else:
            try:
                self.cursor.execute("UPDATE students SET name=%s, email=%s, gender=%s, contact=%s, dob=%s WHERE roll_no=%s",
                                    (name, email, gender, contact, dob, roll_no))
                self.connection.commit()
                messagebox.showinfo("Success", "Record updated successfully")
                self.clear_entries()
                self.display_students()
            except Error as e:
                print("Error occurred while updating student:", e)
                messagebox.showerror("Error", "Failed to update student")

    def delete_students(self):
        roll_no = self.Roll_No_var.get()

        if roll_no == "":
            messagebox.showerror("Error", "Please select a student from the table to delete")
        else:
            confirmation = messagebox.askyesno("Confirmation", "Do you want to delete this student?")
            if confirmation == 1:
                try:
                    self.cursor.execute("DELETE FROM students WHERE roll_no=%s", (roll_no,))
                    self.connection.commit()
                    messagebox.showinfo("Success", "Record deleted successfully")
                    self.clear_entries()
                    self.display_students()
                except Error as e:
                    print("Error occurred while deleting student:", e)
                    messagebox.showerror("Error", "Failed to delete student")

    def clear_entries(self):
        self.Roll_No_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")
        self.dob_var.set("")

    def display_students(self):
        try:
            self.cursor.execute("SELECT * FROM students")
            rows = self.cursor.fetchall()
            self.student_table.delete(*self.student_table.get_children())
            for row in rows:
                self.student_table.insert("", tk.END, values=row)
        except Error as e:
            print("Error occurred while fetching students:", e)
            messagebox.showerror("Error", "Failed to fetch students")

    def get_selected_row(self, event):
        try:
            row = self.student_table.focus()
            content = self.student_table.item(row)
            row = content["values"]
            self.Roll_No_var.set(row[0])
            self.name_var.set(row[1])
            self.email_var.set(row[2])
            self.gender_var.set(row[3])
            self.contact_var.set(row[4])
            self.dob_var.set(row[5])
        except IndexError:
            pass

root = tk.Tk()
obj = StudentManagementSystem(root)
root.mainloop()
