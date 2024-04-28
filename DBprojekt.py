from DBoperations import DBoperations

# connect to DB
connection ='mat/1324@localhost:1521/xe'
db_ops = DBoperations(connection)


#db_ops.create_user('test', 'test.test@example.com', '0955654321','1324')
#user = db_ops.read_user(2)
#print(user)

'''
user_id = 1
feature_id = 2 #2=Compact

db_ops.link_user_to_feature(user_id, feature_id)

feature = db_ops.check_user_feature(user_id)
if feature:
    print(f"User {user_id} is linked to feature: {feature}")
else:
    print(f"No feature linked to user")
'''
#print(db_ops.get_all_products())
print(db_ops.get_products_by_category("Automation"))

# close DB conn
db_ops.close_connection()
