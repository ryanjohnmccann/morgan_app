"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    08/28/2020

~ Purpose:
    N/A

~ Issues/Needed Improvements:
    N/A

~ Other Notes:
    - Skipped over alaska for the time being
"""
import unittest
import json
from property_tax_rates.scripts.link_counties_to_cities_towns import link_towns_cities_to_counties


def test_find_undesired_characters(state):
    invalid_string_list = [
        "'",
        "[",
        "]",
        " County",
        " county",
        "Town",
        "4",
        "5",
        "8",
        "9",
        "†",
        'I',
        'II',
        "Town of",
        "City of",
        ",",
        '/',
        '-'
    ]
    response_dict = link_towns_cities_to_counties(state)
    for state, cities_towns_list in response_dict.items():
        for obj in cities_towns_list:
            for key, val in obj.items():
                if val is None:
                    continue
                if len(val) <= 1:
                    print(val)
                    return False
                for string in invalid_string_list:
                    if string in val:
                        print(string)
                        return False
    return True


def test_find_first_last_location(state, first_location, last_location):
    response_dict = link_towns_cities_to_counties(state)
    for state, locations in response_dict.items():
        if locations[0]['location'] != first_location:
            return False
        elif locations[-1]['location'] != last_location:
            return False
        else:
            return True


class TestEveryState(unittest.TestCase):

    def test_alabama(self):
        flag_one = test_find_first_last_location(state='alabama', first_location='abbeville', last_location='york')
        flag_two = test_find_undesired_characters(state='alabama')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    @unittest.skip('=== Skipping unit test for Alaska ===')
    def alaska(self):
        pass

    def test_arizona(self):
        flag_one = test_find_first_last_location(state='alabama', first_location='abbeville', last_location='york')
        flag_two = test_find_undesired_characters(state='alabama')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_arkansas(self):
        flag_one = test_find_first_last_location(state='arkansas', first_location='little_rock',
                                                 last_location='gilbert')
        flag_two = test_find_undesired_characters(state='arkansas')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_california(self):
        flag_one = test_find_first_last_location(state='california', first_location='adelanto',
                                                 last_location='yucca_valley')
        flag_two = test_find_undesired_characters(state='california')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_colorado(self):
        flag_one = test_find_first_last_location(state='colorado', first_location='aguilar', last_location='yuma')
        flag_two = test_find_undesired_characters(state='colorado')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_connecticut(self):
        flag_one = test_find_first_last_location(state='connecticut', first_location='andover',
                                                 last_location='woodstock')
        flag_two = test_find_undesired_characters(state='connecticut')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_delaware(self):
        flag_one = test_find_first_last_location(state='delaware', first_location='wilmington',
                                                 last_location='hartly')
        flag_two = test_find_undesired_characters(state='delaware')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_florida(self):
        flag_one = test_find_first_last_location(state='florida', first_location='alachua',
                                                 last_location='zolfo_springs')
        flag_two = test_find_undesired_characters(state='florida')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_hawaii(self):
        flag_one = test_find_first_last_location(state='hawaii', first_location='honolulu',
                                                 last_location='manele')
        flag_two = test_find_undesired_characters(state='hawaii')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_idaho(self):
        flag_one = test_find_first_last_location(state='idaho', first_location='boise',
                                                 last_location='warm_river')
        flag_two = test_find_undesired_characters(state='idaho')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_indiana(self):
        flag_one = test_find_first_last_location(state='indiana', first_location='indianapolis',
                                                 last_location='cannelton')
        flag_two = test_find_undesired_characters(state='indiana')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_iowa(self):
        flag_one = test_find_first_last_location(state='iowa', first_location='ackley',
                                                 last_location='zwingle')
        flag_two = test_find_undesired_characters(state='iowa')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_kansas(self):
        flag_one = test_find_first_last_location(state='kansas', first_location='wichita',
                                                 last_location='concordia')
        flag_two = test_find_undesired_characters(state='kansas')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_kentucky(self):
        flag_one = test_find_first_last_location(state='kentucky', first_location='adairville',
                                                 last_location='wurtland')
        flag_two = test_find_undesired_characters(state='kentucky')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_louisiana(self):
        flag_one = test_find_first_last_location(state='louisiana', first_location='abbeville',
                                                 last_location='zwolle')
        flag_two = test_find_undesired_characters(state='louisiana')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_maine(self):
        flag_one = test_find_first_last_location(state='maine', first_location='portland',
                                                 last_location='eastport')
        flag_two = test_find_undesired_characters(state='maine')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_maryland(self):
        flag_one = test_find_first_last_location(state='maryland', first_location='aberdeen',
                                                 last_location='woodsboro')
        flag_two = test_find_undesired_characters(state='maryland')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_massachusetts(self):
        flag_one = test_find_first_last_location(state='massachusetts', first_location='abington',
                                                 last_location='yarmouth')
        flag_two = test_find_undesired_characters(state='massachusetts')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_michigan(self):
        flag_one = test_find_first_last_location(state='michigan', first_location='acme',
                                                 last_location='zilwaukee')
        flag_two = test_find_undesired_characters(state='michigan')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_minnesota(self):
        flag_one = test_find_first_last_location(state='minnesota', first_location='minneapolis',
                                                 last_location='rothsay')
        flag_two = test_find_undesired_characters(state='minnesota')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_mississippi(self):
        flag_one = test_find_first_last_location(state='mississippi', first_location='abbeville',
                                                 last_location='yazoo_city')
        flag_two = test_find_undesired_characters(state='mississippi')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_missouri(self):
        flag_one = test_find_first_last_location(state='missouri', first_location='adrian',
                                                 last_location='zalma')
        flag_two = test_find_undesired_characters(state='missouri')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_montana(self):
        flag_one = test_find_first_last_location(state='montana', first_location='alberton',
                                                 last_location='wolf_point')
        flag_two = test_find_undesired_characters(state='montana')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_nebraska(self):
        flag_one = test_find_first_last_location(state='nebraska', first_location='omaha',
                                                 last_location='valley')
        flag_two = test_find_undesired_characters(state='nebraska')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_nevada(self):
        flag_one = test_find_first_last_location(state='nevada', first_location='boulder_city',
                                                 last_location='yerington')
        flag_two = test_find_undesired_characters(state='nevada')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_new_hampshire(self):
        flag_one = test_find_first_last_location(state='new_hampshire', first_location='acworth',
                                                 last_location='woodstock')
        flag_two = test_find_undesired_characters(state='new_hampshire')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_new_jersey(self):
        flag_one = test_find_first_last_location(state='new_jersey', first_location='newark',
                                                 last_location='tavistock')
        flag_two = test_find_undesired_characters(state='new_jersey')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_new_mexico(self):
        flag_one = test_find_first_last_location(state='new_mexico', first_location='alamogordo',
                                                 last_location='williamsburg')
        flag_two = test_find_undesired_characters(state='new_mexico')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_new_york(self):
        flag_one = test_find_first_last_location(state='new_york', first_location='albany',
                                                 last_location='yonkers')
        flag_two = test_find_undesired_characters(state='new_york')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_north_carolina(self):
        flag_one = test_find_first_last_location(state='north_carolina', first_location='charlotte',
                                                 last_location='boone')
        flag_two = test_find_undesired_characters(state='north_carolina')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_north_dakota(self):
        flag_one = test_find_first_last_location(state='north_dakota', first_location='fargo',
                                                 last_location='ruso')
        flag_two = test_find_undesired_characters(state='north_dakota')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_ohio(self):
        flag_one = test_find_first_last_location(state='ohio', first_location='akron',
                                                 last_location='zanesville')
        flag_two = test_find_undesired_characters(state='ohio')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_oklahoma(self):
        flag_one = test_find_first_last_location(state='oklahoma', first_location='oklahoma_city',
                                                 last_location='poteau')
        flag_two = test_find_undesired_characters(state='oklahoma')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_oregon(self):
        flag_one = test_find_first_last_location(state='oregon', first_location='portland',
                                                 last_location='greenhorn')
        flag_two = test_find_undesired_characters(state='oregon')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_pennsylvania(self):
        flag_one = test_find_first_last_location(state='pennsylvania', first_location='philadelphia',
                                                 last_location='centralia')
        flag_two = test_find_undesired_characters(state='pennsylvania')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_rhode_island(self):
        flag_one = test_find_first_last_location(state='rhode_island', first_location='barrington',
                                                 last_location='woonsocket')
        flag_two = test_find_undesired_characters(state='rhode_island')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_south_carolina(self):
        flag_one = test_find_first_last_location(state='south_carolina', first_location='abbeville',
                                                 last_location='york')
        flag_two = test_find_undesired_characters(state='south_carolina')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_south_dakota(self):
        flag_one = test_find_first_last_location(state='south_dakota', first_location='sioux_falls',
                                                 last_location='buffalo_chip')
        flag_two = test_find_undesired_characters(state='south_dakota')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_tennessee(self):
        flag_one = test_find_first_last_location(state='tennessee', first_location='adams',
                                                 last_location='yorkville')
        flag_two = test_find_undesired_characters(state='tennessee')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_texas(self):
        flag_one = test_find_first_last_location(state='texas', first_location='abbott',
                                                 last_location='zavalla')
        flag_two = test_find_undesired_characters(state='texas')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_utah(self):
        flag_one = test_find_first_last_location(state='utah', first_location='alpine',
                                                 last_location='woods_cross')
        flag_two = test_find_undesired_characters(state='utah')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_vermont(self):
        flag_one = test_find_first_last_location(state='vermont', first_location='burlington',
                                                 last_location='vergennes')
        flag_two = test_find_undesired_characters(state='vermont')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_washington(self):
        flag_one = test_find_first_last_location(state='washington', first_location='aberdeen',
                                                 last_location='zillah')
        flag_two = test_find_undesired_characters(state='washington')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_west_virginia(self):
        flag_one = test_find_first_last_location(state='west_virginia', first_location='charleston',
                                                 last_location='clearview')
        flag_two = test_find_undesired_characters(state='west_virginia')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_wisconsin(self):
        flag_one = test_find_first_last_location(state='wisconsin', first_location='abbotsford',
                                                 last_location='wisconsin_rapids')
        flag_two = test_find_undesired_characters(state='wisconsin')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")

    def test_wyoming(self):
        flag_one = test_find_first_last_location(state='wyoming', first_location='afton',
                                                 last_location='yoder')
        flag_two = test_find_undesired_characters(state='wyoming')
        self.assertTrue(flag_one, "Invalid first and last locations")
        self.assertTrue(flag_two, "Invalid characters exist within strings")


if __name__ == '__main__':
    unittest.main()

