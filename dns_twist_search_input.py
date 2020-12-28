import connection
import datetime;

search_string = input("Enter a string to search for the domain name:")
ct = datetime.datetime.now()

mycol = connection.mydb["search_input"]

search = {}
search["input_text"] = search_string
search["created_on"] = ct

x = mycol.insert_one(search)

connection.connect_close()
