import tkinter as tk
from tkinter import simpledialog
from utilities import extract_numerical
from Kmeans import KMeans
from collections import Counter

class PurchaseHistoryWindow:
    def __init__(self, master, db_ops, user_id):
        self.master = master
        self.db_ops = db_ops
        self.user_id = extract_numerical(str(user_id))
        print(str(self.user_id))
        
        # Create a new Toplevel window for the purchase history window
        self.window = tk.Toplevel(master)
        self.window.title("Purchase History")
        
        # Add a label for purchase history
        self.label = tk.Label(self.window, text="Purchase History")
        self.label.pack(pady=20)
        
        # Create a canvas with a scrollbar for scrolling
        self.canvas = tk.Canvas(self.window)
        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Link the canvas and scrollbar
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas to hold the purchase widgets
        self.inner_frame = tk.Frame(self.canvas)
        self.inner_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')
        
        # Bind the Configure event to update the scroll region
        self.inner_frame.bind("<Configure>", self.update_scroll_region)
        
        # Display purchase history
        self.display_purchase_history()
        
    def update_scroll_region(self, event):
        # Update the canvas scroll region to fit the inner frame
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def display_purchase_history(self):
        # Retrieve purchase history for the user
        purchase_history = self.db_ops.get_purchase_history(self.user_id)
        
        if purchase_history:
            # Display purchase history
            for purchase in purchase_history:
                self.create_purchase_widget(purchase)
        else:
            # If no purchase history found, display a message
            no_purchase_label = tk.Label(self.inner_frame, text="No purchase history found.")
            no_purchase_label.pack()
    
    def create_purchase_widget(self, purchase):
        # Create a frame for each purchase item
        purchase_frame = tk.Frame(self.inner_frame, relief=tk.SUNKEN, borderwidth=1)
        purchase_frame.pack(fill=tk.X, pady=5, padx=10)
        
        # Display purchase information
        purchase_info = f"Name: {purchase[1]}, Description: {purchase[2]}, Price: {purchase[3]}, Category: {purchase[4]}"
        purchase_label = tk.Label(purchase_frame, text=purchase_info, wraplength=400)
        purchase_label.pack(side=tk.LEFT, padx=5)
        
        # Create a review button
        review_button = tk.Button(purchase_frame, text="Review", command=lambda p=purchase: self.review_product(p))
        review_button.pack(side=tk.RIGHT, padx=5)

    def review_product(self, purchase):
        # Create a popup window for the review
        review_popup = tk.Toplevel(self.window)
        review_popup.title("Review Product")
        
        # Add a label for the product being reviewed
        review_label = tk.Label(review_popup, text=f"Reviewing: {purchase[1]}")
        review_label.pack(pady=5)
        
        # Add a text entry for the review
        review_text = tk.Text(review_popup, width=40, height=10)
        review_text.pack(pady=5)

        # Create a frame for the 5-star rating system
        rating_frame = tk.Frame(review_popup)
        rating_frame.pack(pady=5)
        
        # Add a label for the rating system
        rating_label = tk.Label(rating_frame, text="Rate this product:")
        rating_label.pack(side=tk.LEFT)

        # Create star buttons for rating
        self.rating_var = tk.IntVar()
        for i in range(1, 6):
            star_button = tk.Radiobutton(rating_frame, text="★", variable=self.rating_var, value=i, indicatoron=0)
            star_button.pack(side=tk.LEFT)

        # Add a submit button for the review
        submit_button = tk.Button(review_popup, text="Submit Review", command=lambda: self.submit_review(review_popup, purchase[0], self.rating_var.get(), review_text.get("1.0", tk.END)))
        submit_button.pack(pady=5)
    
    def submit_review(self, review_popup, product_id, rating, review_text):
        # Store the review in the database
        success = self.db_ops.set_review(self.user_id, product_id, rating, review_text)
        if success:
            print(f"Submitted review for product {product_id}: Rating={rating}, Review={review_text}")
            review_popup.destroy()
        else:
            print("Failed to submit review")
        # Recalculate feature, reasign if needed =========================================
        kmeans = KMeans(15)
        kmeans.fit_from_file("commentGenSamples.txt")

        assigned_feature, assigned_feature_id = kmeans.predict(review_text)
        assigned_feature_id = assigned_feature_id + 1
        print(f"\nAssigned Feature: {assigned_feature}, Feature ID: {assigned_feature_id}\n")

        text_reviews = self.db_ops.get_text_reviews(product_id)
        # Predict features for all reviews
        predicted_features = [kmeans.predict(review)[1] for review in text_reviews]
        # Count occurrences of each feature
        feature_counts = Counter(predicted_features)
        # Find the most common feature
        most_common_feature, count = feature_counts.most_common(1)[0]
        
        print(f"Most Common Feature for product {product_id}: {most_common_feature + 1} (Count: {count})") #dnt kn why ??
        print(f"Comment: {review_text}\nAssigned Feature: {most_common_feature + 1}\n")

        self.db_ops.link_feature_to_product(product_id, most_common_feature + 1) #dnt kn why ??