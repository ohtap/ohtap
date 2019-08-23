import React from 'react';
import loadable from '@loadable/component';
import CircularProgress from '@material-ui/core/CircularProgress';
import axios from 'axios';

const Navigation = loadable(() => import('../Navigation'));
const SummaryReport = loadable(() => import('../SummaryReport'));
const IndividualReport = loadable(() => import('../IndividualReport'));

class PastRunsReport extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			loading: true,
			summary: true,
			collection: '',
			keywordList: '',
			data: {},
		};
	}

	// Callback from child Loading component when done loading
	componentDidMount() {
		axios.get('/get_current_run_data')
			.then(res => this.setState({ data: res.data }))
			.then(data => this.setState({ loading: false }))
			.catch(err => console.log("Error getting current run data (" + err + ")"));	
	};

	changeNavigation = (summary, collection, keywordList) => {
		this.setState({ summary: summary, collection: collection, keywordList: keywordList });
	};

	renderNavigation = () => {
		if (!this.state.loading) {
			return (<Navigation parentData={this.state.data} callbackChangeNavigation={this.changeNavigation} />);
		}
	}

	renderReport = () => {
		if (this.state.loading) {
			return (<CircularProgress />);
		}
		if (this.state.summary) {
			return (<SummaryReport parentData={this.state.data} />);
		}

		return (<IndividualReport parentData={this.state} />);
	}

	render() {
		return (
			<div>
				{this.renderNavigation()}
				<br />
				{this.renderReport()}
			</div>
		);
	}
}

export default PastRunsReport;
