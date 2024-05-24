import cx_Oracle

class DBoperations:
    def __init__(self, connection_string):
        # Create a connection to the Oracle database
        self.connection = cx_Oracle.connect(connection_string)
        # Create a cursor for executing SQL queries
        self.cursor = self.connection.cursor()
    
    def create_user(self, username, email, phone, password):
        try:
            # Insert the new user into the users table with the provided password
            self.cursor.execute("""
                INSERT INTO users (username, email, phone, password)
                VALUES (:username, :email, :phone, :password)
            """, {'username': username, 'email': email, 'phone': phone, 'password': password})
            
            # Commit the transaction
            self.connection.commit()
            print(f"User created successfully.")
        except cx_Oracle.IntegrityError as e:
            print("Failed to create user.")
            print(f"Error: {e}")
            # Roll back the transaction to avoid partial data insertion
            self.connection.rollback()
    
    def read_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = :id", {'id': user_id})
        
        user = self.cursor.fetchone()
        return user
    
    def update_user_email(self, user_id, new_email):
        self.cursor.execute("""
            UPDATE users
            SET email = :email
            WHERE id = :id
        """, {'email': new_email, 'id': user_id})
        
        self.connection.commit()
    
    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id = :id", {'id': user_id})
        
        self.connection.commit()
    
    def close_connection(self):
        # Close the cursor and connection
        self.cursor.close()
        self.connection.close()

    def check_user_feature(self, user_id):
            query = """
                SELECT f.feature
                FROM user_preferences up
                JOIN features f ON up.feature_id = f.id
                WHERE up.user_id = :user_id
            """
            self.cursor.execute(query, {'user_id': user_id})
            
            feature = self.cursor.fetchone()
            
            if feature:
                return feature[0]
            else:
                # If the user does not have a linked feature
                return None
            
    def link_user_to_feature(self, user_id, feature_id):
        try:
            self.cursor.execute("""
                INSERT INTO user_preferences (user_id, feature_id)
                VALUES (:user_id, :feature_id)
            """, {'user_id': user_id, 'feature_id': feature_id})
            
            self.connection.commit()
            print(f"User {user_id} has been successfully linked to feature {feature_id}.")
        except cx_Oracle.IntegrityError as e:
            # Handle duplicate or foreign key constraint violation
            print(f"Failed to link user {user_id} to feature {feature_id}.")
            print(f"Error: {e}")
            # avoid partial data insertion
            self.connection.rollback()

    def check_product_feature(self, product_id):
        query = """
            SELECT f.feature
            FROM product_features pf
            JOIN features f ON pf.feature_id = f.id
            WHERE pf.product_id = :product_id
        """
        self.cursor.execute(query, {'product_id': product_id})
        
        feature = self.cursor.fetchone()
        
        if feature:
            return feature[0]
        else:
            # If the product does not have a linked feature
            return None

    def login(self, username, password):
        # Define the SQL query to check the username and password in the database
        query = """
            SELECT id
            FROM users
            WHERE username = :username AND password = :password
        """
        # Execute the query with the entered username and password as parameters
        self.cursor.execute(query, {'username': username, 'password': password})
        
        # Fetch the result (user ID if the credentials are correct)
        user = self.cursor.fetchone()
        
        if user:
            return user
        else:            
            return False
        
    def get_products_by_category(self, category):
        query = """
                SELECT 
                    p.name AS product_name,
                    p.description AS product_description,
                    p.price,
                    c.name AS category_name
                FROM 
                    products p
                JOIN 
                    categories c ON p.category_id = c.id
                WHERE c.name = :category
                """

        self.cursor.execute(query, {'category': category})

        products = self.cursor.fetchall()

        product_list = []

        for product in products:
            product_dict = {
                'name': product[0],
                'description': product[1],
                'price': product[2],
                'category': product[3]
            }
            product_list.append(product_dict)

        return product_list
    
    def get_all_products(self):
        query = """
                SELECT 
                    p.id AS product_id,
                    p.name AS product_name,
                    p.description AS product_description,
                    p.price,
                    c.name AS category_name
                FROM 
                    products p
                JOIN 
                    categories c ON p.category_id = c.id
                """
        
        self.cursor.execute(query)
        
        products = self.cursor.fetchall()
        
        product_list = []
        
        for product in products:
            product_dict = {
                'id': product[0],  # Add the product ID to the dictionary
                'name': product[1],
                'description': product[2],
                'price': product[3],
                'category': product[4]
            }
            product_list.append(product_dict)
        
        return product_list
    
    def get_categories(self):
    # Define the SQL query to retrieve all categories
        query = """
            SELECT id, name, description
            FROM categories
        """
        
        # Execute the query
        self.cursor.execute(query)
        
        # Fetch all results
        categories = self.cursor.fetchall()
        
        # Define a list to hold the formatted results
        category_list = []
        
        # Iterate over the categories and format them in the specified format
        for category in categories:
            category_dict = {
                'id': category[0],
                'name': category[1],
                'description': category[2]
            }
            category_list.append(category_dict)
        
        # Return the list of categories in the specified format
        return category_list

    def save_purchase_history(self, user_id, product_names):
        try:
            for product_name in product_names:
                # Retrieve the product ID based on the product name
                self.cursor.execute("SELECT id FROM products WHERE name = :1", (product_name,))
                product_id = self.cursor.fetchone()[0]

                # Insert the purchase record into the purchase_history table
                self.cursor.execute("INSERT INTO purchase_history (user_id, product_id) VALUES (:1, :2)", (user_id, product_id))

            # Commit the transaction
            self.connection.commit()

            return True
        except Exception as e:
            print("Error saving purchase history:", e)
            return False

    def get_purchase_history(self, user_id):
        try:
            # Query to retrieve purchase history for the given user
            query = """
                    SELECT
                        p.id AS product_id, 
                        p.name AS product_name,
                        p.description AS product_description,
                        p.price,
                        c.name AS category_name
                    FROM 
                        purchase_history ph
                    JOIN 
                        products p ON ph.product_id = p.id
                    JOIN 
                        categories c ON p.category_id = c.id
                    WHERE 
                        ph.user_id = :user_id
                    """
            
            # Execute the query
            self.cursor.execute(query, {'user_id': user_id})

            # Fetch all rows from the result set
            purchase_history = self.cursor.fetchall()

            return purchase_history
        except Exception as e:
            print("Error retrieving purchase history:", e)
            return None

    def set_review(self, user_id, product_id, rating, text_review):
        try:
            print(f"Prod: {product_id}, USer:{user_id} , Rate:{rating}, Text: {text_review}")
            query = """
                INSERT INTO reviews (id, product_id, reviewer_id, rating, text_review) 
                VALUES (review_seq.NEXTVAL, :product_id, :reviewer_id, :rating, :text_review)
            """
            self.cursor.execute(query, {
                'product_id': product_id,
                'reviewer_id': user_id,
                'rating': rating,
                'text_review': text_review
            })
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error saving review: {e}")
            return False
        
    def get_recommended_products(self, user_id):
        #WIP
        return user_id
    
    def get_average_rating(self, product_id):
        try:
            query = """
                SELECT AVG(rating) AS average_rating
                FROM reviews
                WHERE product_id = :product_id
            """
            self.cursor.execute(query, {'product_id': product_id})
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0  # Return 0 if there are no ratings
        except Exception as e:
            print("Error retrieving average rating:", e)
            return None
        
    def get_text_reviews(self, product_id):
        try:
            query = """
                SELECT text_review
                FROM reviews
                WHERE product_id = :product_id
            """
            self.cursor.execute(query, {'product_id': product_id})
            text_reviews = self.cursor.fetchall()
            return [review[0] for review in text_reviews]  # Return a list of text reviews
        except Exception as e:
            print("Error retrieving text reviews:", e)
            return None
        
    