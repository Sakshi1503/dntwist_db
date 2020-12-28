import os
import dnstwist
import json
import connection

mycol = connection.mydb["dns_from_dnstwist"]

command = "dnstwist --format json patel.com | jq > file.json"
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


x = mycol.insert_many(data)

connection.connect_close()
