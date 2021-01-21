"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    01/19/2020

~ Purpose:
    To collect federal and state income tax rates

~ Issues/Needed Improvements:
    N/A

~ Other Notes:
    I took the rates for 2021 because...why not
"""
import requests
import bs4


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
        for curr_span in spans[3:]:
            curr_text = curr_span.text
            print(curr_text)
            # Edge case here, there is no constant amount due on top of the percentage
            if count == 0:
                pass
            elif count == 1:
                pass
            else:
                pass


def get_states_rates():
    pass


def main():
    get_federal_rates()


if __name__ == '__main__':
    main()
