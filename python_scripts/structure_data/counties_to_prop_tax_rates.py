# Last updated by:
# Ryan McCann

# Last updated:
# 05/13/20

# Purpose:
# Creates json file linking counties to their average property tax rates
#   - New York

# Issues/Needed Improvements:
# N/A

# Other Notes:
# Some states' rates are found for their counties. Another script will be made linking
# cities and towns to those counties

# I'm looking into automating this

import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

# *** These rates are assessing for every $1,000 of the home value ***
fp = '/Users/ryanmccann/Desktop/misc/programming/morty_app/data/property_tax_rates/'
# *** Tax rates from New York are assumed to be from 2019 ***

des_page = requests.get('https://smartasset.com/taxes/new-york-property-tax-calculator#z2SjW9yFlE')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in html tds.
all_tds = des_content.find_all('td')
# Resulting list for New York.
ny_res_list = list()

# To filter all other undesired tds
check_var = False
count = 0
# Current county and current rate
curr_county = curr_rate = ''
temp_dict = dict()
res_list = list()
for obj in all_tds:
    # check_divs = obj.find_all('div')
    # for check in check_divs:
    #     for check_2 in check:
    #         if check_2 == 'Please enter a valid email':
    #             print(check_2)
    print(obj)
    for obj_2 in obj:
        # This is where desired html code starts, when the string Albany shows up
        if obj_2 == 'Albany':
            curr_county = 'albany'
            check_var = True
            count += 1
            continue
        if check_var:
            if count == 0:
                # For St. Lawrence county
                if 'St.' in obj_2:
                    temp_list = obj_2.split(' ')
                    curr_county = 'saint_' + temp_list[1].lower()
                    count += 1
                    continue
                curr_county = obj_2.lower()
                curr_county = curr_county.replace(' ', '_')
            elif count == 3:
                # For some reason there are blank strings that exists in the html
                if obj_2 != ' ':
                    obj_2 = obj_2.replace('%', '')
                    # Convert to decimal and then to a dollar value
                    curr_rate = round(((float(obj_2) / 100) * 1000), 2)
                    temp_dict = {'county': curr_county, 'rate': curr_rate}
                    res_list.append(temp_dict)
                    # Yates is the last county, everything after is irrelevant html
                    if curr_county == 'yates':
                        pass
                        # with open(fp + 'new_york_counties.json', 'w') as f_path:
                        #     json.dump(res_list, f_path)
                    temp_dict = dict()
                    count = 0
                    continue
            count += 1

# *** Tax rates from Pennsylvania are assumed to be from 2019 ***
des_page = requests.get('https://smartasset.com/taxes/pennsylvania-property-tax-calculator')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in html tds.
all_tds = des_content.find_all('td')
# Resulting list for New York.
pa_res_list = list()

start = False
end = False
count = 0
for obj in all_tds:
    for obj_2 in obj:
        if obj_2 == 'Adams':
            start = True
            curr_county = 'adams'
            count += 1
            continue
        if start:
            # Must be a county
            if count == 0:
                curr_county = obj_2.lower()
                curr_county = curr_county.replace(' ', '_')
            # Must be a rate
            elif count == 3:
                curr_rate = round(((float(obj_2.replace('%', '')) / 100) * 1000), 2)
                temp_dict = {'county': curr_county, 'rate': curr_rate}
                pa_res_list.append(temp_dict)
                temp_dict = dict()
                count = 0
                continue
            count += 1
            if curr_county == 'york':
                end = True
        if end:
            # with open(fp + 'pennsylvania/counties.json', 'w') as f_path:
            #     json.dump(res_list, f_path)
            break
