import os
from dotenv import load_dotenv
import requests
import json
from utilities.api_tools import search_call

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