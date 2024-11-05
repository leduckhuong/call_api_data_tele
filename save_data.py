import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('config.ini')

# Kết nối MongoDB
client = MongoClient(config['MONGO_API']['M0NGO_URI'])
db = client[config['MONGO_API']['MONGO_DB']]
collection = db[config['MONGO_API']['MONGO_CL']]


async def save_data(channel, filename, url, user, password, name, phone):
    print("saving")
    try:
        if user != '' and password != '':
            document = {'channel': channel, 'filename': filename, 'user': user, 'pass': password}
            if url != '':
                document['url'] = url 
            if name != '':
                document['name'] = name
            if phone != '':
                document['phone'] = phone
            
            collection.insert_one(document)

    except Exception as e:
        print(f'Error: {e}')
