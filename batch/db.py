from pymongo import MongoClient
import os

def get_mongo_collection(collection_name: str):
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client.mlops_db
    return db[collection_name]