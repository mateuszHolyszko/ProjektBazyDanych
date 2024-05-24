import random
import re

def generate_insert_query(category, companies, price_range, features, starting_index, num_products):
    # Dictionary to map category names to their corresponding IDs
    category_to_id = {
        "Kitchen": 1,
        "Laundry": 2,
        "Cleaning": 3,
        "Heating": 4,
        "Cooling": 5,
        "PersonalCare": 6,
        "Entertainment": 7,
        "Lighting": 8,
        "Outdoors": 9,
        "Security": 10,
        "Automation": 11,
        "Cooking": 12
    }

    # Get the ID for the given category
    category_id = category_to_id.get(category)

    

    queries = []

    for i in range(num_products):
        current_id = starting_index + i
        company = companies[i % len(companies)]

        name = f"{category}Product{current_id}"
        description = f"{category}{company}{current_id}"

        if features:
            random_feature = random.choice(features)
            description += f" - {random_feature}"

        price = round(random.uniform(price_range[0], price_range[1]), 2)

        query = (
            f"INSERT INTO products (id, name, description, price, category_id) "
            f"VALUES ({current_id}, '{name}', '{description}', {price}, {category_id});"
        )

        queries.append(query)
    
    # Save the queries to a file called productsSeeder.sql
    with open("productsSeeder.sql", "a") as file:
        for query in queries:
            file.write(query + "\n")

    return queries


def generate_reviews(num_reviews):
        with open("productsSeeder.sql", "r") as file:
            products = file.readlines()

        with open("commentGenSamples.txt", "r") as file:
            comments = file.readlines()

        feature_to_comment = {}
        for line in comments:
            if line.startswith('['):
                feature = line.split(']')[0][1:]
                comment = line.split(']')[1].strip()
                if feature not in feature_to_comment:
                    feature_to_comment[feature] = []
                feature_to_comment[feature].append(comment)

        queries = []
        user_queries = []
        for i in range(num_reviews):
            product = random.choice(products)
            product_details = re.search(r'\((\d+), \'([^\']+)\', \'([^\']+)\', (\d+\.\d+), (\d+)\)', product)
            
            if product_details:
                product_id = product_details.group(1)
                description = product_details.group(3)
                feature_match = re.search(r'- (.+)', description)
                feature = feature_match.group(1) if feature_match else "No feature"

                if feature in feature_to_comment:
                    comment = random.choice(feature_to_comment[feature])
                else:
                    comment = "No comment available."

                rating = random.randint(1, 5)
                reviewer_id = i + 1  # Simplification for this example, normally would be different

                review_query = (
                    f"INSERT INTO reviews (id, product_id, reviewer_id, rating, text_review) "
                    f"VALUES (REVIEW_SEQ.NEXTVAL, {product_id}, {reviewer_id}, {rating}, '{comment}');"
                )

                user_query = (
                    f"INSERT INTO users (id, username, email, phone, password) "
                    f"VALUES ({reviewer_id}, 'user{reviewer_id}', 'user{reviewer_id}@example.com', '1234567890', '1234');"
                )

                user_queries.append(user_query)
                queries.append(review_query)

        with open("reviewsSeeder.sql", "a") as file:
            for query in user_queries + queries:
                file.write(query + "\n")

        return queries

features = ["Energy-Efficient",
                "Compact",
                "Durable",
                "Innovative",
                "Ergonomic",
                "Quiet",
                "Smart",
                "Stylish",
                "Versatile",
                "High-Capacity",
                "Fast",
                "Safe",
                "User-Friendly",
                "Affordable",
                "Reliable"]
category_to_id = [
    "Kitchen",
    "Laundry",
    "Cleaning",
    "Heating",
    "Cooling",
    "PersonalCare",
    "Entertainment",
    "Lighting",
    "Outdoors",
    "Security",
    "Automation",
    "Cooking",
]
price_ranges = [
        (1000.00, 5000.00),
        (1000.00, 3000.00),
        (500.00, 1000.00),
        (500.00, 1500.00),
        (500.00, 3500.00),
        (100.00, 300.00),
        (1000.00, 5000.00),
        (100.00, 500.00),
        (1000.00, 3000.00),
        (500.00, 2000.00),
        (500.00, 2000.00),
        (200.00, 1000.00)
]
feature_to_id = {
            "Energy-Efficient": 1,
            "Compact": 2,
            "Durable": 3,
            "Innovative": 4,
            "Ergonomic": 5,
            "Quiet": 6,
            "Smart": 7,
            "Stylish": 8,
            "Versatile": 9,
            "High-Capacity": 10,
            "Fast": 11,
            "Safe": 12,
            "User-Friendly": 13,
            "Affordable": 14,
            "Reliable": 15
        }

def generate_product_features():
        with open("productsSeeder.sql", "r") as file:
            products = file.readlines()

        queries = []
        for product in products:
            product_details = re.search(r'\((\d+), \'([^\']+)\', \'([^\']+)\', (\d+\.\d+), (\d+)\)', product)
            
            if product_details:
                product_id = product_details.group(1)
                description = product_details.group(3)
                feature_match = re.search(r'- (.+)', description)
                feature = feature_match.group(1) if feature_match else None

                if feature:
                    feature_id = feature_to_id.get(feature)
                    if feature_id:
                        query = (
                            f"INSERT INTO product_features (product_id, feature_id) "
                            f"VALUES ({product_id}, {feature_id});"
                        )
                        queries.append(query)

        with open("productFeaturesSeeder.sql", "a") as file:
            for query in queries:
                file.write(query + "\n")

        return queries

"""
for i in range(1,12):

    category = category_to_id[i]
    companies = ["producer1_", "producer2_", "producer3_"]
    price_range = price_ranges[i]
    starting_index = 10*i
    num_products = 5

    queries = generate_insert_query(category, companies, price_range, features, starting_index, num_products)
"""
#generate_reviews(50)
#generate_product_features()
