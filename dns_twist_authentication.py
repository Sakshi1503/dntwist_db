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
    from dns_twist_search_input import search_string, search
    searchInputList = list(connection.mydb.searchInput.distinct('input_text'))

##    i = 0

    #Extract the data from the database if already searched before-hand
    if search_string in searchInputList:
        x = connection.mydb.dnsFromDnstwist.find({"searched-input" : search_string})
        connection.mydb.searchInput.update_one({"input_text" : search_string},{"$push":{"created_on": str(datetime.datetime.now())}},upsert=True)
##        for j in x:
##            i += 1
##            print(j,i)
            
    else:

        #insert the search into the database
        search_input = connection.mydb["searchInput"]
        x = search_input.insert_one(search)

        #Using the DnsTwist API
        jsonObj = dns.dnsTwist(search_string)
        collection = dns.createCollection(jsonObj, search_string)
        
        # connect with collection
        dns_from_dnstwist = connection.mydb["dnsFromDnstwist"]
        
        # insert into database
        x = connection.mydb.dnsFromDnstwist.insert_many(collection)
        
else:
    print("Not Authenticated")

#closing the connection
connection.connect_close()
