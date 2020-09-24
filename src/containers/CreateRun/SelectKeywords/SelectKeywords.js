import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Typography from '@material-ui/core/Typography';
import Select from '@material-ui/core/Select';
import Chip from '@material-ui/core/Chip';
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

const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

function getStyles(name, that) {
  return {
    fontWeight:
      that.state.selected.indexOf(name) === -1
        ? that.props.theme.typography.fontWeightRegular
        : that.props.theme.typography.fontWeightMedium,
  };
}

class SelectKeywords extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      keywords: [],
      selected: [],
      isButtonDisabled: true,
      redirect: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleChangeMultiple = this.handleChangeMultiple.bind(this);
    this.updateSelection = this.updateSelection.bind(this);
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.renderRedirect = this.renderRedirect.bind(this);
  }

  // Get our data once the component mounts
  componentDidMount() {
    axios.get('/get_keywords')
      .then(res => this.setState({keywords: res.data}) )
      .then(data => this.updateSelection())
      .catch(err => console.log("Error getting keyword lists (" + err + ")"));
  }

  updateSelection() {
    const keywords = this.state.keywords;
    var menuBody = [];
    for (var k in keywords) {
      const item = keywords[k];
      console.log("keyword changed to (" + k + ")")
      const name = item['name'] + '-' + item['version'];
      menuBody.push(<MenuItem key={name} value={name} style={getStyles(name, this)}>{name}</MenuItem>);
    }

    this.setState({ menuBody: menuBody });
  }
  
  handleChange = event => {
    this.setState({ selected: event.target.value });
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
      selected: value,
    });

    this.setState({ isButtonDisabled: false });
  };

  handleButtonClick = () => {
    axios.post('/choose_keywords', {
      data: this.state.selected
    })
    .then(function (res) {
      console.log("Successfully posted keywords");
    })
    .catch(function (err) {
      console.log(err);
    });

    this.setState({ redirect: true });
  }


  renderRedirect = () => {
		if (this.state.redirect) {
			return <Redirect to='/create_run/select_metadata' />
		}
	}

  render() {
    const { classes } = this.props;

    return (
      <div>
      	<Typography variant='h4'>
      		Select keyword lists <br />
      	</Typography>
      	<br />
      	<Typography paragraph>
      		Select the keyword lists that you want to include in your run.
      	</Typography>
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="select-multiple-chip">Selected</InputLabel>
          <Select
            multiple
            value={this.state.selected}
            onChange={this.handleChange}
            input={<Input id="select-multiple-chip" />}
            renderValue={selected => (
              <div className={classes.chips}>
                {selected.map(value => (
                  <Chip key={value} label={value} className={classes.chip} />
                ))}
              </div>
            )}
            MenuProps={MenuProps}
          >
            {this.state.menuBody}
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
