from dotenv import load_dotenv
import requests
import json
import os
import re

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

def search_call(search_query='pie', language_code='en', number_of_results=1):

    # build url to call
    base_url = 'https://api.wikimedia.org/core/v1/wikipedia/'
    endpoint = '/search/page'
    url = base_url + language_code + endpoint
    parameters = {'q': search_query, 'limit': number_of_results}

    # make API call for searching
    response = requests.get(url, headers=headers, params=parameters)

    # close program if status is an error
    if response.status_code >= 400:
        print(f'Error with Search Query ({response.status_code})')
        return []

    # convert response to json format and get the first title from the search query
    response = json.loads(response.text)
    return response['pages']

def get_page_text(title):
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

def cleanup_page_text(text):

    # Removes references section
    # Removes external links
    # Removes images/gallery
    # Removes references/further readings
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