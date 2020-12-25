/**
 * @author Ryan McCann
 * @summary Error checks and structures input from the user in the home tab.
 * @bugs N/A
 * @file handle_input.js
 * @version 12/25/2020
 */

import {initiate_sim} from './calc_finances.js'
import {useful_functions} from '../morty_js/useful_functions.js'

var useful_function_methods = new useful_functions()

function error_check_input (input_list) {
    var i, j, k
    // Loads in all states and cities that exist in so far
    const states_and_cities = require('../data/all_states_and_cities.json')
    // Could be an abbreviation i.e. 'massachusetts' could be input as 'ma'
    const abbr_to_name_arr = require('../data/state_abbreviations/abbr_name_list.json')
    // Error check down payment vs. purchase price
    if (input_list[1]['down_payment'] > input_list[0]['purchase_price']) {
        window.alert('Down Payment Cannot Be More Than The Purchase Price')
        return null
    }
    // So the error can easily be displayed for the user
    var locate_error_arr = [
        'Purchase Price',
        'Down Payment',
        'Interest Rate',
        'Loan Duration',
        'City',
        'State',
        'Income',
        'Tax Filing Status',
        'Yearly Payments',
        'Property Type'
    ]
    var curr_val
    for (i = 0; i < input_list.length; i++) {
        if (i === 0 || i === 1 || i === 2 || i === 3 || i === 6) {
            curr_val = Object.values(input_list[i])[0]
            // No NaN or negative numerical values allowed here
            if (curr_val < 0 || isNaN(curr_val)) {
                window.alert('Invalid Numerical Input At ' + locate_error_arr[i])
                return null
            }
        }
    }
    var check_state = false, check_city = false, found_state = false
    var user_state = useful_function_methods.clean_string(input_list[5]['state'])
    console.log(user_state)
    while(!found_state) {
        for (j = 0; j < abbr_to_name_arr.length; j++) {
            // Current abbreviation and current state
            var curr_abbr = Object.keys(abbr_to_name_arr[j])[0],
                curr_state = Object.values(abbr_to_name_arr[j])[0]
            if (curr_abbr === user_state) {
                user_state = curr_state
            }
            if (user_state === curr_state) {
                found_state = true
                check_state = true
                break
            }
        }
        if (!found_state) {
            window.alert('Invalid State')
            return null
        }
    }
    for (j = 0; j < states_and_cities.length; j++) {
        var curr_key = Object.keys(states_and_cities[j])
        if (user_state === curr_key[0]) {
            check_state = true
            input_list[5]['state'] = user_state
            var user_city = input_list[4]['city']
            // Means it is a zip code because all zip codes in New England start with a zero
            if (user_city[0] === '0') {
                var temp_data = require('../data/zip_codes/' + user_state + '.json')
                for (i = 0; i < temp_data.length; i++) {
                    if (temp_data[i]['zip_code'] === user_city) {
                        input_list[4]['city'] = temp_data[i]['city/town']
                        check_city = true
                        break
                    }
                }
            }
            else {
                user_city = useful_function_methods.clean_string(user_city)
                for (k = 0; k < states_and_cities[j][user_state].length; k++) {
                if (user_city === states_and_cities[j][user_state][k]) {
                    check_city = true
                    input_list[4]['city'] = user_city
                    }
                }
            }
        }
    }
    if (check_state === false) {
        window.alert('State Not Found')
        return null
    }
    if (check_city === false) {
        window.alert('City Not Found')
        return null
    }
    // *** Will eventually error check the rest of my input in the future ***
    return initiate_sim(input_list)   
}

export function handle_input (input) {
    var des_values_arr = [], temp_var, fixed_var = '', i
    for (var val of Object.values(input)) {
        // Removes commas
        for (i = 0; i < val['value'].length; i++) {
            temp_var = val['value'][i]
            if (temp_var !== ',') {
                fixed_var += temp_var
            }
        }
        des_values_arr.push(fixed_var)
        fixed_var = ''
    }
    temp_var = ''
    // Converts necessary string numerical values to floats
    for (i = 0; i < des_values_arr.length; i++) {
        if (i === 4 || i === 5 || i === 7 || i === 9) {
            continue
        }
        // Convert the String of yearly payments to a numerical value
        else if (i === 8) {
            if (des_values_arr[i] === "12 (Monthly)") {
                des_values_arr[i] = 12
            }
            else if (des_values_arr[i] === "26 (Bi-Weekly)") {
                des_values_arr[i] = 26
            }
            else {
                des_values_arr[i] = 52
            }
        }
        else {
            temp_var = des_values_arr[i]
            fixed_var = parseFloat(temp_var)
            des_values_arr[i] = fixed_var
        }
    }
    // Our final array to be passed on to be error checked
    var response_arr = [
        {purchase_price: des_values_arr[0]},
        {down_payment: des_values_arr[1]},
        {interest_rate: des_values_arr[2]},
        {loan_duration: des_values_arr[3]},
        {city: des_values_arr[4]},
        {state: des_values_arr[5]},
        {income: des_values_arr[6]},
        {tax_filing_status: des_values_arr[7]},
        {yearly_payments: des_values_arr[8]},
        {property_type: des_values_arr[9]}
    ]
    // // Made for my convenience of checking my code
    // var response_arr = [
    //     {purchase_price: 100000},
    //     {down_payment: 20000},
    //     {interest_rate: 15},
    //     {loan_duration: 12},
    //     {yearly_payments: 12},
    //     {city: 'lowell'},
    //     {state: 'Massachusetts'},
    //     {property_type: 'house'},
    //     {income: 100000},
    //     {tax_filing_status: 'single'}
    // ]
    return error_check_input(response_arr)
}
