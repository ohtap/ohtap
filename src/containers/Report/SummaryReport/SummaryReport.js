import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import Chip from '@material-ui/core/Chip';
import Input from '@material-ui/core/Input';
import {Line, Bar, Doughnut} from 'react-chartjs-2';

const styles = theme => ({
	root: {

	},
	chart: {
    paddingRight: '20px',
  },
  title: {
    whiteSpace: 'pre',
  },
	paper: {
		...theme.mixins.gutters(),
    paddingTop: theme.spacing.unit * 2,
    paddingBottom: theme.spacing.unit * 2,
	},
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  chip: {
    margin: theme.spacing.unit / 4,
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

const format = () => tick => tick;

// Helper function to sort an map; returns an array of key-value pairs, sorted
function sortMap(map) {
  var keyValues = [];

  for (var key in map) {
    keyValues.push([ key, map[key] ]);
  }

  keyValues.sort();

  return keyValues;
}

// Creates a dataset for a line graph
function createLineDataset(label, values) {
  var dataset = {
    label: label,
    fill: false,
    type: 'line',
    lineTension: 0.1,
    backgroundColor: 'rgba(75,192,192,0.4)',
    borderColor: 'rgba(75,192,192,1)',
    borderCapStyle: 'butt',
    borderDash: [],
    borderDashOffset: 0.0,
    borderJoinStyle: 'miter',
    pointBorderColor: 'rgba(75,192,192,1)',
    pointBackgroundColor: '#fff',
    pointBorderWidth: 1,
    pointHoverRadius: 5,
    pointHoverBackgroundColor: 'rgba(75,192,192,1)',
    pointHoverBorderColor: 'rgba(220,220,220,1)',
    pointHoverBorderWidth: 2,
    pointRadius: 1,
    pointHitRadius: 10,
    data: values
  };

  return dataset;
}

// Creates a dataset for a bar graph
function createBarDataset(label, values) {
  var dataset = {
    data: values,
    label: label,
    backgroundColor: 'rgba(255,99,132,0.2)',
    borderColor: 'rgba(255,99,132,1)',
    borderWidth: 1,
    hoverBackgroundColor: 'rgba(255,99,132,0.4)',
    hoverBorderColor: 'rgba(255,99,132,1)',
  };

  return dataset;
}

// Creates a dataset for the doughnut graph
function createDoughnutDataset(values) {
  var dataset = {
    data: values,
    backgroundColor: [
    '#FF6384',
    '#36A2EB',
    '#FFCE56'
    ],
    hoverBackgroundColor: [
    '#FF6384',
    '#36A2EB',
    '#FFCE56'
    ]
  };

  return dataset;
}

class SummaryReport extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      data: this.props.parentData, // Passed from the parent report

      timeRangeInterviewData: {},
      timeRangeBirthYearData: {},
      keywordCountsData: {},
      intervieweeRaceData: {},
      intervieweeSexData: {},
      keywordsOverTimeData: {},
      keywordsOverTimeSelections: [],
      keywordsOverTimeChosen: [],
    };

    // Helps with data validation in case data is formatted incorrectly
    if (!('summary-report' in this.state.data)) {
      console.log("ERROR: No summary report data");
      var data = this.state.data;
      data['summary-report'] = {};
      this.setState({ data: data });
    }
  }

  componentDidMount() {
    this.generateKeywordsOverTimeSelections();
    this.generateTimeRangeInterviewData();
    this.generateTimeRangeBirthYear();
    this.generateIntervieweeRaceData();
    this.generateIntervieweeSexData();
  }

  generateKeywordsOverTimeSelections = () => {
    var data = {};
    var newData = {
      'not-given': 0
    };

    if ('keywords-over-time' in this.state.data['summary-report']) {
      data = this.state.data['summary-report']['keywords-over-time'];
    }

    var selections = [];
    var allKeywords = [];
    selections.push((<MenuItem value=""><em></em></MenuItem>));
    for (var k in data) {
      var item = (
        <MenuItem value={ k }>{ k }</MenuItem>
      );
      selections.push(item);
      allKeywords.push(k);
    }

    this.setState({ keywordsOverTimeSelections: selections, keywordsOverTimeChosen: allKeywords }, () => {
      this.generateKeywordsOverTimeData();
    });
  }

  handleKeywordsOverTimeChange = event => {
    this.setState({ keywordsOverTimeChosen: event.target.value }, () => {
      this.generateKeywordsOverTimeData();
    });
  }

  // Generates data for the keywords over time
  generateKeywordsOverTimeData = () => {
    var data = {};
    var newData = {
      'not-given': 0
    };

    if ('keywords-over-time' in this.state.data['summary-report']) {
      data = this.state.data['summary-report']['keywords-over-time'];
    }

    var labels = [];
    var dataSets = [];
    var addLabels = true;

    var testDataSets = [];

    for (var i = 0; i < this.state.keywordsOverTimeChosen.length; i++) {
      var k = this.state.keywordsOverTimeChosen[i];
      console.log(k);
      if (k === "") {
        continue;
      }
      var v = data[k];
      var values = [];
      var sortedData = sortMap(v);

      for (var j = 0; j < sortedData.length; j++) {
        const kv = sortedData[j];
        const key = kv[0];
        const value = kv[1];

        if (key === 'Not given') {
          newData['not-given'] += value;
          continue;
        }

        if (addLabels) {
          labels.push(key);
        }
        values.push(value);
      }

      addLabels = false;
      dataSets.push(createLineDataset(k, values));
    }

    newData['graph-data'] = {
      labels: labels,
      datasets: dataSets
    };
    
    this.setState({ keywordsOverTimeData: newData });
  }

  // Generates data for the time range graph of interviews
  generateTimeRangeInterviewData = () => {
    var labels = [];
    var values = [];
    var data = {};
    var newData = {};

    if ('time-range-interviews' in this.state.data['summary-report']) {
      data = this.state.data['summary-report']['time-range-interviews'];
    }

    var sortedData = sortMap(data);

    for (var i = 0; i < sortedData.length; i++) {
      const kv = sortedData[i];
      const key = kv[0];
      const value = kv[1];

      if (key === 'Not given') {
        newData['not-given'] = value;
        continue;
      }

      labels.push(key);
      values.push(value);
    }

    var dataSets = [];
    dataSets.push(createLineDataset('Time Range of Interviews (by decade)', values));

    newData['graph-data'] = {
      labels: labels,
      datasets: dataSets
    };

    this.setState({ timeRangeInterviewData: newData });
  }

  // Generates data for the time range graph of birth years of interviewees
  generateTimeRangeBirthYear = () => {
    var labels = [];
    var values = [];
    var data = {};
    var newData = {};

    if ('time-range-birth-year' in this.state.data['summary-report']) {
      data = this.state.data['summary-report']['time-range-birth-year'];
    }

    var sortedData = sortMap(data);

    for (var i = 0; i < sortedData.length; i++) {
      const kv = sortedData[i];
      const key = kv[0];
      const value = kv[1];

      if (key === 'Not given') {
        newData['not-given'] = value;
        continue;
      }

      labels.push(key);
      values.push(value);
    }

    var dataSets = [];
    dataSets.push(createLineDataset('Time Range of Interviewee Birth Dates (by decade)', values));

    newData['graph-data'] = {
      labels: labels,
      datasets: dataSets
    };

    this.setState({ timeRangeBirthYearData: newData });
  }

  // Generates data for the circle chart for race of interviewees
  generateIntervieweeRaceData = () => {
    var labels = [];
    var values = [];
    var data = {};
    var newData = {};

    if ('race' in this.state.data['summary-report']) {
      data = this.state.data['summary-report']['race'];
    }

    for (var key in data) {
      const value = data[key];
      labels.push(key);
      values.push(value);
    }

    var dataSets = [];
    dataSets.push(createDoughnutDataset(values));

    newData['graph-data'] = {
      labels: labels,
      datasets: dataSets
    };

    this.setState({ intervieweeRaceData: newData });
  }

  // Generates data for the circle chart for the sex of interviewees
  generateIntervieweeSexData = () => {
    var labels = [];
    var values = [];
    var data = {};
    var newData = {};

    if ('sex' in this.state.data['summary-report']) {
      data = this.state.data['summary-report']['sex'];
    }

    for (var key in data) {
      const value = data[key];
      labels.push(key);
      values.push(value);
    }

    var dataSets = [];
    dataSets.push(createDoughnutDataset(values));

    newData['graph-data'] = {
      labels: labels,
      datasets: dataSets
    };

    this.setState({ intervieweeSexData: newData });
  }

  render() {
    const { classes } = this.props;
    const {
      timeRangeInterviewData: triData,
      timeRangeBirthYearData: trbyData,
      intervieweeRaceData: irData,
      intervieweeSexData: isData,
      keywordsOverTimeData: kotData,
      keywordsOverTimeSelections: kotSelections,
    } = this.state;
    const summaryData = this.state.data['summary-report'];

    return (
      <div className={classes.root}>
        <Paper className={classes.paper} elevation={1}>
          <Typography variant="h5" component="h3">
            Basic Information
          </Typography>
          <Typography component="p">
            <b>Total collections: </b>{ summaryData['total-collections'] }<br />
            <b>&#x00025; collections with keywords: </b>{ (summaryData['total-collections-with-keywords'] / summaryData['total-collections']) * 100 } &#x00025;<br />
            <b>Total interviews: </b>{ summaryData['total-interviews'] }<br />
            <b>&#x00025; interviews with keywords: </b>{ (summaryData['total-interviews-with-keywords'] / summaryData['total-interviews']) * 100 } &#x00025;<br />
            <b>Total keywords searched for: </b>{ summaryData['total-keywords'] }<br />
            <b>Total keywords found: </b>{ summaryData['total-keywords-found'] }<br />
          </Typography>
        </Paper>
        <br />
        <Paper className={classes.paper} elevation={1}>
          <Typography variant="h5" component="h3">
            Keyword Use Over Time
          </Typography>
          <br />
          <Select
            multiple
            value={ this.state.keywordsOverTimeChosen }
            onChange={ this.handleKeywordsOverTimeChange }
            input={<Input id="select-multiple-chip" />}
            renderValue={keywordsOverTimeChosen => (
              <div className={classes.chips}>
                {keywordsOverTimeChosen.map(value => (
                  <Chip key={value} label={value} className={classes.chip} />
                ))}
              </div>
            )}
            MenuProps={MenuProps}
          >
            { kotSelections }
          </Select>
          <Typography component="p">
            <b>Total keywords found with no labeled year: </b>{ kotData['not-given'] }
          </Typography>
          <br />
          <Bar data={kotData['graph-data']} legend={{
            display: false
          }} />
        </Paper>
        <br />
        <Paper className={classes.paper} elevation={1}>
          <Typography variant="h5" component="h3">
              Time Range of Interviews
          </Typography>
          <br />
          <Typography component="p">
            <b>Total interviews with no interview data given: </b>{ triData['not-given'] }
          </Typography>
          <br />
          <Bar data={ triData['graph-data'] } />
        </Paper>
        <Paper className={classes.paper} elevation={1}>
          <Typography variant="h5" component="h3">
              Time Range of Interviewee Birth Dates
            </Typography>
            <br />
            <Typography component="p">
              <b>Total interviewees with no birth date given: </b>{ trbyData['not-given'] }
            </Typography>
            <br />
            <Bar data={ trbyData['graph-data'] } />
        </Paper>
        <br />
        <Paper className={classes.paper} elevation={1}>
          <Typography variant="h5" component="h3">
            Race of Interviewees
          </Typography>
          <Doughnut data={ irData['graph-data'] } />
        </Paper>
        <br />
        <Paper className={classes.paper} elevation={1}>
          <Typography variant="h5" component="h3">
            Sex of Interviewees
          </Typography>
          <Doughnut data={ isData['graph-data'] } />
        </Paper>
      </div>
    );
  }
}

SummaryReport.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SummaryReport);
