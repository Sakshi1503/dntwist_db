import connection
import datetime
import bcrypt

register = {}
register['first_name'] = input("Enter first_name: ")
register['last_name'] = input("Enter last name: ")
register['email'] = input("Enter email ID: ")
register['phone_number'] = input("Enter phone number: ")
register['username'] = input("Enter username: ")

#encoding the password to hash it further
password = input("Enter Password: ").encode('UTF-8')

#hashing and salt to the password before inserting the info into DB
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt)
register['password'] = hashed
register["created_on"] = datetime.datetime.now()
register["lasatest_login_time"] = datetime.datetime.now()

#using the collection 'user'
register_input = connection.mydb["user"]

#inserting into mongodb
x = register_input.insert_one(register)

#closing the connection with mongodb
connection.connect_close()
