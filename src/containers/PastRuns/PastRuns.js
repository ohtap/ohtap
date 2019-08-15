import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import { Link as RouterLink } from 'react-router-dom';
import Link from '@material-ui/core/Link';
import AssessmentRoundedIcon from '@material-ui/icons/AssessmentRounded';
import axios from 'axios';

const CustomTableCell = withStyles(theme => ({
  head: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  body: {
    fontSize: 14,
  },
}))(TableCell);

const styles = theme => ({
  root: {
    width: '100%',
    marginTop: theme.spacing.unit * 3,
    overflowX: 'auto',
  },
  table: {
    minWidth: 700,
  },
  row: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.background.default,
    },
  },
});

function createData(id, name, date_ran, link) {
  return { id, name, date_ran, link };

}

class PastRuns extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      keywords: [],
      rows: [
        { 
          id: '', 
          name: '', 
          date_ran: '', 
          link: ''
        }
      ],
    };

    // this.updateTable = this.updateTable.bind(this);
  }

  // TODO: Fix data retrieval and add data retrieval in backend
  // Gets our data once the component mounts
  componentDidMount() {
  	axios.get('/get_past_runs')
  		.then(res => this.setState({runs: res.data}))
  		.then(data => this.updateTable())
  		.catch(err => console.log("Error getting runs (" + err + ")"));
  }

  // Updates the front-end selection with our current keyword information
  updateTable() {
    var rows = [];
    for (var id in this.state.runs) {
      var v = this.state.runs[id];
      var name = v["name"];
      var date = v["date"];
      var link = v["name"] + "-report";
      var data = createData(id, name, date, link);
      rows.push(data);
    }
    this.setState({ rows: rows });
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Typography variant="h4">
          Past Runs
        </Typography>
        <Typography paragraph>
          Access old runs.
        </Typography>
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <CustomTableCell>Run Name</CustomTableCell>
                <CustomTableCell>Date of Run</CustomTableCell>
                <CustomTableCell>Reports</CustomTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.rows.map(row => (
                <TableRow className={classes.row} key={row.id}>
                  <CustomTableCell component="th" scope="row">
                    {row.name}
                  </CustomTableCell>
                  <CustomTableCell>{row.date_ran}</CustomTableCell>
                  <CustomTableCell><Link component={RouterLink} to="/report">{row.link}</Link></CustomTableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      </div>
    );
  }
}

PastRuns.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(PastRuns);
