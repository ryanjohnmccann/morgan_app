# Last updated by:
# Ryan McCann

# Last updated:
# 05/13/20

# Purpose:
# Goes through all 50 states and links their counties to a property tax rate

# Issues/Needed Improvements:
# N/A

# Other Notes:
# N/A

import requests
import json
from bs4 import BeautifulSoup as bs
import os

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
    if state in comp_states:
        continue
    curr_page = requests.get('https://smartasset.com/taxes/' + state + '-property-tax-calculator')
    curr_content = bs(curr_page.content, "html.parser")
    all_tds = curr_content.find_all('td')
    curr_res_list = list()
    for td in all_tds:
        if end:
            comp_count += 1
            print(comp_count, 'states completed.', '--> ' + state)
            state = state.replace('-', '_')
            # os.mkdir(fp + state)
            # with open(fp + state + '/counties_rates.json', 'w') as f_path:
            #     json.dump(curr_res_list, f_path)
            curr_res_list = list()
            end = False
            start = False
            break
        elif start:
            for content in td:
                # Tells us our endpoint
                if content == ' ':
                    end = True
                    break
                elif count == 0:
                    if 'St.' in content:
                        temp_list = content.split(' ')
                        content = 'saint_' + temp_list[1]
                    curr_county = content.lower()
                    curr_county = curr_county.replace(' ', '_')
                elif count == 3:
                    curr_rate = round(((float(content.replace('%', '')) / 100) * 1000), 2)
                    temp_dict = {'county': curr_county, 'rate': curr_rate}
                    curr_res_list.append(temp_dict)
                    temp_dict = dict()
                    count = -1
                count += 1
        else:
            # To identify our starting point
            check_divs = td.find_all('div')
            for div in check_divs:
                for content in div:
                    if content == 'Please enter a valid email':
                        start = True

print('Completed.')
