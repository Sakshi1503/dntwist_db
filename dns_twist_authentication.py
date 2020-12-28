import connection
import datetime
import bcrypt

emailID = input("Enter emailID")
password = input("Enter password").encode('UTF-8')

#finding the mail ID from DB
data = connection.mydb.user.find_one({"email":emailID})

#checking the encrypted password to get authenticated
if bcrypt.checkpw(password,data['password']):
    print("Authenticated")
else:
    print("Not Authenticated")


