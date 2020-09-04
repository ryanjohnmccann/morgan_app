"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    08/28/2020

~ Purpose:
    N/A

~ Issues/Needed Improvements:
    - If a city/town lies in multiple counties, only one is taken

~ Other Notes:
    N/A
"""

import requests
from bs4 import BeautifulSoup
from morty_py.useful_functions import clean_string_property_taxes


# TODO: Web scrape towns that were not included in select states (see comments below)
# TODO: Add all counties states belong to in a list form
# TODO: It may be easier to select hyperlinks instead of table data
# TODO: Have input parameters to show certain things (Like print_url=True)
# TODO: Comment this code better, more specifically formats
# TODO: Create a different class with formats?
# TODO: If something fails on one format, switch to the next
# TODO: Decrease the amount of formats
# TODO: Format six and seven are exactly the same I think
# TODO:

class States:

    def __init__(self, state):
        self.state = state
        self.response_list = list()
        print(f'\t*** NOW BEGINNING TO LINK STATES AND CITIES TO A COUNTY FOR {state} ***')
        url_index = 0
        response = find_correct_wiki_url(state=state, url_index=url_index)
        while True:
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                des_table = soup.select('.wikitable.sortable')[0]
                break
            except IndexError:
                url_index += 1
                response = find_correct_wiki_url(state=state, url_index=url_index)
                continue
        self.table_rows_list = des_table.select('tr')

    def format_one(self, location_index, location_type_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[location_index].text)
            location_type = clean_string_property_taxes(table_data[location_type_index].text)
            county = clean_string_property_taxes(table_data[county_index].text)
            self.response_list.append({'location': location, 'location_type': location_type, 'county': county})
        return self.response_list

    def format_two(self, location_index, location_type_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(item.select('th')[location_index].text)
            location_type = clean_string_property_taxes(table_data[location_type_index].text)
            county = clean_string_property_taxes(table_data[county_index].text)
            self.response_list.append({'location': location, 'location_type': location_type, 'county': county})
        return self.response_list

    def format_three(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[location_index].text)
            county = clean_string_property_taxes(table_data[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_four(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(item.select('th')[location_index].text)
            county = clean_string_property_taxes(table_data[0].select('a')[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_five(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[location_index].text)
            county = clean_string_property_taxes(table_data[5].select('a')[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_six(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            if len(table_data) == 1:
                continue
            location = clean_string_property_taxes(table_data[location_index].text)
            county = clean_string_property_taxes(table_data[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_seven(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            if len(table_data) == 1:
                continue
            location = clean_string_property_taxes(table_data[location_index].text)
            county = clean_string_property_taxes(table_data[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_eight(self, location_index, location_type_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[location_index].text)
            location_type = clean_string_property_taxes(table_data[location_type_index].text)
            county = clean_string_property_taxes(table_data[county_index].select('a')[0].text)
            self.response_list.append({'location': location, 'location_type': location_type, 'county': county})
        return self.response_list

    def format_nine(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[location_index].text)
            county = clean_string_property_taxes(table_data[county_index].select('a')[0].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_ten(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            if not len(item.select('th')):
                continue
            location = clean_string_property_taxes(item.select('th')[location_index].text)
            county = clean_string_property_taxes(table_data[0].select('a')[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_eleven(self, location_index, county_index, start_index, stop_index=None):
        if stop_index is not None:
            self.table_rows_list = self.table_rows_list[start_index: stop_index]
        else:
            self.table_rows_list = self.table_rows_list[start_index:]
        for item in self.table_rows_list:
            table_data = item.select('td')
            if len(table_data) < 4:
                continue
            location = clean_string_property_taxes(table_data[location_index].text)
            county = clean_string_property_taxes(table_data[county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def alabama(self):
        return self.format_one(start_index=2, stop_index=-3, location_index=0, location_type_index=1, county_index=2)

    def alaska(self):
        return self.response_list

    def arizona(self):
        return self.format_one(start_index=2, stop_index=-2, location_index=0, location_type_index=1, county_index=2)

    def arkansas(self):
        return self.format_one(start_index=1, stop_index=None, location_index=1, location_type_index=2, county_index=3)

    def california(self):
        return self.format_two(start_index=2, stop_index=None, location_index=0, location_type_index=0, county_index=1)

    def colorado(self):
        return self.format_one(start_index=1, stop_index=None, location_index=0, location_type_index=1, county_index=4)

    def connecticut(self):
        return self.format_one(start_index=1, stop_index=-1, location_index=1, location_type_index=2, county_index=7)

    def delaware(self):
        return self.format_one(start_index=1, stop_index=None, location_index=1, location_type_index=2, county_index=5)

    def florida(self):
        return self.format_eight(start_index=1, stop_index=None, location_index=0, location_type_index=5, county_index=1)

    def georgia(self):
        return self.format_one(start_index=1, stop_index=None, location_index=1, location_type_index=5, county_index=6)

    def hawaii(self):
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=3)

    def idaho(self):
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=5)

    def illinois(self):
        return self.format_one(start_index=1, stop_index=None, location_index=0, location_type_index=1, county_index=3)

    def indiana(self):
        # Towns are missing for indiana, they're in a separate wiki page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Indiana
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=5)

    def iowa(self):
        return self.format_four(start_index=2, stop_index=None, location_index=0, county_index=0)

    def kansas(self):
        # Towns are missing for kansas, they're in a separate wiki page:
        # https://en.wikipedia.org/wiki/List_of_townships_in_Kansas
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=5)

    def kentucky(self):
        return self.format_nine(start_index=1, stop_index=None, location_index=0, county_index=6)

    def louisiana(self):
        return self.format_one(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=2)

    def maine(self):
        # Towns are missing for maine, they're in a separate wiki page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Maine
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=5)

    def maryland(self):
        return self.format_one(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=2)

    def massachusetts(self):
        return self.format_one(start_index=1, stop_index=None, location_index=0, location_type_index=1, county_index=2)

    def michigan(self):
        return self.format_eight(start_index=2, stop_index=None, location_index=0, location_type_index=1,
                                 county_index=2)

    def minnesota(self):
        # Towns are missing for minnesota, they currently cannot be found on Wikipedia
        return self.format_five(start_index=1, stop_index=None, location_index=1, county_index=0)

    def mississippi(self):
        return self.format_one(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=2)

    def missouri(self):
        return self.format_one(start_index=1, stop_index=None, location_index=0, location_type_index=1, county_index=3)

    def montana(self):
        return self.format_one(start_index=2, stop_index=-3, location_index=0, location_type_index=1, county_index=2)

    def nebraska(self):
        # Towns are missing for Nebraska, they currently cannot be found on Wikipedia
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=5)

    def nevada(self):
        # Towns are missing for Nevada, they currently cannot be found on Wikipedia
        return self.format_one(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=2)

    def new_hampshire(self):
        return self.format_three(start_index=1, stop_index=None, location_index=0, county_index=1)

    def new_jersey(self):
        return self.format_one(start_index=1, stop_index=None, location_index=1, location_type_index=5, county_index=2)

    def new_mexico(self):
        return self.format_eight(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=3)

    def new_york(self):
        # Towns are missing for New York, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_New_York
        return self.format_nine(start_index=1, stop_index=None, location_index=0, county_index=1)

    def north_carolina(self):
        return self.format_one(start_index=1, stop_index=None, location_index=1, location_type_index=5, county_index=6)

    def north_dakota(self):
        # Towns are missing for North Dakota, they currently cannot be found on Wikipedia
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=5)

    def ohio(self):
        # Towns are missing for Ohio, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_villages_in_Ohio
        return self.format_six(start_index=1, stop_index=None, location_index=0, county_index=2)

    def oklahoma(self):
        # Towns are missing for oklahoma, they are on the same page. I need to figure out how to get them
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=6)

    def oregon(self):
        # Towns are missing for oklahoma, they currently cannot be found on Wikipedia
        return self.format_three(start_index=1, stop_index=None, location_index=1, county_index=6)

    def pennsylvania(self):
        # Towns are missing for Pennsylvania, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_and_boroughs_in_Pennsylvania
        res_list = self.format_seven(start_index=1, stop_index=None, location_index=1, county_index=2)
        for obj in res_list:
            location = obj['location']
            if location.endswith('town'):
                obj['location_type'] = 'town'
                location = location.replace('_town', '')
            elif location.endswith('borough'):
                obj['location_type'] = 'borough'
                location = location.replace('_borough', '')
            elif location.endswith('city'):
                obj['location_type'] = 'city'
                location = location.replace('_city', '')
            elif location.endswith('comb'):
                obj['location_type'] = 'comb'
                location = location.replace('_comb', '')
            else:
                obj['location_type'] = None
            obj['location'] = location
        return res_list

    def rhode_island(self):
        return self.format_one(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=2)

    def south_carolina(self):
        return self.format_eight(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=3)

    def south_dakota(self):
        # Towns are missing for South Dakota, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_South_Dakota
        return self.format_nine(start_index=1, location_index=1, county_index=5)

    def tennessee(self):
        return self.format_nine(start_index=1, location_index=0, county_index=1)

    def texas(self):
        # Towns are missing for Texas, they currently cannot be found on Wikipedia
        return self.format_ten(start_index=1, location_index=0, county_index=0)

    def utah(self):
        return self.format_one(start_index=1, location_index=0, location_type_index=2, county_index=1)

    def vermont(self):
        # Towns are missing for South Dakota, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Vermont
        return self.format_three(start_index=1, location_index=0, county_index=1)

    def virginia(self):
        # Cities are missing for Virginia, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_cities_and_counties_in_Virginia
        res_list = self.format_eleven(start_index=1, location_index=0, county_index=2)
        for obj in res_list:
            if obj['county'] == 'isle':
                obj['county'] = 'isle_of_wight'
        return res_list

    def washington(self):
        # Have to fix Washington, there are multiple tables on the page.
        return self.format_eight(start_index=2, stop_index=None, location_index=0, location_type_index=1, county_index=2)

    def west_virginia(self):
        # Towns are missing for West Virginia, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_West_Virginia
        return self.format_three(start_index=1, location_index=1, county_index=5)

    def wisconsin(self):
        # Towns are missing for West Virginia, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Wisconsin
        return self.format_nine(start_index=1, location_index=0, county_index=1)

    def wyoming(self):
        return self.format_one(start_index=2, stop_index=-1, location_index=0, location_type_index=1, county_index=2)

    def __str__(self):
        return ''


def find_correct_wiki_url(state, url_index):
    """

    :param state:
    :param url_index:
    :return:
    """
    urls = [
        f'https://en.wikipedia.org/wiki/List_of_municipalities_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_places_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_cities_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_municipalities_in_{state.title()}_(U.S._state)',
    ]
    if state == 'virginia':
        return requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_Virginia')
    if url_index >= len(urls):
        raise IndexError('Website was not found')
    else:
        return requests.get(urls[url_index])


def link_towns_cities_to_counties(state):
    """

    :param state:
    :return:
    """
    scrape_any_state = States(state)
    state_to_functions_dict = {
        'alabama': scrape_any_state.alabama,
        'alaska': scrape_any_state.alaska,
        'arizona': scrape_any_state.arizona,
        'arkansas': scrape_any_state.arkansas,
        'california': scrape_any_state.california,
        'colorado': scrape_any_state.colorado,
        'connecticut': scrape_any_state.connecticut,
        'delaware': scrape_any_state.delaware,
        'florida': scrape_any_state.florida,
        'georgia': scrape_any_state.georgia,
        'hawaii': scrape_any_state.hawaii,
        'idaho': scrape_any_state.idaho,
        'illinois': scrape_any_state.illinois,
        'indiana': scrape_any_state.indiana,
        'iowa': scrape_any_state.iowa,
        'kansas': scrape_any_state.kansas,
        'kentucky': scrape_any_state.kentucky,
        'louisiana': scrape_any_state.louisiana,
        'maine': scrape_any_state.maine,
        'maryland': scrape_any_state.maryland,
        'massachusetts': scrape_any_state.massachusetts,
        'michigan': scrape_any_state.michigan,
        'minnesota': scrape_any_state.minnesota,
        'mississippi': scrape_any_state.mississippi,
        'missouri': scrape_any_state.missouri,
        'montana': scrape_any_state.montana,
        'nebraska': scrape_any_state.nebraska,
        'nevada': scrape_any_state.nevada,
        'new_hampshire': scrape_any_state.new_hampshire,
        'new_jersey': scrape_any_state.new_jersey,
        'new_mexico': scrape_any_state.new_mexico,
        'new_york': scrape_any_state.new_york,
        'north_carolina': scrape_any_state.north_carolina,
        'north_dakota': scrape_any_state.north_dakota,
        'ohio': scrape_any_state.ohio,
        'oklahoma': scrape_any_state.oklahoma,
        'oregon': scrape_any_state.oregon,
        'pennsylvania': scrape_any_state.pennsylvania,
        'rhode_island': scrape_any_state.rhode_island,
        'south_carolina': scrape_any_state.south_carolina,
        'south_dakota': scrape_any_state.south_dakota,
        'tennessee': scrape_any_state.tennessee,
        'texas': scrape_any_state.texas,
        'utah': scrape_any_state.utah,
        'vermont': scrape_any_state.vermont,
        'virginia': scrape_any_state.virginia,
        'washington': scrape_any_state.washington,
        'west_virginia': scrape_any_state.west_virginia,
        'wisconsin': scrape_any_state.wisconsin,
        'wyoming': scrape_any_state.wyoming
    }
    des_function = state_to_functions_dict[state]
    print(f'\t...Complete')
    return {state: des_function()}


def main():
    pass


if __name__ == '__main__':
    main()
