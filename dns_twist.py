import os
import dnstwist
import json
import cassandra
from cassandra.cluster import Cluster



command = "dnstwist --format json patel.com | jq > file.json"
os.system(command)

with open("file.json", "r") as read_file:
    data = json.load(read_file)

str = ""
domain_dict = {i['domain-name'] : (str.join(i['dns-a']) if 'dns-a' in i else 'None') for i in data}

cluster = Cluster()
session = cluster.connect()
session = cluster.connect('task1')

id = 1
for key, value in domain_dict.items():
    if value == 'None':
        avail = True
    else:
        avail = False
    session.execute("INSERT INTO dns_from_dnstwist (dns_id, domain_name, ip, is_available) VALUES (%s, %s, %s, %s)", (id, key , value , avail))
    id += 1

