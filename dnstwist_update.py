import connection

#domains searched by the users
searchInputList = list(connection.mydb.searchInput.distinct('input_text'))

#make a list of existing domains
existingDomain = list(connection.mydb.dnsFromDnstwist.find({},{'domain-name':1, 'ip-address':1, '_id':0}))
print(existingDomain)

for searchString in searchInputList:
    
    import dns_from_dnstwist_no_file as dns
    jsonObj = dns.dnsTwist(searchString)
    data = dns.createCollection(jsonObj)

    for element in data:
        
        #check if the domain name if it is already existing in the db and whether the IP is changed or not
        if element.get('domain-name') in [x['domain-name'] for x in existingDomain]:

                #updating the collections
                connection.mydb.dnsFromDnstwist.replace_one({"domain-name": element.get('domain-name')}, element)


# closing the connection
connection.connect_close() 
    
    
    
    

