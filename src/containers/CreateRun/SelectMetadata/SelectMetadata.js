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
import LinearProgress from '@material-ui/core/LinearProgress';
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

function getStyles(name, that) {
  return {
    fontWeight:
      that.state.name.indexOf(name) === -1
        ? that.props.theme.typography.fontWeightRegular
        : that.props.theme.typography.fontWeightMedium,
  };
}

class SelectKeywords extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      name: '',
      isButtonDisabled: true,
      redirect: false,
      selectedFile: null,
      progress: 0,
      metadataFiles: [],
    };

    this.onChangeUpload = this.onChangeUpload.bind(this);
    this.uploadMetadata = this.uploadMetadata.bind(this);
  }

  // Gets our data once the component mounts
  componentDidMount() {
    axios.get("/get_metadata_files")
      .then(res => this.setState({ metadataFiles: res.data }))
      .catch(err => console.log("Error getting metadata files (" + err + ")"));
  }

  // Uploads the metadata file
  uploadMetadata() {
    var data = new FormData();
    data.append('file', this.state.selectedFile);
    const config = {
      onUploadProgress: progressEvent => this.setState({ progress: progressEvent.loaded })
    };

    axios.post("/upload_metadata", data, config)
      .then((res) => {
        axios.get("/get_metadata_files")
          .then(res => this.setState({ metadataFiles: res.data, isButtonDisabled: false }))
          .catch(err => console.log("Error getting metadata files (" + err + ")"));
      })
      .catch(function(err) {
        console.log(err);
      });
  }

  handleChange = event => {
    this.setState({ name: event.target.value, isButtonDisabled: false });
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
    axios.post('/choose_metadata', {
      data: this.state.name
    })
    .then(function (res) {
      console.log("Successfully got first metadata file");
    })
    .catch(function (err) {
      console.log(err);
    });
    this.setState({ redirect: true });
  }

  onChangeUpload(e) {
    this.setState({ selectedFile: e.target.files[0], progress: 0 });
  }

  renderRedirect = () => {
    if (this.state.redirect) {
      return <Redirect to='/create_run/select_metadata_second_sheet' />
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
      		Select the interview metadata for your collection data. Ensure that your metadata contains all the information for your collection.
      	</Typography>
        <FormControl className={classes.formControl}>
          <InputLabel htmlFor="select-multiple-chip">Selected</InputLabel>
          <Select
            value={this.state.name}
            onChange={this.handleChange}
            inputProps={{
              name: 'interviews',
              id: 'interviews',
            }}
          >
            {this.state.metadataFiles.map(name => (
              <MenuItem key={name} value={name} style={getStyles(name, this)}>
                {name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <br />
        <Typography paragraph>Upload a new metadata file.</Typography>
        <br />
        <input
          id="raised-button-file"
          type="file"
          name="file"
          onChange={this.onChangeUpload}
        />
        <Button onClick={this.uploadMetadata} color="primary">
          Upload
        </Button>
        <LinearProgress variant="determinate" value={this.state.progress} />
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
