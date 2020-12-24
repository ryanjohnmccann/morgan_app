"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    12/19/2020

~ Purpose:
    Contains functions used in multiple scripts in this project.

~ Issues/Needed Improvements:
    N/A

~ Other Notes:
    N/A
"""


def clean_string_property_taxes(string):
    """
    This function was used when obtaining property tax rates. Cleans a string by doing the following:
        - Converts it to snake case
        - Removes invalid characters
    :param string: A string
    :return: A new string in snake case with punctuation, and special characters removed
    """
    split_string_list = [
        ' of ',
        '[',
        ',',
        '/',
        '3',
    ]
    endswith_list = [
        ' I',
        ' II',
        ' County',
        ' County[9]',
        ' County[8]'
    ]
    starts_with_list = [
        'City and County of'
    ]
    replace_dict = {
        '(seat)': '',
        'St.': 'saint',
        '-': ' ',
        'Township': 'town',
        'Coös': 'coos'
    }
    if string == '—':
        string = 'Unknown'
    for index, item in enumerate(starts_with_list):
        if item in string:
            string = string.replace(item, '')
    for index, item in enumerate(split_string_list):
        if item in string:
            if string.startswith(item):
                break
            string = string.split(split_string_list[index])
            if item == 'of':
                string = string[1]
            else:
                string = string[0]
    for index, item in enumerate(endswith_list):
        if string.endswith(item):
            string = string.split(item)[0]
    for key in replace_dict.keys():
        if key in string:
            string = string.replace(key, replace_dict[key])
    # Removes special characters, punctuation, leading and trailing spaces, and replace spaces with underscores
    new_string = ''.join(e for e in string if e.isalnum() or e == ' ').strip().lower().replace(' ', '_')
    if '_county' in new_string:
        new_string = new_string.split('_county')[0]
    if '__' in new_string:
        new_string = new_string.replace('__', '_')
    if 'county' == new_string:
        new_string = 'unknown'
    if not len(new_string):
        raise Warning('=== EMPTY STRING WAS RETURNED ===')
    return new_string


def clean_string_js(string):
    """

    :param string:
    :return:
    """
    string = string.lower()
    return string.replace(' ', '_')
