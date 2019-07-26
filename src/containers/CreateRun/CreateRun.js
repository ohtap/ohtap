import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { Redirect } from 'react-router-dom';
import axios from 'axios';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  button: {
    margin: theme.spacing.unit,
  },
});

class CreateRun extends React.Component {
	constructor(props) {
		super(props);

		// Gets the current date and time
		var today = new Date();
		var dd = String(today.getDate()).padStart(2, '0');
		var mm = String(today.getMonth() + 1).padStart(2, '0');
		var yyyy = today.getFullYear();
		var hour = today.getHours();
		var min = today.getMinutes();
		if (min < 10) {
			min = "0" + min;
		}
		var sec = today.getSeconds();
		if (sec < 10) {
			sec = "0" + sec;
		}
		var currDate = mm + '/' + dd + '/' + yyyy;
		var currTime = hour + ':' + min + ":" + sec;

		this.state = {
			name: '',
			time: currDate + ' ' + currTime,
			isButtonDisabled: true,
			redirect: false,
		};

		this.handleNameChange = this.handleNameChange.bind(this);
		this.handleButtonChange = this.handleButtonChange.bind(this);
		this.renderRedirect = this.renderRedirect.bind(this);
	}

	// Updates the run name and disables/enables the next button depending on the content.
	handleNameChange(event) {
		this.setState({ name: event.target.value });
		this.setState({ isButtonDisabled: (!event.target.value) });
	};

	// Updates the data in the backend and redirects the page to the next step
	handleButtonChange(event) {
		axios.post('/set_run_name', {
			data: {name: this.state.name, time: this.state.time}
		})
		.then(function (res) {
			console.log("Successfully posted name and time of the run");
		})
		.catch(function (err) {
			console.log(err);
		});

		this.setState({ redirect: true });
	}

	renderRedirect = () => {
		if (this.state.redirect) {
			return <Redirect to='/create_run/select_collections' />
		}
	}

	render() {
		const { classes } = this.props;

		return (
			<div>
				<Typography variant='h4'>
					Name your run
				</Typography>
				<br />
				<Typography paragraph>
					Give this run a name.
				</Typography>
				<form className={classes.container} noValidate autoComplete="off">
			        <TextField
			          id="standard-name"
			          label="Name"
			          value={this.state.name}
			          className={classes.textField}
			          onChange={this.handleNameChange}
			          margin="normal"
			        />

			        <TextField
			          disabled
			          id="standard-disabled"
			          label="Date"
			          defaultValue={this.state.time}
			          className={classes.textField}
			          margin="normal"
			        />
			    </form>
			    <Button variant="contained" onClick={(e) => {e.preventDefault(); this.handleButtonChange();}} color="primary" disabled={this.state.isButtonDisabled} className={classes.button}>
			    	Next
			    </Button>
			    {this.renderRedirect()}
			</div>
		);
	}
}

CreateRun.propTypes = {
	classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CreateRun);
