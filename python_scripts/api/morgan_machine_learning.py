# Last updated by:
# Ryan McCann

# Last updated:
# 05/09/20

# Purpose:
# Calculates all expenses for the user's mortgage. Here is a machine learning representation

# Issues/Needed Improvements:
# None known at this point in time

import json
import random
import pandas as pd
import numpy as np
import os
from datetime import datetime


# TODO: Calculate percentage of net worth with respect to their take home income
# TODO: Make all expenses a percentage of their wealth to compare
# TODO: Has to break if they cannot afford the monthly payments
# TODO: Need to check on monthly payment percentage
# TODO: Incorporate years saved (eventually compare with rent costs)
# TODO: Calculate mean, median, mode and std for each individual trial
# TODO: Account for raises
# TODO: Account for house value due to the economy
# TODO: Add 'renter' option. Person takes out another mortgage and rents their property
# TODO: Make monthly payment and payment due in my __init__
# TODO: Add furniture and moving expenses
# TODO: Need to account for taxes in take home income
# TODO: Need to be more specific with fees for an apartment or condo
# TODO: More trials and more effectiveness overall

def main():
    class run_program:
        def __init__(self, purchase_price, down_payment, loan_duration, interest_rate, yearly_payments, location,
                     home_type, take_home_income):
            self.purchase_price = purchase_price
            self.down_payment = down_payment
            self.loan_duration = loan_duration
            # Convert interest rate to a decimal
            self.interest_rate = interest_rate / 100
            self.yearly_payments = yearly_payments
            self.location = location
            self.home_type = home_type
            self.take_home_income = take_home_income

        # Take taxes out of users income
        def calculate_income_taxes(self):
            pass

        # Private mortgage insurance
        def calculate_pmi(self):
            if self.down_payment < (self.purchase_price * 0.2):
                yearly_pmi = 0.01 * self.purchase_price
                total_pmi = yearly_pmi * self.loan_duration
                monthly_pmi = yearly_pmi / 12
            # No private mortgage insurance with down payments greater than or equal to twenty percent
            else:
                monthly_pmi = yearly_pmi = total_pmi = 0
            return [monthly_pmi, yearly_pmi, total_pmi]

        def calculate_interest(self):
            # Strictly used to calculate costs of interest
            remaining_principle = self.purchase_price - self.down_payment
            # Dividing annual interest by number of yearly payments to calculate monthly payment due
            monthly_interest = self.interest_rate / self.yearly_payments
            payment_due = remaining_principle / (((1 + monthly_interest) ** (self.yearly_payments * self.loan_duration)
                                                  - 1) / (monthly_interest * (1 + monthly_interest) **
                                                          (self.yearly_payments * self.loan_duration)))
            total_interest = 0
            while True:
                temp_interest = ((self.interest_rate / self.yearly_payments) * remaining_principle)
                total_interest += temp_interest
                payment = (payment_due - temp_interest)
                remaining_principle -= payment
                if remaining_principle <= self.purchase_price / self.loan_duration / self.yearly_payments:
                    yearly_interest = total_interest / self.loan_duration
                    monthly_interest = yearly_interest / 12
                    return [monthly_interest, yearly_interest, total_interest]

        def calculate_property_tax(self):
            fp = '/Users/ryanmccann/Desktop/misc/programming/finance_project/'
            for state, city in self.location.items():
                state = state.lower()
                city = city.lower()
                if ' ' in state:
                    state = state.replace(' ', '_')
                if ' ' in city:
                    city = city.replace(' ', '_')
                # For a zip code entry
                # All zip codes in New England begin with a zero
                if city[0] == '0':
                    zip_code = city
                    temp_data = json.load(open(fp + 'zip_codes/' + state + '.json'))
                    for obj in temp_data:
                        if obj['zip_code'] == zip_code:
                            city = obj['city/town']
                # For town or city entry directly
                des_data = json.load(open(fp + 'property_tax_rates/' + state + '.json'))
                for obj in des_data:
                    if city == obj['city/town']:
                        prop_tax_rate = obj['rate']
                monthly_prop_tax = ((self.purchase_price / 1000) * prop_tax_rate) / 12
                yearly_prop_tax = monthly_prop_tax * 12
                total_prop_tax = monthly_prop_tax * 12 * self.loan_duration
                return [monthly_prop_tax, yearly_prop_tax, total_prop_tax]

        def calculate_maintenance(self):
            if self.home_type == 'house' or self.home_type == 'House':
                # Putting upkeep a half a percent yearly to be safe
                yearly_upkeep = self.purchase_price * 0.005
            # Assuming apartment or condo. Average condo fees.
            else:
                yearly_upkeep = 330 * 12
            """
            After loan is paid off, it's safe to say upkeep will not be a problem. 
            Focusing on costs during the loan duration for now.
            """
            total_upkeep = yearly_upkeep * self.loan_duration
            monthly_upkeep = yearly_upkeep / 12
            return [monthly_upkeep, yearly_upkeep, total_upkeep]

        def calculate_smart_savings(self, yearly_costs):
            savings_duration = 30 - self.loan_duration
            monthly_interest = self.interest_rate / self.yearly_payments
            remaining_principle = self.purchase_price - self.down_payment
            monthly_payment = remaining_principle / (
                    ((1 + monthly_interest) ** (self.yearly_payments * self.loan_duration)
                     - 1) / (monthly_interest * (1 + monthly_interest) **
                             (self.yearly_payments * self.loan_duration)))
            return savings_duration * (monthly_payment * 12)

        # Function is a little pointless right now, will eventually calculate factors
        # like the economy.
        def calculate_wealth(self, house_worth, smart_savings):
            assets = house_worth + smart_savings
            weighted_percentage = (assets / self.take_home_income) * 100
            return weighted_percentage

        def calculate_total_costs(self):
            # Non recurring expenses
            closing_costs = self.purchase_price * 0.04
            pmi_list = self.calculate_pmi()
            interest_list = self.calculate_interest()
            prop_tax_list = self.calculate_property_tax()
            maintenance_list = self.calculate_maintenance()
            # To calculate average principle payment
            # Monthly payment of interest and principle amount
            monthly_interest = self.interest_rate / self.yearly_payments
            remaining_principle = self.purchase_price - self.down_payment
            monthly_payment = remaining_principle / (((1 + monthly_interest) **
                                                      (self.yearly_payments * self.loan_duration) - 1) /
                                                     (monthly_interest * (1 + monthly_interest) **
                                                      (self.yearly_payments * self.loan_duration)))
            # The average principle is the difference from the average interest
            monthly_principle = interest_list[0] - monthly_payment
            # Must mean interest is smaller than monthly payment, cannot be non negative
            if monthly_principle <= 0:
                monthly_principle = monthly_payment - interest_list[0]
            yearly_principle = monthly_principle * 12
            total_principle = yearly_principle * self.loan_duration
            principle_payment_list = [monthly_principle, yearly_principle, self.purchase_price - self.down_payment]
            monthly_costs = pmi_list[0] + interest_list[0] + prop_tax_list[0] + \
                            maintenance_list[0] + principle_payment_list[0]
            yearly_costs = pmi_list[1] + interest_list[1] + prop_tax_list[1] + maintenance_list[1] + \
                           principle_payment_list[1]
            total_costs = pmi_list[2] + interest_list[2] + prop_tax_list[2] + maintenance_list[2] + \
                          principle_payment_list[2]
            if self.loan_duration < 30:
                smart_savings = self.calculate_smart_savings(yearly_costs)
            else:
                smart_savings = 0
            wealth = self.calculate_wealth(self.purchase_price, smart_savings)
            if yearly_costs >= (self.take_home_income * 0.4) or self.down_payment > ((self.take_home_income * 0.6) * 7):
                return {'wealth_percent': 0}
            print('Purchase Price: ', self.purchase_price)
            print('Take Home Income: ', self.take_home_income)
            print('Down Payment: ', self.down_payment)
            print('Loan Duration: ', self.loan_duration)
            print('Interest Rate: ', self.interest_rate)
            print('Yearly Payments: ', self.yearly_payments)
            print('Location: ', self.location)
            print('Wealth Percentage: ', wealth.__round__(2))
            print('Total Costs: ', total_costs.__round__(2))
            print('\n')
            winner_dict = {'purchase_price': self.purchase_price, 'take_home_income': self.take_home_income,
                           'down_payment': self.down_payment, 'loan_duration': self.loan_duration, 'interest_rate':
                           self.interest_rate, 'yearly_payments': self.yearly_payments, 'location': self.location,
                           'wealth_percent': wealth}
            return winner_dict

    def run_universe():
        simulation_count = 0
        take_home_income = 70000
        # take_home_income = random.randrange(15000, 300000)
        while simulation_count < 50000:
            purchase_price = random.randrange(10000, 300000)
            down_payment = random.randrange(1, purchase_price)
            loan_duration = random.randrange(10, 30)
            interest_rate = random.randrange(3, 5)
            yearly_payments_list = [12, 26, 52]
            yearly_payments_index = random.randrange(0, 2)
            yearly_payments = yearly_payments_list[yearly_payments_index]
            all_states_cities = json.load(open("/Users/ryanmccann/Desktop/misc/programming/"
                                               "finance_project/all_states_and_cities.json"))
            state_restraint = len(all_states_cities) - 1
            state_index = random.randrange(0, state_restraint)
            for key, val in all_states_cities[state_index].items():
                city_restraint = len(val) - 1
                city_index = random.randrange(0, city_restraint)
                state = key
                city = val[city_index]
                break
            trial = run_program(purchase_price, down_payment, loan_duration, interest_rate, yearly_payments,
                                {state: city}, 'House', take_home_income)
            des_data = trial.calculate_total_costs()
            # If all values are zero, the function has 'failed'
            if des_data['wealth_percent'] == 0:
                continue
            if simulation_count == 0:
                best_dict = des_data
                best_wealth_percent = best_dict['wealth_percent']
                best_simulation = 0
            else:
                if des_data['wealth_percent'] > best_wealth_percent:
                    best_dict = des_data
                    best_wealth_percent = best_dict['wealth_percent']
                    best_simulation = simulation_count
            print('Simulation ' + str(simulation_count) + ' complete.')
            print('\n')
            simulation_count += 1
        print('Best simulation is number', best_simulation, '\n')
        print('Wealth Percentage:', best_dict['wealth_percent'])
        print('Take Home Income Simulation Amount:', take_home_income, '\n')
        for key, val in best_dict.items():
            print(key + ' --> ' + str(val))
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        with open('/Users/ryanmccann/Desktop/misc/programming/finance_project/winner_data/' + dt_string + '.json', 'w') as \
                file_path:
            json.dump(best_dict, file_path)
        del best_dict, trial
    run_universe_count = 0
    while run_universe_count < 20:
        run_universe()
        run_universe_count += 1


if __name__ == '__main__':
    main()
