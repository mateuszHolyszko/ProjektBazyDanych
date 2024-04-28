import random

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

for i in range(1,12):

    category = category_to_id[i]
    companies = ["producer1_", "producer2_", "producer3_"]
    price_range = price_ranges[i]
    starting_index = 10*i
    num_products = 5

    queries = generate_insert_query(category, companies, price_range, features, starting_index, num_products)
