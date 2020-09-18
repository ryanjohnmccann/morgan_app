/**
 * @author Ryan McCann
 * @summary Contains code written for the contact page. Allows the user to type in their email, a message, and upload a picture to give us
 *          feedbac and report bugs they find.
 * @bugs When the submit button is pressed, the site crashes
 * @file contact.js
 * @version 09/11/2020
 */
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { TextField, Button, Typography } from '@material-ui/core'
import Fade from 'react-reveal/Fade'

// Styles
const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center'
  },
  textField: {
    textAlign: 'center',
  },
  field: {
      textAlign: 'center',
      marginTop: '1vmin',
  },
}));
export default function LayoutTextFields() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
        <Fade>
            <Typography align="center" style={{width: '60vmin'}}>
                If you have questions, concerns, or find any issues with the app, please contact us 
                by leaving some contact information and a brief description below. Pictures are most helpful!
            </Typography>     
            <form action="POST" data-netlify="true" name="contact" className={classes.root} autoComplete="off">
            <p>
                <label>Your Name: <input type="text" name="name" /></label>   
            </p>
            <p>
                <label>Your Email: <input type="email" name="email" /></label>
            </p>
            <p>
                <label>Message: <textarea name="message"></textarea></label>
            </p>
            <p>
                <input type="file"/>
            </p>
            <p>
                <button type="submit">Send</button>
            </p>
            </form>
        </Fade>
    </div>
  );
}