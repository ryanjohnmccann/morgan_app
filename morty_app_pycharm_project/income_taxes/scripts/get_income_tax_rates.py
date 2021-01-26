"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    01/26/2020

~ Purpose:
    To collect federal and state income tax rates

~ Issues/Needed Improvements:
    N/A

~ Other Notes:
    I took the rates for 2021 because...why not
"""
import requests
import bs4
import json
from morty_py import useful_functions


def get_federal_rates():
    """
    Gets federal income tax rates for:
        - Single
        - Married (Separate)
        - Married (Joint)
        - Head of Household
    Things to keep in mind are the incomes have a constant added to them and then are multiplied by a percentage over
    a certain amount. For example:
        - The 12% federal income tax rate is $995 PLUS 12% of the amount over $9,950
        - The constant here is $995 and the percentage being multiplied is 12%
    """
    # Response list
    res_list = list()
    des_page = requests.get('https://www.nerdwallet.com/article/taxes/federal-income-tax-brackets')
    des_content = bs4.BeautifulSoup(des_page.content, "html.parser")
    mod_des_content = des_content.select('._2MmLe')
    # Only selecting 2021 federal income taxes for Single, Married, and Head of Household
    des_data = mod_des_content[4:8]
    # To keep track of which tax bracket we're in
    count = 0
    # Keep track of what type of tax filing status we're in
    labels_count = 0
    curr_dict = dict()
    labels_list = ['single', 'married_joint', 'married_separate', 'head_of_household']
    for table in des_data:
        # Data was located in span tags
        spans = table.select('span')
        curr_dict['tax_filing_status'] = labels_list[labels_count]
        # Initializing to remove annoying warnings
        rate = min_income = max_income = None
        for curr_span in spans[3:]:
            curr_text = curr_span.text
            # Percentage
            if count == 0:
                rate = float(curr_text.replace('%', ''))
            # The actual tax bracket
            elif count == 1:
                raw_bracket_list = curr_text.split(' ')
                min_income = float(raw_bracket_list[0].replace('$', '').replace(',', ''))
                if raw_bracket_list[2] == 'more':
                    max_income = None
                else:
                    max_income = float(raw_bracket_list[2].replace('$', '').replace(',', ''))
            # The constant value
            else:
                raw_constant_list = curr_text.split(' ')
                # Edge case, 10% tax bracket has no constant
                if raw_constant_list[0] == '10%':
                    constant = 0.0
                else:
                    constant = float(raw_constant_list[0].replace('$', '').replace(',', ''))
                temp_dict = {'tax_filing_statis': labels_list[labels_count], 'federal_rate': rate / 100,
                             'min_income': min_income, 'max_income': max_income, 'constant': constant}
                res_list.append(temp_dict)
                count = 0
                continue
            count += 1
        labels_count += 1
    # with open('../../../data/income_tax_rates/federal_income_tax_rates.json', 'w')\
    #         as file_name:
    #     json.dump(res_list, file_name)


def get_states_rates():
    pass


def main():
    get_federal_rates()


if __name__ == '__main__':
    main()
