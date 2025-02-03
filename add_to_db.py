from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
from mysql.connector import Error

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    database='inventory_system',
    user='root',
    password='tiger123'
)
mycursor = conn.cursor()
mycursor.execute("SELECT MAX(id) FROM inventory")
result = mycursor.fetchall()
id = result[0][0] if result else 0

class DatabaseAdder:
    def __init__(self, master):
        self.master = master
        self.master.title("Add to Database")
        self.master.geometry("800x400")

        # Create frame for the form
        self.form_frame = Frame(master, padx=20, pady=20)
        self.form_frame.pack(pady=20, expand=True, fill=BOTH)

        # Heading
        self.heading = Label(self.form_frame, text="Add to the Database", font=('Arial', 18, 'bold'), fg='steelblue')
        self.heading.grid(row=0, column=0, columnspan=2, pady=10)

        # Labels and entries for input fields
        self.create_form_field("Product Name", 1, self.form_frame)
        self.create_form_field("Stock", 2, self.form_frame)
        self.create_form_field("Price", 3, self.form_frame)

        # Buttons
        self.btn_add = Button(self.form_frame, text="Add to Database", width=20, bg='steelblue', fg='black', command=self.add_item)
        self.btn_add.grid(row=4, column=0, pady=10, sticky='ew')

        self.btn_clear = Button(self.form_frame, text="Clear All Fields", width=20, bg='gray', fg='black', command=self.clear_all)
        self.btn_clear.grid(row=4, column=1, pady=10, sticky='ew')

        # Log text box
        self.log_box = Text(master, width=80, height=6, padx=20, pady=10, wrap='word')
        self.log_box.pack(pady=10, fill=BOTH, expand=True)
        self.log_box.insert(END, f"ID has reached up to: {id}")

    def create_form_field(self, label_text, row, parent_frame):
        # Label
        label = Label(parent_frame, text=f"Enter {label_text}:", font=('Arial', 12))
        label.grid(row=row, column=0, sticky='w', pady=5)

        # Entry
        entry = Entry(parent_frame, width=30, font=('Arial', 12))
        entry.grid(row=row, column=1, pady=5, sticky='ew')
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def add_item(self):
        # Get values from entries
        name = self.product_name_entry.get().strip()
        stock = self.stock_entry.get().strip()
        price = self.price_entry.get().strip()

        # Check if all fields are filled
        if not name or not stock or not price:
            messagebox.showinfo("Error", "Please fill all the fields.")
            return

        # Validate that stock and price are numeric
        try:
            stock = int(stock)
            price = float(price)
        except ValueError:
            messagebox.showerror("Error", "Stock must be an integer and price must be a number.")
            return

        # Insert data into the database
        mycursor.execute("INSERT INTO inventory (name, stock, price) VALUES (%s, %s, %s)", (name, stock, price))
        conn.commit()
        messagebox.showinfo("Success", "Item added to the database successfully.")

        # Clear all fields after successful addition
        self.clear_all()

    def clear_all(self):
        self.product_name_entry.delete(0, END)
        self.stock_entry.delete(0, END)
        self.price_entry.delete(0, END)

def main2():
    root = Tk()
    app = DatabaseAdder(root)
    root.mainloop()

if __name__ == "__main__":
    main2()
