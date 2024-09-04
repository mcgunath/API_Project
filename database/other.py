
import asyncio
import aioconsole
#links = get_all_pages_links(['Pie', 'Pear', 'Apple'])

#add_to_collection(db_name="Wiki", collection_name="links", items=[{"title": title,"links_on_page":links[title]} for title in links])

outside = True

async def test_func():
    i = 0
    while outside:
        print(i)
        i += 1
        await asyncio.sleep(2)
        
async def input_func():
    global outside
    await aioconsole.ainput("Input anything to stop the program: ")
    outside = False

        
async def running_func():
    await asyncio.gather(
        test_func(),
        input_func()
    )
        
asyncio.run(running_func())