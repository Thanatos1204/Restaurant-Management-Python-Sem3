import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import init
import createMenu


class CustomerOrder(init.Base):
    __tablename__ = 'customer_orders'

    id = Column(Integer, primary_key=True)
    customer_name = Column(String)
    table_number = Column(Integer)
    item_name = Column(String)
    quantity = Column(Integer)

# Connect to the database
engine = create_engine('sqlite:///restaurant.db')

# Create tables if not exists
init.Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

def open_customer_screen():
    
    customer_screen = tk.Toplevel()

    def check_menu_availability():
        menu_items = session.query(createMenu.MenuItem).all()
        return bool(menu_items)

    def display_menu():
        menu_label.config(text="Menu:")
        menu_items = session.query(createMenu.MenuItem).all()
        for item in menu_items:
            menu_text = f"{item.name} - {item.category} - ${item.price:.2f}"
            menu_listbox.insert(tk.END, menu_text)

    def submit_order():
        customer_name = customer_name_entry.get()
        table_number = table_number_entry.get()

        if not customer_name or not table_number:
            messagebox.showerror('Error', 'Please enter both name and table number.')
            return

        if not check_menu_availability():
            messagebox.showerror('Error', 'Restaurant is yet to open. Menu is not available.')
            return

        selected_menu_index = menu_listbox.curselection()
        if not selected_menu_index:
            messagebox.showerror('Error', 'Please select an item from the menu.')
            return

        selected_item_text = menu_listbox.get(selected_menu_index)
        selected_item_name = selected_item_text.split(' - ')[0]

        quantity = quantity_var.get()

        # Save the order to the database
        order = CustomerOrder(
            customer_name=customer_name,
            table_number=table_number,
            item_name=selected_item_name,
            quantity=quantity
        )
        session.add(order)
        session.commit()

        messagebox.showinfo('Success', 'Order placed successfully.')

    def view_order():
        #Code to view Order
         table_number = table_number_entry.get()
         orders = session.query(CustomerOrder).filter_by(table_number=table_number).all()

         if not orders:
            messagebox.showinfo('Order Information', 'No orders placed yet.')
            return

         order_info = 'Your Orders:\n'
         for order in orders:
            order_info += f"Item: {order.item_name}, Quantity: {order.quantity}\n"

         messagebox.showinfo('Order Information', order_info)

    def delete_order():
        table_number = table_number_entry.get()
        orders = session.query(CustomerOrder).filter_by(table_number=table_number).all()

        if not orders:
            messagebox.showerror('Error', 'No orders to delete.')
            return

        for order in orders:
            session.delete(order)

        session.commit()
        messagebox.showinfo('Success', 'Order deleted successfully.')

    def change_order():
        table_number = table_number_entry.get()
        orders = session.query(CustomerOrder).filter_by(table_number=table_number).all()

        if not orders:
            messagebox.showerror('Error', 'No orders to change.')
            return

        # Display a new window for changing the order quantity
        change_order_window = tk.Toplevel()
        change_order_window.title('Change Order Quantity')

        order_label = tk.Label(change_order_window, text='Select the order to change:')
        order_label.pack()

        order_listbox = tk.Listbox(change_order_window, width=30, height=5)
        order_listbox.pack(pady=5)

        for order in orders:
            order_text = f"Item: {order.item_name}, Quantity: {order.quantity}"
            order_listbox.insert(tk.END, order_text)

        quantity_label = tk.Label(change_order_window, text='Enter new quantity:')
        quantity_label.pack()

        new_quantity_var = tk.IntVar()
        new_quantity_entry = tk.Entry(change_order_window, textvariable=new_quantity_var)
        new_quantity_entry.pack(pady=5)

        def apply_change():
            selected_order_index = order_listbox.curselection()
            if not selected_order_index:
                messagebox.showerror('Error', 'Please select an order to change.')
                return

            selected_order = orders[selected_order_index[0]]
            selected_order.quantity = new_quantity_var.get()
            session.commit()

            messagebox.showinfo('Success', 'Order quantity changed successfully.')
            change_order_window.destroy()

        apply_change_button = tk.Button(change_order_window, text='Apply Change', command=apply_change)
        apply_change_button.pack(pady=10)


    def exit_system():
        #Code to exit the session
        init.session.close()
        customer_screen.destroy()         

    customer_screen.title('Customer Screen')

    welcome_label = tk.Label(customer_screen, text='Welcome to the Restaurant!')
    welcome_label.pack(pady=10)

    customer_name_label = tk.Label(customer_screen, text='Enter your name:')
    customer_name_label.pack()
    customer_name_entry = tk.Entry(customer_screen)
    customer_name_entry.pack(pady=5)

    table_number_label = tk.Label(customer_screen, text='Enter table number:')
    table_number_label.pack()
    table_number_entry = tk.Entry(customer_screen)
    table_number_entry.pack(pady=5)

    menu_label = tk.Label(customer_screen, text='Menu: (Todays Specials)')
    menu_label.pack()

    menu_listbox = tk.Listbox(customer_screen, width=50, height=10)
    menu_listbox.pack(padx=10, pady=5)

    display_menu()

    quantity_label = tk.Label(customer_screen, text='Enter quantity:')
    quantity_label.pack()
    quantity_var = tk.IntVar()
    quantity_entry = tk.Entry(customer_screen, textvariable=quantity_var)
    quantity_entry.pack(pady=5)

    submit_button = tk.Button(customer_screen, text='Submit Order', command=submit_order)
    submit_button.pack(pady=10)

    view_order_button = tk.Button(customer_screen, text='View Order', command=view_order)
    view_order_button.pack(pady=5)

    delete_order_button = tk.Button(customer_screen, text='Delete Order', command=delete_order)
    delete_order_button.pack(pady=5)

    change_order_button = tk.Button(customer_screen, text='Change Order', command=change_order)
    change_order_button.pack(pady=5)

    exit_button = tk.Button(customer_screen, text='Exit System', command=exit_system)
    exit_button.pack(pady=10)




# Close the session
session.close()
