import os
import dnstwist
import json
import connection
from dns_twist_search_input import search_string
import requests

# connect with collection
dns_from_dnstwist = connection.mydb["dns_from_dnstwist"]

# run the command and save it into json
command = "dnstwist --format json " + search_string + " | jq > file.json"
os.system(command)

# reading the json file
with open("file.json", "r") as read_file:
    data = json.load(read_file)

# creating the dict to be inserted into collection as per the requirement
for element in data:
    element.pop('dns-mx', None)
    element.pop('dns-ns', None)
    element.pop('fuzzer', None)
    if 'dns-a' in element:
        element.update({"is-avail": False})
        #extract the location of the IP address from IPSTACK API
        for ip_address in element['dns-a']:
            element.update({"location": json.loads(requests.get(
                'http://api.ipstack.com/' + ip_address + '?access_key=027ce8919364c2616e482ab0e9a23e55').content.decode(
                'utf-8'))})
    else:
        element.update({"is-avail": True})
    element["ip-address"] = element.pop('dns-a', None)

# insert into database
x = dns_from_dnstwist.insert_many(data)

# closing the connection
connection.connect_close()
