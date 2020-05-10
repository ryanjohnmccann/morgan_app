# Last updated by:
# Ryan McCann

# Last updated:
# 05/09/20

# Purpose:
# Creates a json file with property tax rates for states in New England

# Issues/Needed Improvements:
# Some cities and towns are missing, need to find them elsewhere

import requests
import pandas as pd
import json
import numpy as np
from bs4 import BeautifulSoup as bs

# *** These tax rates for Massachusetts are from 2019. ***
# Missing towns/cities for Massachusetts:
# - Colrain
# - Florida
# - Gill
# - Gosnold
# - Hardwick
# - Monroe
# - Royalston
# - Wendell
# - Westport
# *** All numbers are for Massachusetts, New Hampshire, Connecticut, and Rhode Island are per $1,000 assessed value ***

des_page = requests.get('https://patch.com/massachusetts/boston/ma-residential-property-tax-rates-each-community')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in html lists.
all_lists = des_content.find_all('li')
# Resulting list for Massachusetts.
ma_res_list = list()
for li in all_lists:
    for obj in li:
        # Town or city names had a dash separating them from the tax rate.
        if '-' in obj:
            temp_list = obj.split('-')
            temp_dict = dict()
            temp_dict['city/town'] = temp_list[0].rstrip(' ').lstrip(' ')
            temp_dict['rate'] = float(temp_list[1].rstrip(' ').lstrip(' ').strip('$'))
            ma_res_list.append(temp_dict)
# Forgot to keep consistency with punctuation. States are all lowercase with a '_' instead of a space.
# For example, up to this point it looks like --> 'city/town': 'North Hampton' instead of 'north_hampton'
# This was done for every states' cities and towns.
for obj in ma_res_list:
    temp_city = obj['city/town'].lower()
    city = temp_city.replace(' ', '_')
    obj['city/town'] = city

# with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/massachusetts.json', 'w')\
#         as file_path:
#     json.dump(ma_res_list, file_path)

# *** Tax rates from New Hampshire are from 2018. ***
# It is unknown at this time is any towns/cities are missing.

temp_rate_list = list()
temp_location_list = list()
raw_data = pd.read_excel('/Users/ryanmccann/Desktop/misc/programming/finance_project/raw_data/'
                         'new_hampshire_tax_rates.xlsx')
for num in raw_data['Total Rate ']:
    # Excel read in with a slightly off format, causing a bunch of 'nan' values between desired values.
    # Each row is a town/city
    if np.isnan(num):
        continue
    temp_rate_list.append(num)

for location in raw_data['Municipality ']:
    try:
        # Same goes here as noted above. Random type 'nan' values were in between desired data.
        # If location is a float, it must be undesired data.
        float(location)
    except:
        # Not sure why '(U)' was in town/city names.
        if '(U)' in location:
            location = location.strip(' (U)')
        if '&' in location:
            location = location.replace(' & ', ' and ')
        if "'" in location:
            location = location.replace("'", "")
        location = location.rstrip(' ').lstrip(' ')
        temp_location_list.append(location)
count = 0
nh_res_list = list()
# There were 260 locations for New Hampshire at this point in time.
while count < 260:
    temp_dict = dict()
    temp_dict = {'city/town': temp_location_list[count], 'rate': temp_rate_list[count]}
    count += 1
    nh_res_list.append(temp_dict)
for obj in nh_res_list:
    temp_city = obj['city/town'].lower()
    city = temp_city.replace(' ', '_')
    obj['city/town'] = city

# with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/new_hampshire.json', 'w')\
#         as file_path:
#     json.dump(nh_res_list, file_path)

# *** Tax rates from Connecticut are from 2019 ***
# It is unknown at this time if any cities/towns are missing.

des_page = requests.get('https://patch.com/connecticut/across-ct/connecticut-property-taxes-every-town-who-pays-most')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in standard cells.
all_tds = des_content.find_all('td')
count = 0
temp_dict = dict()
ct_res_list = list()
for td in all_tds:
    count += 1
    for obj in td:
        if count == 1:
            temp_dict['city/town'] = str(obj)
        elif count == 2:
            try:
                temp_dict['rate'] = float(obj)
            # Some places had an empty string for their rate. If so, unknown was put in place.
            except:
                temp_dict['rate'] = 'unknown'
        elif count == 3:
            ct_res_list.append(temp_dict)
            temp_dict = dict()
            count = 0
            continue

# Average town  list created to take towns with different listed districts and averaged them into
# one town name for simplicity. Rates were reasonably close enough to do so.
avg_towns_list = ['Windham', 'Manchester', 'Norwalk', 'Stamford', 'Groton']

for town in avg_towns_list:
    temp_rate_list = list()
    temp_dict = dict()
    for obj in ct_res_list:
        if town in obj['city/town'] and obj['rate'] != 'unknown':
            temp_rate_list.append(obj['rate'])
    town_avg = round(np.average(temp_rate_list), 2)
    temp_dict = {'city/town': town, 'rate': town_avg}
    ct_res_list.append(temp_dict)

# Now removing all undesired cities and towns. The 'unwanted list' was not based on
# anything other than rates that were extremely low or had names that seemed off and did not seem to fit with
# other cities and towns. For instance, "Stonington Pawcatuck FD #264" with a rate of '0.00158' was deemed undesirable.

undes_ct_list = json.load(open('/Users/ryanmccann/Desktop/misc/programming/finance_project/raw_data/'
                               'unwanted_connecticut_cities.json'))

for town in undes_ct_list:
    for obj in ct_res_list:
        if town in obj['city/town']:
            ct_res_list.remove(obj)
        # Had trouble removing towns with quotations in the name like Stamford "C"
        if 'Stamford' in obj['city/town'] and len(obj['city/town']) > 8:
            ct_res_list.remove(obj)
