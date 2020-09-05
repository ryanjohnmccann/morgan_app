import React from 'react';
import PropTypes from 'prop-types';
import { AppBar, Tabs, Tab, Typography, Box } from '@material-ui/core'
import { makeStyles } from '@material-ui/core/styles';
import Home from './components/home.js';
import Compare from './components/compare.js'
import Contact from './components/contact.js'

// Random comment, bleep bloop
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <Typography
      component="div"
      role="tabpanel"
      hidden={value !== index}
      id={`nav-tabpanel-${index}`}
      aria-labelledby={`nav-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </Typography>
  );
}

TabPanel.propTypes = {
  children: PropTypes.node,
  index: PropTypes.any.isRequired,
  value: PropTypes.any.isRequired,
};

function a11yProps(index) {
  return {
    id: `nav-tab-${index}`,
    'aria-controls': `nav-tabpanel-${index}`,
  };
}

function LinkTab(props) {
  return (
    <Tab
      component="a"
      onClick={event => {
        event.preventDefault();
      }}
      {...props}
    />
  );
}

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    backgroundColor: theme.palette.background.paper,
  },
}));

function Main() {

  const classes = useStyles();
  const [value, setValue] = React.useState(0);

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return(
    <div className={classes.root}>
      <AppBar position="static">
        <Tabs
          variant="fullWidth"
          value={value}
          onChange={handleChange}
          aria-label="nav tabs example"
        >
          <LinkTab label="Home" href="/home" {...a11yProps(0)} />
          <LinkTab label="Compare" href="/compare" {...a11yProps(1)} />
          <LinkTab label="Contact" href="/contact" {...a11yProps(2)} />
        </Tabs>
      </AppBar>
    {/* Home tab */}
    <TabPanel value={value} index={0}>
      <Home/>
    </TabPanel>
    {/* Compare tab */}
    <TabPanel value={value} index={1}>
      <Compare/>
    </TabPanel>
    {/* Contact tab */}
    <TabPanel value={value} index={2}>
      <Contact/>
    </TabPanel>
  </div>
  )
}

export default Main;
