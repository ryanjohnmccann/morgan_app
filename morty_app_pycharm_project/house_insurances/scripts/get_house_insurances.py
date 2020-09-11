"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    09/11/2020

~ Purpose:
    N/A

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
    """
    # Response list
    res_list = list()
    des_page = requests.get('https://www.policygenius.com/homeowners-insurance/'
                            'how-much-does-homeowners-insurance-cost/')
    des_content = BeautifulSoup(des_page.content, "html.parser")
    # Selected by class name
    des_data = des_content.select('.bq_d3.bM_pt.bc_hw')
    # Controls when to stop scraping the data
    count = 0
    for item in des_data:
        new_item = item.text
        if count == 101:
            break
        # House Insurance
        if new_item.startswith('$'):
            rate = float(new_item.replace('$', '').replace(',', ''))
            res_list.append({'state': state, 'rate': rate})
        # State
        else:
            state = new_item.lower().replace(' ', '_')
        count += 1
    with open('../data/house_insurance_by_state.json', 'w') as file_path:
        json.dump(res_list, file_path)


def main():
    get_home_owners_insurances()


if __name__ == '__main__':
    main()
