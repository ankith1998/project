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

def on_enter(e):
    generate_button['background'] = '#0052cc'
    generate_button['foreground'] = '#ffffff'

def on_leave(e):
    generate_button['background'] = '#ffffff'
    generate_button['foreground'] = '#000000'
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

# Bind hover effects
generate_button.bind("<Enter>", on_enter)
generate_button.bind("<Leave>", on_leave)

# Run the application
root.mainloop()
