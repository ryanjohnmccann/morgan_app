# Last updated by:
# Ryan McCann

# Last updated:
# 05/08/20

# Purpose:
# Creates a json file with all zip codes for every state I have so far

# Issues/Needed Improvements:
# None known at this point in time

import json
from bs4 import BeautifulSoup as bs
import requests

# Since all data was taken from the same website with the same html layout, an algorithm was created for simplicity.
# dictionary of states and links
state_link_dict = {'massachusetts': 'https://www.zip-codes.com/state/ma.asp',
                   'new_hampshire': 'https://www.zip-codes.com/state/nh.asp',
                   'connecticut': 'https://www.zip-codes.com/state/ct.asp',
                   'rhode_island': 'https://www.zip-codes.com/state/ri.asp',
                   'vermont': 'https://www.zip-codes.com/state/vt.asp',
                   'maine': 'https://www.zip-codes.com/state/me.asp'}

for state, website in state_link_dict.items():
    curr_website = requests.get(website)
    des_content = bs(curr_website.content, "html.parser")
    all_links = des_content.find_all('a')
    curr_res_list = list()
    temp_dict = dict()
    for obj in all_links:
        obj_2 = obj.get('href')
        if obj_2 is None:
            continue
        elif '/city/' in obj_2:
            raw_city = obj_2[9:]
            raw_city = raw_city.split('.asp')
            city = raw_city[0].title()
            # To correctly format cities/towns like north-tewksbury
            if '-' in city:
                temp_list = city.split('-')
                city = temp_list[0] + ' ' + temp_list[1]
            temp_dict['city/town'] = city
            curr_res_list.append(temp_dict)
            temp_dict = dict()
        elif '/zip-code/' in obj_2:
            zip_code = obj_2[10:15]
            temp_dict['zip_code'] = zip_code
    for obj in curr_res_list:
        temp_city = obj['city/town'].lower()
        city = temp_city.replace(' ', '_')
        obj['city/town'] = city

    # with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/zip_codes/' + state + '.json', 'w') as fp:
    #     json.dump(curr_res_list, fp)
    print(state + ' completed.')
