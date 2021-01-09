/**
 * @author Ryan McCann
 * @summary Useful functions to use on the front-end side of the application
 * @bugs N/A
 * @file useful_functions.js
 * @version 01/08/2020
 */
export class useful_functions {

    clean_string(string) {
        string = string.toLowerCase()
        string = string.replace(' ', '_')
        return string
    }

    remove_commas(string) {
        var i, res_string = ''
        for (i = 0; i < string.length; i++) {
            if (string[i] === ',') {
                continue
            }
            res_string += string[i]
        }
        console.log(res_string)
        return res_string
    }

}
