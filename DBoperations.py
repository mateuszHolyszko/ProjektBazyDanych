import cx_Oracle

class DBoperations:
    def __init__(self, connection_string):
        self.connection = cx_Oracle.connect(connection_string)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        # Close the cursor and connection
        self.cursor.close()
        self.connection.close()
    
    def create_user(self, username, email, phone, password):
        try:
            self.cursor.callproc("create_user", [username, email, phone, password])
            self.connection.commit()
            print(f"User created successfully.")
        except cx_Oracle.IntegrityError as e:
            print("Failed to create user.")
            print(f"Error: {e}")
            self.connection.rollback()

    def read_user(self, user_id):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("read_user", [user_id, out_cursor])
            user = out_cursor.getvalue().fetchone()
            return user
        except Exception as e:
            print(f"Error reading user: {e}")
            return None
    
    def update_user_email(self, user_id, new_email):
        try:
            self.cursor.callproc("update_user_email", [user_id, new_email])
            self.connection.commit()
        except Exception as e:
            print(f"Error updating email: {e}")
            self.connection.rollback()

    def delete_user(self, user_id):
        try:
            self.cursor.callproc("delete_user", [user_id])
            self.connection.commit()
        except Exception as e:
            print(f"Error deleting user: {e}")
            self.connection.rollback()
    
    def check_user_feature(self, user_id):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("check_user_feature", [user_id, out_cursor])
            feature = out_cursor.getvalue().fetchone()
            return feature[0] if feature else None
        except Exception as e:
            print(f"Error checking user feature: {e}")
            return None
            
    def link_user_to_feature(self, user_id, feature_id):
        try:
            self.cursor.callproc("link_user_to_feature", [user_id, feature_id])
            self.connection.commit()
            print(f"User {user_id} has been successfully linked to feature {feature_id}.")
        except Exception as e:
            print(f"Failed to link user {user_id} to feature {feature_id}. Error: {e}")
            self.connection.rollback()

    def get_average_rating(self, product_id):
        try:
            avg_rating = self.cursor.var(cx_Oracle.NUMBER)
            self.cursor.callproc("get_average_rating", [product_id, avg_rating])
            return avg_rating.getvalue() if avg_rating.getvalue() is not None else 0  # Return 0 if there are no ratings
        except Exception as e:
            print(f"Error retrieving average rating: {e}")
            return None


        # Check Product Feature
    def check_product_feature(self, product_id):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("check_product_feature", [product_id, out_cursor])
            feature = out_cursor.getvalue().fetchone()
            return feature[0] if feature else None
        except Exception as e:
            print(f"Error checking product feature: {e}")
            return None

    # Link Feature to Product
    def link_feature_to_product(self, product_id, feature_id):
        try:
            self.cursor.callproc("link_feature_to_product", [product_id, feature_id])
            self.connection.commit()
            print(f"Product {product_id} has been successfully linked to feature {feature_id}.")
            return True
        except cx_Oracle.IntegrityError as e:
            print(f"Failed to link product {product_id} to feature {feature_id}. Error: {e}")
            self.connection.rollback()
            return False

    # Login
    def login(self, username, password):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("login", [username, password, out_cursor])
            user = out_cursor.getvalue().fetchone()
            return user if user else False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    # Get Products by Category
    def get_products_by_category(self, category):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("get_products_by_category", [category, out_cursor])
            products = out_cursor.getvalue().fetchall()
            product_list = [{'name': product[0], 'description': product[1], 'price': product[2], 'category': product[3], 'id': product[4]} for product in products]
            return product_list
        except Exception as e:
            print(f"Error getting products by category: {e}")
            return []

    # Get All Products
    def get_all_products(self):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("get_all_products", [out_cursor])
            products = out_cursor.getvalue().fetchall()
            product_list = [{'id': product[0], 'name': product[1], 'description': product[2], 'price': product[3], 'category': product[4]} for product in products]
            return product_list
        except Exception as e:
            print(f"Error getting all products: {e}")
            return []

    # Get Categories
    def get_categories(self):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("get_categories", [out_cursor])
            categories = out_cursor.getvalue().fetchall()
            category_list = [{'id': category[0], 'name': category[1], 'description': category[2]} for category in categories]
            return category_list
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []

    # Save Purchase History
    def save_purchase_history(self, user_id, product_names):
        try:
            # Use cursor.arrayvar to create an array of product names
            product_names_array = self.cursor.arrayvar(cx_Oracle.STRING, product_names)
            self.cursor.callproc("save_purchase_history", [user_id, product_names_array])
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving purchase history: {e}")
            self.connection.rollback()
            return False


    # Get Purchase History
    def get_purchase_history(self, user_id):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("get_purchase_history", [user_id, out_cursor])
            purchase_history = out_cursor.getvalue().fetchall()
            return purchase_history
        except Exception as e:
            print(f"Error getting purchase history: {e}")
            return []

    # Set Review
    def set_review(self, user_id, product_id, rating, text_review):
        try:
            self.cursor.callproc("set_review", [user_id, product_id, rating, text_review])
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error setting review: {e}")

    def get_text_reviews(self, product_id):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("get_text_reviews", [product_id, out_cursor])
            text_reviews = out_cursor.getvalue().fetchall()
            return [review[0] for review in text_reviews]  # Return a list of text reviews
        except Exception as e:
            print(f"Error retrieving text reviews: {e}")
            return None
        
    def get_product_by_id(self, product_id):
        try:
            out_cursor = self.cursor.var(cx_Oracle.CURSOR)
            self.cursor.callproc("get_product_by_id", [product_id, out_cursor])
            product = out_cursor.getvalue().fetchone()
            if product:
                product_dict = {
                    'id': product[0],
                    'name': product[1],
                    'description': product[2],
                    'price': product[3],
                    'category': product[4]
                }
                return product_dict
            else:
                return None
        except Exception as e:
            print(f"Error retrieving product by ID: {e}")
            return None

    def get_feature_id(self, feature):
        try:
            feature_id = self.cursor.var(cx_Oracle.NUMBER)
            self.cursor.callproc("get_feature_id", [feature, feature_id])
            return feature_id.getvalue() if feature_id.getvalue() is not None else None
        except Exception as e:
            print(f"Error retrieving feature ID: {e}")
            return None  

    def update_user_feature(self, user_id):
        try:
            # Retrieve the user's purchase history
            purchase_history = self.get_purchase_history(user_id)
            
            # Dictionary to count the frequency of each feature
            feature_count = {}
            
            # Iterate over each purchase in the purchase history
            for purchase in purchase_history:
                product_id = purchase[0]
                
                # Get the feature of the current product
                feature = self.check_product_feature(product_id)
                
                if feature:
                    if feature in feature_count:
                        feature_count[feature] += 1
                    else:
                        feature_count[feature] = 1
            
            # Find the most frequent feature
            most_frequent_feature = max(feature_count, key=feature_count.get, default=None)
            
            if most_frequent_feature:
                # Get the current feature linked to the user
                current_feature = self.check_user_feature(user_id)
                
                if current_feature != most_frequent_feature:
                    # Get the feature_id for the most frequent feature
                    feature_id = self.get_feature_id(most_frequent_feature)
                    
                    # Link the most frequent feature to the user
                    self.link_user_to_feature(user_id, feature_id)
                    
                    print(f"Updated user {user_id} with the most frequent feature: {most_frequent_feature}")
        except Exception as e:
            print(f"Error updating user feature: {e}")



