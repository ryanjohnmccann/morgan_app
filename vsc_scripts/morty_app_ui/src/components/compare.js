import React from 'react';
import Fade from 'react-reveal/Fade'
import { makeStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore'
import InputAdornment from '@material-ui/core/InputAdornment';
import TextField from '@material-ui/core/TextField';
import clsx from 'clsx';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import TablePagination from '@material-ui/core/TablePagination';
import {handle_mult_input} from './handle_mult_input.js'

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    flexBasis: '33.33%',
    flexShrink: 0,
  },
  secondaryHeading: {
    fontSize: theme.typography.pxToRem(15),
    color: theme.palette.text.secondary,
  },
  textField: {
    width: 230,
    // iPhone 5, SE
    [theme.breakpoints.between("0", "360")]: {
      width: 90,
    },
    // Galaxy S5
    [theme.breakpoints.between("360", "370")]: {
      width: 110,
    },
    // iPhone 6, 7, 8
    [theme.breakpoints.between("370", "380")]: {
      width: 115,
    },
    // Pixel 2, Pixel 2 XL, iPhone 6, 7, 8 Plus
    [theme.breakpoints.between("400", "420")]: {
      width: 135,
    },
    // iPad
    [theme.breakpoints.between("750", "770")]: {
      width: 110,
    },
    // iPad Pro
    [theme.breakpoints.between("1000", "1030")]: {
      width: 160,
    },
    // Larger monitors (Than my MacBook Pro 13.3")
    [theme.breakpoints.between("1100", "2000")]: {
      width: 335,
    },
  },
  margin: {
    margin: theme.spacing(1.3)
  },
  table: {
    width: '100%',
  },
  container: {
    maxHeight: 440,
    width: '33%',
    float: 'left',
    marginBottom: '2vmin',
    [theme.breakpoints.down("l")]: {
      float: 'none',
      width: '100%',
    },
  },
}));

// Creates default TextField values
function create_text_field(key, label, id, start_adornment, end_adornment, value) {
  return {key, label, id, start_adornment, end_adornment, value, error_value: false}
}

