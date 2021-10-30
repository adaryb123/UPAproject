import pymongo
import certifi
import json

address = "mongodb+srv://dbUser:potkan420@cluster0.bkic2.mongodb.net/public_health_system?retryWrites=true&w=majority"
database_name = "public_health_system"
collection_name = "public_health_system"

certificate = certifi.where()
cluster = pymongo.MongoClient(address, tlsCAFile=certificate)
database = cluster[database_name]
collection = database[collection_name]

def clear_collection():
    collection.drop()

#takes about 30 min to insert all data. There are 39472 entries
def insert_json_file(json_file_path):
    print("data import strated...")
    with open(json_file_path) as file:
         data = json.load(file)
         index = 0
         for i in data:
            data[i]["_id"] = index
            collection.insert_one(data[i])
            index += 1

    print("data import finished...")