# Last updated by:
# Ryan McCann

# Last updated:
# 05/13/20

# Purpose:
# Link towns and cities to their appropriate county for:
#   - New York

# Issues/Needed Improvements:
# N/A

# Other Notes:
# Looking into automating this

import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

fp = '/Users/ryanmccann/Desktop/misc/programming/morty_app/data/property_tax_rates/new_york/'

# *** New York ***

des_page = requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_New_York')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in html tds.
all_tds = des_content.find_all('td')

curr_town = ''
curr_county = ''
check_town_var = False
check_county_var = False
count = 0
res_list = list()
# For New York towns
for obj in all_tds:
    for obj_2 in obj:
        # Towns were nested inside a 'td' tag and then in an 'a' tag
        all_as = obj.find_all('a')
        if all_as:
            for obj_3 in all_as[0]:
                # Adams is the first piece of desired html
                if obj_3 == 'Adams':
                    obj_3 = 'adams'
                    check_town_var = True
                    check_county_var = True
                if check_town_var:
                    curr_town = obj_3.lower()
                    curr_town = curr_town.replace(' ', '_')
                    check_county_var = True
                    break
            continue
        # Counties were only inside a 'td' tag
        if check_county_var:
            # For St. Lawrence county
            if 'St.' in obj_2:
                temp_list = obj_2.split(' ')
                curr_county = 'saint_' + temp_list[1].lower()
            else:
                curr_county = obj_2.lower()
                curr_county = curr_county.replace(' ', '_')
            temp_dict = {'city/town': curr_town, 'county': curr_county}
            res_list.append(temp_dict)
            temp_dict = dict()
            check_county_var = False
    # Last piece of desired html ends here
    if curr_county == 'westchester' and curr_town == 'yorktown':
        break

# For New York Cities
des_page = requests.get('https://en.wikipedia.org/wiki/List_of_cities_in_New_York')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in html a tags.
all_tds = des_content.find_all('a')

start = False
stop = False
# For if a city lies in multiple counties
mult_counties = False
num_counties = 0
term_mult_counties = 0
curr_city = ''
curr_county = ''
count = 0
# There are multiple New Yorks, some considered cities and some counties
# This count is created to identify between them
ny_count = 0
for obj in all_tds:
    for obj_2 in obj:
        if '[' in obj_2:
            continue
        # For cities with multiple counties
        if obj_2 == 'Geneva' and start:
            curr_city = 'geneva'
            mult_counties = True
            num_counties = 2
            counties_list = list()
            continue
        elif obj_2 == 'New York' and start and ny_count == 0:
            ny_count += 1
            curr_city = 'new_york'
            mult_counties = True
            num_counties = 5
            counties_list = list()
            continue
        if mult_counties:
            curr_county = obj_2.lower()
            curr_county = curr_county.replace(' ', '_')
            counties_list.append(curr_county)
            term_mult_counties += 1
            if term_mult_counties == num_counties:
                mult_counties = False
                term_mult_counties = 0
                temp_dict = {'city/town': curr_city, 'county': counties_list}
                res_list.append(temp_dict)
                temp_dict = dict()
            continue
        # Desired html data starts here
        # There are multiple 'Albany' strings so we don't want this
        # if statement to execute unless it's the first 'Albany' seen
        if obj_2 == 'Albany' and count == 0:
            start = True
            count += 1
        if start and check_county_var is False:
            curr_city = obj_2.lower()
            curr_city = curr_city.replace(' ', '_')
            check_county_var = True
            continue
        if check_county_var:
            if 'St.' in obj_2:
                temp_list = obj_2.split(' ')
                curr_county = 'saint_' + temp_list[1].lower()
            else:
                curr_county = obj_2.lower()
                curr_county = curr_county.replace(' ', '_')
            temp_dict = {'city/town': curr_city, 'county': curr_county}
            res_list.append(temp_dict)
            temp_dict = dict()
            check_county_var = False
    if stop:
        break
    if curr_city == 'yonkers' and curr_county == 'westchester':
        stop = True

# with open(fp + 'new_york_cities_towns_to_county.json', 'w') as f_path:
#     json.dump(res_list, f_path)

# *** Pennsylvania ***

# For towns
des_page = requests.get('https://en.wikipedia.org/wiki/List_of_towns_and_boroughs_in_Pennsylvania')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in html a tags.
all_as = des_content.find_all('a')

start = False
end = False
mult_counties = False
count = 0
# For multiple counties
mult_count = 0
pa_res_list = list()
counties_list = list()
# A list with towns that are in multiple counties
mult_counties_list = ['Adamstown', 'Ashland', 'Ellwood City', 'Falls Creek', 'Emlenton', 'Mcdonald',
                      'Seven Springs', 'Shippensburg', 'Telford', 'Trafford', 'Tunnelhill']
for obj in all_as:
    for obj_2 in obj:
        if obj_2 == 'Abbottstown':
            start = True
            curr_town = 'abbottstown'
            count += 1
            continue
        # All towns were in two counties. No more no less
        if obj_2 in mult_counties_list:
            curr_town = obj_2.lower()
            curr_town = curr_town.replace(' ', '_')
            mult_counties = True
            continue
        if mult_counties:
            curr_county = obj_2.lower()
            curr_county = curr_county.replace(' ', '_')
            counties_list.append(curr_county)
        if start:
            # Towns
            if count == 0:
                curr_town = obj_2.lower()
                curr_town = curr_town.replace(' ', '_')
                count += 1
            # Rates
            elif count == 1:
                count = 0
                curr_county = obj_2.lower()
                curr_county = curr_county.replace(' ', '_')
                temp_dict = {'city/town': curr_town, 'county': curr_county}
                pa_res_list.append(temp_dict)
                print(temp_dict)
                temp_dict = dict()
            if curr_town == 'zelienople' and curr_county == 'butler':
                end = True
        if end:
            break
