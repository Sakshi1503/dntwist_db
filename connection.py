import pymongo

myclient = pymongo.MongoClient("mongodb+srv://dbSakshi:6066@cluster0.rait6.mongodb.net/test?authSource=admin&replicaSet=atlas-s7vzo4-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
mydb = myclient["mydatabase"]
    #print("connected")

def connect_close():
    myclient.close()
    #print("disconnected")

