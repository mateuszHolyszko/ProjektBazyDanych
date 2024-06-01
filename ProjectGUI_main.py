import tkinter as tk
from tkinter import messagebox
from DBoperations import DBoperations
from ProjectGUI_login import LoginWindow
from ProjectGUI_mainMenu import MainMenuWindow
from ProjectGUI_browse import BrowseWindow
from ProjectGUI_purchaseHistory import PurchaseHistoryWindow
from ProjectGUI_recommendedWindow import RecommendedWindow

# Initialize the database connection
connection_string = 'mat/1324@172.33.5.17:1521/xe'
db_ops = DBoperations(connection_string)

# Callback function to close the database connection when the application exits
def on_closing():
    db_ops.close_connection()
    root.destroy()

def on_browse(user_id): #WIP +++++++++++++++++++++++++++++
    #retrive products
    
    browse_window = BrowseWindow(root, db_ops, user_id)
    browse_window.window.deiconify()  # Show the browse window

def on_purchase_history(user_id): #WIP +++++++++++++++++++++++++++++
    purchase_history_window = PurchaseHistoryWindow(root, db_ops, user_id)
    purchase_history_window.window.deiconify()  # Show the purchase history window

def on_recommended(user_id):  #WIP +++++++++++++++++++++++++++++
    recommended_window = RecommendedWindow(root, db_ops, user_id)
    recommended_window.window.deiconify()  # Show the recommended window

def on_logout(): #WIP +++++++++++++++++++++++++++++
    messagebox.showinfo("Log Out", "Logged out successfully!")
    root.withdraw()  # Hide the main window 
    # Create an instance of the LoginWindow class
    login_window = LoginWindow(root, db_ops, on_login_successful)
    # Show the login window
    login_window.show()

def clear_existing_widgets():
    # Clear existing widgets from the main application window
    for widget in root.winfo_children():
        widget.destroy()


# Function to handle successful login
def on_login_successful(user_id):
    # Clear existing widgets from the main application window
    clear_existing_widgets()
    
    # Show the main menu
    main_menu_window = MainMenuWindow(root, db_ops, on_browse, on_purchase_history, on_recommended, on_logout, on_exit, user_id)
    main_menu_window.show()

def on_exit():
    root.destroy()  # Close the main application window

# Create the main application window
root = tk.Tk()
root.title("Application")

# Set up the application close event to close the database connection
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the application by showing the login window
login_window = LoginWindow(root, db_ops, on_login_successful)

# Start the Tkinter event loop
root.mainloop()
