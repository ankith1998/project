import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
from tkcalendar import DateEntry
import pandas as pd
from sqlalchemy import create_engine
import openpyxl
import datetime
from tkinter import font

def generate_report():
    selected_date = date_entry.get_date().strftime('%Y-%m-%d')
    # Database connection and data processing logic here
    # Example:
    engine = create_engine('sqlite:///your_database.db')  # Replace with your actual database connection string
    query = f"SELECT * FROM your_table WHERE date_column = '{selected_date}'"
    df = pd.read_sql(query, engine)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    hourly_avg = df.resample('H').mean()
    hourly_avg.to_excel('report.xlsx', engine='openpyxl')
    messagebox.showinfo("Success", "Report generated successfully!")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

# def on_enter(e):
#     generate_button['background'] = '#0052cc'
#     generate_button['foreground'] = '#ffffff'

# def on_leave(e):
#     generate_button['background'] = '#ffffff'
#     generate_button['foreground'] = '#000000'

def open_login_screen():
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    center_window(login_window, 300, 200)

    ttk.Label(login_window, text="Username:").grid(column=0, row=0, padx=10, pady=10)
    username_entry = ttk.Entry(login_window)
    username_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(login_window, text="Password:").grid(column=0, row=1, padx=10, pady=10)
    password_entry = ttk.Entry(login_window, show="*")
    password_entry.grid(column=1, row=1, padx=10, pady=10)

    login_button = ttk.Button(login_window, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), login_window))
    login_button.grid(column=0, row=2, columnspan=2, pady=10)

def login(username, password,screen):
    # Replace with actual authentication logic
    if username == "admin" and password == "password":
        messagebox.showinfo("Login Success", "Welcome, Admin!")
        open_admin_options()  # Open the admin options window on successful login
        screen.destroy()  # Close the window on successful creation
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        screen.lift()  # Bring the login window to the front

def open_admin_options():
    global admin_window
    if 'admin_window' in globals() and admin_window.winfo_exists():
        admin_window.destroy()
    admin_window = tk.Toplevel(root)
    admin_window.title("Admin Options")
    center_window(admin_window, 300, 200)

    # Configure grid to center widgets
    admin_window.grid_rowconfigure(0, weight=1)
    admin_window.grid_rowconfigure(1, weight=1)
    admin_window.grid_rowconfigure(2, weight=1)
    admin_window.grid_columnconfigure(0, weight=1)

    ttk.Button(admin_window, text="Add Database Details", command=lambda: close_and_open(add_database_details)).grid(column=0, row=0, padx=10, pady=10)
    ttk.Button(admin_window, text="Add Admin", command=lambda: close_and_open(open_add_admin_window)).grid(column=0, row=1, padx=10, pady=10)

def close_and_open(func):
    admin_window.destroy()
    func()

def open_add_admin_window():
    add_admin_window = tk.Toplevel(root)
    add_admin_window.title("Add Admin")
    center_window(add_admin_window, 300, 200)

    ttk.Label(add_admin_window, text="Username:").grid(column=0, row=0, padx=10, pady=10)
    username_entry = ttk.Entry(add_admin_window)
    username_entry.grid(column=1, row=0, padx=10, pady=10)

    ttk.Label(add_admin_window, text="Password:").grid(column=0, row=1, padx=10, pady=10)
    password_entry = ttk.Entry(add_admin_window, show="*")
    password_entry.grid(column=1, row=1, padx=10, pady=10)

    ttk.Label(add_admin_window, text="Confirm Password:").grid(column=0, row=2, padx=10, pady=10)
    confirm_password_entry = ttk.Entry(add_admin_window, show="*")
    confirm_password_entry.grid(column=1, row=2, padx=10, pady=10)

    submit_button = ttk.Button(add_admin_window, text="Submit", command=lambda: submit_admin(username_entry.get(), password_entry.get(), confirm_password_entry.get(), add_admin_window))
    submit_button.grid(column=0, row=3, columnspan=2, pady=10)

    back_button = ttk.Button(add_admin_window, text="Back", command=lambda: go_back_to_admin_options(add_admin_window))
    back_button.grid(column=0, row=4, columnspan=2, pady=10)

def go_back_to_admin_options(window):
    window.destroy()
    open_admin_options()  # Show the admin options window again

def submit_admin(username, password, confirm_password,window):
    if password == confirm_password:
        # Add logic to save the new admin details
        messagebox.showinfo("Success", "Admin added successfully!")
        window.destroy()  # Close the window on successful creation
        if 'admin_window' in globals() and admin_window.winfo_exists():
            admin_window.deiconify()  # Show the admin options window again
    else:
        messagebox.showerror("Error", "Passwords do not match. Please try again.")

def add_database_details():
    # Functionality to add database details
    messagebox.showinfo("Add Database Details", "This feature is under construction.")

# def add_admin():
#     # Functionality to add a new admin
#     messagebox.showinfo("Add Admin", "This feature is under construction.")  
# Create the main window
root = tk.Tk()
root.title("Reporting Software")

# Set window size
center_window(root, 400, 200)   # Set the window size to 400x300 pixels

# Define font
custom_font = font.Font(family="Times New Roman", size=10)

# Configure grid to center widgets
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Date selection with DateEntry and default to current date
ttk.Label(root, text="Select Date:", font=custom_font).grid(column=0, row=0, padx=10, pady=10,sticky="e")
current_date = datetime.date.today()
date_entry = DateEntry(root, width=12, background='teal', foreground='#000000', borderwidth=2, font=custom_font, year=current_date.year, month=current_date.month, day=current_date.day)
date_entry.grid(column=1, row=0, padx=10, pady=10,sticky="w")

# Create a style for the button
style = ttk.Style()
style.configure('TButton', font=('Arial', 8), background='#ffffff', foreground='#000000')

# Generate button
generate_button = ttk.Button(root, text="Generate Report", command=generate_report,style='TButton')
generate_button.grid(column=0, row=1, columnspan=2, padx=15, pady=15)

# # Bind hover effects
# generate_button.bind("<Enter>", on_enter)
# generate_button.bind("<Leave>", on_leave)

# Admin Center button
admin_button = ttk.Button(root, text="Admin Center", command=open_login_screen)
admin_button.grid(column=1, row=2, padx=10, pady=10, sticky="se")

# Run the application
root.mainloop()
