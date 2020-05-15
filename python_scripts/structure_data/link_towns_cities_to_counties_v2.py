# Last updated by:
# Ryan McCann

# Last updated:
# 05/13/20

# Purpose:

# Issues/Needed Improvements:
# Alaska and Hawaii have not been included yet

# Other Notes:

import json
import requests
from bs4 import BeautifulSoup as bs

fp = '/Users/ryanmccann/Desktop/misc/programming/morty_app/data/property_tax_rates/'
all_states = json.load(open(fp + 'all_states.json'))
# Already completed states
comp_states = [
    'massachusetts',
    'new-york',
    'maine',
    'vermont',
    'connecticut',
    'rhode-island',
    'new-hampshire'
]
count = 0
comp_count = 0
start = False
end = False
for state in all_states:
    def identify_category(html):
        pass
    if state in comp_states:
        continue
    temp_state = state.title()
    temp_state = temp_state.replace('-', '_')
    curr_page_towns = requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_' + temp_state)
    curr_page_cities = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_' + temp_state)
    curr_content_towns = bs(curr_page_towns.content, "html.parser")
    curr_content_cities = bs(curr_page_cities.content, "html.parser")
    all_as_towns = curr_content_towns.find_all('td')
    all_as_cities = curr_content_cities.find_all('td')

    for obj in all_as_towns:
        print(obj)
    print('========== STATE COMPLETED ==========')

# TODO: Create categories of different layouts
# Categories:
#   - type_a (name, type, counties)
# Indiana is different