// Creates default data for the DataTable
function create_data(id, name, monthly, yearly, total) {
  return { id, name, monthly, yearly, total }
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

function get_comparator(order, orderBy) {
  return order === 'desc'
    ? (a, b) => descending_comparator(a, b, orderBy)
    : (a, b) => -descending_comparator(a, b, orderBy);
}

function stable_sort(array, comparator) {
  const stabilizedThis = array.map((el, index) => [el, index]);
  stabilizedThis.sort((a, b) => {
    const order = comparator(a[0], b[0]);
    if (order !== 0) return order;
    return a[1] - b[1];
  });
  return stabilizedThis.map((el) => el[0]);
}

export default function Compare() {
  const classes = useStyles();
  const [expanded, set_expanded] = React.useState(false);
  // For TextFields
  const [values_a, set_values_a] = React.useState([
    create_text_field(0, 'Purchase Price', 'purchase_price_a', '$', '' ,''),
    create_text_field(1, 'Down Payment', 'down_payment_a', '$', '' ,''),
    create_text_field(2, 'Interest Rate', 'interest_rate_a', '%', '' ,''),
    create_text_field(3, 'Loan Duration', 'loan_duration_a', '', 'Years' ,''),
    create_text_field(4, 'Yearly Payments', 'yearly_payments_a', '', '' ,''),
    create_text_field(5, 'City', 'city_a', '', '' ,''),
    create_text_field(6, 'State', 'state_a', '', '' ,''),
    create_text_field(7, 'Type Of Property', 'type_of_property_a', '', '' ,''),
    create_text_field(8, 'Income', 'income_a', '$', '' ,''),
    create_text_field(9, 'Tax Filing Status', 'tax_filing_status_a', '', '' ,''),
  ]);
  const [values_b, set_values_b] = React.useState([
    create_text_field(0, 'Purchase Price', 'purchase_price_b', '$', '' ,''),
    create_text_field(1, 'Down Payment', 'down_payment_b', '$', '' ,''),
    create_text_field(2, 'Interest Rate', 'interest_rate_b', '%', '' ,''),
    create_text_field(3, 'Loan Duration', 'loan_duration_b', '', 'Years' ,''),
    create_text_field(4, 'Yearly Payments', 'yearly_payments_b', '', '' ,''),
    create_text_field(5, 'City', 'city_b', '', '' ,''),
    create_text_field(6, 'State', 'state_b', '', '' ,''),
    create_text_field(7, 'Type Of Property', 'type_of_property_b', '', '' ,''),
    create_text_field(8, 'Income', 'income_b', '$', '' ,''),
    create_text_field(9, 'Tax Filing Status', 'tax_filing_status_b', '', '' ,''),
  ]);
  const [values_c, set_values_c] = React.useState([
    create_text_field(0, 'Purchase Price', 'purchase_price_c', '$', '' ,''),
    create_text_field(1, 'Down Payment', 'down_payment_c', '$', '' ,''),
    create_text_field(2, 'Interest Rate', 'interest_rate_c', '%', '' ,''),
    create_text_field(3, 'Loan Duration', 'loan_duration_c', '', 'Years' ,''),
    create_text_field(4, 'Yearly Payments', 'yearly_payments_c', '', '' ,''),
    create_text_field(5, 'City', 'city_c', '', '' ,''),
    create_text_field(6, 'State', 'state_c', '', '' ,''),
    create_text_field(7, 'Type Of Property', 'type_of_property_c', '', '' ,''),
    create_text_field(8, 'Income', 'income_c', '$', '' ,''),
    create_text_field(9, 'Tax Filing Status', 'tax_filing_status_c', '', '' ,''),
  ]);
  // Handle change for TextFields A, B, and C
  const handle_change_a = prop => event => {
    var check_var
    values_a[prop]['value'] = event.target.value
    // Make sure our numerical values are not less than zero and they're not strings
    if (prop === 0 || prop === 1 || prop === 2 || prop === 3 || prop === 4 || prop === 8) {
      check_var = values_a[prop]['value']
      if ((parseFloat(check_var) < 0 || isNaN(parseFloat(check_var))) && check_var !== '') {
        values_a[prop]['error_value'] = true
      }
      else {
        values_a[prop]['error_value'] = false
      }
    }
    set_values_a([...values_a])
  };

  const handle_change_b = prop => event => {
    var check_var
    values_b[prop]['value'] = event.target.value
    // Make sure our numerical values are not less than zero and they're not strings
    if (prop === 0 || prop === 1 || prop === 2 || prop === 3 || prop === 4 || prop === 8) {
      check_var = values_b[prop]['value']
      if ((parseFloat(check_var) < 0 || isNaN(parseFloat(check_var))) && check_var !== '') {
        values_b[prop]['error_value'] = true
      }
      else {
        values_b[prop]['error_value'] = false
      }
    }
    set_values_b([...values_b])
  };

  const handle_change_c = prop => event => {
    var check_var
    values_c[prop]['value'] = event.target.value
    // Make sure our numerical values are not less than zero and they're not strings
    if (prop === 0 || prop === 1 || prop === 2 || prop === 3 || prop === 4 || prop === 8) {
      check_var = values_c[prop]['value']
      if ((parseFloat(check_var) < 0 || isNaN(parseFloat(check_var))) && check_var !== '') {
        values_c[prop]['error_value'] = true
      }
      else {
        values_c[prop]['error_value'] = false
      }
    }
    set_values_c([...values_c])
  };

  // For opening and closing each purchases TextFields panel
  const handle_change = (panel) => (event, isExpanded) => {
    set_expanded(isExpanded ? panel : false);
  };
  // For TableRows
  const [data_a, set_data_a] = React.useState([
      create_data(0, 'Principle', 0, 0, 0),
      create_data(1, 'Interest', 0, 0, 0),
      create_data(2, 'Private Mortgage Insurance', 0, 0, 0),
      create_data(3, 'Property Taxes', 0, 0, 0),
      create_data(4, 'Maintenance', 0, 0, 0),
      create_data(5, 'Recurring Expenses Total', 0, 0, 0),
      create_data(6, 'Closing Costs', 0, 0, 0),
      create_data(7, 'Non-Recurring Expenses Total', 0, 0, 0),
      create_data(8, 'Total', 0, 0, 0),
  ]),
    [data_b, set_data_b] = React.useState([
    create_data(0, 'Principle', 0, 0, 0),
    create_data(1, 'Interest', 0, 0, 0),
    create_data(2, 'Private Mortgage Insurance', 0, 0, 0),
    create_data(3, 'Property Taxes', 0, 0, 0),
    create_data(4, 'Maintenance', 0, 0, 0),
    create_data(5, 'Recurring Expenses Total', 0, 0, 0),
    create_data(6, 'Closing Costs', 0, 0, 0),
    create_data(7, 'Non-Recurring Expenses Total', 0, 0, 0),
    create_data(8, 'Total', 0, 0, 0),
  ]),
    [data_c, set_data_c] = React.useState([
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

  // For TablePagination
  const [page_a, set_page_a] = React.useState(0);
  const [rows_per_page_a, set_rows_per_page_a] = React.useState(6);
  const [page_b, set_page_b] = React.useState(0);
  const [rows_per_page_b, set_rows_per_page_b] = React.useState(6);
  const [page_c, set_page_c] = React.useState(0);
  const [rows_per_page_c, set_rows_per_page_c] = React.useState(6);
  const handle_change_page_a = (event, newPage) => {
      set_page_a(newPage);
  };
  const handle_change_rows_per_page_a = (event) => {
      set_rows_per_page_a(parseInt(event.target.value, 10));
      set_page_a(0);
  };
  const handle_change_page_b = (event, newPage) => {
    set_page_b(newPage);
};
const handle_change_rows_per_page_b = (event) => {
    set_rows_per_page_b(parseInt(event.target.value, 10));
    set_page_b(0);
};
const handle_change_page_c = (event, newPage) => {
  set_page_c(newPage);
};
const handle_change_rows_per_page_c = (event) => {
  set_rows_per_page_c(parseInt(event.target.value, 10));
  set_page_c(0);
};

  // For the submit button
  function handle_click(raw_data_arr) {
    var response_arr = handle_mult_input(raw_data_arr)
    console.log(response_arr)
    if (response_arr !== null) {
      // For the data_tables
      set_data_a(response_arr[0])
      set_data_b(response_arr[1])
      set_data_c(response_arr[2])
    }
  }

  const [order] = React.useState('asc');
  const [orderBy] = React.useState('id');

  return (
    <div className={classes.root}>
        <Fade>
          <div>
            <ExpansionPanel expanded={expanded === 'panel1'} onChange={handle_change('panel1')} style={{marginBottom: '1vmin'}}>
              <ExpansionPanelSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel1bh-content"
                id="panel1bh-header"
              >
                <Typography className={classes.heading}>Purchase A</Typography>
                <Typography className={classes.secondaryHeading}>
                </Typography>
              </ExpansionPanelSummary>
              <ExpansionPanelDetails>
                <div className={classes.root} id="1">
                  {values_a.map(value => (
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
                        onChange={handle_change_a(value.key)}
                        error={value.error_value}
                      />
                  ))}
                </div>
              </ExpansionPanelDetails>
            </ExpansionPanel>
            <ExpansionPanel expanded={expanded === 'panel2'} onChange={handle_change('panel2')} style={{marginBottom: '1vmin'}}>
              <ExpansionPanelSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel2bh-content"
                id="panel2bh-header"
              >
                <Typography className={classes.heading}>Purchase B</Typography>
              </ExpansionPanelSummary>
              <ExpansionPanelDetails>
                <div className={classes.root} id="2">
                  {values_b.map(value => (
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
                        onChange={handle_change_b(value.key)}
                        error={value.error_value}
                      />
                  ))}
                </div>
              </ExpansionPanelDetails>
            </ExpansionPanel>
            <ExpansionPanel expanded={expanded === 'panel3'} onChange={handle_change('panel3')} style={{marginBottom: '1vmin'}}>
              <ExpansionPanelSummary
                expandIcon={<ExpandMoreIcon />}
                aria-controls="panel3bh-content"
                id="panel3bh-header"
              >
                <Typography className={classes.heading}>Purchase C</Typography>
              </ExpansionPanelSummary>
              <ExpansionPanelDetails>
                <div className={classes.root} id="3">
                    {values_c.map(value => (
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
                          onChange={handle_change_c(value.key)}
                          error={value.error_value}
                        />
                    ))}
                  </div>
              </ExpansionPanelDetails>
            </ExpansionPanel>
          </div>
          <div style={{textAlign: 'center'}}>
          <Button 
                    size="large" variant="contained" color="primary" 
                    style={{marginBottom: '5.2vmin'}}
                    onClick={() => handle_click([values_a, values_b, values_c])}
            >
              Submit All
            </Button>
        </div>
            <div>
              <TableContainer component={Paper} className={classes.container}>
                <Table stickyHeader className={classes.table} aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Purchase 'A' Expenses</TableCell>
                      <TableCell align="right">Monthly&nbsp;($)</TableCell>
                      <TableCell align="right">Yearly&nbsp;($)</TableCell>
                      <TableCell align="right">Total&nbsp;($)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {stable_sort(data_a, get_comparator(order, orderBy))
                      .slice(page_a * rows_per_page_a, page_a * rows_per_page_a + rows_per_page_a)
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
                count={data_a.length}
                rowsPerPage={rows_per_page_a}
                page={page_a}
                onChangePage={handle_change_page_a}
                onChangeRowsPerPage={handle_change_rows_per_page_a}
              />
              </TableContainer>
            </div>
            <div>
              <TableContainer component={Paper} className={classes.container}>
                <Table stickyHeader className={classes.table} aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Purchase 'B' Expenses</TableCell>
                      <TableCell align="right">Monthly&nbsp;($)</TableCell>
                      <TableCell align="right">Yearly&nbsp;($)</TableCell>
                      <TableCell align="right">Total&nbsp;($)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {stable_sort(data_b, get_comparator(order, orderBy))
                      .slice(page_b * rows_per_page_b, page_b * rows_per_page_b + rows_per_page_b)
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
                count={data_b.length}
                rowsPerPage={rows_per_page_b}
                page={page_b}
                onChangePage={handle_change_page_b}
                onChangeRowsPerPage={handle_change_rows_per_page_b}
              />
              </TableContainer>
            </div>
            <div>
              <TableContainer component={Paper} className={classes.container}>
                <Table stickyHeader className={classes.table} aria-label="simple table">
                  <TableHead>
                    <TableRow>
                      <TableCell>Purchase 'C' Expenses</TableCell>
                      <TableCell align="right">Monthly&nbsp;($)</TableCell>
                      <TableCell align="right">Yearly&nbsp;($)</TableCell>
                      <TableCell align="right">Total&nbsp;($)</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                  {stable_sort(data_c, get_comparator(order, orderBy))
                      .slice(page_c * rows_per_page_c, page_c * rows_per_page_c + rows_per_page_c)
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
                count={data_c.length}
                rowsPerPage={rows_per_page_c}
                page={page_c}
                onChangePage={handle_change_page_c}
                onChangeRowsPerPage={handle_change_rows_per_page_c}
              />
              </TableContainer>
            </div>
        </Fade>
    </div>
  );
}