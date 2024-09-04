from dotenv import load_dotenv
import requests
import json
import os
import re
import aioconsole
import asyncio

# load info from .env file
load_dotenv()

# assign values from .env file if they exist
WIKI_ACCESS_TOKEN = os.getenv('WIKI_ACCESS_TOKEN')
APP_NAME = os.getenv('APP_NAME')
WIKI_EMAIL = os.getenv('WIKI_EMAIL')

headers = {
    'Authorization': f'Bearer {WIKI_ACCESS_TOKEN}',
    'User-Agent': f'{APP_NAME} ({WIKI_EMAIL})'
}

def get_all_pages_links(titles):
    links = {}
    continuation = True
    # make titles usable in the url
    url_titles = '|'.join(titles)
    url = f'https://en.wikipedia.org/w/api.php?action=query&titles={url_titles}&prop=links&pllimit=max&format=json'

    # the links cannot all be retrieved in one call, so a followup request is required
    while continuation:
        response = requests.get(url)
        
        # close program if status is an error
        if response.status_code >= 400:
            print(f'Unexpected error with article call ({response.status_code})')
            return {}
        
            # convert the response to json
        response = json.loads(response.text)
        
        pages = response['query']['pages']

        # loop for appending the links to each page title
        for pageid in pages:
            if 'links' not in pages[pageid]:
                continue
            page_links = pages[pageid]['links']
            temp_list = []
            for link in page_links:
                temp_list.append(link['title'])
            if pages[pageid]['title'] not in links:
                links[pages[pageid]['title']] = temp_list
            else:
                links[pages[pageid]['title']] += temp_list
                # removes duplicates from the list
                links[pages[pageid]['title']] = list(set(links[pages[pageid]['title']]))
                links[pages[pageid]['title']].sort()
            
        # check if more links can be obtained
        continuation = response['continue']['plcontinue'] if 'continue' in response else ''
        # recreate the url to be used at start of the loop
        url = f'https://en.wikipedia.org/w/api.php?action=query&titles={url_titles}&prop=links&pllimit=max&format=json&plcontinue={continuation}'

    return links

async def get_all_wiki_titles():
    await asyncio.sleep(1)
    global not_stopped
    not_stopped = True
    titles = []
    continuation = True
    url = f'https://en.wikipedia.org/w/api.php?action=query&list=allpages&aplimit=max&format=json'

    while continuation and not_stopped:
        response = requests.get(url)
        # close program if status is an error
        if response.status_code >= 400:
            print(f'Unexpected error with article call ({response.status_code})')
            return ""
        
        # convert the response to json
        response = json.loads(response.text)
        pages = response['query']['allpages']
        for page in pages:
            titles.append({'title': page['title'], 'pageid': page['pageid']})
        
        continuation = response['continue']['apcontinue'] if 'continue' in response else ''
        url = f'https://en.wikipedia.org/w/api.php?action=query&list=allpages&aplimit=max&format=json&apcontinue={continuation}'  
        await asyncio.sleep(0)
    return titles, continuation

def get_page_text(title):
    def cleanup_page_text(text):
        # Removes references/further reading section
        # Removes external links
        # Removes images/gallery
        # Removes reference links
        # Removes double curly brace enclosures
        text = re.sub("==References==.*|==External links==.*|<gallery.*?</gallery>|<ref>.*?</ref>|{{.*?}}|<ref.*?/>", "", text, flags=re.DOTALL)
        
        # Removes file lines
        text = re.sub("^(\[\[)?File.*", "", text, flags=re.MULTILINE)
        
        # Removes the square brackets and left side of words that go to other wikis
        text = re.sub("\[\[([^\|\]\[]*\|([^\|\]\[]*))\]\]", "\g<2>", text, flags=re.DOTALL)
        # Removes the square brackets of words that go to other wikis
        text = re.sub("\[\[(.*?)\]\]", "\g<1>", text, flags=re.DOTALL)
        
        # Removes additional spaces
        text = re.sub("\n\n\n+", "\n\n", text)
        return text
    
    url = f'https://en.wikipedia.org/w/index.php?title={title}&action=raw'
    
    # make API call for getting page text
    response = requests.get(url)
    
    # close program if status is an error
    if response.status_code >= 400:
        print(f'Unexpected error with article call ({response.status_code})')
        return []
    
    # clean the wikitext so that it is readable
    response = cleanup_page_text(response.text)

    return response

def search_call(search_query='pie', language_code='en', number_of_results=1):

    # build url to call
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}

    # make API call for searching
    response = requests.get(url, params=parameters)

    # close program if status is an error
    if response.status_code >= 400:
        print(f'Error with Search Query ({response.status_code})')
        return []

    # convert response to json format
    response = json.loads(response.text)
    
    # return the list of pages found
    return response['pages']

async def stop_api_call():
    global not_stopped
    await aioconsole.ainput("Input anything to stop the program: ")
    not_stopped = False