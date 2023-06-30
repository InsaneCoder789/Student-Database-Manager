import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x600")
        self.root.config(bg="white")

        # Student Details Variables
        self.Roll_No_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.txt_Address = tk.Text()

        self.search_by = tk.StringVar()
        self.search_txt = tk.StringVar()

        # Create the connection
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="studentms"
            )
        except Error as e:
            print("Error occurred while connecting to the database: ", e)
            messagebox.showerror("Error", "Failed to connect to the database.")
            self.root.destroy()
            return

        self.cursor = self.connection.cursor()

        # Student Details Frame
        details_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        details_frame.place(x=20, y=20, width=750, height=250)

        # Student Details Title
        details_title = tk.Label(details_frame, text="Student Details", font=("Arial", 18, "bold"), bg="white")
        details_title.grid(row=0, columnspan=2, pady=10)

        # Student Details Labels
        roll_label = tk.Label(details_frame, text="Roll No.", font=("Arial", 12), bg="white")
        roll_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        name_label = tk.Label(details_frame, text="Name", font=("Arial", 12), bg="white")
        name_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        email_label = tk.Label(details_frame, text="Email", font=("Arial", 12), bg="white")
        email_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        gender_label = tk.Label(details_frame, text="Gender", font=("Arial", 12), bg="white")
        gender_label.grid(row=1, column=1, padx=20, pady=10, sticky="w")
        contact_label = tk.Label(details_frame, text="Contact", font=("Arial", 12), bg="white")
        contact_label.grid(row=2, column=1, padx=20, pady=10, sticky="w")
        dob_label = tk.Label(details_frame, text="DOB", font=("Arial", 12), bg="white")
        dob_label.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        address_label = tk.Label(details_frame, text="Address", font=("Arial", 12), bg="white")
        address_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # Student Details Entry
        roll_entry = tk.Entry(details_frame, textvariable=self.Roll_No_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        roll_entry.grid(row=1, column=0, padx=150, pady=10)
        name_entry = tk.Entry(details_frame, textvariable=self.name_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        name_entry.grid(row=2, column=0, padx=150, pady=10)
        email_entry = tk.Entry(details_frame, textvariable=self.email_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        email_entry.grid(row=3, column=0, padx=150, pady=10)
        gender_combo = ttk.Combobox(details_frame, textvariable=self.gender_var, font=("Arial", 12), state="readonly")
        gender_combo['values'] = ('Male', 'Female', 'Other')
        gender_combo.grid(row=1, column=1, padx=150, pady=10)
        contact_entry = tk.Entry(details_frame, textvariable=self.contact_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        contact_entry.grid(row=2, column=1, padx=150, pady=10)
        dob_entry = tk.Entry(details_frame, textvariable=self.dob_var, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        dob_entry.grid(row=3, column=1, padx=150, pady=10)
        address_entry = tk.Text(details_frame, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        address_entry.grid(row=4, column=0, columnspan=2, padx=150, pady=10)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        buttons_frame.place(x=20, y=280, width=750, height=60)

        # Buttons
        add_btn = tk.Button(buttons_frame, text="Add", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.add_students)
        add_btn.grid(row=0, column=0, padx=10, pady=10)
        update_btn = tk.Button(buttons_frame, text="Update", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.update_data)
        update_btn.grid(row=0, column=1, padx=10, pady=10)
        delete_btn = tk.Button(buttons_frame, text="Delete", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.delete_data)
        delete_btn.grid(row=0, column=2, padx=10, pady=10)
        clear_btn = tk.Button(buttons_frame, text="Clear", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.clear)
        clear_btn.grid(row=0, column=3, padx=10, pady=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        search_frame.place(x=20, y=350, width=750, height=60)

        # Search Labels
        search_label = tk.Label(search_frame, text="Search By", font=("Arial", 12), bg="white")
        search_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        search_txt = tk.Entry(search_frame, textvariable=self.search_txt, font=("Arial", 12), bd=2, relief=tk.GROOVE)
        search_txt.grid(row=0, column=1, padx=10, pady=10)
        search_by_combo = ttk.Combobox(search_frame, textvariable=self.search_by, font=("Arial", 12), state="readonly")
        search_by_combo['values'] = ('roll_no', 'name', 'email')
        search_by_combo.grid(row=0, column=2, padx=10, pady=10)
        search_btn = tk.Button(search_frame, text="Search", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.search_data)
        search_btn.grid(row=0, column=3, padx=10, pady=10)
        showall_btn = tk.Button(search_frame, text="Show All", font=("Arial", 12, "bold"), bg="blue", fg="white", command=self.fetch_data)
        showall_btn.grid(row=0, column=4, padx=10, pady=10)

        # Student Table Frame
        table_frame = tk.Frame(self.root, bd=4, relief=tk.RIDGE, bg="white")
        table_frame.place(x=20, y=420, width=750, height=160)

        # Student Table
        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        self.Student_table = ttk.Treeview(table_frame, columns=("roll_no", "name", "email", "gender", "contact", "dob", "address"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.config(command=self.Student_table.xview)
        scroll_y.config(command=self.Student_table.yview)
        self.Student_table.heading("roll_no", text="Roll No.")
        self.Student_table.heading("name", text="Name")
        self.Student_table.heading("email", text="Email")
        self.Student_table.heading("gender", text="Gender")
        self.Student_table.heading("contact", text="Contact")
        self.Student_table.heading("dob", text="DOB")
        self.Student_table.heading("address", text="Address")
        self.Student_table['show'] = 'headings'
        self.Student_table.column("roll_no", width=100)
        self.Student_table.column("name", width=100)
        self.Student_table.column("email", width=150)
        self.Student_table.column("gender", width=70)
        self.Student_table.column("contact", width=100)
        self.Student_table.column("dob", width=100)
        self.Student_table.column("address", width=200)
        self.Student_table.pack(fill=tk.BOTH, expand=1)
        self.Student_table.bind("<ButtonRelease-1>", self.get_cursor)

        # Fetch initial data
        self.fetch_data()

    def add_students(self):
        if self.Roll_No_var.get() == "" or self.name_var.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                query = "INSERT INTO students (roll_no, name, email, gender, contact, dob, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (
                    self.Roll_No_var.get(),
                    self.name_var.get(),
                    self.email_var.get(),
                    self.gender_var.get(),
                    self.contact_var.get(),
                    self.dob_var.get(),
                    self.txt_Address.get('1.0', 'end')
                )

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
            query = "SELECT * FROM students"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            if len(rows) != 0:
                self.Student_table.delete(*self.Student_table.get_children())
                for row in rows:
                    self.Student_table.insert('', tk.END, values=row)
                self.connection.commit()
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

    def get_cursor(self, ev):
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
            query = "UPDATE students SET name = %s, email = %s, gender = %s, contact = %s, dob = %s, address = %s WHERE roll_no = %s"
            values = (
                self.name_var.get(),
                self.email_var.get(),
                self.gender_var.get(),
                self.contact_var.get(),
                self.dob_var.get(),
                self.txt_Address.get('1.0', 'end'),
                self.Roll_No_var.get()
            )

            self.cursor.execute(query, values)
            self.connection.commit()
            self.fetch_data()
            self.clear()
            messagebox.showinfo("Success", "Record has been updated")
        except Error as e:
            print("Error occurred while updating student:", e)
            messagebox.showerror("Error", "Failed to update student")

    def delete_data(self):
        try:
            query = "DELETE FROM students WHERE roll_no = %s"
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
        try:
            query = f"SELECT * FROM students WHERE {self.search_by.get()} LIKE '%{self.search_txt.get()}%'"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            if len(rows) != 0:
                self.Student_table.delete(*self.Student_table.get_children())
                for row in rows:
                    self.Student_table.insert('', tk.END, values=row)
                self.connection.commit()
        except Error as e:
            print("Error occurred while searching data:", e)
            messagebox.showerror("Error", "Failed to search data")


root = tk.Tk()
app = StudentManagementSystem(root)
root.mainloop()
