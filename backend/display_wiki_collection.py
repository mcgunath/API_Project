from utilities.database_tools import print_collection, get_database_stats, get_collection_names
from dotenv import load_dotenv
import os

load_dotenv()

WIKI_DATABASE = os.getenv('WIKI_DATABASE')
WIKI_COLLECTION = os.getenv('WIKI_COLLECTION')

print_collection(db_name=WIKI_DATABASE, collection_name=WIKI_COLLECTION, max_items=30)
print(get_database_stats(db_name=WIKI_DATABASE))
print("Wiki Collection Names:", get_collection_names(db_name=WIKI_DATABASE))