"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    09/04/2020

~ Purpose:
    N/A

~ Issues/Needed Improvements:
    - If a city or town lies in multiple counties, it just takes the first county it belongs in
    - Not all states are found
    - Not all cities and towns have been found

~ Other Notes:
    This code needs to be cleaned and commented, will do so when I get the chance.
"""
import json
import requests
from bs4 import BeautifulSoup
from property_tax_rates.scripts.link_counties_to_cities_towns import link_towns_cities_to_counties
import time
from morty_py.useful_functions import clean_string_property_taxes


def get_all_states(save=True):
    """
    Brings in a downloaded file downloaded locally from GitHub that contains all 50 US states. Slightly formats the
    data and saves it to another JSON file
    :return: None
    """
    all_states_res_list = list()
    # Downloaded from: https://gist.github.com/mshafrir/2646763
    des_data = json.load(open('../data/raw_data/states_info/states_hash.json'))
    # This file also contained territories which we do not care about
    undesired_data = ['american_samoa', 'district_of_columbia', 'federated_states_of_micronesia', 'marshall_islands',
                      'northern_mariana_islands', 'palau', 'puerto_rico', 'virgin_islands', 'guam']
    for key, val in des_data.items():
        curr_state = clean_string_property_taxes(val)
        if curr_state not in undesired_data:
            all_states_res_list.append(curr_state)
    if save:
        with open('../data/structured_data/all_states.json', 'w') as file_path:
            json.dump(all_states_res_list, file_path)
    return all_states_res_list


def get_property_tax_rates(state_to_cities_dict, save=True):
    """
    Finds property tax rates for every city and town in a given state
    :param state_to_cities_dict: The key being the state and the value a list of towns and cities along with the
    county they reside in
    :param save:
    :return: None
    """
    county_to_rate_dict = dict()
    for state, towns_cities_list in state_to_cities_dict.items():
        print(f'\n\t*** RETRIEVING PROPERTY TAX RATES FOR {state} ***')
        url = 'https://smartasset.com/taxes/{}-property-tax-calculator'.format(state.lower().replace(' ', '-'))
        res = requests.get(url)
        replace_dict = {
            'dewitt': 'de_witt',
            'la_salle': 'lasalle',
            'hood_river': 'hoodriver'
        }
        skip_list = [
            'unknown',
            'issaquena',
            'independent_city',
            'none',
            'oglala_lakota',

        ]
        soup = BeautifulSoup(res.text, 'lxml')
        des_table = soup.select('.table-border-top.tab-ctr.wide75.table-columns-left-center'
                                '.table-columns-tight.hide-tabs-in-mobile')[0]
        table_body = des_table.select('tbody')[0]
        items_list = table_body.select('tr')
        for item in items_list:
            county = clean_string_property_taxes(item.select('td')[0].text)
            rate = float(item.select('td')[3].text.replace('%', ''))
            county_to_rate_dict[county] = rate / 100
        for obj in towns_cities_list:
            county = obj['county']
            # Error on their website, has a space then it doesn't
            if county in skip_list:
                continue
            if county in replace_dict.keys() and state != 'texas':
                county = replace_dict[obj['county']]
            obj['rate'] = county_to_rate_dict[county]
        print(f'\t...Complete\n')
        if save:
            with open(f'../data/structured_data/{state}.json', 'w') as file_path:
                json.dump(state_to_cities_dict, file_path)
            with open(f'/Users/ryanmccann/Desktop/misc/programming/morty_app/vsc_scripts/morty_app_ui/src/data/'
                      f'property_tax_rates/{state}.json', 'w') as file_path:
                json.dump(state_to_cities_dict, file_path)
        return state_to_cities_dict


def get_cities_towns(state):
    """
    Given a state, finds all of the cities and town within it
    :param state: A state in the US
    :return: A dictionary that has the state as a key and a list of towns and cities as a value
    """
    print(f'\n\t*** RETRIEVING TOWNS AND CITIES FOR {state} ***')
    url = f"https://www.50states.com/zipcodes/{state.lower().replace(' ', '').replace('_', '')}.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    des_table = soup.select('table')[0]
    towns_cities_list = list()
    for item in des_table.select('a'):
        towns_cities_list.append(clean_string_property_taxes(item.text))
    print(f'\t...Complete\n')
    return {state: towns_cities_list}


def main():
    states_list = get_all_states(save=False)
    for state in states_list:
        if state == 'alaska':
            continue
        print(f'\n=== GETTING PROPERTY TAX RATES FOR {state} ===\n')
        time.sleep(2)
        towns_cities_counties = link_towns_cities_to_counties(state=state)
        get_property_tax_rates(save=True, state_to_cities_dict=towns_cities_counties)


if __name__ == '__main__':
    main()
