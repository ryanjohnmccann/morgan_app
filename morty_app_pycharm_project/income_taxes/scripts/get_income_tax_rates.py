"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    01/08/2020

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
    """
    # Response list
    res_list = list()
    des_page = requests.get('https://www.nerdwallet.com/article/taxes/federal-income-tax-brackets')
    des_content = bs4.BeautifulSoup(des_page.content, "html.parser")
    mod_des_content = des_content.select('._2MmLe')
    for obj in mod_des_content:
        print(obj)
    # print(des_content.prettify())


def main():
    get_federal_rates()


if __name__ == '__main__':
    main()
