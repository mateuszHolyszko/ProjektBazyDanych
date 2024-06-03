from DBoperations import DBoperations
from RecommendationAlgorithm import RecommendationAlgorithm

# connect to DB
connection ='mat/1324@localhost:1521/xe'
db_ops = DBoperations(connection)

db_ops.update_user_feature(21)
#db_ops.create_user('test', 'test.test@example.com', '0955654321','1324')
#user = db_ops.read_user(2)
#print(user)

'''
user_id = 21
feature_id = 6 

db_ops.link_user_to_feature(user_id, feature_id)

feature = db_ops.check_user_feature(user_id)
if feature:
    print(f"User {user_id} is linked to feature: {feature}")
else:
    print(f"No feature linked to user")
'''
'''
#print(db_ops.get_all_products())
print(db_ops.get_products_by_category("Automation"))
'''

'''
# TEST ALGO
user_id = 21  # Replace with the actual user ID
rating_threshold = 4  # Set the rating threshold
recommender = RecommendationAlgorithm(db_ops, user_id, rating_threshold)

# Get recommended product IDs
recommended_products = recommender.get_recommendations()

# Print the recommended products
print("Recommended product IDs:", recommended_products)
'''
'''
print(db_ops.link_feature_to_product(113, 1))


# close DB conn
db_ops.close_connection()
'''
