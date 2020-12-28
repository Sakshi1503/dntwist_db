import os
import dnstwist
import json
import connection
from dns_twist_search_input import search_string

#connect with collection
dns_from_dnstwist = connection.mydb["dns_from_dnstwist"]

#run the command and save it into json
command = "dnstwist --format json "+ search_string +" | jq > file.json"
os.system(command)

#reading the json file
with open("file.json", "r") as read_file:
    data = json.load(read_file)

#creating the dict to be inserted into collection as per the requirement
for element in data:
	    element.pop('dns-mx', None)
	    element.pop('dns-ns', None)
	    element.pop('fuzzer', None)
	    if 'dns-a' in element:
		    element.update({"is-avail":False})
	    else:
		    element.update({"is-avail":True}) 

#insert into database
x = dns_from_dnstwist.insert_many(data)

#closing the connectioin
connection.connect_close()
