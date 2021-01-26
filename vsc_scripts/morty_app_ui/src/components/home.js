/**
 * @author Ryan McCann
 * @summary The home page. Allows the user to input their details and display details about their mortgage with ease
 * @bugs N/A
 * @file home.js
 * @version 01/22/2021
 */
import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import { InputAdornment, TextField, Table, TableBody,
         TableCell, TableContainer, TableHead, TableRow, 
         Paper, Button, TablePagination, Select, MenuItem,
         FormControl, InputLabel, Container, Grid, Hidden, } from '@material-ui/core'
import Fade from 'react-reveal/Fade'
import {handle_input} from './handle_input.js'
import { ResponsivePie } from '@nivo/pie'
import {useful_functions} from '../morty_js/useful_functions'

var useful_function_methods = new useful_functions()

// Overlay margin params
const margin = { top: 30, right: 30, bottom: 30, left: 30 };

// Legend for the Pie chart
const legend = [
  {
      anchor: 'bottom',
      direction: 'row',
      justify: false,
      translateX: 15,
      translateY: 25,
      itemsSpacing: 0,
      itemWidth: 100,
      itemHeight: 0,
      itemTextColor: 'black',
      itemDirection: 'left-to-right',
      itemOpacity: 1,
      symbolSize: 20,
      symbolShape: 'circle',
      effects: [
          {
              on: 'hover',
              style: {
                  itemTextColor: 'red'
              }
          }
      ]
  }
]

const useStyles = makeStyles(theme => ({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
      justifyContent: 'center',
    },
    margin: {
      margin: theme.spacing(1.5),
    },
    textField: {
      width: "29vmin",
    },
    table: {
      width: '100%',
    },
    container: {
      maxHeight: 440,
      maxWidth: 530,
    },
    pie: {
      height: 440,
      fontFamily: "consolas, sans-serif",
      textAlign: "center",
      fontWeight: 'bold',
      position: 'relative',
    },
    overlay: {
      position: "absolute",
      top: 0,
      right: margin.right,
      bottom: 35,
      left: margin.left,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      fontSize: "6vmin",
      fontWeight: 'normal',
      color: "black",
      textAlign: "center",
      // This is important to preserve the chart interactivity
      pointerEvents: "none"
    },
    totalLabel: {
      fontSize: "3.5vmin",
    },
  }));
  
  // Creates default data for the DataTable
  function create_data(id, name, monthly, yearly, total) {
    return { id, name, monthly, yearly, total }
  }
  
  // Creates default TextField values
  function create_text_field(key, label, id, start_adornment, end_adornment, value) {
    return {key, label, id, start_adornment, end_adornment, value, error_value: false}
  }

  // Create SelectFields
  function create_select_field(fc_key, il_key, s_key, label_value, select_id, value, labels_arr) {
    return {fc_key, il_key, s_key, label_value, select_id, value, labels_arr}
  }
  // For changing SelectField values
  const tax_filing_status_arr = [
    {
      value: 'Single',
      label: 'Single',
    },
    {
      value: 'Married (Joint)',
      label: 'Married (Joint)',
    },
    {
      value: 'Married (Separate)',
      label: 'Married (Separate)',
    },
    {
      value: 'Head of Household',
      label: 'Head of Household',
    },
  ];
  const yearly_payments_arr = [
    {
      value: '12 (Monthly)',
      label: '12 (Monthly)',
    },
    {
      value: '26 (Bi-Weekly)',
      label: '26 (Bi-Weekly)',
    },
    {
      value: '52 (Weekly)',
      label: '52 (Weekly)',
    },
  ];
  const property_type_arr = [
    {
      value: 'House',
      label: 'House',
    },
    {
      value: 'Condo',
      label: 'Condo',
    },
    {
      value: 'Apartment',
      label: 'Apartment',
    },
  ];
  
  // For sorting rows in the DataTable
  function descending_comparator(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) {
      return -1;
    }
    if (b[orderBy] > a[orderBy]) {
      return 1;
    }
    return 0;
  }
  
  // For sorting rows in the DataTable
  function get_comparator(order, orderBy) {
    return order === 'desc'
      ? (a, b) => descending_comparator(a, b, orderBy)
      : (a, b) => -descending_comparator(a, b, orderBy);
  }
  
  // For sorting rows in the DataTable
  function stable_sort(array, comparator) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a, b) => {
      const order = comparator(a[0], b[0]);
      if (order !== 0) return order;
      return a[1] - b[1];
    });
    return stabilizedThis.map((el) => el[0]);
  }

  function create_pi_data(id, label, value, color) {
    return {id, label, value, color}
  }

