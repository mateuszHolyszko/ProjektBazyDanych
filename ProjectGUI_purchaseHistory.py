import tkinter as tk
from utilities import extract_numerical

class PurchaseHistoryWindow:
    def __init__(self, master, db_ops, user_id):
        self.master = master
        self.db_ops = db_ops
        self.user_id = extract_numerical(str(user_id))
        print(str(self.user_id))
        
        # Create a new Toplevel window for the browse window
        self.window = tk.Toplevel(master)
        self.window.title("PurchaseHistory")
        
        # Add a label for purchase history
        self.label = tk.Label(self.window, text="Purchase History")
        self.label.pack(pady=20)
        
        # Display purchase history
        self.display_purchase_history()
        
    def display_purchase_history(self):
        # Retrieve purchase history for the user
        purchase_history = self.db_ops.get_purchase_history(self.user_id)
        
        if purchase_history:
            # Display purchase history in a listbox or other suitable format
            for purchase in purchase_history:
                purchase_info = f"Name: {purchase[0]}, Description: {purchase[1]}, Price: {purchase[2]}, Category: {purchase[3]}"
                purchase_label = tk.Label(self.window, text=purchase_info)
                purchase_label.pack()
        else:
            # If no purchase history found, display a message
            no_purchase_label = tk.Label(self.window, text="No purchase history found.")
            no_purchase_label.pack()
