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
                password="Rahul@5111",
                database="studentms"
            )
            self.cursor = self.connection.cursor()
        except Error as e:
            print("Error occurred while connecting to database:", e)
            messagebox.showerror("Error", "Failed to connect to database")

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

        gender_combo = tk.Entry(details_frame, textvariable=self.gender_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        gender_combo.grid(row=4, column=1, padx=10, pady=5)

        # Student Table Frame
        table_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="black")  # Change background color here
        table_frame.place(x=20, y=370, width=750, height=200)

        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.Student_table = ttk.Treeview(table_frame, columns=("roll", "name", "email", "gender", "contact", "dob", "address"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)

        self.Student_table.heading("roll", text="Roll No.")
        self.Student_table.heading("name", text="Name")
        self.Student_table.heading("email", text="Email")
        self.Student_table.heading("gender", text="Gender")
        self.Student_table.heading("contact", text="Contact")
        self.Student_table.heading("dob", text="Date of Birth")
        self.Student_table.heading("address", text="Address")
        self.Student_table['show'] = 'headings'
        self.Student_table.column("roll", width=50)
        self.Student_table.column("name", width=150)
        self.Student_table.column("email", width=150)
        self.Student_table.column("gender", width=50)
        self.Student_table.column("contact", width=100)
        self.Student_table.column("dob", width=100)
        self.Student_table.column("address", width=200)
        self.Student_table.pack(fill=tk.BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

        # Buttons Frame
        button_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="light blue")  # Change background color here
        button_frame.place(x=20, y=580, width=750, height=70)

        add_button = tk.Button(button_frame, text="Add", command=self.add_students, font=("Arial", 12), bg="light green")  # Change background color here
        add_button.grid(row=0, column=0, padx=10, pady=10)

        update_button = tk.Button(button_frame, text="Update", command=self.update_data, font=("Arial", 12), bg="light blue")  # Change background color here
        update_button.grid(row=0, column=1, padx=10, pady=10)

        delete_button = tk.Button(button_frame, text="Delete", command=self.delete_data, font=("Arial", 12), bg="red")  # Change background color here
        delete_button.grid(row=0, column=2, padx=10, pady=10)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear, font=("Arial", 12), bg="orange")  # Change background color here
        clear_button.grid(row=0, column=3, padx=10, pady=10)

        # Search Frame
        search_frame = tk.LabelFrame(self.root, bd=4, relief=tk.RIDGE, bg="light blue")  # Change background color here
        search_frame.place(x=20, y=330, width=750, height=35)

        search_label = tk.Label(search_frame, text="Search By", font=("Arial", 12), bg="light blue", fg="black")  # Change background and foreground color here
        search_label.grid(row=0, column=0, padx=10, pady=5)

        search_combo = ttk.Combobox(search_frame, font=("Arial", 12), state='readonly', width=10)
        search_combo['values'] = ("roll", "name", "email", "gender", "contact", "dob", "address")
        search_combo.grid(row=0, column=1, padx=10, pady=5)

        search_entry = tk.Entry(search_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        search_entry.grid(row=0, column=2, padx=10, pady=5)

        search_button = tk.Button(search_frame, text="Search", command=self.search_data, font=("Arial", 12), bg="light green")  # Change background color here
        search_button.grid(row=0, column=3, padx=10, pady=5)

        showall_button = tk.Button(search_frame, text="Show All", command=self.fetch_data, font=("Arial", 12), bg="light blue")  # Change background color here
        showall_button.grid(row=0, column=4, padx=10, pady=5)

    def add_students(self):
        if self.Roll_No_var.get() == "" or self.name_var.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                query = "INSERT INTO students (roll_no, name, email, gender, contact, dob, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (self.Roll_No_var.get(), self.name_var.get(), self.email_var.get(), self.gender_var.get(), self.contact_var.get(), self.dob_var.get(), self.txt_Address.get('1.0', tk.END))
                self.cursor.execute(query, values)
                self.connection.commit()
                self.fetch_data()
                self.clear()
                messagebox.showinfo("Success", "Record has been inserted")
            except Error as e:
                print("Error occurred while adding student:", e)
                messagebox.showerror("Error", "Failed to add student")

    def fetch_data(self):
        try:
            self.cursor.execute("SELECT * FROM students")
            rows = self.cursor.fetchall()
            if len(rows) != 0:
                self.Student_table.delete(*self.Student_table.get_children())
                for row in rows:
                    self.Student_table.insert("", tk.END, values=row)
        except Error as e:
            print("Error occurred while fetching data:", e)
            messagebox.showerror("Error", "Failed to fetch data")

    def clear(self):
        self.Roll_No_var.set("")
        self.name_var.set("")
        self.email_var.set("")
        self.gender_var.set("")
        self.contact_var.set("")
        self.dob_var.set("")
        self.txt_Address.delete("1.0", tk.END)

    def get_cursor(self, event):
        cursor_row = self.Student_table.focus()
        contents = self.Student_table.item(cursor_row)
        row = contents['values']
        self.Roll_No_var.set(row[0])
        self.name_var.set(row[1])
        self.email_var.set(row[2])
        self.gender_var.set(row[3])
        self.contact_var.set(row[4])
        self.dob_var.set(row[5])
        self.txt_Address.delete("1.0", tk.END)
        self.txt_Address.insert(tk.END, row[6])

    def update_data(self):
        try:
            query = "UPDATE students SET name=%s, email=%s, gender=%s, contact=%s, dob=%s, address=%s WHERE roll_no=%s"
            values = (self.name_var.get(), self.email_var.get(), self.gender_var.get(), self.contact_var.get(), self.dob_var.get(), self.txt_Address.get('1.0', tk.END), self.Roll_No_var.get())
            self.cursor.execute(query, values)
            self.connection.commit()
            self.fetch_data()
            self.clear()
            messagebox.showinfo("Success", "Record has been updated")
        except Error as e:
            print("Error occurred while updating student:", e)
            messagebox.showerror("Error", "Failed to update student")

    def delete_data(self):
        if self.Roll_No_var.get() == "":
            messagebox.showerror("Error", "Please select a record to delete")
        else:
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
            if confirm:
                try:
                    query = "DELETE FROM students WHERE roll_no=%s"
                    value = (self.Roll_No_var.get(),)
                    self.cursor.execute(query, value)
                    self.connection.commit()
                    self.fetch_data()
                    self.clear()
                    messagebox.showinfo("Success", "Record has been deleted")
                except Error as e:
                    print("Error occurred while deleting student:", e)
                    messagebox.showerror("Error", "Failed to delete student")

    def search_data(self):
        if self.Roll_No_var.get() == "" and self.name_var.get() == "" and self.email_var.get() == "" and self.gender_var.get() == "" and self.contact_var.get() == "" and self.dob_var.get() == "":
            messagebox.showerror("Error", "Please enter a search criteria")
        else:
            try:
                query = "SELECT * FROM students WHERE " + self.search_combo.get() + " LIKE '%" + self.search_entry.get() + "%'"
                self.cursor.execute(query)
                rows = self.cursor.fetchall()
                if len(rows) != 0:
                    self.Student_table.delete(*self.Student_table.get_children())
                    for row in rows:
                        self.Student_table.insert("", tk.END, values=row)
                else:
                    messagebox.showinfo("No Results", "No matching records found")
            except Error as e:
                print("Error occurred while searching data:", e)
                messagebox.showerror("Error", "Failed to search data")

root = tk.Tk()
student_management_system = StudentManagementSystem(root)
root.mainloop()
