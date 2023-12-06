import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fpdf import FPDF
import init
import customer_screen
import createMenu


# Connect to the database
engine = create_engine('sqlite:///restaurant.db')

# Create tables if not exists
init.Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def open_employee_screen():
    employee_screen = tk.Toplevel()

    def calculate_subtotal(orders):
        subtotal = 0
        for order in orders:
            item = session.query(createMenu.MenuItem).filter_by(name=order.item_name).first()
            subtotal += item.price * order.quantity
        return subtotal

    def calculate_gst(amount):
        return 0.05 * amount

    def calculate_ambience_tax(amount):
        return 0.03 * amount

    def calculate_discount(amount):
        return 0.10 * amount

    def calculate_total(subtotal, gst, ambience_tax, discount):
        return subtotal + gst + ambience_tax - discount

    def print_bill(orders, subtotal, gst, ambience_tax, discount, total):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Restaurant Bill", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(50, 10, txt="Item", ln=True)
        pdf.cell(50, 10, txt="Quantity", ln=True)
        pdf.cell(50, 10, txt="Price", ln=True)
        pdf.ln(5)

        for order in orders:
            item = session.query(createMenu.MenuItem).filter_by(name=order.item_name).first()
            pdf.cell(50, 10, txt=item.name, ln=True)
            pdf.cell(50, 10, txt=str(order.quantity), ln=True)
            pdf.cell(50, 10, txt=f"${item.price * order.quantity:.2f}", ln=True)

        pdf.ln(10)
        pdf.cell(50, 10, txt=f"Subtotal: ${subtotal:.2f}", ln=True)
        pdf.cell(50, 10, txt=f"GST (5%): ${gst:.2f}", ln=True)
        pdf.cell(50, 10, txt=f"Ambience Tax (3%): ${ambience_tax:.2f}", ln=True)
        pdf.cell(50, 10, txt=f"Loyalty Discount (10%): ${discount:.2f}", ln=True)
        pdf.cell(50, 10, txt=f"Total: ${total:.2f}", ln=True)
        table_number = table_number_entry.get()
        pdf_filename = f"bill_table_{table_number}.pdf"
        pdf.output(pdf_filename)

    def create_bill():
        table_number = table_number_entry.get()
        orders = session.query(customer_screen.CustomerOrder).filter_by(table_number=table_number).all()

        if not orders:
            messagebox.showerror('Error', 'No orders for the specified table.')
            return

        subtotal = calculate_subtotal(orders)
        gst = calculate_gst(subtotal)
        ambience_tax = calculate_ambience_tax(subtotal)
        discount = calculate_discount(subtotal)
        total = calculate_total(subtotal, gst, ambience_tax, discount)

        print_bill(orders, subtotal, gst, ambience_tax, discount, total)
        messagebox.showinfo('Bill Created', 'Bill created successfully.')
    
    def view_bill():
        table_number = table_number_entry.get()
        orders = session.query(customer_screen.CustomerOrder).filter_by(table_number=table_number).all()

        if not orders:
            messagebox.showerror('Error', 'No orders for the specified table.')
            return

        subtotal = calculate_subtotal(orders)
        gst = calculate_gst(subtotal)
        ambience_tax = calculate_ambience_tax(subtotal)
        discount = calculate_discount(subtotal)
        total = calculate_total(subtotal, gst, ambience_tax, discount)

        view_bill_window = tk.Toplevel()
        view_bill_window.title('Bill Preview')

        bill_text = f"Item\t\tQuantity\t\tPrice\n"
        for order in orders:
            item = session.query(createMenu.MenuItem).filter_by(name=order.item_name).first()
            bill_text += f"{item.name}\t\t{order.quantity}\t\t${item.price * order.quantity:.2f}\n"

        bill_text += f"\nSubtotal: ${subtotal:.2f}\n"
        bill_text += f"GST (5%): ${gst:.2f}\n"
        bill_text += f"Ambience Tax (3%): ${ambience_tax:.2f}\n"
        bill_text += f"Loyalty Discount (10%): ${discount:.2f}\n"
        bill_text += f"Total: ${total:.2f}\n"

        bill_label = tk.Label(view_bill_window, text=bill_text)
        bill_label.pack()

    employee_screen.title('Employee Screen')

    table_number_label = tk.Label(employee_screen, text='Enter table number:')
    table_number_label.pack()
    table_number_entry = tk.Entry(employee_screen)
    table_number_entry.pack(pady=5)

    create_bill_button = tk.Button(employee_screen, text='Create Bill', command=create_bill)
    create_bill_button.pack(pady=10)

    # Additional buttons for taxes and discounts
    def add_gst():
        messagebox.showinfo('GST Added', 'GST (5%) added to the bill.')
    
    def add_ambience_tax():
        messagebox.showinfo('Ambience Tax Added', 'Ambience Tax (3%) added to the bill.')
    
    def add_loyalty_discount():
        messagebox.showinfo('Loyalty Discount Added', 'Loyalty Discount (10%) added to the bill.')

    add_gst_button = tk.Button(employee_screen, text='Add GST (5%)', command=add_gst)
    add_gst_button.pack(pady=5)

    add_ambience_tax_button = tk.Button(employee_screen, text='Add Ambience Tax (3%)', command=add_ambience_tax)
    add_ambience_tax_button.pack(pady=5)

    add_loyalty_discount_button = tk.Button(employee_screen, text='Add Loyalty Discount (10%)', command=add_loyalty_discount)
    add_loyalty_discount_button.pack(pady=5)    

    view_bill_button = tk.Button(employee_screen, text='View Bill', command=view_bill)
    view_bill_button.pack(pady=10)

    print_bill_button = tk.Button(employee_screen, text='Print Bill', command=print_bill)
    print_bill_button.pack(pady=10)

    




# Close the session
session.close()