function Home() {
    const classes = useStyles();
    // For TextFields
    const [values, set_values] = React.useState([
      create_text_field(0, 'Purchase Price', 'purchase_price', '$', '' ,''),
      create_text_field(1, 'Down Payment', 'down_payment', '$', '' ,''),
      create_text_field(2, 'Interest Rate', 'interest_rate', '%', '' ,''),
      create_text_field(3, 'Loan Duration', 'loan_duration', '', 'Years' ,''),
      create_text_field(4, 'City', 'city', '', '' ,''),
      create_text_field(5, 'State', 'state', '', '' ,''),
      create_text_field(6, 'Income', 'income', '$', '' ,''),
    ]);
    const [select_values, set_select_values] = React.useState([
      create_select_field(0, 1, 2, 'Tax Filing Status', 'Tax Filing Status', ' ', tax_filing_status_arr),
      create_select_field(3, 4, 5, 'Yearly Payments', 'Yearly Payments', ' ', yearly_payments_arr),
      create_select_field(6, 7, 8, 'Type Of Property', 'Type Of Property', ' ', property_type_arr)
    ]);
    // For TableRows
    const [data, set_data] = React.useState([
      create_data(0, 'Principle', 0, 0, 0),
      create_data(1, 'Interest', 0, 0, 0),
      create_data(2, 'Private Mortgage Insurance', 0, 0, 0),
      create_data(3, 'Property Taxes', 0, 0, 0),
      create_data(4, 'Maintenance', 0, 0, 0),
      create_data(5, 'Recurring Expenses Total', 0, 0, 0),
      create_data(6, 'Closing Costs', 0, 0, 0),
      create_data(7, 'Non-Recurring Expenses Total', 0, 0, 0),
      create_data(8, 'Total', 0, 0, 0),
    ])
    // Handle change for TextFields
    const handle_change = prop => event => {
      var check_var
      values[prop]['value'] = event.target.value
      // Make sure our numerical values are not less than zero and they're not strings
      if (prop === 0 || prop === 1 || prop === 2 || prop === 3) {
        check_var = values[prop]['value']
        if ((parseFloat(check_var) < 0 || isNaN(parseFloat(check_var))) && check_var !== '') {
          values[prop]['error_value'] = true
        }
        else {
          values[prop]['error_value'] = false
        }
      }
      set_values([...values])
    };
    // Handle change for Selection dropdown
    const handle_select_change = select_prop => select_event => {
      var key;
      // Tax filing status
      if (select_prop === 2) {
        key = 0
      }
      // Yearly Payments
      else if (select_prop === 5) {
        key = 1
      }
      // Type of property
      else {
        key = 2
      }
      select_values[key]['value'] = select_event.target.value
      set_select_values([...select_values])
    };
    // For the submit button
    function handle_click(raw_values, raw_select_values) {
      var raw_data = [], i
      for (i = 0; i < raw_values.length; i++) {
        raw_data.push(raw_values[i])
      }
      for (i = 0; i < raw_select_values.length; i++) {
        raw_data.push(raw_select_values[i])
      }
      var response_arr = handle_input(raw_data)
      if (response_arr !== null) {
        set_data(response_arr)
        handle_pi_data(response_arr)
      }
    }
    // For TablePagination
    const [page, set_page] = React.useState(0);
    const [rows_per_page, set_rows_per_page] = React.useState(6);
    const handle_change_page = (event, newPage) => {
      set_page(newPage);
    };
    const handle_change_rows_per_page = (event) => {
      set_rows_per_page(parseInt(event.target.value, 10));
      set_page(0);
    };
    const [order] = React.useState('asc');
    const [orderBy] = React.useState('id');
    // For pi chart
    const [pi_data, set_pi_data] = React.useState([
      create_pi_data('Principle', 'Principle', 500, 'hsl(318, 70%, 50%)'),
      create_pi_data('Interest', 'Interest', 200, 'hsl(202, 70%, 50%)'),
      create_pi_data('PMI', 'PMI', 50, 'hsl(177, 70%, 50%)'),
      create_pi_data('Taxes', 'Taxes', 100, 'hsl(19, 70%, 50%)'),
      create_pi_data('Maintenance', 'Maintenance', 50, 'hsl(105, 70%, 50%)'),
    ])
    // Monthly payment to display in the middle of the pi-chart
    const [monthly_payment, set_monthly_payment] = React.useState('$900')
    // Updates the data displayed on the pi chart
    function handle_pi_data(arr) {
      var mod_arr, res_arr = [], i
      // Don't display a value if it's zero
      mod_arr = [
        {id: 'Principle', label: 'Principle', value: parseInt(useful_function_methods.remove_commas(arr[0]['monthly'])), color: 'hsl(318, 70%, 50%)'},
        {id: 'Interest', label: 'Interest', value: parseInt(useful_function_methods.remove_commas(arr[1]['monthly'])), color: 'hsl(202, 70%, 50%)'},
        {id: 'PMI', label: 'PMI', value: parseInt(useful_function_methods.remove_commas(arr[2]['monthly'])), color: 'hsl(177, 70%, 50%)'},
        {id: 'Taxes', label: 'Taxes', value: parseInt(useful_function_methods.remove_commas(arr[3]['monthly'])), color: 'hsl(19, 70%, 50%)'},
        {id: 'Maintenance', label: 'Maintenance', value: parseInt(useful_function_methods.remove_commas(arr[4]['monthly'])), color: 'hsl(105, 70%, 50%)'},
      ]
      // Don't display a value if it's zero
      for (i = 0; i < mod_arr.length; i++) {
        if (mod_arr[i]['value'] === 0) {
          continue
        }
        res_arr.push(mod_arr[i])
      }
      set_pi_data([...res_arr])
      set_monthly_payment('$' + arr[8]['monthly'])
    }
    const handle_pi_click = event => {
      const info_arr = [
        {Principle: 'Explanation of principle calculation coming soon!'},
        {Interest: 'Explanation of interest calculation coming soon!'},
        {PMI: 'Explanation of private mortgage insurance calculation coming soon!'},
        {Taxes: 'Explanation of property taxes calculation coming soon!'},
        {Maintenance: 'Explanation of maintenance calculation coming soon!'},
      ]
      var i
      for (i = 0; i < info_arr.length; i++) {
        if (event['id'] === Object.keys(info_arr[i])[0]) {
          window.alert(Object.values(info_arr[i])[0])
        }
      }
    }
    return(
        <div>
            {/* Creates TextFields */}
            <Fade top cascade>
              <div id="home_tfs_sfs" className={classes.root}>
                  {values.map(value => (
                    <TextField
                        key={value.key}
                        label={value.label}
                        id={value.id}
                        className={clsx(classes.margin, classes.textField)}
                        InputProps={{
                        startAdornment: <InputAdornment position="start">{value.start_adornment}</InputAdornment>,
                        endAdornment: <InputAdornment position="start">{value.end_adornment}</InputAdornment>,
                        }}
                        variant="outlined"
                        value={value.value}
                        onChange={handle_change(value.key)}
                        error={value.error_value}
                    />
                  ))}
                  {/* Creates Selections */}
                  {select_values.map(select_value => (
                    <FormControl key={select_value.fc_key} variant="outlined" className={classes.root}>
                      <InputLabel key={select_value.il_key} id="demo-simple-select-outlined-label" className={clsx(classes.margin, classes.textField)}
                      >{select_value.label_value}
                      </InputLabel>
                      <Select
                        key={select_value.s_key}
                        labelId="demo-simple-select-outlined-label"
                        id={select_value.select_id}
                        className={clsx(classes.margin, classes.textField)}
                        value={select_value.select_value}
                        onChange={handle_select_change(select_value.s_key)}
                        label={select_value.label_value}
                      >
                        {select_value.labels_arr.map((option) => (
                          <MenuItem key={option.value} value={option.value}>
                            {option.label}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  ))}
              </div>
              {/* Submit Button */}
              <div style={{textAlign: 'center'}}>
                <Button 
                          size="large" variant="contained" color="primary" 
                          style={{marginBottom: '5.2vmin'}}
                          onClick={() => handle_click(values, select_values)}
                  >
                    Submit
                  </Button>
              </div>
            </Fade>
          {/* DataTable and Pie Chart */}
          <Grid container spacing={3}>
            <Grid item xs={12} sm={12} md={6} lg={6}>
              <Fade left cascade>
                <Container>
                  <div className={classes.pie}>
                    <ResponsivePie 
                      margin={{ bottom: 40 }}
                      data={pi_data}
                      colors={{ scheme: 'category10' }}
                      innerRadius={0.7}
                      padAngle={1}
                      cornerRadius={5}
                      enableRadialLabels={false}
                      legends={legend}
                      borderWidth={1}
                      borderColor={{ from: 'color', modifiers: [ [ 'darker', 0.2 ] ] }}
                      sliceLabelsTextColor="#333333"
                      onClick={handle_pi_click}
                    />
                    <div className={classes.overlay}>
                      <span>{monthly_payment}</span>
                      <span className={classes.totalLabel}>Monthly Payment</span>
                    </div>
                  </div>
                </Container>
              </Fade>
            </Grid>
            <Grid item xs={12} sm={12} md={6} lg={6}>
            <Hidden smDown>
               <Fade right cascade>
                  <TableContainer component={Paper} className={classes.container}>
                    <Table stickyHeader className={classes.table} aria-label="simple table">
                      <TableHead>
                        <TableRow>
                          <TableCell>Expenses</TableCell>
                          <TableCell align="right">Monthly&nbsp;($)</TableCell>
                          <TableCell align="right">Yearly&nbsp;($)</TableCell>
                          <TableCell align="right">Total&nbsp;($)</TableCell>
                        </TableRow>
                      </TableHead>
                      {/* Creates rows for the DataTable */}
                      <TableBody>
                      {stable_sort(data, get_comparator(order, orderBy))
                          .slice(page * rows_per_page, page * rows_per_page + rows_per_page)
                          .map((row) => {
                            return (
                              <TableRow key={row.name} hover>
                              <TableCell component="th" scope="row">
                                {row.name}
                              </TableCell>
                              <TableCell align="right">{row.monthly}</TableCell>
                              <TableCell align="right">{row.yearly}</TableCell>
                              <TableCell align="right">{row.total}</TableCell>
                            </TableRow>
                            );
                          })}
                      </TableBody>
                    </Table>
                    <TablePagination
                    rowsPerPageOptions={[6, 9]}
                    component="div"
                    count={data.length}
                    rowsPerPage={rows_per_page}
                    page={page}
                    onChangePage={handle_change_page}
                    onChangeRowsPerPage={handle_change_rows_per_page}
                    />
                  </TableContainer>
                </Fade>
              </Hidden>
            </Grid>
          </Grid>
      </div>
    )
}

export default Home