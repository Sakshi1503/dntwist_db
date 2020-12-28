import os
import dnstwist
import json
import connection
from dns_twist_search_input import search_string

dns_from_dnstwist = connection.mydb["dns_from_dnstwist"]

command = "dnstwist --format json "+ search_string +" | jq > file.json"
print(command)
os.system(command)


with open("file.json", "r") as read_file:
    data = json.load(read_file)

for element in data:
	    element.pop('dns-mx', None)
	    element.pop('dns-ns', None)
	    element.pop('fuzzer', None)
	    if 'dns-a' in element:
		    element.update({"is-avail":False})
	    else:
		    element.update({"is-avail":True}) 


x = dns_from_dnstwist.insert_many(data)

connection.connect_close()
