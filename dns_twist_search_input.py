import connection
import datetime;

search_string = input("Enter a string to search for the domain name:")
ct = datetime.datetime.now()

search = {}
search["input_text"] = search_string
search["created_on"] = ct

search_input = connection.mydb["search_input"]
x = search_input.insert_one(search)

connection.connect_close()
