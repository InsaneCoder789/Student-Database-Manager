import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv
import mysql.connector
from mysql.connector import Error

class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1250x625")
        self.root.resizable(False, False)
        self.root.tk.call("source", "azure.tcl")
        self.root.tk.call("set_theme", "light")
        
        #Style configuration
        style = ttk.Style()
        style.configure(
                "Treeview", #Widget Nme 
                background="black", 
                foreground="white",
                fieldbackground="black",
                font=("Helvetica", 10),
                rowheight=25
                )
        style.configure(
                "Accent.TButton", 
                foreground="white", 
                background="blue",
                borderwidth=0,
                relief=tk.RAISED,
                padding=10
                )
        self.students = []
        self.Student_Id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.grade_section_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.gender_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.dob_var = tk.StringVar()

        self.search_by = tk.StringVar()
        self.search_txt = tk.StringVar()

        self.title = ttk.Label(root, text="Student Management System", font=("bold", 16), style="Title.TLabel")
        self.title.pack(pady=20)


        

        self.manage_frame = ttk.Frame(root, borderwidth=0, relief="flat", style="Frame.TFrame")
        self.manage_frame.pack(side=tk.LEFT, padx=20, pady=20, expand=True, fill=tk.BOTH)

        self.manage_title = ttk.Label(self.manage_frame, text="Manage Students", font=("bold", 16), style="Title.TLabel")
        self.manage_title.pack(side=tk.TOP, pady=10)

        self.roll_label = ttk.Label(self.manage_frame, text="Student ID", font=("bold", 11), style="Label.TLabel")
        self.roll_label.pack()
        self.roll_entry = ttk.Entry(self.manage_frame, textvariable=self.Student_Id_var, font=("bold", 9), style="Entry.TEntry")
        self.roll_entry.pack()

        self.name_label = ttk.Label(self.manage_frame, text="Name", font=("bold", 11), style="Label.TLabel")
        self.name_label.pack()
        self.name_entry = ttk.Entry(self.manage_frame, textvariable=self.name_var, font=("bold", 9), style="Entry.TEntry")
        self.name_entry.pack()

        self.grade_section_label = ttk.Label(self.manage_frame, text="Grade and Section", font=("bold", 11), style="Label.TLabel")
        self.grade_section_label.pack()
        self.grade_section_entry = ttk.Entry(self.manage_frame, textvariable=self.grade_section_var, font=("bold", 9), style="Entry.TEntry")
        self.grade_section_entry.pack()

        self.email_label = ttk.Label(self.manage_frame, text="Email", font=("bold", 11), style="Label.TLabel")
        self.email_label.pack()
        self.email_entry = ttk.Entry(self.manage_frame, textvariable=self.email_var, font=("bold", 9), style="Entry.TEntry")
        self.email_entry.pack()

        self.gender_label = ttk.Label(self.manage_frame, text="Gender", font=("bold", 11), style="Label.TLabel")
        self.gender_label.pack()
        self.gender_combo = ttk.Combobox(self.manage_frame, textvariable=self.gender_var, state='readonly', font=("bold", 9), style="Combobox.TCombobox")
        self.gender_combo['values'] = ('Male', 'Female', 'Other')
        self.gender_combo.pack()

        self.contact_label = ttk.Label(self.manage_frame, text="Contact", font=("bold", 11), style="Label.TLabel")
        self.contact_label.pack()
        self.contact_entry = ttk.Entry(self.manage_frame, textvariable=self.contact_var, font=("bold", 9), style="Entry.TEntry")
        self.contact_entry.pack()

        self.dob_label = ttk.Label(self.manage_frame, text="DOB", font=("bold", 11), style="Label.TLabel")
        self.dob_label.pack()
        self.dob_entry = ttk.Entry(self.manage_frame, textvariable=self.dob_var, width=25, font=("bold",9 ), style="Entry.TEntry")
        self.dob_entry.pack()

        self.button_frame = ttk.Frame(self.manage_frame, relief="flat",borderwidth=0, style="Frame.TFrame")
        self.button_frame.pack(pady=13)

        self.add_button = ttk.Button(self.button_frame, text="Add", style="Accent.TButton", command=self.add_student)
        self.add_button.grid(row=0, column=0, padx=5, pady=10)
        self.update_button = ttk.Button(self.button_frame, text="Update", style="Accent.TButton", command=self.update_student)
        self.update_button.grid(row=0, column=1, padx=5, pady=10)
        self.delete_button = ttk.Button(self.button_frame, text="Delete", style="Accent.TButton", command=self.delete_student)
        self.delete_button.grid(row=0, column=2, padx=5, pady=10)
        self.clear_button = ttk.Button(self.button_frame, text="Clear", style="Accent.TButton", command=self.clear_entries)
        self.clear_button.grid(row=0, column=3, padx=5, pady=10)


        self.details_frame = ttk.Frame(root, borderwidth=0, relief="flat", style="Frame.TFrame")
        self.details_frame.pack(side=tk.TOP, padx=20, pady=20)

        self.data_frame = ttk.Frame(root, borderwidth=0, relief="flat", style="Frame.TFrame")
        self.data_frame.pack(side=tk.TOP, padx=20, pady=5)

        # Add buttons for data export and import to the data frame
        self.export_button = ttk.Button(self.data_frame, text="Export Data", command=self.export_data,style="Accent.TButton",width=20)
        self.export_button.grid(row=0, column=1, padx=10, pady=5)

        self.import_button = ttk.Button(self.data_frame, text="Import Data", command=self.import_data,style="Accent.TButton",width=20)
        self.import_button.grid(row=0, column=0, padx=10, pady=5)

        self.clear_button = ttk.Button(self.data_frame, text="Clear Data", command=self.delete_table,style="Accent.TButton",width=20)
        self.clear_button.grid(row=0, column=2, padx=10, pady=5)

        self.search_frame = ttk.Frame(self.details_frame, borderwidth=0, relief="flat", style="Frame.TFrame")
        self.search_frame.pack(side=tk.TOP, pady=20)

        self.search_label = ttk.Label(self.search_frame, text="Search By", font=("bold", 14), style="Label.TLabel")
        self.search_label.grid(row=0, column=0, padx=5)
        self.search_combo = ttk.Combobox(self.search_frame, textvariable=self.search_by, state='readonly', style="Combobox.TCombobox")
        self.search_combo['values'] = ('Student_Id', 'Name', 'Grade_Section')
        self.search_combo.grid(row=0, column=1, padx=5)
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_txt, style="Entry.TEntry")
        self.search_entry.grid(row=0, column=2, padx=5)
        self.search_button = ttk.Button(self.search_frame, text="Search", style="Accent.TButton", command=self.search_students)
        self.search_button.grid(row=0, column=3, padx=5)
        self.left_button = ttk.Button(self.search_frame, text="<", command=self.move_left,style="Accent.TButton",width=1)
        self.left_button.grid(row=0, column=5, padx=5)
        self.right_button = ttk.Button(self.search_frame, text=">", command=self.move_right,style="Accent.TButton",width=1)
        self.right_button.grid(row=0, column=6, padx=5)
        self.show_all_button = ttk.Button(self.search_frame, text="Show All", style="Accent.TButton", command=self.display_students)
        self.show_all_button.grid(row=0, column=4, padx=5)

        self.students_tree = ttk.Treeview(self.details_frame, columns=(
            'Student_Id', 'Name', 'Grade_Section', 'Email', 'Gender', 'Contact', 'DOB'))

        self.students_tree.heading('Student_Id', text='Student ID', anchor='w')
        self.students_tree.heading('Name', text='Name', anchor='w')
        self.students_tree.heading('Grade_Section', text='Grade and Section', anchor='w')
        self.students_tree.heading('Email', text='Email', anchor='w')
        self.students_tree.heading('Gender', text='Gender', anchor='w')
        self.students_tree.heading('Contact', text='Contact', anchor='w')
        self.students_tree.heading('DOB', text='DOB', anchor='w')


        self.students_tree['show'] = 'headings'
        self.students_tree.column('Student_Id', width=100)
        self.students_tree.column('Name', width=150)
        self.students_tree.column('Grade_Section', width=120)
        self.students_tree.column('Email', width=200)
        self.students_tree.column('Gender', width=100)
        self.students_tree.column('Contact', width=120)
        self.students_tree.column('DOB', width=100)

        self.students_tree.pack(fill=tk.BOTH, expand=1)
        self.students_tree.bind('<ButtonRelease-1>', self.get_selected_row)

        self.display_students()

    def change_theme(self):
        print("Button Pressed!")

    def move_left(self):
        self.students_tree.xview_scroll(-30, "units")

    def move_right(self):
        self.students_tree.xview_scroll(30, "units")

    def export_data(self):
        search_by = self.search_by.get()
        search_text = self.search_txt.get()

        conn = self.connect_to_database()
        cursor = conn.cursor()

        try:
            query = f"SELECT * FROM students WHERE {search_by} LIKE '%{search_text}%'"
            print(query)  # Add this line to print the query statement
            cursor.execute(query)
            results = cursor.fetchall()

            if len(results) == 0:
                messagebox.showwarning("No Records Found", "No records matching the search criteria.")
                return
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if not file_path:
                return

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Student_Id", "Name", "Grade_Section", "Email", "Gender", "Contact", "DOB"])
                writer.writerows(results)

            messagebox.showinfo("Export Successful", "Data exported to CSV file successfully.")
            self.students_tree.delete(*self.students_tree.get_children())
            delete_table = "DROP TABLE students"
            cursor.execute(delete_table)
            print("Data Table Deleted!")


        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred while exporting data: {str(e)}")

        finally:
            # Close the database connection
            cursor.close()
            conn.close()


        
    def import_data(self):
    # Open a file dialog to choose the import file
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            # Clear existing student data
            self.students_tree.delete(*self.students_tree.get_children())
            self.students.clear()

            # Read the CSV file
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                headings = next(reader)  # Get the column headings

                # Check if the file has the expected columns
                if headings != ["Student_Id", "Name", "Grade_Section", "Email", "Gender", "Contact", "DOB"]:
                    messagebox.showerror("Invalid File", "The selected file does not have the expected columns.")
                    return

                # Connect to the MySQL database
                conn = self.connect_to_database()
                cursor = conn.cursor()

                table_name = "students"

                # Create the "students" table if it doesn't exist
                create_table_query = """
                CREATE TABLE IF NOT EXISTS students (
                    Student_Id INT PRIMARY KEY,
                    Name VARCHAR(255),
                    Grade_Section VARCHAR(255),
                    Email VARCHAR(255),
                    Gender VARCHAR(255),
                    Contact VARCHAR(255),
                    DOB VARCHAR(255)
                )
                """
                cursor.execute(create_table_query)

                # Process each row of data
                for row in reader:
                    student_data = dict(zip(headings, row))
                    self.students.append(student_data)
                    self.students_tree.insert('', tk.END, values=list(student_data.values()))

                    # Insert the data into the "students" table
                    insert_query = """
                    INSERT INTO students (Student_Id, Name, Grade_Section, Email, Gender, Contact, DOB)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
                    values = (
                        student_data['Student_Id'],
                        student_data['Name'],
                        student_data['Grade_Section'],
                        student_data['Email'],
                        student_data['Gender'],
                        student_data['Contact'],
                        student_data['DOB']
                    )
                    cursor.execute(insert_query, values)

                # Commit the changes and close the database connection
                conn.commit()
                conn.close()

                messagebox.showinfo("Import Successful", "Data imported from CSV file successfully.")
        except Exception as e:
                messagebox.showerror("Import Error", f"An error occurred while importing data: {str(e)}")



    def add_student(self):
        if self.Student_Id_var.get() == '' or self.name_var.get() == '' or self.grade_section_var.get() == '':
            messagebox.showerror("Error", "Please fill in all required fields")
        else:
            try:
                connection = self.connect_to_database()
                cursor = connection.cursor()
                table_query = """
                CREATE TABLE IF NOT EXISTS students (
                    Student_Id INT PRIMARY KEY,
                    Name VARCHAR(255),
                    Grade_Section VARCHAR(255),
                    Email VARCHAR(255),
                    Gender VARCHAR(255),
                    Contact VARCHAR(255),
                    DOB VARCHAR(255)
                )
                """
                cursor.execute(table_query)
                print("Student Table Created!!!")
                query = "INSERT INTO students (Student_Id, Name, Grade_Section, Email, Gender, Contact, DOB) " \
                        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
                values = (self.Student_Id_var.get(), self.name_var.get(), self.grade_section_var.get(),
                          self.email_var.get(), self.gender_var.get(), self.contact_var.get(), self.dob_var.get())
                cursor.execute(query, values)
                print("Data Added To Database")
                connection.commit()
                connection.close()
                self.clear_entries()
                self.display_students()
                messagebox.showinfo("Success", "Student added successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def update_student(self):
        if self.Student_Id_var.get() == '' or self.name_var.get() == '' or self.grade_section_var.get() == '':
            messagebox.showerror("Error", "Please select a student")
        else:
            try:
                connection = self.connect_to_database()
                cursor = connection.cursor()
                query = "UPDATE students SET Name=%s, Grade_Section=%s, Email=%s, Gender=%s, Contact=%s, DOB=%s " \
                        "WHERE Student_Id=%s"
                values = (self.name_var.get(), self.grade_section_var.get(), self.email_var.get(),
                          self.gender_var.get(), self.contact_var.get(), self.dob_var.get(), self.Student_Id_var.get())
                cursor.execute(query, values)
                print("Data Updated in Database!!!")
                connection.commit()
                connection.close()
                self.clear_entries()
                self.display_students()
                messagebox.showinfo("Success", "Student updated successfully")
            except Error as e:
                messagebox.showerror("Error", f"Error while connecting to the database: {e}")

    def delete_student(self):
        if self.Student_Id_var.get() == '':
            messagebox.showerror("Error", "Please select a student")
        else:
            confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this student?")
            if confirmation == 1:
                try:
                    connection = self.connect_to_database()
                    cursor = connection.cursor()
                    query = "DELETE FROM students WHERE Student_Id=%s"
                    value = (self.Student_Id_var.get(),)
                    cursor.execute(query, value)
                    print("Data Deleted from Database!")
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
            if self.search_by.get() == 'Student_Id':
                query = "SELECT * FROM students WHERE Student_Id=%s"
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

    def delete_table(self):
        try:
            connection = self.connect_to_database()
            cursor = connection.cursor()

            table_name = 'students'

            # Check if the table exists before deleting it
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            table_exists = cursor.fetchone()

            if table_exists:
                cursor.execute(f"DROP TABLE {table_name}")
                messagebox.showinfo("Table Deleted", f"The table '{table_name}' has been deleted successfully.")
                self.students_tree.delete(*self.students_tree.get_children())
            else:
                messagebox.showwarning("Table Not Found", f"The table '{table_name}' does not exist.")

            connection.close()

        except Error as e:
            print(f"Error deleting table: {e}")


    def get_selected_row(self, event):
        try:
            selected_row = self.students_tree.focus()
            values = self.students_tree.item(selected_row, 'values')
            self.Student_Id_var.set(values[0])
            self.name_var.set(values[1])
            self.grade_section_var.set(values[2])
            self.email_var.set(values[3])
            self.gender_var.set(values[4])
            self.contact_var.set(values[5])
            self.dob_var.set(values[6])
        except IndexError:
            pass

    def clear_entries(self):
        self.Student_Id_var.set('')
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
#open_student_system()
