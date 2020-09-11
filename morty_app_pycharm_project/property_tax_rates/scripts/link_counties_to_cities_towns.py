"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    09/11/2020

~ Purpose:
    Given a state, query a wikipedia page that gives us all the cities and towns in the state and links them to the
    county they reside in.

~ Issues/Needed Improvements:
    - If a city/town lies in multiple counties, only one is taken

~ Other Notes:
    N/A
"""
import requests
from bs4 import BeautifulSoup
from morty_py.useful_functions import clean_string_property_taxes


# TODO: Web scrape towns that were not included in select states but are found on different wiki pages
# TODO: It may be easier to select hyperlinks instead of table data
# TODO: Have input parameters to show certain things (Like print_url=True)
# TODO: Comment this code better, more specifically formats
# TODO: If something fails on one format, switch to the next automatically, check with unittests?
# TODO: Decrease the amount of formats
# TODO: Format six and seven are exactly the same I think
# TODO: If location index is none, return a different dictionary
# TODO: Provide examples in docstrings
# TODO: Provide examples for Formats methods


class Formats:

    def __init__(self, table_rows_list=None, location_index=None, location_type_index=None, county_index=None,
                 start_index=None, stop_index=None):
        """
        There was very little consistency when web scraping wikipedia pages for cities and towns linked to their
        counties. Here we have multiple formats to handle most formats the HTML was written in
        :param table_rows_list: The table rows from the table with the desired data
        :param location_index: Where the location is located in the table row
        :param location_type_index: Where the location type is located in the table row
        :param county_index: Where the county is located in the table row
        :param start_index: What row to start at in the table
        :param stop_index: What row to end at in the table
        """
        self.location_index = location_index
        self.location_type_index = location_type_index
        self.county_index = county_index
        self.start_index = start_index
        self.stop_index = stop_index
        self.response_list = list()
        self.table_rows_list = table_rows_list

    def define_start_end(self):
        """
        To define which table row to start and end at in the table
        """
        if self.stop_index is not None:
            self.table_rows_list = self.table_rows_list[self.start_index: self.stop_index]
        else:
            self.table_rows_list = self.table_rows_list[self.start_index:]

    """
    The following functions do essentially the same thing in a slightly different way. As noted before, each Wikipedia
    page has different formats for this data. Here the functions deal with each of the formats and return a list of
    dictionaries with the location, location type, and the county the location resides in.
    """
    def format_one(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[self.location_index].text)
            county = clean_string_property_taxes(table_data[self.county_index].text)
            if self.location_type_index:
                location_type = clean_string_property_taxes(table_data[self.location_type_index].text)
                self.response_list.append({'location': location, 'location_type': location_type, 'county': county})
            else:
                self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_two(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(item.select('th')[self.location_index].text)
            location_type = clean_string_property_taxes(table_data[self.location_type_index].text)
            county = clean_string_property_taxes(table_data[self.county_index].text)
            self.response_list.append({'location': location, 'location_type': location_type, 'county': county})
        return self.response_list

    def format_three(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(item.select('th')[self.location_index].text)
            county = clean_string_property_taxes(table_data[0].select('a')[self.county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_four(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[self.location_index].text)
            county = clean_string_property_taxes(table_data[5].select('a')[self.county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_five(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            if len(table_data) == 1:
                continue
            location = clean_string_property_taxes(table_data[self.location_index].text)
            county = clean_string_property_taxes(table_data[self.county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_six(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            location = clean_string_property_taxes(table_data[self.location_index].text)
            county = clean_string_property_taxes(table_data[self.county_index].select('a')[0].text)
            if self.location_type_index:
                location_type = clean_string_property_taxes(table_data[self.location_type_index].text)
                self.response_list.append({'location': location, 'location_type': location_type, 'county': county})
            else:
                self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_seven(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            if not len(item.select('th')):
                continue
            location = clean_string_property_taxes(item.select('th')[self.location_index].text)
            county = clean_string_property_taxes(table_data[0].select('a')[self.county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list

    def format_eight(self):
        """
        Examples of the pages under this format:
        """
        self.define_start_end()
        for item in self.table_rows_list:
            table_data = item.select('td')
            if len(table_data) < 4:
                continue
            location = clean_string_property_taxes(table_data[self.location_index].text)
            county = clean_string_property_taxes(table_data[self.county_index].text)
            self.response_list.append({'location': location, 'location_type': None, 'county': county})
        return self.response_list


class States(Formats):

    def __init__(self, state):
        """
        Given a state, finds the correct Wikipedia URL to web scrape. Then, grabs the proper table with the desired
        data. Each state scraped has its own method with parameters described in the 'declare_format_params' function.
        These return a list of dictionaries.
        :param state: One of the fifty US states
        """
        print(f'\t*** NOW BEGINNING TO LINK STATES AND CITIES TO A COUNTY FOR {state} ***')
        url_index = 0
        des_table = None
        response = find_correct_wiki_url(state=state, url_index=url_index)
        # Loops through a list of possible URLs and finds the correct one to query
        while True:
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                des_table = soup.select('.wikitable.sortable')[0]
                break
            except IndexError:
                url_index += 1
                response = find_correct_wiki_url(state=state, url_index=url_index)
                continue
        self.state = state
        self.table_rows_list = des_table.select('tr')
        # There are a variety of different formats of the HTML scrapped on these Wikipedia pages. There was very little
        # consistency so there are multiple different functions to handle most of the formats encountered
        Formats.__init__(self, table_rows_list=self.table_rows_list)

    def declare_format_params(self, start_index=None, stop_index=None, location_index=None, location_type_index=None,
                              county_index=None):
        """
        Defines necessary parameters for the Format class
        :param start_index: Which table row to start at
        :param stop_index: Which table row to end at
        :param location_index: The index where the location is found
        :param location_type_index: The index where the location type is found
        :param county_index: The index where the county the location resides in is found
        """
        self.location_index = location_index
        self.location_type_index = location_type_index
        self.county_index = county_index
        self.start_index = start_index
        self.stop_index = stop_index

    def alabama(self):
        self.declare_format_params(start_index=2, stop_index=-3, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def alaska(self):
        return self.response_list

    def arizona(self):
        self.declare_format_params(start_index=2, stop_index=-2, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def arkansas(self):
        self.declare_format_params(start_index=1, location_index=1, location_type_index=2, county_index=3)
        return self.format_one()

    def california(self):
        self.declare_format_params(start_index=2, location_index=0, location_type_index=0, county_index=1)
        return self.format_two()

    def colorado(self):
        self.declare_format_params(start_index=1, location_index=0, location_type_index=1, county_index=4)
        return self.format_one()

    def connecticut(self):
        self.declare_format_params(start_index=1, stop_index=-1, location_index=1, location_type_index=2,
                                   county_index=7)
        return self.format_one()

    def delaware(self):
        self.declare_format_params(start_index=1, location_index=1, location_type_index=2, county_index=5)
        return self.format_one()

    def florida(self):
        self.declare_format_params(start_index=1, location_index=0, location_type_index=5, county_index=1)
        return self.format_six()

    def georgia(self):
        self.declare_format_params(start_index=1, location_index=1, location_type_index=5, county_index=6)
        return self.format_one()

    def hawaii(self):
        self.declare_format_params(start_index=1, location_index=1, county_index=3)
        return self.format_one()

    def idaho(self):
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def illinois(self):
        self.declare_format_params(start_index=1, location_index=0, location_type_index=1, county_index=3)
        return self.format_one()

    def indiana(self):
        # Towns are missing for indiana, they're in a separate wiki page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Indiana
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def iowa(self):
        self.declare_format_params(start_index=2, location_index=0, county_index=0)
        return self.format_three()

    def kansas(self):
        # Towns are missing for kansas, they're in a separate wiki page:
        # https://en.wikipedia.org/wiki/List_of_townships_in_Kansas
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def kentucky(self):
        self.declare_format_params(start_index=1, location_index=0, county_index=6)
        return self.format_six()

    def louisiana(self):
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def maine(self):
        # Towns are missing for maine, they're in a separate wiki page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Maine
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def maryland(self):
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def massachusetts(self):
        self.declare_format_params(start_index=1, location_index=0, location_type_index=1, county_index=2)
        return self.format_one()

    def michigan(self):
        self.declare_format_params(start_index=2, location_index=0, location_type_index=1, county_index=2)
        return self.format_six()

    def minnesota(self):
        # Towns are missing for minnesota, they currently cannot be found on Wikipedia
        self.declare_format_params(start_index=1, location_index=1, county_index=0)
        return self.format_four()

    def mississippi(self):
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def missouri(self):
        self.declare_format_params(start_index=1, location_index=0, location_type_index=1, county_index=3)
        return self.format_one()

    def montana(self):
        self.declare_format_params(start_index=2, stop_index=-3, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def nebraska(self):
        # Towns are missing for Nebraska, they currently cannot be found on Wikipedia
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def nevada(self):
        # Towns are missing for Nevada, they currently cannot be found on Wikipedia
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def new_hampshire(self):
        self.declare_format_params(start_index=1, location_index=0, county_index=1)
        return self.format_one()

    def new_jersey(self):
        self.declare_format_params(start_index=1, location_index=1, location_type_index=5, county_index=2)
        return self.format_one()

    def new_mexico(self):
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=3)
        return self.format_six()

    def new_york(self):
        # Towns are missing for New York, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_New_York
        self.declare_format_params(start_index=1, location_index=0, county_index=1)
        return self.format_six()

    def north_carolina(self):
        self.declare_format_params(start_index=1, location_index=1, location_type_index=5, county_index=6)
        return self.format_one()

    def north_dakota(self):
        # Towns are missing for North Dakota, they currently cannot be found on Wikipedia
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def ohio(self):
        # Towns are missing for Ohio, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_villages_in_Ohio
        self.declare_format_params(start_index=1, location_index=0, county_index=2)
        return self.format_five()

    def oklahoma(self):
        # Towns are missing for oklahoma, they are on the same page. I need to figure out how to get them
        self.declare_format_params(start_index=1, location_index=1, county_index=6)
        return self.format_one()

    def oregon(self):
        # Towns are missing for oklahoma, they currently cannot be found on Wikipedia
        self.declare_format_params(start_index=1, location_index=1, county_index=6)
        return self.format_one()

    def pennsylvania(self):
        # Towns are missing for Pennsylvania, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_and_boroughs_in_Pennsylvania
        self.declare_format_params(start_index=1, location_index=1, county_index=2)
        res_list = self.format_five()
        # Edge case in Pennsylvania formatting
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
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()

    def south_carolina(self):
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=3)
        return self.format_six()

    def south_dakota(self):
        # Towns are missing for South Dakota, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_South_Dakota
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_six()

    def tennessee(self):
        self.declare_format_params(start_index=1, location_index=0, county_index=1)
        return self.format_six()

    def texas(self):
        # Towns are missing for Texas, they currently cannot be found on Wikipedia
        self.declare_format_params(start_index=1, location_index=0, county_index=0)
        return self.format_seven()

    def utah(self):
        self.declare_format_params(start_index=1, location_index=0, location_type_index=2, county_index=1)
        return self.format_one()

    def vermont(self):
        # Towns are missing for South Dakota, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Vermont
        self.declare_format_params(start_index=1, location_index=0, county_index=1)
        return self.format_one()

    def virginia(self):
        # Cities are missing for Virginia, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_cities_and_counties_in_Virginia
        self.declare_format_params(start_index=1, location_index=0, county_index=2)
        res_list = self.format_eight()
        for obj in res_list:
            if obj['county'] == 'isle':
                obj['county'] = 'isle_of_wight'
        return res_list

    def washington(self):
        # Have to fix Washington, there are multiple tables on the page.
        self.declare_format_params(start_index=2, location_index=0, location_type_index=1, county_index=2)
        return self.format_six()

    def west_virginia(self):
        # Towns are missing for West Virginia, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_West_Virginia
        self.declare_format_params(start_index=1, location_index=1, county_index=5)
        return self.format_one()

    def wisconsin(self):
        # Towns are missing for West Virginia, they are located on another page:
        # https://en.wikipedia.org/wiki/List_of_towns_in_Wisconsin
        self.declare_format_params(start_index=1, location_index=0, county_index=1)
        return self.format_six()

    def wyoming(self):
        self.declare_format_params(start_index=2, stop_index=-1, location_index=0, location_type_index=1,
                                   county_index=2)
        return self.format_one()


def find_correct_wiki_url(state, url_index):
    """
    There are a variety of URLs on wikipedia where this desired data is found. Try's to find the correct url for the
    given state
    :param state: One of the 50 US states
    :param url_index: Indexes the urls list to choose the desired url
    :return: The response from the correct website
    """
    urls = [
        f'https://en.wikipedia.org/wiki/List_of_municipalities_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_places_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_cities_in_{state.title()}',
        f'https://en.wikipedia.org/wiki/List_of_municipalities_in_{state.title()}_(U.S._state)',
    ]
    # Virginia is separate here because there was a valid URL found before this one but was not the correct one.
    # This only happened with virginia so an edge case was created
    if state == 'virginia':
        return requests.get('https://en.wikipedia.org/wiki/List_of_towns_in_Virginia')
    if url_index >= len(urls):
        raise IndexError('Website was not found')
    else:
        return requests.get(urls[url_index])


def link_towns_cities_to_counties(state):
    """
    Given a state finds all of the cities and towns in it linking the cities and towns to the county they're in
    :param state: One of the 50 US states
    :return: A dictionary with the state as the key and a list of dictionaries as the value. The list of dictionaries
    has the keys as all of the cities and towns within the state and the county they belong in
    """
    scrape_any_state = States(state)
    # Each state has it's own method, the data was scraped from Wikipedia which had next to zero consistency in terms
    # of HTML layout
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
    # Gets the method
    des_function = state_to_functions_dict[state]
    print(f'\t...Complete')
    return {state: des_function()}


def main():
    pass


if __name__ == '__main__':
    main()
