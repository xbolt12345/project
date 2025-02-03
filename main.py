import tkinter as tk
from tkinter import messagebox, ttk, filedialog, Menu
from datetime import datetime
import mysql.connector
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
import subprocess

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    database='inventory_system',
    user='root',
    password='tiger123'
)
mycursor = conn.cursor()
date = datetime.now().date()

# Class for generating bills
class BillGenerator:
    def __init__(self, master):
        self.master = master
        self.master.geometry("1000x600")
        self.master.title("Inventory Management System")

        # Setting a consistent font
        self.font_style = ('Arial', 14)

        # Heading
        self.heading = tk.Label(master, text="Inventory Management System", font=('Arial', 24, 'bold'), fg='steelblue')
        self.heading.grid(row=0, column=0, columnspan=3, pady=5, sticky='n')

        # Menu bar
        self.menu_bar = Menu(master)
        master.config(menu=self.menu_bar)

        # Add menu items
        self.create_menu()

        # Search frame
        self.id_label = tk.Label(master, text="Enter Product ID:", font=self.font_style)
        self.id_label.grid(row=1, column=0, sticky='e', padx=5)

        self.id_entry = tk.Entry(master, font=self.font_style, width=15)
        self.id_entry.grid(row=1, column=1, padx=5)

        self.btn_search = tk.Button(master, text="Search", width=12, bg='orange', command=self.search)
        self.btn_search.grid(row=1, column=2, padx=5)

        # Product details frame
        self.name_label = tk.Label(master, text="", font=self.font_style)
        self.name_label.grid(row=2, column=0, columnspan=3, sticky='w', padx=10, pady=5)

        self.stock_label = tk.Label(master, text="", font=self.font_style)
        self.stock_label.grid(row=3, column=0, columnspan=3, sticky='w', padx=10, pady=5)

        self.price_label = tk.Label(master, text="", font=self.font_style)
        self.price_label.grid(row=4, column=0, columnspan=3, sticky='w', padx=10, pady=5)

        # Quantity input
        self.quantity_label = tk.Label(master, text="Enter Quantity:", font=self.font_style)
        self.quantity_label.grid(row=5, column=0, sticky='e', padx=5, pady=5)

        self.quantity_entry = tk.Entry(master, font=self.font_style, width=15)
        self.quantity_entry.grid(row=5, column=1, padx=5, pady=5)

        # Add to bill button
        self.btn_add_to_bill = tk.Button(master, text="Add to Bill", width=15, bg='steelblue', fg='black', command=self.add_to_bill)
        self.btn_add_to_bill.grid(row=5, column=2, padx=5)

        # Bill text box and scrollbar
        self.bill_box = tk.Text(master, width=60, height=18, wrap=tk.WORD, font=self.font_style)
        self.bill_box.grid(row=6, column=0, columnspan=3, pady=5)

        self.scrollbar = tk.Scrollbar(master, command=self.bill_box.yview)
        self.scrollbar.grid(row=6, column=3, sticky='ns')
        self.bill_box.configure(yscrollcommand=self.scrollbar.set)

        # Total amount label
        self.total_label = tk.Label(master, text="", font=('Arial', 18, 'bold'), fg='green')
        self.total_label.grid(row=7, column=0, columnspan=3, pady=5)

        # Print Bill button
        self.btn_print_bill = tk.Button(master, text="Print Bill", width=15, bg='green', fg='black', command=self.print_bill)
        self.btn_print_bill.grid(row=7, column=2, padx=5)

        # Initialize total amount
        self.total_amount = 0

        # Initialize inventory treeview
        self.inventory_frame = tk.Frame(master)
        self.inventory_frame.grid(row=1, column=4, rowspan=6, sticky='n')

        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=('ID', 'Name', 'Stock', 'Price'), show='headings')
        self.inventory_tree.heading('ID', text='ID')
        self.inventory_tree.heading('Name', text='Name')
        self.inventory_tree.heading('Stock', text='Stock')
        self.inventory_tree.heading('Price', text='Price')
        
        self.inventory_tree.grid(row=0, column=0, sticky='nsew')

        self.inventory_scrollbar = tk.Scrollbar(self.inventory_frame, orient=tk.VERTICAL, command=self.inventory_tree.yview)
        self.inventory_scrollbar.grid(row=0, column=1, sticky='ns')
        
        self.inventory_tree.configure(yscrollcommand=self.inventory_scrollbar.set)

        self.load_inventory()

    def create_menu(self):
        # Create "File" menu
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Add to Database", command=self.open_add_to_database)
        file_menu.add_command(label="Update Database", command=self.open_update_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)

        # Add "File" menu to menu bar
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def open_add_to_database(self):
        # Open the add_to_Database.py script using subprocess
        subprocess.Popen(["python3", "/Users/atharvjoshi/Desktop/cs/inventory/add_to_db.py"])


    def open_update_database(self):
        # Open the update.py script using subprocess
        subprocess.Popen(["python3", "/Users/atharvjoshi/Desktop/cs/inventory/update.py"])

    def load_inventory(self):
        # Load inventory from database and update the treeview
        mycursor.execute("SELECT * FROM inventory")
        rows = mycursor.fetchall()
        
        # Clear the treeview before inserting new rows
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)

        for row in rows:
            self.inventory_tree.insert('', tk.END, values=row)

    def search(self):
        # Search for product in database
        product_id = self.id_entry.get()
        mycursor.execute("SELECT * FROM inventory WHERE id = %s", [product_id])
        product = mycursor.fetchone()

        if product:
            self.product_name = product[1]
            self.product_stock = product[2]
            self.product_price = product[3]

            # Display product details
            self.name_label.configure(text=f"Product Name: {self.product_name}")
            self.stock_label.configure(text=f"Stock: {self.product_stock}")
            self.price_label.configure(text=f"Price: ₹{self.product_price}")
        else:
            # Show error if product is not found
            messagebox.showerror("Error", "Product not found")

    def add_to_bill(self):
        product_id = self.id_entry.get()

        # Add product to bill
        try:
            quantity = int(self.quantity_entry.get())
            if quantity > self.product_stock:
                messagebox.showerror("Error", "Insufficient stock")
            else:
                total_price = quantity * self.product_price
                self.bill_box.insert(tk.END, f"Product: {self.product_name}\nQuantity: {quantity}\nPrice: ₹{total_price}\n\n")
                
                # Update total amount and display it
                self.total_amount += total_price
                self.total_label.configure(text=f"Total: ₹{self.total_amount}")

                # Update product stock in the database
                updated_stock = self.product_stock - quantity
                mycursor.execute("UPDATE inventory SET stock = %s WHERE id = %s", (updated_stock, product_id))
                conn.commit()

                # Update transaction history in the database
                mycursor.execute("INSERT INTO transaction(product_name, quantity, amount, date) VALUES (%s, %s, %s, %s)",
                                 (self.product_name, quantity, total_price, date))
                conn.commit()

                # Clear quantity entry
                self.quantity_entry.delete(0, tk.END)

                # Show success message
                messagebox.showinfo("Success", "Product added to bill")

                # Refresh the inventory list
                self.load_inventory()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity")

    def print_bill(self):
        # Open file save dialog for the user to specify where to save the PDF file
        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Save Bill As")
    
        # Check if the user selected a file path
        if filename:
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)
        
            # Bill header
            c.drawString(100, 700, "Bill Summary")
        
            # Bill content
            lines = self.bill_box.get("1.0", tk.END).split("\n")
            y = 680
        
            for line in lines:
                if line:
                    c.drawString(100, y, line)
                    y -= 15
        
            # Total amount
            c.drawString(100, y, f"Total: ₹{self.total_amount}")
        
            # Save and close the PDF file
            c.showPage()
            c.save()
        
            # Show success message
            messagebox.showinfo("Success", "Bill saved as PDF")
    
# Main function
if __name__ == '__main__':
    root = tk.Tk()
    app = BillGenerator(root)
    root.mainloop()