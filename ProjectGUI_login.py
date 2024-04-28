import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, master, db_ops, on_login_successful):
        self.master = master
        self.db_ops = db_ops
        self.on_login_successful = on_login_successful
        
        # Create the login frame
        self.frame = tk.Frame(master)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Create labels and entry fields for username and password
        self.username_label = tk.Label(self.frame, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Create the login button
        self.login_button = tk.Button(self.frame, text="Login", command=self.on_login)
        self.login_button.grid(row=2, column=0, padx=10, pady=10)

        # Create the clear button
        self.clear_button = tk.Button(self.frame, text="Clear", command=self.clear_inputs)
        self.clear_button.grid(row=2, column=1, padx=10, pady=10)

    def clear_inputs(self):
        # Clear the username and password entries
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def on_login(self):
        # Get the username and password entered by the user
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Authenticate the user
        user_id = self.db_ops.login(username, password)
        if user_id:
            # Successful login, call the callback function
            self.on_login_successful()
            messagebox.showinfo("Login Successful", f"User ID: {user_id}")
        else:
            # Failed login, show error message
            messagebox.showerror("Login Failed", "Invalid username or password")

    def show(self):
        # Show the login frame and bring it to the foreground
        self.frame.lift()
        self.master.deiconify()
