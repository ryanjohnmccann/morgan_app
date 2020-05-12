# Last updated by:
# Ryan McCann

# Last updated:
# 05/11/20

# Purpose:

# Issues/Needed Improvements:
# N/A

# Other Notes:
# Some states' rates are found for their counties. Another script will be made linking
# cities and towns to those counties

# TODO: Have to link all other cities and towns to their proper county

import requests
import json
from bs4 import BeautifulSoup as bs

# *** These rates are assessing for every $1,000 of the home value ***

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
    for obj_2 in obj:
        pass
        # if obj_2 == 'Albany':
        #     curr_county = 'albany'
        #     check_var = True
        #     count += 1
        #     continue
        # if check_var:
        #     if count == 0:
        #         pass
        #     elif count == 3:
        #         # Convert to decimal and then to a dollar value
        #         curr_rate = (obj_2 / 100) * 1000
        #         temp_dict = {'county': curr_county, 'rate': curr_rate}
        #         res_list.append(temp_dict)
        #         temp_dict = dict()
        #     count += 1

# If it equals Albany then we should begin appending to our final list
# Then comes two number we don't care about
# Then comes the percentage
# After that we can continue as normal with the same pattern







