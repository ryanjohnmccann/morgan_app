"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    09/05/2020

~ Purpose:
    Create a JSON file with all states and cities that exist within the data so far

~ Issues/Needed Improvements:
    N/A

~ Other Notes:
    N/A
"""
import os
import json


def main():
    # Response list
    res_list = list()
    file_names = [f for f in os.listdir('../data/structured_data/') if '.json' in f and f != 'all_states.json']
    for curr_f_name in file_names:
        curr_dict = json.load(open('../data/structured_data/' + curr_f_name))
        for state, lst in curr_dict.items():
            temp_dict = {state: []}
            for obj in lst:
                temp_dict[state].append(obj['location'])
        res_list.append(temp_dict)
    # Save in this pycharm project
    with open('../data/structured_data/all_states_and_cities.json', 'w') as file_path:
        json.dump(res_list, file_path)
    # Save within the Morty App Visual Studio Code Project
    with open('/Users/ryanmccann/Desktop/misc/programming/morty_app/vsc_scripts/morty_app_ui/src/data/'
              'all_states_and_cities.json', 'w') as file_path:
        json.dump(res_list, file_path)


if __name__ == '__main__':
    main()