for obj in ct_res_list:
    temp_city = obj['city/town'].lower()
    city = temp_city.replace(' ', '_')
    obj['city/town'] = city

# with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/connecticut.json', 'w')\
#         as file_path:
#     json.dump(ct_res_list, file_path)

# *** Tax rates from Rhode Island are from 2019 ***
# It is assumed no towns or cities are missing at this time.

# The first raw_data file holds all of the data. A second raw_data file was created because the majority of towns/cities
# were hard to brake up into dictionaries due to extra unwanted data mixed in. So, I copied and pasted towns/cities and
# rates myself into a json file as a list to simply loop over.
raw_data = json.load(open('/Users/ryanmccann/Desktop/misc/programming/finance_project/raw_data/'
                          'raw_rhode_island_data.json'))
raw_data_2 = json.load(open('/Users/ryanmccann/Desktop/misc/programming/finance_project/raw_data/'
                            'raw_rhode_island_data_2.json'))
rhode_res_list = list()
raw_list = list()
for obj in raw_data:
    raw_list.append(obj.split(' '))

# A lot of towns/cities had extra data hard to extract. If the length was five it did not have this extra data.
for obj in raw_list:
    temp_dict = dict()
    if len(obj) == 5:
        rate = obj[1].strip('$')
        city = obj[0].title()
        temp_dict = {'city/town': city, 'rate': float(rate)}
        rhode_res_list.append(temp_dict)

temp_dict = dict()
for obj in raw_data_2:
    if type(obj) is str:
        city = obj.title()
        temp_dict['city/town'] = city
    else:
        temp_dict['rate'] = obj
        rhode_res_list.append(temp_dict)
        temp_dict = dict()
for obj in rhode_res_list:
    temp_city = obj['city/town'].lower()
    city = temp_city.replace(' ', '_')
    obj['city/town'] = city

# with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/rhode_island.json', 'w')\
#         as file_path:
#     json.dump(rhode_res_list, file_path)

# *** Tax rates from Vermont are from 2019 ***
# It is assumed no towns or cities are missing at this time, but unsure.
# Original rates are a percentage per 100 dollar assessed value.
# These rates should not be 100 percent trusted. Since Vermont property tax rates are poorly documented online,
# this is what I came up with.

vermont_res_list = list()
des_page = requests.get('http://www.nancyjenkins.com/Vermont-Property-Tax-Rates')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in standard cells.
all_tds = des_content.find_all('td')

raw_list = list()
temp_dict = dict()
count = 0
for obj in all_tds:
    # City/town and rate came after one another.
    for obj_2 in obj:
        if count == 1:
            temp_dict['rate'] = float(obj_2)
            vermont_res_list.append(temp_dict)
            temp_dict = dict()
            count = 0
        else:
            temp_dict['city/town'] = str(obj_2)
            count += 1

# Undesired city/town names as keys, desired city/town names as values.
remake_dict = {'Bristol (Police District)': 'Bristol', 'St. Albans City': 'Saint Albans City',
               'St. Albans Town': 'Saint Albans Town', 'Jeffersonville (village)': 'Jeffersonville',
               'St. George': 'Saint George'}

for obj in vermont_res_list:
    if obj['city/town'] in remake_dict:
        obj['city/town'] = remake_dict[obj['city/town']]

    # Convert to numerical value per 1,000 value instead of 100
    temp_rate = obj['rate']
    decimal = temp_rate / 100
    num_value = round(1000 * decimal, 2)
    obj['rate'] = float(num_value)
for obj in vermont_res_list:
    temp_city = obj['city/town'].lower()
    city = temp_city.replace(' ', '_')
    obj['city/town'] = city

# with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/vermont.json', 'w')\
#         as file_path:
#     json.dump(vermont_res_list, file_path)

# *** Tax rates from Maine are from 2017 ***
# It is assumed no cities/towns are missing at this time.

maine_res_list = list()
des_page = requests.get('http://mainer.co/maine-property-tax-rates-town/')
des_content = bs(des_page.content, "html.parser")
# In this case, all desired data was located in standard cells.
all_tds = des_content.find_all('td')

count = 0
temp_dict = dict()
# The order in which information comes up is city/town, county, 2017 rate, followed by prior years' rates.
for obj in all_tds:
    for obj_2 in obj:
        if count == 0:
            # Replacing Plt with Plantation.
            if 'PLT' in obj_2:
                temp_list = obj_2.split(' ')
                new_word = ''
                for word in temp_list:
                    if word != 'PLT' and new_word == '':
                        new_word = word
                    elif word != 'PLT':
                        new_word += (' ' + word)
                    else:
                        word = 'Plantation'
                        new_word += (' ' + word)
                        temp_dict['city/town'] = new_word.title()
                        new_word = ''
            else:
                if 'LAKE STR' in obj_2:
                    obj_2 = 'Grand Lake Stream'
                elif "SWAN'S" in obj_2:
                    obj_2 = 'Swans Island'
                temp_dict['city/town'] = obj_2.title()
        # For rates.
        elif count == 2:
            obj_2 = obj_2.strip('$')
            obj_2 = float(obj_2)
            temp_dict['rate'] = obj_2
            # Getting rid of country averages.
            if temp_dict['city/town'] == 'County Average':
                count += 1
                continue
            maine_res_list.append(temp_dict)
            temp_dict = dict()
        elif count == 4:
            count = 0
            continue
        count += 1
for obj in maine_res_list:
    temp_city = obj['city/town'].lower()
    city = temp_city.replace(' ', '_')
    obj['city/town'] = city

# with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/maine.json', 'w')\
#         as file_path:
#     json.dump(maine_res_list, file_path)
