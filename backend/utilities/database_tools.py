from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load info from .env file
load_dotenv()

# assign values from .env file if they exist
MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')

def add_to_collection(db_name="empty", collection_name="empty", items={}):
    with MongoClient(MONGO_CONNECTION) as client:
        db = client[db_name]
        col = db[collection_name]
        print(items)
        col.insert_many(items)
    return True
        
def clear_collection(db_name="empty", collection_name="empty"):
    with MongoClient(MONGO_CONNECTION) as client:
        db = client[db_name]
        col = db[collection_name]
        col.drop()
    return True

def get_collection_names(db_name="empty"):
    with MongoClient(MONGO_CONNECTION) as client:
        db = client[db_name]
        return db.list_collection_names()

def get_database_names():
    return MongoClient(MONGO_CONNECTION).list_database_names()
        
def print_collection(db_name="empty", collection_name="empty", max_items=10):
    with MongoClient(MONGO_CONNECTION) as client:
        db = client[db_name]
        col = db[collection_name]
        
        if collection_name not in db.list_collection_names():
            print("This collection is empty or does not exist.")
            return False
        
        for i, item in enumerate(col.find()):
            if i == max_items:
                break
            print(f'\n{i+1}: ', item)
        print("This collection has", col.count_documents({}), "documents.")
    return True
        
        