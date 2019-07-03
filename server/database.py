
from pymongo import MongoClient

class database():
    def store_in_database(response):
    client = MongoClient()
    db = client.marmobox_test
    db.marmosets.insert_one({
        'name':"MARMOMIKE",
        'id': "F1234"
    })