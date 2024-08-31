import os
from dotenv import load_dotenv
import requests
import json

# TODO: clean up code and make asynchronous

# load info from .env file
load_dotenv()

# assign values from .env file if they exist
WIKI_ACCESS_TOKEN = os.getenv('WIKI_ACCESS_TOKEN')
APP_NAME = os.getenv('APP_NAME')
WIKI_EMAIL = os.getenv('WIKI_EMAIL')

# define parameters for search query
language_code = 'en'
search_query = 'pie'
number_of_results = 1

headers = {
  'Authorization': f'Bearer {WIKI_ACCESS_TOKEN}',
  'User-Agent': f'{APP_NAME} ({WIKI_EMAIL})'
}

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
    raise SystemExit

# convert response to json format and get the first title from the search query
response = json.loads(response.text)
title = response['pages'][0]['key']

# make API call for previously retrieved article title
url = f'https://api.wikimedia.org/core/v1/wikipedia/en/page/{title}'
response = requests.get(url, headers=headers)

# close program if search status is an error
if response.status_code >= 400:
    print(f'Unexpected error with article call ({response.status_code})')
    raise SystemExit

# convert the response to json
response = json.loads(response.text)

print(response.keys())

# source appears to be where all the content is, could probably remove left and right square brackets from the text??
print(response['source'])