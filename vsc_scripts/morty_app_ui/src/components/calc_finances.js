/**
 * @author Ryan McCann
 * @summary Calculates all necessary costs and return appropriately structured results.
 * @bugs N/A
 * @file calc_finances.js
 * @version 12/23/2020
 */

class run_simulation {
    constructor(error_checked_arr) {
        this.purchase_price = error_checked_arr[0]['purchase_price']
        this.down_payment = error_checked_arr[1]['down_payment']
        this.interest_rate = error_checked_arr[2]['interest_rate'] / 100
        this.loan_duration = error_checked_arr[3]['loan_duration']
        this.city = error_checked_arr[4]['city']
        this.state = error_checked_arr[5]['state']
        this.income = error_checked_arr[6]['income']
        this.tax_filing_status = error_checked_arr[7]['tax_filing_status']
        this.yearly_payments = error_checked_arr[8]['yearly_payments']
        this.property_type = error_checked_arr[9]['property_type']
        this.monthly_interest = this.interest_rate / this.yearly_payments
        // Equation found online. A monthly payment formula for a home mortgage
        this.payment_due = (this.purchase_price - this.down_payment) /
                            (((1 + (this.monthly_interest)) **
                            (this.yearly_payments * this.loan_duration) - 1) /
                            (this.monthly_interest * (1 + this.monthly_interest) **
                            (this.yearly_payments * this.loan_duration)))
    }
    // Private Mortgage Insurance
    calculate_pmi() {
        if (this.down_payment < (this.purchase_price * 0.2)) {
            var yearly_pmi = (0.01 * this.purchase_price),
            total_pmi = yearly_pmi * this.loan_duration,
            monthly_pmi = yearly_pmi / 12
        }
        // No pmi if the down payment is greater or equal to 20 percent
        else {
            monthly_pmi = yearly_pmi = total_pmi = 0
        }
        return [monthly_pmi, yearly_pmi, total_pmi]
    }
    calculate_interest() {
        var remaining_principle = (this.purchase_price - this.down_payment),
        total_interest = 0,
        temp_interest,
        payment
        while (true) {
            temp_interest = ((this.interest_rate / this.yearly_payments) * remaining_principle)
            total_interest += temp_interest
            payment = (this.payment_due - temp_interest)
            remaining_principle -= payment
            // If remaining principle is less than or equal to the monthly payment,
            // we know this has to be the last iteration
            if (remaining_principle <= this.purchase_price / this.loan_duration /
                this.yearly_payments) {
                    var yearly_interest = total_interest / this.loan_duration,
                    monthly_interest = yearly_interest / 12
                    return [monthly_interest, yearly_interest, total_interest]
            }
        }
    }
    calculate_property_tax() {
        var city = this.city
        // All zip codes in New England start with a zero
        if (this.city[0] === '0') {   
            var zip_code = this.city
            var temp_data = require('../data/zip_codes/' + this.state + '.json'),
            i
            for (i = 0; i < temp_data.length; i++) {
                if (temp_data[i]['zip_code'] === zip_code) {
                    city = temp_data[i]['city/town']
                    break
                }
            }
        }
        var des_data = require('../data/property_tax_rates/' + this.state + '.json')
        const cities_towns_arr = Object.values(des_data)[0]
        for (i = 0; i < cities_towns_arr.length; i++) {
            if (city === cities_towns_arr[i]['location']) {
                var property_tax_rate = cities_towns_arr[i]['rate']
                break
            }
        }
        var monthly_property_tax = ((this.purchase_price) * property_tax_rate) / 12,
        yearly_property_tax = monthly_property_tax * 12,
        total_property_tax = monthly_property_tax * 12 * this.loan_duration
        return [monthly_property_tax, yearly_property_tax, total_property_tax]
    }
    calculate_maintenance() {
        if (this.property_type === 'house') {
            var yearly_upkeep = this.purchase_price * 0.005
        }
        else {
            yearly_upkeep = 330 * 12
        }
        var total_upkeep = yearly_upkeep * this.loan_duration,
        monthly_upkeep = yearly_upkeep / 12
        return [monthly_upkeep, yearly_upkeep, total_upkeep]
    }
    calculate_smart_savings () {
        var savings_duration = 30 - this.loan_duration
        return (savings_duration * (this.payment_due))
    }
    calculate_total_costs() {
        // No recurring expenses
        var closing_costs = this.purchase_price * 0.04,
        // Our desired lists
        pmi_arr = this.calculate_pmi(),
        interest_arr = this.calculate_interest(),
        property_tax_arr = this.calculate_property_tax(),
        maintenance_arr = this.calculate_maintenance(),
        // The average principle is the difference from the average interest
        monthly_principle = interest_arr[0] - this.payment_due
        if (monthly_principle <= 0) {
            monthly_principle = this.payment_due - interest_arr[0]
        }
        var yearly_principle = monthly_principle * 12,
        principle_payment_arr = [monthly_principle, yearly_principle,
                                (this.purchase_price - this.down_payment)],
        monthly_costs = pmi_arr[0] + interest_arr[0] + property_tax_arr[0] +
                        maintenance_arr[0] + principle_payment_arr[0],
        yearly_costs = monthly_costs * 12,
        // Since yearly and monthly costs are averages, they will never
        //  Add up exactly
        total_costs = pmi_arr[2] + interest_arr[2] + property_tax_arr[2] +
                        maintenance_arr[2] + principle_payment_arr[2]
        // EVENTUALLY WANT TO ADD SMART SAVINGS HERE
        // Total recurring and non-recurring expenses
        var tot_rec_exp,
        tot_non_rec_exp,
        rec_exp_arr

        tot_rec_exp = principle_payment_arr[2] + pmi_arr[2] + interest_arr[2] + property_tax_arr[2] +
                        maintenance_arr[2]
        tot_non_rec_exp = closing_costs
        rec_exp_arr = [tot_rec_exp/this.loan_duration/12, tot_rec_exp/this.loan_duration, tot_rec_exp]

        var res_arr = [
            {
                id: '0',
                name: 'Principle',
                monthly: principle_payment_arr[0].toFixed(2),
                yearly: principle_payment_arr[1].toFixed(2),
                total: principle_payment_arr[2].toFixed(2),
            },
            {
                id: '1',
                name: 'Interest',
                monthly: interest_arr[0].toFixed(2),
                yearly: interest_arr[1].toFixed(2),
                total: interest_arr[2].toFixed(2),
            },
            {
                id : '2',
                name: 'Private Mortgage Insurance',
                monthly: pmi_arr[0].toFixed(2),
                yearly: pmi_arr[1].toFixed(2),
                total: pmi_arr[2].toFixed(2),
            },
            {
                id: '3',
                name: 'Property Taxes',
                monthly: property_tax_arr[0].toFixed(2),
                yearly: property_tax_arr[1].toFixed(2),
                total: property_tax_arr[2].toFixed(2),
            },            {
                id: '4',
                name: 'Maintenance',
                monthly: maintenance_arr[0].toFixed(2),
                yearly: maintenance_arr[1].toFixed(2),
                total: maintenance_arr[2].toFixed(2),
            },
            {
                id: '5',
                name: 'Recurring Expenses Total',
                monthly: rec_exp_arr[0].toFixed(2),
                yearly: rec_exp_arr[1].toFixed(2),
                total: rec_exp_arr[2].toFixed(2)

            },
            {
                id: '6',
                name: 'Closing Costs',
                monthly: "0.00",
                yearly: "0.00",
                total: closing_costs.toFixed(2),
            },
            {
                id: '7',
                name: 'Non-Recurring Expenses Total',
                monthly: "0.00",
                yearly: "0.00",
                total: tot_non_rec_exp.toFixed(2)
            },
            {
                id: '8',
                name: 'Total',
                monthly: monthly_costs.toFixed(2),
                yearly: yearly_costs.toFixed(2),
                total: (total_costs + tot_non_rec_exp).toFixed(2),
            },
        ], i, j, k, r, q
        // Adds commas to final output
        for (i = 0; i < res_arr.length; i++) {
            var temp_arr = [res_arr[i]['monthly'], res_arr[i]['yearly'],
                            res_arr[i]['total']],
            new_res_arr = []
            for (j = 0; j < temp_arr.length; j++) {
                var temp_val = temp_arr[j].split("."),
                before_dec = temp_val[0], after_dec = temp_val[1],
                count = 0, new_var = '', reversed_bef_dec = '', temp_rev, var_len
                var_len = before_dec.length - 1
                // Reverses string
                for (r = var_len; r >= 0; r--) {
                    temp_rev = before_dec[r]
                    reversed_bef_dec += temp_rev
                }
                // Adds commas back
                for (k = 0; k < reversed_bef_dec.length; k++) {
                    var temp_let = reversed_bef_dec[k]
                    count += 1
                    if (count === 3 && (k !== reversed_bef_dec.length - 1)) {
                        temp_let += ','
                        count = 0
                    }
                    new_var += temp_let
                }
                var_len = new_var.length - 1
                var new_before_dec = '' 
                // Reverses string back to normal with commas
                for (q = var_len; q >= 0; q-- ) {
                    temp_rev = new_var[q]
                    new_before_dec += temp_rev
                }
                //  Our final response variable
                var res_var = new_before_dec + '.' + after_dec
                new_res_arr.push(res_var)
            }
            res_arr[i]['monthly'] = new_res_arr[0]
            res_arr[i]['yearly'] = new_res_arr[1]
            res_arr[i]['total'] = new_res_arr[2]
        }
        return res_arr
    }
}

export function initiate_sim(input_arr) {
    var sim_1 = new run_simulation(input_arr),
    res_data = sim_1.calculate_total_costs()
    return res_data
}