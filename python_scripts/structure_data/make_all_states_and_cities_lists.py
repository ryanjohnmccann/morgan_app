# Last updated by:
# Ryan McCann

# Last updated:
# 05/08/20

# Purpose:
# Creates a json file with all states and cities on file at the moment

# Issues/Needed Improvements:
# None known at this point in time

import json
import os

fp = '/Users/ryanmccann/Desktop/misc/programming/finance_project/property_tax_rates/'

temp_list = os.listdir(fp)
all_states_list = list()
res_list = list()
# For states
for obj in temp_list:
    if '.json' in obj:
        state = obj.split('.json')
        all_states_list.append(state[0])
# For cities and towns
for state in all_states_list:
    temp_file = json.load(open(fp + state + '.json'))
    temp_list = list()
    temp_dict = dict()
    for obj in temp_file:
        temp_city = obj['city/town'].lower()
        city = temp_city.replace(' ', '_')
        temp_list.append(city)
    temp_dict = {state: temp_list}
    res_list.append(temp_dict)

with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/all_states_and_cities.json', 'w') as file_path:
    json.dump(res_list, file_path)
