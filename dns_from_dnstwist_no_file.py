import os
import dnstwist
import json
import connection
import requests
import dns.resolver

#######################################################################   DNS TWIST COMMAND   ###################################################################
def dnsTwist(search_string):
    # run the command
    command = "dnstwist --format json " + search_string + " | jq"

    #retrieving the o/p of cmd
    stream = os.popen(command)
    output = stream.read()

    #storing the output of cmd into a json object
    data = json.loads(output.replace("\n",""))
    return data

#######################################################################   CREATING A COLLECTION   ################################################################
def createCollection(data, search_string):
    # creating the dict to be inserted into collection as per the requirement
    for element in data:
        element.pop('dns-mx', None)
        element.pop('fuzzer', None)
        if 'dns-a' in element:
            element.update({"registered?": True})
            
            for ip_address in element['dns-a']:
                
                #extract the location of the IP address from IPSTACK API
                ipStack(ip_address, element)

                #adding text record using dns.resolver
                dnsResolver(element)
        else:
            element.update({"registered?": False})
            
        element["ip-address"] = element.pop('dns-a', None)
        element.update({"searched-input" : search_string})
    return data

######################################################################   IP STACK   ################################################################################
def ipStack(ipAddress, item):
    item.update({"location": json.loads(requests.get(
                    'http://api.ipstack.com/' + ipAddress + '?access_key=027ce8919364c2616e482ab0e9a23e55').content.decode(
                    'utf-8'))})

######################################################################   DNS RESOLVER   #############################################################################
def dnsResolver(item):
    try:
        answers = dns.resolver.resolve(item['domain-name'], 'TXT')
    except:
        item.update({"text-record": None})
    else:
        item.update({"text-record":[txt_string.decode('utf-8') for rdata in answers for txt_string in rdata.strings]})
        
    

