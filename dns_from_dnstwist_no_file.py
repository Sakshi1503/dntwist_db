import os
import dnstwist
import json
import connection
import requests
import dns.resolver

def dnsTwist():
    from dns_twist_search_input import search_string
    # connect with collection
    dns_from_dnstwist = connection.mydb["dns_from_dnstwist"]

    # run the command
    command = "dnstwist --format json " + search_string + " | jq"

    #retrieving the o/p of cmd
    stream = os.popen(command)
    output = stream.read()

    #storing the output of cmd into a json object
    data = json.loads(output.replace("\n",""))

    # creating the dict to be inserted into collection as per the requirement
    for element in data:
        element.pop('dns-mx', None)
        element.pop('fuzzer', None)
        if 'dns-a' in element:
            element.update({"registered?": False})
            #extract the location of the IP address from IPSTACK API
            for ip_address in element['dns-a']:
                element.update({"location": json.loads(requests.get(
                    'http://api.ipstack.com/' + ip_address + '?access_key=027ce8919364c2616e482ab0e9a23e55').content.decode(
                    'utf-8'))})
                #adding text record using dns.resolver
                try:
                    answers = dns.resolver.resolve(element['domain-name'], 'TXT')
                except:
                    element.update({"text-record": None})
                else:
                    element.update({"text-record":[txt_string.decode('utf-8') for rdata in answers for txt_string in rdata.strings]})
        else:
            element.update({"registered?": True})
        element["ip-address"] = element.pop('dns-a', None)


    # insert into database
    x = dns_from_dnstwist.insert_many(data)

    # closing the connection
    connection.connect_close()

