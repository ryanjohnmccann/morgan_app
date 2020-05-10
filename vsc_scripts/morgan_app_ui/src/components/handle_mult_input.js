import {initiate_mult_sim} from './calc_mult_finances.js'

function error_check_input(input_arr) {
    var i, j, k, r, loc_purch_error, final_res_arr = []
    // Loads in all states and cities that exist thus far
    var states_and_cities = require('../data/all_states_and_cities.json');
    // Access each individual input list from input array
    for (i = 0; i < input_arr.length; i++) {
        if (i === 0) {
            loc_purch_error = 'A'
        }
        else if (i === 1) {
            loc_purch_error = 'B'
        }
        else {
            loc_purch_error = 'C'
        }
        for (j = 0; j < input_arr[i].length; j++) {
            if (Object.values(input_arr[0][1])[0] > Object.values(input_arr[0][0])[0]) {
                window.alert('Down Payment Cannot Be More Than The Purchase Price In Purchase ' + loc_purch_error)
                return null
            }
            // No NaN or negative numerical values allowed
            if (j === 0 || j === 1 || j === 2 || j === 3 || j === 4 || j === 8) {
                var curr_val = Object.values(input_arr[i][j])[0],
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
                    window.alert('Invalid Numerical Input At ' + locate_error_arr[j] + ' In Purchase ' + loc_purch_error)
                    return null
                }
            }
            // State and city
            if (j === 6) {
                var check_state = false, user_state, check_city = false
                user_state = input_arr[i][6]['state'].toLowerCase()
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
                for (k = 0; k < states_and_cities.length; k++) {
                    var curr_key = Object.keys(states_and_cities[k])
                    if (user_state === curr_key[0]) {
                        check_state = true
                        input_arr[i][6]['state'] = user_state
                        var user_city = input_arr[i][5]['city']
                        // Means it is a zip code because all zip codes in New England start with a zero
                        if (user_city[0] === '0') {
                            var temp_data = require('../data/zip_codes/' + user_state + '.json')
                            for (r = 0; r < temp_data.length; r++) {
                                if (temp_data[r]['zip_code'] === user_city) {
                                    input_arr[5]['city'] = temp_data[r]['city/town']
                                    check_city = true
                                    break
                                }
                            }
                        }
                        else {
                            user_city = user_city.toLowerCase()
                            user_city = user_city.replace(' ', '_')
                            for (r = 0; r < states_and_cities[k][user_state].length; r++) {
                            if (user_city === states_and_cities[k][user_state][r]) {
                                check_city = true
                                input_arr[i][5]['city'] = user_city
                                }
                            }
                        }
                    }
                }
                if (check_state === false) {
                    window.alert('State Not Found In Purchase ' + loc_purch_error)
                    return null
                }
                if (check_city === false) {
                    window.alert('City Not Found In Purchase ' + loc_purch_error)
                    return null
                }
            }
            // Property type
            else if (j === 7) {
                var prop_type = input_arr[i][7]['property_type'].toLowerCase(),
                valid_props_arr = ['house', 'apartment', 'home', 'condo', 'condominium'],
                check_prop = false
                prop_type = prop_type.replace(' ', '_')
                for (k = 0; k < valid_props_arr.length; k++) {
                    if (prop_type === valid_props_arr[k]) {
                        check_prop = true
                        input_arr[i][7]['property_type'] = prop_type
                    }
                }
                if (check_prop === false) {
                    window.alert('Property Type Invalid In Purchase ' + loc_purch_error)
                    return null
                }
            }
            // Tax filing status, nothing until I get data and update this
            else if (i === 9) {
            }
            else {
                continue
            }
            // *** Will eventually error check the rest of my input in the future ***
        }
        final_res_arr.push(input_arr[i])
    }
    return initiate_mult_sim(final_res_arr)
}

export function handle_mult_input(input_arr) {
    var i, j, response_arr = []
    for (j = 0; j < input_arr.length; j++) {
        var des_values_arr = [], temp_var, fixed_var = ''
        for (var val of Object.values(input_arr[j])) {
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
        var temp_arr = [
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
        console.log(temp_arr)
        response_arr.push(temp_arr)
    }

    // // Made for my convenience of checking my code
    // var response_arr_a = [
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
    // ],
    // response_arr_b = [
    //     {purchase_price: 100000},
    //     {down_payment: 20000},
    //     {interest_rate: 15},
    //     {loan_duration: 12},
    //     {yearly_payments: 12},
    //     {city: 'tewksbury'},
    //     {state: 'Massachusetts'},
    //     {property_type: 'house'},
    //     {income: 100000},
    //     {tax_filing_status: 'single'}
    // ],
    // response_arr_c = [
    //     {purchase_price: 100000},
    //     {down_payment: 20000},
    //     {interest_rate: 15},
    //     {loan_duration: 12},
    //     {yearly_payments: 12},
    //     {city: 'andover'},
    //     {state: 'Massachusetts'},
    //     {property_type: 'house'},
    //     {income: 100000},
    //     {tax_filing_status: 'single'}
    // ]
    return error_check_input(response_arr)
}