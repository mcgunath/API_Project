from utilities.wiki_api_tools import *
from utilities.database_tools import *
import asyncio
#links = get_all_pages_links(['Pie', 'Pear', 'Apple'])

#add_to_collection(db_name="Wiki", collection_name="links", items=[{"title": title,"links_on_page":links[title]} for title in links])
async def main():
    response = await asyncio.gather(
        stop_api_call(),
        get_all_wiki_titles(),
    )
    
    list_of_titles = response[1][0]
    next_title = response[1][1]
    
    print(list_of_titles)
    print("Number of Titles Retrieved:", len(list_of_titles))
    print("Next Title:", next_title)
    
asyncio.run(main())