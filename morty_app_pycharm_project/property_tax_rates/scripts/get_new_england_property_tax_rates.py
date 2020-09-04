"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    08/24/2020

~ Purpose:
    Creates a json file with property tax rates for most cities and towns in New England

~ Issues/Needed Improvements:
    Some cities and towns are missing, working on finding them elsewhere

~ Other Notes:
    All rates are per $1,000 assessed value
"""
import requests
import pandas as pd
import json
import numpy as np
from bs4 import BeautifulSoup as bs


def massachusetts():
    """
    Gets property tax rates for the state of Massachusetts
    *** These tax rates for Massachusetts are from 2019. ***
    ~ Missing towns/cities for Massachusetts:
        - Colrain
        - Florida
        - Gill
        - Gosnold
        - Hardwick
        - Monroe
        - Royalston
        - Wendell
        - Westport
    :return: None
    """
    des_page = requests.get('https://patch.com/massachusetts/boston/ma-residential-property-tax-rates-each-community')
    des_content = bs(des_page.content, "html.parser")
    # In this case, all desired data was located in html lists.
    all_lists = des_content.find_all('li')
    # Resulting list for Massachusetts.
    ma_res_list = list()
    for curr_li in all_lists:
        for obj in curr_li:
            # Town or city names had a dash separating them from the tax rate.
            if '-' in obj:
                temp_list = obj.split('-')
                temp_dict = dict()
                temp_dict['city/town'] = temp_list[0].strip(' ').lower().replace(' ', '_')
                temp_dict['rate'] = float(temp_list[1].strip(' ').strip('$'))
                ma_res_list.append(temp_dict)
    with open('../data/misc/massachusetts.json', 'w') as file_path:
        json.dump(ma_res_list, file_path)


def new_hampshire():
    """
    Gets property tax rates for the state of New Hampshire
    *** Tax rates from New Hampshire are from 2018. ***
    ~ It is unknown at this time is any towns/cities are missing.
    :return: None
    """
    # File found somewhere online which I copy and pasted into an excel file.
    raw_data = pd.read_excel('../data/raw_data/new_hampshire_tax_rates.xlsx')
    # Excel read in with a strange format, causing a bunch of 'nan' values between desired values.
    # Each row is a town/city.
    temp_rate_list = [rate for rate in raw_data['Total Rate '] if not np.isnan(rate)]
    temp_location_list = list()
    for location in raw_data['Municipality ']:
        # Same goes here as noted above. Random type 'nan' values were in between desired data.
        # If location is a float, it must be undesired data.
        if isinstance(location, float):
            continue
        # Not sure why '(U)' was in town/city names.
        if '(U)' in location:
            location = location.strip(' (U)')
        if '&' in location:
            location = location.replace(' & ', ' and ')
        if "'" in location:
            location = location.replace("'", "")
        temp_location_list.append(location.strip(' '))
    # The resulting list for New Hampshire
    nh_res_list = list()
    for index in range(0, len(temp_rate_list)):
        nh_res_list.append({'city/town': temp_location_list[index].lower().replace(' ', '_'),
                            'rate': temp_rate_list[index]})
    with open('../data/misc/new_hampshire.json', 'w') as file_path:
        json.dump(nh_res_list, file_path)


def vermont():
    """
    Gets property tax rates for the state of New Hampshire
    *** Tax rates from Vermont are from 2019 ***
    ~ It is assumed no towns or cities are missing at this time

    Original rates are a percentage per 100 dollar assessed value.
    These rates should not be 100 percent trusted. Since Vermont property tax rates are poorly documented online,
    this is what I came up with.
    :return: None
    """
    # The resulting list for vermont
    vermont_res_list = list()
    des_page = requests.get('http://www.nancyjenkins.com/Vermont-Property-Tax-Rates')
    des_content = bs(des_page.content, "html.parser")
    # In this case, all desired data was located in standard cells.
    all_tds = des_content.find_all('td')
    temp_dict = dict()
    count = 0
    # Undesired city/town names as keys, desired city/town names as values.
    remake_dict = {'Bristol (Police District)': 'Bristol', 'St. Albans City': 'Saint Albans City',
                   'St. Albans Town': 'Saint Albans Town', 'Jeffersonville (village)': 'Jeffersonville',
                   'St. George': 'Saint George'}
    for obj in all_tds:
        # City/town and rate came after one another.
        for obj_2 in obj:
            if count == 1:
                temp_rate = float(obj_2)
                decimal = temp_rate / 100
                temp_dict['rate'] = round(1000 * decimal, 2)
                vermont_res_list.append(temp_dict)
                temp_dict = dict()
                count = 0
            else:
                if str(obj_2) in remake_dict:
                    temp_dict['city/town'] = remake_dict[str(obj_2)['city/town']]
                else:
                    temp_dict['city/town'] = str(obj_2).lower().replace(' ', '_')
                count += 1
    with open('../data/misc/vermont.json', 'w') as file_path:
        json.dump(vermont_res_list, file_path)


def connecticut():
    """
    Gets property tax rates for the state of Connecticut
    *** Tax rates from Connecticut are from 2019 ***
    ~ It is unknown at this time if any cities/towns are missing.
    :return: None
    """
    des_page = requests.get('https://patch.com/connecticut/across-ct/'
                            'connecticut-property-taxes-every-town-who-pays-most')
    des_content = bs(des_page.content, "html.parser")
    # In this case, all desired data was located in standard cells.
    all_tds = des_content.find_all('td')
    count = 0
    temp_dict = dict()
    # The resulting list for Connecticut
    ct_res_list = list()
    for curr_td in all_tds:
        count += 1
        for obj in curr_td:
            if count == 1:
                temp_dict['city/town'] = str(obj)
            elif count == 2:
                try:
                    temp_dict['rate'] = float(obj)
                # Some places had an empty string for their rate. If so, unknown was put in place.
                except ValueError:
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
        for obj in ct_res_list:
            if town in obj['city/town'] and obj['rate'] != 'unknown':
                temp_rate_list.append(obj['rate'])
        town_avg = round(np.average(temp_rate_list), 2)
        temp_dict = {'city/town': town, 'rate': town_avg}
        ct_res_list.append(temp_dict)
    # Now removing all undesired cities and towns. The 'unwanted list' was not based on
    # anything other than rates that were extremely low or had names that seemed off and did not fit with
    # other cities and towns. For instance, "Stonington Pawcatuck FD #264" with a rate of '0.00158' is undesirable.
    undes_ct_list = json.load(open('../data/raw_data/unwanted_connecticut_cities.json'))
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
    with open('../data/misc/connecticut.json', 'w') as file_path:
        json.dump(ct_res_list, file_path)


def rhode_island():
    """
    Gets property tax rates for the state of Rhode Island
    *** Tax rates from Rhode Island are from 2019 ***
    ~ It is assumed no towns or cities are missing at this time.
    :return: None
    """
    # The first raw_data file holds all of the data. A second raw_data file was created because the majority of
    # towns/cities were hard to brake up into dictionaries due to extra unwanted data mixed in. So, I copied and pasted
    # towns/cities and rates myself into a json file as a list to simply loop over.
    raw_data = json.load(open('../data/raw_data/raw_rhode_island_data.json'))
    raw_data_2 = json.load(open('../data/raw_data/raw_rhode_island_data_2.json'))
    # The resulting list for Rhode Island
    rhode_res_list = list()
    for obj in raw_data:
        new_obj = obj.split(' ')
        # A lot of towns/cities had extra data hard to extract. If the length was five it did not have this extra data.
        if len(new_obj) == 5:
            rate = new_obj[1].strip('$')
            city = new_obj[0].title()
            temp_dict = {'city/town': city.lower().replace(' ', '_'), 'rate': float(rate)}
            rhode_res_list.append(temp_dict)
    temp_dict = dict()
    for obj in raw_data_2:
        if type(obj) is str:
            temp_dict['city/town'] = obj.lower().replace(' ', '_')
        else:
            temp_dict['rate'] = float(obj)
            rhode_res_list.append(temp_dict)
            temp_dict = dict()
    with open('../data/misc/rhode_island.json', 'w') as file_path:
        json.dump(rhode_res_list, file_path)


def maine():
    """
    Gets property tax rates for the state of Maine
    *** Tax rates from Maine are from 2017 ***
    ~ It is assumed no cities/towns are missing at this time.
    :return: None
    """
    # The resulting list for Maine
    maine_res_list = list()
    des_page = requests.get('http://mainer.co/maine-property-tax-rates-town/')
    des_content = bs(des_page.content, "html.parser")
    # In this case, all desired data was located in standard cells.
    all_tds = des_content.find_all('td')
    count = 0
    temp_dict = dict()
    # The order in which information comes up is city/town, county, 2017 rate, followed by prior year's rates.
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
                            temp_dict['city/town'] = new_word.lower().replace(' ', '_')
                            new_word = ''
                else:
                    if 'LAKE STR' in obj_2:
                        obj_2 = 'Grand Lake Stream'
                    elif "SWAN'S" in obj_2:
                        obj_2 = 'Swans Island'
                    temp_dict['city/town'] = obj_2.lower().replace(' ', '_')
            # For rates
            elif count == 2:
                obj_2 = obj_2.strip('$')
                temp_dict['rate'] = float(obj_2)
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
    with open('../data/misc/maine.json', 'w') as file_path:
        json.dump(maine_res_list, file_path)


def main():
    massachusetts()
    maine()
    connecticut()
    rhode_island()
    vermont()
    new_hampshire()


if __name__ == '__main__':
    main()
