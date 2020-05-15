# Last updated by:
# Ryan McCann

# Last updated:
# 05/13/20

# Purpose:
# Creates json file with property tax rates for
#   - New York

# Issues/Needed Improvements:
# N/A

# Other Notes:
# N/A

import requests
import json
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

# *** These rates are assessing for every $1,000 of the home value ***
fp = '/Users/ryanmccann/Desktop/misc/programming/morty_app/data/property_tax_rates/'

# *** Tax rates from New York are assumed to be from 2019 ***

# New York counties and their property tax rates
ny_rates = json.load(open(fp + 'new_york/counties.json'))
# New York cities and towns linked to their county
ny_cit_count = json.load(open(fp + 'new_york/cities_towns_to_county.json'))

res_list = list()
for obj in ny_cit_count:
    curr_city = obj['city/town']
    curr_county = obj['county']
    if 'st.' in curr_city:
        temp_var = curr_city.split('_')
        curr_city = 'saint_' + temp_var[1]
    # Cities that are in multiple counties
    # An average is taken of the counties it is in
    if type(curr_county) == list:
        # Average of the multiple counties
        # There exists a town and a city with the name 'geneva'
        if curr_city == 'geneva':
            curr_city = 'geneva_city'
        mult_rates = list()
        for county in curr_county:
            for obj_3 in ny_rates:
                if obj_3['county'] == county:
                    mult_rates.append(obj_3['rate'])
        des_rate = np.mean(mult_rates)
    else:
        for obj_2 in ny_rates:
            if curr_county == obj_2['county']:
                des_rate = obj_2['rate']
    temp_dict = {'city/town': curr_city, 'rate': des_rate}
    res_list.append(temp_dict)
    temp_dict = dict()

# with open(fp + 'new_york.json', 'w') as f_path:
#     json.dump(res_list, f_path)
