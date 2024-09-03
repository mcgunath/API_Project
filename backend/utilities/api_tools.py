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

    # close program if search status is an error
    if response.status_code >= 400:
        print(f'Error with Search Query ({response.status_code})')
        return []

    # convert response to json format and get the first title from the search query
    response = json.loads(response.text)
    return response['pages']

def get_page_text(title):
    url = f'https://api.wikimedia.org/core/v1/wikipedia/en/page/{title}'
    response = requests.get(url, headers=headers)
    # close program if search status is an error
    if response.status_code >= 400:
        print(f'Unexpected error with article call ({response.status_code})')
        return []
    
    # convert the response to json, 'parse' encompasses the json
    response = json.loads(response.text)
    response = response['source']
    response = re.sub("{{.*}}", "", response)
    response = re.sub("==References==.*== Further reading ==", "== Further reading ==", response, flags=re.DOTALL)
    #response = re.sub("\[\[^(\]).*\]\]", "", response)
    #response = response.replace("[[", "")
    #response = response.replace("]]", "")
    return response