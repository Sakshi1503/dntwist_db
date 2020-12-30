import connection
import datetime
import bcrypt

emailID = input("Enter emailID: ")
password = input("Enter password: ").encode('UTF-8')

#finding the mail ID from DB
data = connection.mydb.user.find_one({"email":emailID})

#checking the encrypted password to get authenticated
if bcrypt.checkpw(password,data['password']):
    print("Authenticated")
    #updating the time-stamp
    connection.mydb.user.find_one_and_update({"email" : emailID},{"$set":{"latest_login_time": datetime.datetime.now()}},upsert=True)
else:
    print("Not Authenticated")

#closing the connection
connection.connect_close()
