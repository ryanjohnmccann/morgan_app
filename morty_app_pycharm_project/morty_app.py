"""
~ Last updated by:
    Ryan McCann

~ Last updated:
    09/11/2020

~ Purpose:
    Runs the simulation for calculating fees for a mortgage. This is the original

~ Issues/Needed Improvements:
    This does not work at the moment, need to update paths and things like that.

~ Other Notes:
    This code is used to check code written in javascript on the morty app ui
"""
import json


class run_simulation:
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

    def calculate_pmi(self):
        """
        Private mortgage insurance
        :return: Monthly, yearly, and total private mortgage insurance paid
        """
        if self.down_payment < (self.purchase_price * 0.2):
            yearly_pmi = 0.01 * self.purchase_price
            total_pmi = yearly_pmi * self.loan_duration
            monthly_pmi = yearly_pmi / 12
        # No private mortgage insurance with down payments greater than or equal to twenty percent
        else:
            monthly_pmi = yearly_pmi = total_pmi = 0
        return [monthly_pmi, yearly_pmi, total_pmi]

    def calculate_interest(self):
        """
        Interest
        :return: Monthly, yearly, and total interest
        """
        # remaining_principle strictly used to calculate costs of interest
        remaining_principle = self.purchase_price - self.down_payment
        # Dividing annual interest by number of yearly payments to calculate monthly payment due
        monthly_interest = self.interest_rate / self.yearly_payments
        # This equation was found online. A basic Interest rate formula for a mortgage.
        payment_due = remaining_principle / (((1 + monthly_interest) ** (self.yearly_payments * self.loan_duration)
                                              - 1) / (monthly_interest * (1 + monthly_interest) **
                                                      (self.yearly_payments * self.loan_duration)))
        total_interest = 0
        while True:
            temp_interest = ((self.interest_rate / self.yearly_payments) * remaining_principle)
            total_interest += temp_interest
            payment = (payment_due - temp_interest)
            remaining_principle -= payment
            # If the remaining principle is equal or less than the monthly payment, we know this is the
            # last iteration
            if remaining_principle <= self.purchase_price / self.loan_duration / self.yearly_payments:
                yearly_interest = total_interest / self.loan_duration
                monthly_interest = yearly_interest / 12
                return [monthly_interest, yearly_interest, total_interest]

    def calculate_property_tax(self):
        """
        Finds the property taxes for location entered
        :return: Monthly, yearly, and total property taxes paid
        """
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
                # TODO: This needs to be updated
                temp_data = json.load(open('zip_codes/' + state + '.json'))
                for obj in temp_data:
                    if obj['zip_code'] == zip_code:
                        city = obj['city/town']
            # For town or city entry directly
            des_data = json.load(open('./property_tax_rates/data/structured_data/' + state + '.json'))
            for s, locations in des_data.items():
                for obj in locations:
                    if city == obj['location']:
                        prop_tax_rate = obj['rate']
            monthly_prop_tax = ((self.purchase_price / 1000) * prop_tax_rate) / 12
            yearly_prop_tax = monthly_prop_tax * 12
            total_prop_tax = monthly_prop_tax * 12 * self.loan_duration
            return [monthly_prop_tax, yearly_prop_tax, total_prop_tax]

    def calculate_maintenance(self):
        """
        Maintenance only calculated for a house right now. Randomly making it one half of a percent of the house value
        :return: Monthly, yearly, and total Maintenance
        """
        if self.home_type == 'house' or self.home_type == 'House':
            # Putting upkeep a half a percent yearly to be safe
            yearly_upkeep = self.purchase_price * 0.005
        # Assuming apartment or condo. Average condo or hoa fees.
        else:
            yearly_upkeep = 330 * 12
        """
        After loan is paid off, it's safe to say upkeep will not be a problem.
        Focusing on costs during the loan duration for now.
        """
        total_upkeep = yearly_upkeep * self.loan_duration
        monthly_upkeep = yearly_upkeep / 12
        return [monthly_upkeep, yearly_upkeep, total_upkeep]

    def calculate_smart_savings(self):
        """
        If your mortgage is less than 30 years, the user will 'pay yourself' your mortgage payment until the
        30 year mark of the initial purchase.
        :return: The amount of savings obtained
        """
        savings_duration = 30 - self.loan_duration
        monthly_interest = self.interest_rate / self.yearly_payments
        remaining_principle = self.purchase_price - self.down_payment
        monthly_payment = remaining_principle / (
                ((1 + monthly_interest) ** (self.yearly_payments * self.loan_duration)
                 - 1) / (monthly_interest * (1 + monthly_interest) **
                         (self.yearly_payments * self.loan_duration)))
        return savings_duration * (monthly_payment * 12)

    def calculate_total_costs(self):
        """
        Main function, brings all information into one spot for final calculations
        :return: Update this!$$$$$$$$$$
        """
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
        monthly_costs = pmi_list[0] + interest_list[0] + prop_tax_list[0] + maintenance_list[0] +\
                        principle_payment_list[0]
        yearly_costs = pmi_list[1] + interest_list[1] + prop_tax_list[1] + maintenance_list[1] + \
                       principle_payment_list[1]
        total_costs = pmi_list[2] + interest_list[2] + prop_tax_list[2] + maintenance_list[2] + \
                      principle_payment_list[2]
        # If your mortgage payment with all costs is more than 25 percent of your take home income,
        # this is a poor home purchase.
        if monthly_costs > (self.take_home_income * 0.25) / 12:
            print('\n--- THIS IS NOT AN OPTIMAL HOME PURCHASE ---\n\n')
            print('-- It is strongly recommended you reconsider either: --\n')
            print('     - Purchase a cheaper home\n'
                  '     - Increase your down payment\n'
                  '     - Increase your income\n\n')
        else:
            print('\n--- CONGRATS! THIS IS AN OPTIMAL AND SAFE HOME PURCHASE ---\n\n')
        if self.loan_duration > 15:
            print('Even though this may or may not be an optimal home purchase,\nit is strongly '
                  'recommended to do nothing above a 15 year loan duration.\nThe average millionaire pays '
                  'their house off in just 11 years!\n')

        if self.loan_duration < 30:
            smart_savings = self.calculate_smart_savings(yearly_costs)
        else:
            smart_savings = None
        # Recommended maximum monthly payment
        rec_payment = self.take_home_income * 0.25 / 12
        print('*** YOUR INPUT ***')
        print(' - Purchase Price -->', self.purchase_price)
        print(' - Down Payment -->', self.down_payment)
        print(' - Loan Duration --> ' + str(self.loan_duration) + ' years')
        print(' - Interest Rate -->', self.interest_rate)
        print(' - Yearly Payments -->', self.yearly_payments)
        print(' - Location -->', self.location)
        print(' - Home Type -->', self.home_type)
        print(' - Take Home Income After Taxes --> ' + str(self.take_home_income) + '\n')
        print('=== Your recommended max monthly payment --> %.2f ===\n' % rec_payment)

        print('*** NON RECURRING EXPENSES ***')
        print(' - Closing Costs --> %.2f' % closing_costs)
        print(' - Furniture --> N/A')
        print(' - Moving Costs --> N/A\n')

        print('*** MONTHLY EXPENSES ***')
        print(' - Principle Payment --> %.2f' % principle_payment_list[0])
        print(' - Private Mortgage Insurance --> %.2f' % pmi_list[0])
        print(' - Interest --> %.2f' % interest_list[0])
        print(' - Property Taxes --> %.2f' % prop_tax_list[0])
        print(' - Maintenance --> %.2f' % maintenance_list[0])
        print(' - Total --> %.2f\n' % monthly_costs)

        print('*** YEARLY EXPENSES ***')
        print(' - Principle Payment --> %.2f' % principle_payment_list[1])
        print(' - Private Mortgage Insurance --> %.2f' % pmi_list[1])
        print(' - Interest --> %.2f' % interest_list[1])
        print(' - Property Taxes --> %.2f' % prop_tax_list[1])
        print(' - Maintenance --> %.2f' % maintenance_list[1])
        print(' - Total --> %.2f\n' % yearly_costs)

        print('*** TOTAL EXPENSES PAID DURING LOAN DURATION ***')
        print(' - Principle Payment --> %.2f' % principle_payment_list[2])
        print(' - Private Mortgage Insurance --> %.2f' % pmi_list[2])
        print(' - Interest --> %.2f' % interest_list[2])
        print(' - Property Taxes --> %.2f' % prop_tax_list[2])
        print(' - Maintenance --> %.2f' % maintenance_list[2])
        print(' - Total --> %.2f\n' % total_costs)

        if self.loan_duration < 30 and monthly_costs <= (self.take_home_income * 0.25) / 12:
            print("Since you decided to take out LESS than a 30 year mortgage, let's see how much you could put"
                  " into a savings\naccount if you 'payed yourself' your prior monthly mortgage payment until we "
                  "reach 30 years.\n")
            print(' - Amount In Savings Account --> %.2f' % smart_savings)

        print('--------------------------------------------------------\n')


"""
    User input should include the following:

    trial_number = run_simulation(
                               1.) Amount the house was purchased for,
                               2.) Down payment, --> (If a percentage, must be done manually)
                               3.) Loan duration,
                               4.) Interest rate, --> (MUST be a percentage)
                               5.) Amount of payments made in a year,
                               6.) {'State': 'Zip Code' -or- 'City'},
                               7.) Home type,
                               8.) Your income before taxes
                               9.) How you plan to file your taxes
                                   - Single
                                   - Married (Joined)
                                   - Married (Separate)
                                   - Head of Household

    trial_number.calculate_total_costs()

    If total monthly expenses are more than 25 percent of your take home income,
    it is considered NOT an optimal home purchase.

"""


def main():
    pass


if __name__ == '__main__':
    main()
