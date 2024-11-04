import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('config.ini')

# Kết nối MongoDB
client = MongoClient(config['MONGO_API']['M0NGO_URI'])
db = client[config['MONGO_API']['M0NGO_DB']]
collection = db[config['MONGO_API']['M0NGO_CL']]

async def save_data(channel, filename, url, user, password, name, phone):
    document = {"channel": channel, "filename": filename, "user": user}

    if url != "":
        document["url"]: url
    if password != "":
        document["password"] = password
    if name != "":
        document["name"] = name
    if phone != "":
        document["phone"] = phone
    
    await collection.insert_one(document)