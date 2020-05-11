import {initiate_sim} from './calc_finances.js'

function error_check_input (input_list) {
    var i, j, k
    // Loads in all states and cities that exist in thus far
    var states_and_cities = require('../data/all_states_and_cities.json');
    for (i = 0; i < input_list.length; i++) {
        if (Object.values(input_list[1])[0] > Object.values(input_list[0])[0]) {
            window.alert('Down Payment Cannot Be More Than The Purchase Price')
            return null
        }
        // No NaN or negative numerical values allowed
        if (i === 0 || i === 1 || i === 2 || i === 3 || i === 4 || i === 8) {
            var curr_val = Object.values(input_list[i])[0],
            // So the error can easily be displayed for the user
            locate_error_arr = [
                'Purchase Price',
                'Down Payment',
                'Interest Rate',
                'Loan Duration',
                'Yearly Payments',
                'City',
                'State',
                'Property Type',
                'Income',
                'Tax Filing Status'
            ]  
            if (curr_val < 0 || isNaN(curr_val)) {
                window.alert('Invalid Numerical Input At ' + locate_error_arr[i])
                return null
            }
        }
        // State and city
        if (i === 6) {
            var check_state = false, user_state, check_city = false
            user_state = input_list[6]['state'].toLowerCase()
            user_state = user_state.replace(' ', '_')
            if (user_state === 'ma') {
                user_state = 'massachusetts'
            }
            else if (user_state === 'nh') {
                user_state = 'new_hampshire'
            }
            else if (user_state === 'vt') {
                user_state = 'vermont'
            }
            else if (user_state === 'ri') {
                user_state = 'rhode_island'
            }
            else if (user_state === 'me') {
                user_state = 'maine'
            }
            else if (user_state === 'ct') {
                user_state = 'connecticut'
            }
            for (j = 0; j < states_and_cities.length; j++) {
                var curr_key = Object.keys(states_and_cities[j])
                if (user_state === curr_key[0]) {
                    check_state = true
                    input_list[6]['state'] = user_state
                    var user_city = input_list[5]['city']
                    // Means it is a zip code because all zip codes in New England start with a zero
                    if (user_city[0] === '0') {
                        var temp_data = require('../data/zip_codes/' + user_state + '.json')
                        for (i = 0; i < temp_data.length; i++) {
                            if (temp_data[i]['zip_code'] === user_city) {
                                input_list[5]['city'] = temp_data[i]['city/town']
                                check_city = true
                                break
                            }
                        }
                    }
                    else {
                        user_city = user_city.toLowerCase()
                        user_city = user_city.replace(' ', '_')
                        for (k = 0; k < states_and_cities[j][user_state].length; k++) {
                        if (user_city === states_and_cities[j][user_state][k]) {
                            check_city = true
                            input_list[5]['city'] = user_city
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
        }
        // Property type
        else if (i === 7) {
            var prop_type = input_list[7]['property_type'].toLowerCase(),
            valid_props_arr = ['house', 'apartment', 'home', 'condo', 'condominium'],
            check_prop = false
            prop_type = prop_type.replace(' ', '_')
            for (j = 0; j < valid_props_arr.length; j++) {
                if (prop_type === valid_props_arr[j]) {
                    check_prop = true
                    input_list[7]['property_type'] = prop_type
                }
            }
            if (check_prop === false) {
                window.alert('Property Type Invalid')
                return null
            }
        }
        // Tax filing status, nothing until I get data and update this
        else if (i === 9) {
        }
        else {
            continue
        }
    }
    // *** Will eventually error check the rest of my input in the future ***

    // Final calculations are ran here
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
    // Converts string numerical values to floats
    for (i = 0; i < des_values_arr.length; i++) {
        if (i === 5 || i === 6 || i === 7 || i === 8 || i === 9) {
            continue
        }
        temp_var = des_values_arr[i]
        fixed_var = parseFloat(temp_var)
        des_values_arr[i] = fixed_var
    }
    // Our final array to be passed on to be error checked
    var response_arr = [
        {purchase_price: des_values_arr[0]},
        {down_payment: des_values_arr[1]},
        {interest_rate: des_values_arr[2]},
        {loan_duration: des_values_arr[3]},
        {yearly_payments: des_values_arr[4]},
        {city: des_values_arr[5]},
        {state: des_values_arr[6]},
        {property_type: des_values_arr[7]},
        {income: des_values_arr[8]},
        {tax_filing_status: des_values_arr[9]}
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
