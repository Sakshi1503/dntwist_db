import connection
import datetime

search_string = input("Enter a string to search for the domain name:")
#get current date and time
ct = datetime.datetime.now()

search = {}
search["input_text"] = search_string
search["created_on"] = ct

#insert the search into the database
search_input = connection.mydb["search_input"]
x = search_input.insert_one(search)

#closing the connection
connection.connect_close()
