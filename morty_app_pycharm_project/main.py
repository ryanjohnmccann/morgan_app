"""

"""

import morty_app


def main():
    simulation = morty_app.run_simulation(purchase_price=100000, down_payment=20000, loan_duration=15,
                                          interest_rate=3.75,
                                          yearly_payments=12, location={'Massachusetts': 'Tewksbury'},
                                          home_type='House',
                                          take_home_income=100000)
    simulation.calculate_total_costs()


if __name__ == '__main__':
    main()

