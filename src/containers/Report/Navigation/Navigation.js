import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';

const styles = theme => ({
	root: {
		display: 'flex',
		flexWrap: 'wrap',
	},
	formControl: {
    margin: theme.spacing.unit,
    minWidth: 120,
  },
  button: {
    margin: theme.spacing.unit,
  },
  selectEmpty: {
    marginTop: theme.spacing.unit * 2,
  },
});

class Navigation extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			data: this.props.parentData, // Passed from the parent report
			collectionMenuItems: [],
			keywordListMenuItems: [],
			summary: true,
			type: "Summary",
			collection: '',
			keywordList: '',
		};

		this.handleClick = this.handleClick.bind(this);
		this.updateCollectionMenuItems = this.updateCollectionMenuItems.bind(this);
		this.updateKeywordListMenuItems = this.updateKeywordListMenuItems.bind(this);
	}

	componentWillMount() {
		this.updateCollectionMenuItems();
		this.updateKeywordListMenuItems();
	}

	handleChange = event => {
    this.setState({ [event.target.name]: event.target.value });

    if (event.target.name === "type") {
    	if (event.target.value === "Summary") {
    		this.setState({ summary: true, collection: '', keywordList: '' });
    	} else {
    		this.setState({ summary: false });
    	}
    }
  };

	  handleClick() {	
	  	const { summary, collection, keywordList } = this.state;	
	  	if ((!summary && collection != '' && keywordList !='') || summary){	
	  		this.props.callbackChangeNavigation(summary, collection, keywordList);	
	  	}	
	  }

  updateCollectionMenuItems() {
  	const collections = this.state.data['collections'];

  	var options = [];
  	for (var i in collections) {
  		const c = collections[i];
  		options.push(<MenuItem value={c}>{c}</MenuItem>);
  	}

  	this.setState({ collectionMenuItems: options });
  }

  updateKeywordListMenuItems() {
  	const keywordLists = this.state.data['keyword-lists'];

  	var options = [];
  	for (var i in keywordLists) {
  		const k = keywordLists[i];
  		options.push(<MenuItem value={k}>{k}</MenuItem>);
  	}

  	this.setState({ keywordListMenuItems: options });
  }

	render() {
		const { classes } = this.props;

		return (
			<div>
				<Typography variant='h6'>
					Report Navigation
				</Typography>
				<div className={classes.root}>
					<form autocomplete="off">
						<FormControl className={classes.formControl}>
		          <InputLabel shrink htmlFor="type-label-placeholder">
		            Type
		          </InputLabel>
		          <Select
		            value={this.state.type}
		            onChange={this.handleChange}
		            input={<Input name="type" id="type-label-placeholder" />}
		            displayEmpty
		            name="type"
		            className={classes.selectEmpty}
		          >
		            <MenuItem value="Summary">Summary</MenuItem>
		            <MenuItem value="Individual">Individual</MenuItem>
		          </Select>
	          </FormControl>

	          <FormControl className={classes.formControl} disabled={this.state.summary}>
	          	<InputLabel shrink htmlFor="collection-label-placeholder">
	          		Collection
	          	</InputLabel>
	          	<Select
		            value={this.state.collection}
		            onChange={this.handleChange}
		            input={<Input name="type" id="collection-label-placeholder" />}
		            displayEmpty
		            name="collection"
		            className={classes.selectEmpty}
		          >
		          	{this.state.collectionMenuItems}
		          </Select>
	          </FormControl>

	          <FormControl className={classes.formControl} disabled={this.state.summary}>
	          	<InputLabel shrink htmlFor="keywordList-label-placeholder">
	          		Keyword List
	          	</InputLabel>
	          	<Select
		            value={this.state.keywordList}
		            onChange={this.handleChange}
		            input={<Input name="type" id="keywordList-label-placeholder" />}
		            displayEmpty
		            name="keywordList"
		            className={classes.selectEmpty}
		          >
		          	{this.state.keywordListMenuItems}
		          </Select>
	          </FormControl>
					</form>
				</div>
				<div>
					<Button onClick={this.handleClick} variant="contained" color="primary" className={classes.button}>
		        VIEW
		      </Button>
		     </div>
			</div>
		);
	}
}

Navigation.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(Navigation);
