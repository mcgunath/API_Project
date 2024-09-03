from utilities.wiki_api_tools import *
from utilities.database_tools import *

links = get_all_pages_links(['Pie', 'Pear', 'Apple'])

add_to_collection(db_name="Wiki", collection_name="links", items=[{title:links[title]} for title in links])
print_collection(db_name="Wiki", collection_name="links", max_items=4)
print(get_database_names())
print(get_collection_names(db_name="Wiki"))
clear_collection(db_name="Wiki", collection_name="links")