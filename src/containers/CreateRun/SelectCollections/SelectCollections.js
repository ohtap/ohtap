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
    maxWidth: 500,
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

class SelectCollections extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      collections: [],
      selected: [],
      selectedIds: [],
      idsOrder: [],
      isButtonDisabled: true,
      redirect: false,
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleChangeMultiple = this.handleChangeMultiple.bind(this);
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.updateSelection = this.updateSelection.bind(this);
    this.renderRedirect = this.renderRedirect.bind(this);
  }

  // Get our data once the component mounts
  componentDidMount() {
    axios.get('/get_collections')
      .then(res => this.setState({collections: res.data}) )
      .then(data => this.updateSelection())
      .catch(err => console.log("Error getting collections (" + err + ")"));
  }

  // Updates the front-end selection with our current selectable collections
  updateSelection() {
    const collections = this.state.collections;
    var menuBody = [];
    var idsOrder = [];
    for (var k in collections) {
      const item = collections[k];
      const name = item['shortened-name'];
      const _id = item['id'];
      idsOrder.push(_id);
      menuBody.push(<MenuItem key={_id} value={_id} style={getStyles(name, this)}>{name}</MenuItem>);
    }

    this.setState({ menuBody: menuBody, idsOrder: idsOrder });
  }
  

  /* Functions to handle change of the selector */

  handleChange = event => {
    this.setState({ selected: event.target.value });
    this.setState({ isButtonDisabled: false });
  };

  handleChangeMultiple = event => {
    const { options } = event.target;
    const value = [];
    const valueIds = [];
    for (let i = 0, l = options.length; i < l; i += 1) {
      if (options[i].selected) {
        value.push(options[i].value);
        valueIds.push(this.state.idsOrder[i]);
      }
    }

    this.setState({
      selected: value,
      selectedIds: valueIds,
    });

    this.setState({ isButtonDisabled: false });
  };

  // Updates the data in the backend and redirects the page to the next step
  handleButtonClick = () => {
    axios.post('/choose_collections', {
      data: this.state.selected
    })
    .then(function (res) {
      console.log("Successfully posted collections");
    })
    .catch(function (err) {
      console.log(err);
    });

    this.setState({ redirect: true });
  }


  // Redirects the page to the next page
  renderRedirect = () => {
    if (this.state.redirect) {
      return <Redirect to='/create_run/select_keywords' />
    }
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Typography variant='h4'>
          Select collections <br />
        </Typography>
        <br />
        <Typography paragraph>
          Choose the collections to include in your run.
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

SelectCollections.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(SelectCollections);
