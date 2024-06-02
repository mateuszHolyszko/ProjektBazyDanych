import tkinter as tk
from tkinter import ttk, messagebox
from RecommendationAlgorithm import RecommendationAlgorithm
from utilities import extract_numerical

class RecommendedWindow:
    def __init__(self, master, db_ops, user_id):
        self.master = master
        self.db_ops = db_ops

        self.user_id = extract_numerical(str(user_id))
        print(str(self.user_id))

        # Initialize total_price attribute
        self.total_price = 0
        
        # Create a new Toplevel window for the recommended products window
        self.window = tk.Toplevel(master)
        self.window.title("Recommended Products, userId: "+ str(user_id))
        self.window.minsize(600, 400)
        
        # Create a frame for the top choice
        self.top_choice_frame = tk.Frame(self.window, bd=2, relief=tk.SOLID)
        self.top_choice_frame.pack(fill=tk.X, pady=10, padx=10)

        # Create a label for the top choice title
        top_choice_title_label = tk.Label(self.top_choice_frame, text="Top Choice for You", font=('Helvetica', 14, 'bold'))
        top_choice_title_label.pack(pady=5)

        # Create a frame for the shopping cart on the left side
        self.cart_frame = tk.Frame(self.window, width=200, bd=2, relief=tk.SOLID)
        self.cart_frame.pack(fill=tk.Y, side=tk.LEFT, padx=10, pady=10)

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

        # Create a frame for the browse area
        self.frame = tk.Frame(self.window)
        self.frame.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT, padx=10, pady=10)
        
        # Create a canvas with a horizontal scrollbar for scrolling
        self.canvas = tk.Canvas(self.frame)
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Link the canvas and scrollbar
        self.canvas.config(xscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the product widgets
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        
        # Bind the Configure event to update the scroll region
        self.inner_frame.bind("<Configure>", self.update_scroll_region)

        # Display recommended products
        self.display_recommended_products()

    def update_scroll_region(self, event):
        # Update the canvas scroll region to fit the inner frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def display_recommended_products(self):
        # Clear the inner frame
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        # Get recommended product IDs
        recommender = RecommendationAlgorithm(self.db_ops, self.user_id)
        recommended_product_ids = recommender.get_recommendations()

        # Retrieve products by their IDs
        all_products = self.db_ops.get_all_products()
        recommended_products = [product for product in all_products if product['id'] in recommended_product_ids]

        # Display the top choice product separately
        if recommended_products:
            top_choice_product = recommended_products.pop(0)
            self.display_top_choice(top_choice_product)

        # Display each recommended product in the inner frame
        for product in recommended_products:
            # Create a pane for each product
            product_frame = tk.Frame(self.inner_frame, relief=tk.SUNKEN, borderwidth=1)
            product_frame.pack(side=tk.LEFT, fill=tk.Y, pady=5, padx=10)
            
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

    def display_top_choice(self, product):
        # Clear the top choice frame
        for widget in self.top_choice_frame.winfo_children():
            if not isinstance(widget, tk.Label):  # Keep the title label
                widget.destroy()

        # Create labels for product details
        name_label = tk.Label(self.top_choice_frame, text=product['name'], font=('Helvetica', 12, 'bold'))
        name_label.pack(side=tk.TOP, anchor='w', padx=5)
        
        description_label = tk.Label(self.top_choice_frame, text=product['description'], wraplength=200, font=('Helvetica', 10))
        description_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        price_label = tk.Label(self.top_choice_frame, text=f"${product['price']:.2f}", font=('Helvetica', 10, 'bold'))
        price_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        category_label = tk.Label(self.top_choice_frame, text=product['category'], font=('Helvetica', 10, 'italic'))
        category_label.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        # Retrieve and display the average rating as stars
        average_rating = self.db_ops.get_average_rating(product['id'])
        rating_frame = tk.Frame(self.top_choice_frame)
        rating_frame.pack(side=tk.TOP, anchor='w', padx=5, pady=2)
        
        for i in range(1, 6):
            star_label = tk.Label(rating_frame, text="★", font=('Helvetica', 10), fg='gold' if i <= average_rating else 'grey')
            star_label.pack(side=tk.LEFT)

        # Create a purchase button
        purchase_button = tk.Button(self.top_choice_frame, text="Purchase", command=lambda p=product: self.purchase_product(p))
        purchase_button.pack(side=tk.LEFT, anchor='w', padx=5, pady=5)
        
        # Create a button to show reviews in a popup
        show_reviews_button = tk.Button(self.top_choice_frame, text="Show Reviews", command=lambda p=product: self.show_reviews(p['id']))
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
