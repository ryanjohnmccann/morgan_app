# Last updated by:
# Ryan McCann

# Last updated:
# 05/13/20

# Purpose:
# Creates a json file with all fifty states

# Issues/Needed Improvements:
# N/A

# Other Notes:
# N/A

import json

des_data = json.load(open('/Users/ryanmccann/Desktop/2646763-8b0dbb93521f5d6889502305335104218454c2bf/'
                          'states_hash.json'))
res_list = list()
for key, val in des_data.items():
    curr_state = val.lower()
    curr_state = curr_state.replace(' ', '-')
    res_list.append(curr_state)

with open('/Users/ryanmccann/Desktop/misc/programming/morty_app/data/property_tax_rates/all_states.json', 'w') as f_path:
    json.dump(res_list, f_path)
