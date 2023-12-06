import tkinter as tk
from tkinter import messagebox
import init
import createMenu
from tkinter import simpledialog

menu_listbox = None

def open_chef_screen():
    # Code to open the Chef screen goes here
    global menu_listbox
    def add_menu_item():
        # Code to add a new menu item
        name = menu_name_entry.get()
        category = menu_category_entry.get()
        price = menu_price_entry.get()

        # Validate input
        if not name or not category or not price:
            messagebox.showerror('Error', 'Please fill in all fields.')
            return

        # Save the new menu item to the database
        new_item = createMenu.MenuItem(name=name, category=category, price=int(price))
        init.session.add(new_item)
        init.session.commit()

        messagebox.showinfo('Success', 'Menu item added successfully.')
        
        # Clear entry fields after adding the menu item
        menu_name_entry.delete(0, tk.END)
        menu_category_entry.delete(0, tk.END)
        menu_price_entry.delete(0, tk.END)

    def delete_menu_item():
        selected_item_index = menu_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror('Error', 'Please select a menu item to delete.')
            return

        # Get the selected item's name from the listbox
        selected_item_name = menu_listbox.get(selected_item_index)

        # Extract item name from the string (assuming the format is "Name - Category - Price")
        selected_item_name = selected_item_name.split(' - ')[0]

        # Delete the item from the database
        item_to_delete = init.session.query(createMenu.MenuItem).filter_by(name=selected_item_name).first()
        if item_to_delete:
            init.session.delete(item_to_delete)
            init.session.commit()

            messagebox.showinfo('Success', f'Menu item "{selected_item_name}" deleted successfully.')
            view_menu()  # Refresh the displayed menu after deletion

    def update_menu_item():
        # Similar to the delete operation, get the selected item's name
        selected_item_index = menu_listbox.curselection()
        if not selected_item_index:
            messagebox.showerror('Error', 'Please select a menu item to update.')
            return

        selected_item_name = menu_listbox.get(selected_item_index).split(' - ')[0]

        # Fetch the item from the database
        item_to_update = init.session.query(createMenu.MenuItem).filter_by(name=selected_item_name).first()
        if item_to_update:
            # Implement the logic to update the menu item
            # For simplicity, let's assume we are updating the price
            new_price = simpledialog.askinteger('Update Price', f'Enter new price for {selected_item_name}:', parent=chef_screen)

            if new_price is not None:
                item_to_update.price = new_price
                init.session.commit()
                messagebox.showinfo('Success', f'Menu item "{selected_item_name}" updated successfully.')
                view_menu()  # Refresh the displayed menu after update


    def view_menu():
        global menu_listbox
        # Code to view the menu
        menu_items = init.session.query(createMenu.MenuItem).all()

        # Display menu items in a new window (placeholder, customize as needed)
        view_menu_window = tk.Toplevel(chef_screen)
        view_menu_window.title('View Menu')

        # Create a simple listbox to display menu items
        menu_listbox = tk.Listbox(view_menu_window, width=50, height=10)
        menu_listbox.pack(padx=10, pady=10)

        # Populate the listbox with menu items
        for item in menu_items:
            menu_listbox.insert(tk.END, f"{item.name} - {item.category} - ${item.price}")

    def exit_menu():
        #Code to exit the session
        init.session.close()
        chef_screen.destroy()        

    # UI components for the Chef screen
    chef_screen = tk.Tk()
    chef_screen.title('Chef Screen')

    delete_menu_button = tk.Button(chef_screen, text='Delete from Menu', command=delete_menu_item)
    delete_menu_button.grid(row=5, column=1, pady=10)

    update_menu_button = tk.Button(chef_screen, text='Update Menu Item', command=update_menu_item)
    update_menu_button.grid(row=6, column=1, pady=10)

    delete_menu_button = tk.Button(chef_screen, text='Exit from Menu', command=exit_menu)
    delete_menu_button.grid(row=7, column=1, pady=10)

    # Add Menu Item Section
    menu_name_label = tk.Label(chef_screen, text='Menu Item Name:')
    menu_name_entry = tk.Entry(chef_screen)

    menu_category_label = tk.Label(chef_screen, text='Category:')
    menu_category_entry = tk.Entry(chef_screen)

    menu_price_label = tk.Label(chef_screen, text='Price:')
    menu_price_entry = tk.Entry(chef_screen)

    add_menu_item_button = tk.Button(chef_screen, text='Add Menu Item', command=add_menu_item)

    # View Menu Section
    view_menu_button = tk.Button(chef_screen, text='View Menu', command=view_menu)

    # Layout for Add Menu Item Section
    menu_name_label.grid(row=0, column=0, padx=10, pady=10)
    menu_name_entry.grid(row=0, column=1, padx=10, pady=10)
    menu_category_label.grid(row=1, column=0, padx=10, pady=10)
    menu_category_entry.grid(row=1, column=1, padx=10, pady=10)
    menu_price_label.grid(row=2, column=0, padx=10, pady=10)
    menu_price_entry.grid(row=2, column=1, padx=10, pady=10)
    add_menu_item_button.grid(row=3, column=1, pady=20)

    # Layout for View Menu Section
    view_menu_button.grid(row=4, column=1, pady=20)
