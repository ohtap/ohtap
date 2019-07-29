import React from 'react';
import LinearProgress from '@material-ui/core/LinearProgress';
import Typography from '@material-ui/core/Typography';
import axios from 'axios';

class Loading extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			completed: 0,
	    	statusMessage: 'Starting the subcorpora run...',
	    	statusTitle: 'Running...',
		};
	}

	componentDidMount() {
		this.timer = setInterval(this.progress, 500);
	}

	componentWillUnmount() {
		clearInterval(this.timer);
	}

	// Gets the progress of the python process
	progress = () => {
	    const { completed } = this.state;
	    console.log(completed);
	    if (completed === 100) {
	      this.setState({ summary: true, statusTitle: 'Done!', statusMessage: 'Finished running!' });
	      this.props.callbackDone(true); // Tells the parent Report component that we're done loading
	    } else {
	      axios.get('/get_python_progress')
	        .then(res => this.setState({completed: res.data.total, statusMessage: res.data.message}))
	        .catch(err => console.log("Error getting progress (" + err + ")"));
	    }
	};

	render() {
  	return (
  		<div>
	  		<Typography variant='h4'>
	        {this.state.statusTitle}
	      </Typography>
	      <br />
	      <LinearProgress variant="determinate" value={this.state.completed} />
	      <br />
	      <Typography paragraph>
	        <em>{this.state.statusMessage}</em>
	      </Typography>
      </div>
     );
	}
}

export default Loading;