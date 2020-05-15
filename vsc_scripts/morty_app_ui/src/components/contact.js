import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { TextField, Button, Typography } from '@material-ui/core'
import Fade from 'react-reveal/Fade'

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
            <form action="POST" data-netlify="true" name="contact">
                <div className={classes.textField}>
                    <TextField
                        id="standard-full-width"
                        label="Email"
                        name="Email"
                        style={{ width: '100vmin' }}
                        placeholder="name@example.com"
                        margin="normal"
                        InputLabelProps={{
                            shrink: true,
                    }}
                    variant="filled"
                    />
                    <TextField
                        id="standard-multiline-static"
                        label="Message"
                        name="Message"
                        multiline
                        rows={5}
                        defaultValue="Begin your message here."
                        variant="filled"
                        style={{ width: '100vmin' }}
                    />
                </div>
                <div class={classes.field}>
                    <input type="file" placeholder='Upload File'>
                    </input>
                </div>
                <div class={classes.field}>
                    <div data-netlify-recaptcha="true"></div>
                </div>
                <div style={{textAlign: "center", marginTop: '1.5vmin'}}>
                    <Button type="submit" size="large" variant="contained" color="primary">
                        Submit
                    </Button>
                </div>
            </form>
        </Fade>
    </div>
  );
}