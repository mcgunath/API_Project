from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load info from .env file
load_dotenv()

# assign values from .env file if they exist
MONGO_CONNECTION = os.getenv('MONGO_CONNECTION')

def add_to_collection(db_name="empty", collection_name="empty", items={}):
    try:
        with MongoClient(MONGO_CONNECTION) as client:
            db = client[db_name]
            col = db[collection_name]
            col.insert_many(items)
        return True
    except:
        print("Connection to MongoDB failed")
        return False
        
def clear_collection(db_name="empty", collection_name="empty"):
    try:
        with MongoClient(MONGO_CONNECTION) as client:
            db = client[db_name]
            col = db[collection_name]
            col.drop()
        return True
    except:
        print("Connection to MongoDB failed")
        return False

def get_collection_names(db_name="empty"):
    try:
        with MongoClient(MONGO_CONNECTION) as client:
            db = client[db_name]
            return db.list_collection_names()
    except:
        print("Connection to MongoDB failed")
        return False

def get_database_names():
    try:
        names = MongoClient(MONGO_CONNECTION).list_database_names()
        return names
    except:
        print("Connection to MongoDB failed")
        return ""

def get_database_stats(db_name="empty"):
    try:
        with MongoClient(MONGO_CONNECTION) as client:
            db = client[db_name]
            stats = db.command("dbstats", scale=1024*1024)
            stats_string = "======================================="
            stats_string += "\nDatabase Name: " + str(stats["db"])
            stats_string += "\nNumber of Collections: " + str(stats["collections"])
            stats_string += "\nItems in Collections: " + str(stats["objects"])
            stats_string += "\nSize (MB): " + str(stats["dataSize"])
            stats_string += "\n======================================="
            return stats_string
    except:
        print("Connection to MongoDB failed")
        return ""
        
def print_collection(db_name="empty", collection_name="empty", max_items=10):
    try:
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
    except:
        print("Connection to MongoDB failed")
        return False
        
        