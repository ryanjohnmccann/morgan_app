/**
 * @author Ryan McCann
 * @summary Useful functions to use on the front-end side of the application
 * @bugs N/A
 * @file useful_functions.js
 * @version 12/23/2020
 */
export class useful_functions {

    clean_string(string) {
        string = string.toLowerCase()
        string = string.replace(' ', '_')
        return string
    }

}
