import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Typography from '@material-ui/core/Typography';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';
import { Redirect } from 'react-router-dom';
import axios from 'axios';

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
    maxWidth: 300,
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: theme.spacing.unit / 4,
  },
  noLabel: {
    marginTop: theme.spacing.unit * 3,
  },
  button: {
    margin: theme.spacing.unit,
  },
  input: {
    display: 'none',
  },
});

const names = [
  'metadata.csv',
];

function getStyles(name, that) {
  return {
    fontWeight:
      that.state.name.indexOf(name) === -1
        ? that.props.theme.typography.fontWeightRegular
        : that.props.theme.typography.fontWeightMedium,
  };
}

class SelectKeywords extends React.Component {
  state = {
    name: '',
    isButtonDisabled: true,
    redirect: false,
  };

  handleChange = event => {
    this.setState({ name: event.target.value });
    this.setState({ isButtonDisabled: false });
  };

  handleChangeMultiple = event => {
    const { options } = event.target;
    const value = [];
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        value.push(options[i].value);
      }
    }
    this.setState({
      name: value,
    });

    this.setState({ isButtonDisabled: false });
  };

  handleButtonClick = () => {
    axios.post('/run_python_script', {
      data: this.state.name
    })
    .then(function (res) {
      console.log("Successfully posted metadata");
    })
    .catch(function (err) {
      console.log(err);
    });

  	this.setState({ redirect: true });
  }

  renderRedirect = () => {
		if (this.state.redirect) {
			return <Redirect to='/report' />
		}
	}

  render() {
    const { classes } = this.props;

    return (
      <div>
      	<Typography variant='h4'>
      		Select metadata <br />
      	</Typography>
      	<br />
      	<Typography paragraph>
      		Select the metadata for your collection data. Ensure that your metadata contains all the information for your collection.
      	</Typography>
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="select-multiple-chip">Selected</InputLabel>
          <Select
            value={this.state.name}
            onChange={this.handleChange}
            inputProps={{
              name: 'metadata',
              id: 'metadata',
            }}
          >
            {names.map(name => (
              <MenuItem key={name} value={name} style={getStyles(name, this)}>
                {name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <br />
        <Button variant="contained" onClick={(e) => {e.preventDefault(); this.handleButtonClick();}} color="primary" disabled={this.state.isButtonDisabled} className={classes.button}>
	        Next
	    </Button>
	    {this.renderRedirect()}
      </div>
    );
  }
}

SelectKeywords.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(SelectKeywords);
