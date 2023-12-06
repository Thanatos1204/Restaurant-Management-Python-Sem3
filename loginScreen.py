import tkinter as tk
from tkinter import messagebox
import init
import chef_screen
import customer_screen
import employee_screen

def authenticate_user(username, password):
    user = init.session.query(init.User).filter_by(username=username, password=password).first()
    return user

def login():
    username = username_entry.get()
    password = password_entry.get()

    user = authenticate_user(username, password)

    if user:
        messagebox.showinfo('Login Successful', f'Welcome, {user.role}!')
        # Proceed to the respective screen based on user role
        if user.role == 'Chef':
            chef_screen.open_chef_screen()
        elif user.role == 'Employee':
            employee_screen.open_employee_screen()
        elif user.role == 'Customer':
            customer_screen.open_customer_screen()
    else:
        messagebox.showerror('Login Failed', 'Invalid username or password')
        init.session.close()

# Create the login window
login_window = tk.Tk()
login_window.title('Restaurant Management System - Login')

# UI components
username_label = tk.Label(login_window, text='Username:')
username_entry = tk.Entry(login_window)
password_label = tk.Label(login_window, text='Password:')
password_entry = tk.Entry(login_window, show='*')
login_button = tk.Button(login_window, text='Login', command=login)

# Layout
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry.grid(row=0, column=1, padx=10, pady=10)
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry.grid(row=1, column=1, padx=10, pady=10)
login_button.grid(row=2, column=1, pady=20)

# Run the Tkinter main loop
login_window.mainloop()
