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
                'name': product[0],
                'description': product[1],
                'price': product[2],
                'category': product[3]
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



