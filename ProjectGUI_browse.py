import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from utilities import extract_numerical
import ast

class BrowseWindow:
    def __init__(self, master, db_ops, user_id):
        self.master = master
        self.db_ops = db_ops

        self.user_id = extract_numerical(str(user_id))
        print(str(self.user_id))

        # Initialize total_price attribute
        self.total_price = 0
        
        # Create a new Toplevel window for the browse window
        self.window = tk.Toplevel(master)
        self.window.title("Browse Products, userId: "+ str(user_id))
        self.window.minsize(400, 400)
        
        # Create a frame for the browse area
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)
        
        # Create a canvas with a scrollbar for scrolling
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Link the canvas and scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Calculate the center coordinates of the canvas TODO: updet when resize
        canvas_width = self.canvas.winfo_reqwidth()
        canvas_height = self.canvas.winfo_reqheight()
        center_x = canvas_width // 2
        center_y = canvas_height // 2

        # Create a frame inside the canvas to hold the product widgets
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window(center_x, center_y, window=self.inner_frame, anchor='center')
        
        # Bind the Configure event to update the scroll region
        self.inner_frame.bind("<Configure>", self.update_scroll_region)
        
        # Get the list of categories from db_ops
        self.categories = db_ops.get_categories()  # Retrieve categories from the database
        
        # Add a filter dropdown menu
        self.filter_var = tk.StringVar(value="All")
        self.filter_menu = ttk.Combobox(self.window, textvariable=self.filter_var, values=["All"] + self.categories, state="readonly")
        self.filter_menu.pack(pady=10)

        #product name filter string #WIPPPPPPPPPPPPPPPPP
        self.product_name_var = tk.StringVar()

        self.product_name_entry = tk.Entry(self.window, textvariable=self.product_name_var)
        self.product_name_entry.pack(pady=10)
        
        # Add a button to apply the filter
        self.filter_button = tk.Button(self.window, text="Filter", command=self.apply_filter)
        self.filter_button.pack()

        ######################## shoping cart START
         # Create a frame for the shopping cart on the right side
        self.cart_frame = tk.Frame(self.window, width=200, bd=2, relief=tk.SOLID)
        self.cart_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)

        # Create a label for the shopping cart title
        cart_title_label = tk.Label(self.cart_frame, text="Shopping Cart", font=('Helvetica', 12, 'bold'))
        cart_title_label.pack(pady=5)

        # Create a listbox to display added products in the shopping cart
        self.cart_listbox = tk.Listbox(self.cart_frame, width=30, height=10)
        self.cart_listbox.pack(expand=True, fill=tk.BOTH)

        # Create a label to display the total price of the products in the shopping cart
        self.total_price_label = tk.Label(self.cart_frame, text="Total Price: $0.00", font=('Helvetica', 10))
        self.total_price_label.pack(pady=5)

        # Create a checkout button
        self.checkout_button = tk.Button(self.cart_frame, text="Checkout", command=self.checkout)
        self.checkout_button.pack(pady=5)
        ######################## shoping cart END
        
        # Initially display all products
        self.display_products("All")



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
############################################################################################################################not working?
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
            
            # Retrieve and display the average rating as stars
            print(product)
            average_rating = self.db_ops.get_average_rating(product['id'])
            rating_frame = tk.Frame(product_frame)
            rating_frame.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
            
            for i in range(1, 6):
                star_label = tk.Label(rating_frame, text="★", font=('Helvetica', 10), fg='gold' if i <= average_rating else 'grey')
                star_label.pack(side=tk.LEFT)

            # Create a purchase button
            purchase_button = tk.Button(product_frame, text="Purchase", command=lambda p=product: self.purchase_product(p))
            purchase_button.pack(side=tk.LEFT, anchor='w', padx=5, pady=5)
            
            # Create a button to show reviews in a popup
            show_reviews_button = tk.Button(product_frame, text="Show Reviews", command=lambda p=product: self.show_reviews(p['id']))
            show_reviews_button.pack(side=tk.LEFT, anchor='w', padx=5, pady=5)

    
    def show_reviews(self, product_id):
        # Retrieve text reviews for the product
        text_reviews = self.db_ops.get_text_reviews(product_id)
        
        # Create a popup window to display the reviews
        reviews_popup = tk.Toplevel(self.window)
        reviews_popup.title("Text Reviews")
        
        if text_reviews:
            for review in text_reviews:
                review_label = tk.Label(reviews_popup, text=review, wraplength=400, justify=tk.LEFT)
                review_label.pack(pady=5)
        else:
            no_reviews_label = tk.Label(reviews_popup, text="No reviews found for this product.")
            no_reviews_label.pack(pady=5)

    def apply_filter(self):
        # Get the selected category from the filter menu
        selected_category = self.filter_var.get()  # This is already a string
        
        # Display products based on the selected category
        self.display_products(selected_category)

    def purchase_product(self, product):
        # Add the purchased product to the shopping cart
        self.cart_listbox.insert(tk.END, product['name'])
        # Update the total price
        # Assume product price is stored in 'price' key
        price = product.get('price', 0)
        self.total_price += price
        self.total_price_label.config(text=f"Total Price: ${self.total_price:.2f}")

    def checkout(self):
        # Perform checkout operation
        # Retrieve selected product IDs from the cart_listbox
        selected_product_names = []
        for i in range(self.cart_listbox.size()):
            selected_product_names.append(self.cart_listbox.get(i))
        print(selected_product_names)

        # Save purchase history
        if self.db_ops.save_purchase_history(self.user_id, selected_product_names):
            messagebox.showinfo("Checkout", "Checkout completed successfully!")
            # Clear the cart_listbox after successful checkout
            self.cart_listbox.delete(0, tk.END)
            # Reset total price
            self.total_price = 0
            self.total_price_label.config(text="Total Price: $0.00")
        else:
            messagebox.showerror("Checkout", "Failed to complete checkout!")

        #update users feature if nessecery
        self.db_ops.update_user_feature(self.user_id)


