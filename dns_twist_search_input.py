import connection
import datetime

search_string = input("Enter a string to search for the domain name:")
#get current date and time
ct = datetime.datetime.now()

search = {}
search["input_text"] = search_string
search["created_on"] = [str(ct)]

#closing the connection
connection.connect_close()
