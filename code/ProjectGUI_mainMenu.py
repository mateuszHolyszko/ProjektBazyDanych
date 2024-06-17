import tkinter as tk
from ProjectGUI_browse import BrowseWindow

class MainMenuWindow:
    def __init__(self, master, db_ops, on_browse, on_purchase_history, on_recommended, on_logout, on_exit, user_id):
        self.master = master
        self.db_ops = db_ops
        self.user_id = user_id
        
        # Create a frame to encapsulate the main menu widgets
        self.frame = tk.Frame(master)
        self.frame.grid(row=0, column=0, padx=10, pady=10)
        
        # Add buttons for each option
        self.browse_button = tk.Button(self.frame, text="Browse", command=lambda: on_browse(user_id))
        self.browse_button.grid(row=0, column=0, padx=10, pady=5)

        self.purchase_history_button = tk.Button(self.frame, text="Purchase History", command=lambda: on_purchase_history(user_id))
        self.purchase_history_button.grid(row=1, column=0, padx=10, pady=5)

        self.recommended_button = tk.Button(self.frame, text="Recommended", command=lambda: on_recommended(user_id))
        self.recommended_button.grid(row=2, column=0, padx=10, pady=5)

        self.logout_button = tk.Button(self.frame, text="Log Out", command=on_logout)
        self.logout_button.grid(row=3, column=0, padx=10, pady=5)

        self.exit_button = tk.Button(self.frame, text="Exit", command=on_exit)
        self.exit_button.grid(row=4, column=0, padx=10, pady=5)
        
    def show(self):
        # Show the main menu window by raising the frame and showing the main application window
        self.frame.lift()
        self.master.deiconify()

