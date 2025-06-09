import os

from pymongo import MongoClient
from pymongo.collection import Collection

def get_mongo_collection(collection_name: str) -> Collection:
    """
    Get a MongoDB collection by name.
    """
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client.mlops_db
    return db[collection_name]

