import connection
import datetime
import bcrypt

emailID = input("Enter emailID: ").lower()
password = input("Enter password: ").encode('UTF-8')

#finding the mail ID from DB
data = connection.mydb.user.find_one({"email":emailID})

#checking the encrypted password to get authenticated
if bcrypt.checkpw(password,data['password']):
    #updating the time-stamp
    connection.mydb.user.find_one_and_update({"email" : emailID},{"$set":{"latest_login_time": datetime.datetime.now()}},upsert=True)
    print("Authenticated")
    
    import dns_from_dnstwist_no_file as dns
    from dns_twist_search_input import search_string
    jsonObj = dns.dnsTwist(search_string)
    collection = dns.createCollection(jsonObj)
    
    # connect with collection
    dns_from_dnstwist = connection.mydb["dnsFromDnstwist"]
    
    # insert into database
    x = connection.mydb.dnsFromDnstwist.insert_many(collection)
    
else:
    print("Not Authenticated")

#closing the connection
connection.connect_close()
