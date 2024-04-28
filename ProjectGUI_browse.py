import tkinter as tk
from tkinter import ttk
import ast

class BrowseWindow:
    def __init__(self, master, db_ops):
        self.master = master
        self.db_ops = db_ops
        
        # Create a new Toplevel window for the browse window
        self.window = tk.Toplevel(master)
        self.window.title("Browse Products")
        
        # Create a frame for the browse area
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas with a scrollbar for scrolling
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Link the canvas and scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the product widgets
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        
        # Bind the Configure event to update the scroll region
        self.inner_frame.bind("<Configure>", self.update_scroll_region)
        
        # Get the list of categories from db_ops
        self.categories = db_ops.get_categories()  # Retrieve categories from the database
        
        # Add a filter dropdown menu
        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ttk.Combobox(self.window, textvariable=self.filter_var, values=["All"] + self.categories, state="readonly")
        self.filter_menu.pack(pady=10)
        
        # Add a button to apply the filter
        self.filter_button = tk.Button(self.window, text="Filter", command=self.apply_filter)
        self.filter_button.pack()
        
        # Initially display all products
        self.display_products("All")

        #product name filter string #WIPPPPPPPPPPPPPPPPP
        self.product_name_var = tk.StringVar()

        self.product_name_entry = tk.Entry(self.window, textvariable=self.product_name_var)
        self.product_name_entry.pack(pady=5)



    def update_scroll_region(self, event):
        # Update the canvas scroll region to fit the inner frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
     
    def display_products(self, category):
        # Clear the inner frame
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
            
        # Retrieve products from the database based on the category
        if category == "All":
            products = self.db_ops.get_all_products()  # Retrieve all products
        else:
            dict_ = ast.literal_eval(category)
            print(dict_['name'])
            print(self.product_name_var.get().lower())
            products = self.db_ops.get_products_by_category(dict_['name'])  # Retrieve products in the selected category
############################################################################################################################
            #filter out based on string
            for i, product in enumerate(products):
                if self.product_name_var.get().lower() not in product['name'].lower():
                    del products[i]            

        # Display each product in the inner frame
        for product in products:
            # Create a pane for each product
            product_frame = tk.Frame(self.inner_frame, relief=tk.SUNKEN, borderwidth=1)
            product_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Create labels for product details
            name_label = tk.Label(product_frame, text=product['name'], font=('Helvetica', 12, 'bold'))
            name_label.pack(side=tk.TOP, anchor='w', padx=5)
            
            description_label = tk.Label(product_frame, text=product['description'], wraplength=200, font=('Helvetica', 10))
            description_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
            
            price_label = tk.Label(product_frame, text=f"${product['price']:.2f}", font=('Helvetica', 10, 'bold'))
            price_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
            
            category_label = tk.Label(product_frame, text=product['category'], font=('Helvetica', 10, 'italic'))
            category_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)

    
    def apply_filter(self):
        # Get the selected category from the filter menu
        selected_category = self.filter_var.get()  # This is already a string
        
        # Display products based on the selected category
        self.display_products(selected_category)


