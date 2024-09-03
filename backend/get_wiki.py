import os
from dotenv import load_dotenv
import requests
import json
from utilities.api_tools import search_call, get_page_text

load_dotenv()

# TODO: clean up code and make asynchronous
WIKI_ACCESS_TOKEN = os.getenv('WIKI_ACCESS_TOKEN')
APP_NAME = os.getenv('APP_NAME')
WIKI_EMAIL = os.getenv('WIKI_EMAIL')

headers = {
  'Authorization': f'Bearer {WIKI_ACCESS_TOKEN}',
  'User-Agent': f'{APP_NAME} ({WIKI_EMAIL})'
}

response = search_call()
title = response[0]['key']

url = f'https://en.wikipedia.org/w/api.php?action=query&titles={title}|Pear&curtimestamp&prop=links&format=json'
response = requests.get(url, headers=headers)

# close program if search status is an error
if response.status_code >= 400:
    print(f'Unexpected error with article call ({response.status_code})')
    raise SystemExit

# convert the response to json, 'parse' encompasses the json
response = json.loads(response.text)

print(response.keys())
#print(response['error'])
timestamp = response['curtimestamp']
response = response['query']
pages = response

print(response.keys())

# links that go to other wiki pages can be obtained as so
print(response['links'])
print(timestamp)