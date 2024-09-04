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
    time_elapsed = response[1][2]
    
    number_of_titles = len(list_of_titles)
    print("Number of Titles Retrieved:", number_of_titles)
    print("Next Title:", next_title)
    print("Average Seconds per Query (500 titles):", time_elapsed * 500 / number_of_titles)
    print("Total Time Elapsed:", time_elapsed, "seconds")
    print("Time to retrieve all titles (about 7mil): ~", \
        int((time_elapsed / number_of_titles) * 7000000 / 60), "mins",\
        int((time_elapsed / number_of_titles) * 7000000 % 60), "seconds")
 
if __name__ == '__main__':
    asyncio.run(main())