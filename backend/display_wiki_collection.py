from utilities.database_tools import print_collection
from dotenv import load_dotenv
import os

load_dotenv()

WIKI_DATABASE = os.getenv('WIKI_DATABASE')
WIKI_COLLECTION = os.getenv('WIKI_COLLECTION')

print_collection(db_name=WIKI_DATABASE, collection_name=WIKI_COLLECTION, max_items=30)