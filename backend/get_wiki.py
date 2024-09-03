from utilities.api_tools import *

links = get_all_pages_links(['Pie', 'Pear', 'Apple'])
print(len(links['Pie']))
print(len(links['Pear']))
print(len(links['Apple']))