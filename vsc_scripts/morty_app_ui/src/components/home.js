import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import { InputAdornment, TextField, Table, TableBody,
         TableCell, TableContainer, TableHead, TableRow, 
         Paper, Button, TablePagination } from '@material-ui/core'
import Fade from 'react-reveal/Fade'
import {handle_input} from './handle_input.js'

const useStyles = makeStyles(theme => ({
    root: {
      display: 'flex',
      flexWrap: 'wrap',
    },
    margin: {
      margin: theme.spacing(1.5),
    },
    textField: {
      width: 248,
      // iPhone 5, SE
      [theme.breakpoints.between("0", "360")]: {
        width: 100,
      },
      // Galaxy S5
      [theme.breakpoints.between("360", "370")]: {
        width: 120,
      },
      // iPhone 6, 7, 8
      [theme.breakpoints.between("370", "380")]: {
        width: 130,
      },
      // Pixel 2, Pixel 2 XL
      [theme.breakpoints.between("400", "411")]: {
        width: 145,
      },
      // iPhone 6, 7, 8 Plus
      [theme.breakpoints.between("411", "420")]: {
        width: 150,
      },
      // iPad
      [theme.breakpoints.between("750", "770")]: {
        width: 115,
      },
      // iPad Pro
      [theme.breakpoints.between("1000", "1030")]: {
        width: 165,
      },
      // Larger monitors (Than my MacBook Pro 13.3")
      [theme.breakpoints.between("1500", "2000")]: {
        width: 345,
      },
    },
    table: {
      width: '100%',
    },
    container: {
      maxHeight: 440,
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

function Home() {
    const classes = useStyles();
    // For TextFields
    const [values, set_values] = React.useState([
      create_text_field(0, 'Purchase Price', 'purchase_price', '$', '' ,''),
      create_text_field(1, 'Down Payment', 'down_payment', '$', '' ,''),
      create_text_field(2, 'Interest Rate', 'interest_rate', '%', '' ,''),
      create_text_field(3, 'Loan Duration', 'loan_duration', '', 'Years' ,''),
      create_text_field(4, 'Yearly Payments', 'yearly_payments', '', '' ,''),
      create_text_field(5, 'City', 'city', '', '' ,''),
      create_text_field(6, 'State', 'state', '', '' ,''),
      create_text_field(7, 'Type Of Property', 'type_of_property', '', '' ,''),
      create_text_field(8, 'Income', 'income', '$', '' ,''),
      create_text_field(9, 'Tax Filing Status', 'tax_filing_status', '', '' ,''),
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
      if (prop === 0 || prop === 1 || prop === 2 || prop === 3 || prop === 4 || prop === 8) {
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
    // For the submit button
    function handle_click(raw_data) {
      var response_arr = handle_input(raw_data)
      if (response_arr !== null) {
        set_data(response_arr)
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

    return(
        <div>
            {/* Fade in effect */}
            <Fade>
            {/* Creates our TextFields */}
            <div id="home_tfs" className={classes.root}>
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
            </div>
          {/* Submit Button */}
          <div style={{textAlign: 'center'}}>
            <Button 
                      size="large" variant="contained" color="primary" 
                      style={{marginBottom: '5.2vmin'}}
                      onClick={() => handle_click(values)}
              >
                Submit
              </Button>
          </div>
          {/* DataTable */}
          <div>
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
            </TableContainer>
            <TablePagination
              rowsPerPageOptions={[6, 9]}
              component="div"
              count={data.length}
              rowsPerPage={rows_per_page}
              page={page}
              onChangePage={handle_change_page}
              onChangeRowsPerPage={handle_change_rows_per_page}
            />
          </div>
        </Fade>
      </div>
    )
}

export default Home