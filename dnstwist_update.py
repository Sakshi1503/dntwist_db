import os
import dnstwist
import json
import connection
import requests
import dns.resolver

#domains searched by the users
data = list(connection.mydb.search_input.distinct('input_text'))

#make a list of existing domains
existingDomain = list(connection.mydb.dns_from_dnstwist.distinct('domain-name'))

for x in data:

    command = "dnstwist --format json " + x + " | jq"
    stream = os.popen(command)
    output = stream.read()
    data = json.loads(output.replace("\n",""))
    
    for element in data:
        
        #check if the domain name if it is already existing in the db
        if element.get('domain-name') in existingDomain:
            element.pop('dns-mx', None)
            element.pop('fuzzer', None)
            
            if 'dns-a' in element:
                element.update({"registered?": True})
                
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
                element.update({"registered?": False})
                
            element["ip-address"] = element.pop('dns-a', None)
            connection.mydb.dns_from_dnstwist.replace_one({"domain-name": element.get('domain-name')}, element)
            
    
    
    
    

