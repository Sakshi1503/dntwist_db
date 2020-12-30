import os
import dnstwist
import json
import connection
import requests

def dns():
    from dns_twist_search_input import search_string
    # connect with collection
    dns_from_dnstwist = connection.mydb["dns_from_dnstwist"]

    # run the command and save it as a variable
    command = "dnstwist --format json " + search_string + " | jq"

    #retrieving the o/p of cmd
    stream = os.popen(command)
    output = stream.read()

    #storing the output of cmd into a json object
    data = json.loads(output.replace("\n",""))

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

