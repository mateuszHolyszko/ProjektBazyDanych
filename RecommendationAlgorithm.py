from collections import Counter


class RecommendationAlgorithm:
    def __init__(self, db_ops, user_id, rating_threshold=3):
        self.db_ops = db_ops
        self.user_id = user_id
        self.rating_threshold = rating_threshold
        self.products = self.initialize_products_with_coefficient()
        self.user_feature = self.db_ops.check_user_feature(user_id)  
        self.top_categories = self.get_top_categories(user_id)

    def initialize_products_with_coefficient(self):
        # Retrieve all products from the database
        products = self.db_ops.get_all_products()
        
        # Initialize each product with a coefficient of 1
        product_list = [{'product': product, 'coefficient': 1} for product in products]
        
        return product_list

    def get_top_categories(self, user_id):
            # Retrieve the user's purchase history
            purchase_history = self.db_ops.get_purchase_history(user_id)

            # Count the frequency of each category
            #print(purchase_history[0][4])
            category_counter = Counter([purchase[4] for purchase in purchase_history])  

            # Get the top 3 most common categories
            top_categories = [category for category, _ in category_counter.most_common(3)]
            #print(top_categories)
            return top_categories

    def calculate_recommendation_coefficient(self, product_list):
        updated_product_list = []

        for item in product_list:
            product = item['product']
            coefficient = item['coefficient']
            
            # Get the average rating for the product
            average_rating = self.db_ops.get_average_rating(product['id'])
            
            # Filter out products with an average rating below the threshold
            if average_rating >= self.rating_threshold:
                # Multiply the coefficient by the average rating
                item['coefficient'] = coefficient * average_rating
                updated_product_list.append(item)
        
        # Print state after applying recommendation coefficient algorithm
        print("After applying recommendation coefficient algorithm:")
        for item in updated_product_list:
            print(f"Product ID: {item['product']['id']}, Coefficient: {item['coefficient']}")
        
        return updated_product_list

    def calculate_feature_based_coefficient(self, product_list):
        updated_product_list = []

        for item in product_list:
            product = item['product']
            #print(product)
            coefficient = item['coefficient']
        
            # Check if the product's feature matches the user's feature
            if self.user_feature and self.user_feature == self.db_ops.check_product_feature(product['id']):  
                # Increase the coefficient if the features match
                item['coefficient'] = coefficient * 1.5  # Increase by 50%
                print(" Match found")
            else:
                item['coefficient'] = coefficient * 0.80  # Decrese by 80%

            # Filter out products with an average rating below the threshold
            if item['coefficient'] >= self.rating_threshold:
                updated_product_list.append(item)
            
            #updated_product_list.append(item)
            
        
        # Print state after applying feature-based algorithm
        print("After applying feature-based algorithm:")
        for item in updated_product_list:
            print(f"Product ID: {item['product']['id']}, Coefficient: {item['coefficient']}")
        
        return updated_product_list

    def calculate_purchase_history_coefficient(self, product_list):
        updated_product_list = []
        ##print(self.top_categories)
        for item in product_list:
            product = item['product']
            coefficient = item['coefficient']
            
            ##print(product['category'])
            # Check if the product's category matches one of the user's top categories
            if product['category'] in self.top_categories:
                # Increase the coefficient if the category matches
                item['coefficient'] = coefficient * 1.3  # Increase by 30%
            
            updated_product_list.append(item)
        
        # Print state after applying purchase history algorithm
        print("After applying purchase history algorithm:")
        for item in updated_product_list:
            print(f"Product ID: {item['product']['id']}, Coefficient: {item['coefficient']}")
        
        return updated_product_list

    def get_recommendations(self):
        # Apply the algorithms
        product_list = self.calculate_recommendation_coefficient(self.products)
        product_list = self.calculate_feature_based_coefficient(product_list)
        product_list = self.calculate_purchase_history_coefficient(product_list)
        
        # Sort the products by their total recommendation coefficient in descending order
        sorted_products = sorted(product_list, key=lambda x: x['coefficient'], reverse=True)
        
        # Extract the product IDs of the recommended products
        recommended_product_ids = [item['product']['id'] for item in sorted_products]
        
        
        return recommended_product_ids
