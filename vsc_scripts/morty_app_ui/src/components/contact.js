/**
 * @author Ryan McCann
 * @summary Contains code written for the contact page. Allows the user to type in their email, a message, and upload a picture to give us
 *          feedback and more importantly report bugs they find.
 * @bugs When the submit button is pressed, the site crashes
 * @file contact.js
 * @version 10/09/2020
 */
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Fade from 'react-reveal/Fade'
import './contact.css'

// Styles
const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center'
  },
  field: {
      textAlign: 'center',
      marginTop: '1vmin',
  },
}));
export default function LayoutTextFields() {
  const classes = useStyles();

  return (
    // <div className={classes.root}>
    //   <Fade>
        <form name="contact" method="POST" data-netlify="true" id="fcf-form-id" class="fcf-form-class"> 
          <p class="fcf-p">
            If you have questions, concerns, or find any issues, please contact us by leaving some contact information and a brief description below.
            Screenshots are most helpful!
          </p>
          <div class="fcf-form-group">
              <label for="Name" class="fcf-label">Name</label>
              <div class="fcf-input-group">
                  <input type="text" id="Name" name="name" class="fcf-form-control" required/>
              </div>
          </div>

          <div class="fcf-form-group">
              <label for="Email" class="fcf-label">Email Address</label>
              <div class="fcf-input-group">
                  <input type="email" id="Email" name="email" class="fcf-form-control" required/>
              </div>
          </div>

          <div class="fcf-form-group">
              <label for="Message" class="fcf-label">Message</label>
              <div class="fcf-input-group">
                  <textarea id="Message" name="message" class="fcf-form-control" rows="6" maxlength="3000" required></textarea>
              </div>
          </div>

          <div class="fcf-form-group">
                  <input type="file" name="file" id="File" class="fcf-file"/>
          </div>

          <div class="fcf-form-group">
              <button name="submit" type="submit" id="fcf-button" class="fcf-btn fcf-btn-primary fcf-btn-lg fcf-btn-block">SUBMIT</button>
          </div>
        </form>
    //   </Fade>
    // </div>
  );
}