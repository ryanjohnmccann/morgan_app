"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    08/25/2020

~ Purpose:
    Creates a json file with house insurances by state

~ Issues/Needed Improvements:
    N/A

~ Other Notes:
    These are ANNUAL fees.
"""
import requests
import json
from bs4 import BeautifulSoup


def get_home_owners_insurances():
    """
    Grabs house insurances for every state in the US
    :return: None
    """
    des_page = requests.get('https://www.policygenius.com/homeowners-insurance/'
                            'how-much-does-homeowners-insurance-cost/')
    des_content = BeautifulSoup(des_page.content, "html.parser")
    # Desired data was found in standard cells in this case
    all_tds = des_content.find_all('td')

    res_list = list()
    temp_dict = dict()
    count = 0
    state_count = 0
    for obj in all_tds:
        for obj_2 in obj:
            # Do not want data after fifty, since there are only fifty states
            if state_count > 50:
                break
            # Data came in as the state followed by its premium
            if count == 0:
                temp_dict['state'] = obj_2.lower().replace(' ', '_')
                count += 1
                state_count += 1
            elif count == 1:
                temp_premium = obj_2.strip('$')
                premium = temp_premium.replace(',', '')
                temp_dict['premium'] = float(premium)
                count = 0
                res_list.append(temp_dict)
                temp_dict = dict()
    with open('../data/house_insurance_by_state.json', 'w') as file_path:
        json.dump(res_list, file_path)


def main():
    get_home_owners_insurances()


if __name__ == '__main__':
    main()
