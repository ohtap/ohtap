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
import { Redirect } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
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
      runs: {},
      rows: [],
      redirect: false,
      deleteOpen: false,
      currRowId: null,
    };

    this.goToReport = this.goToReport.bind(this);
    this.askDeleteRow = this.askDeleteRow.bind(this);
    this.handleDeleteRowClose = this.handleDeleteRowClose.bind(this);
    this.deleteRow = this.deleteRow.bind(this);
  }

  // Gets our data once the component mounts
  componentDidMount() {
  	axios.get('/get_past_runs')
  		.then(res => this.setState({ runs: res.data }))
  		.then(data => this.updateTable())
  		.catch(err => console.log("Error getting runs (" + err + ")"));
  }

  // Handles closing the "Delete Row" dialog
  handleDeleteRowClose() {
    this.setState({ deleteOpen: false, currRowId: null });
  }

  // Opens a modal to check if the user really wants to delete the row.
  askDeleteRow(id) {
    this.setState({ deleteOpen: true, currRowId: id });
  }

  // Deletes the current row
  deleteRow() {
    axios.post('/delete_past_run', {
      id: this.state.currRowId
    })
    .then(res => {
      axios.get('/get_past_runs')
        .then(res => this.setState({ runs: res.data }))
        .then(data => this.updateTable())
        .catch(err => console.log("Error getting runs (" + err + ")"));
    })
    .catch(function (err) {
      console.log(err);
    });

    this.handleDeleteRowClose();
  }

  // Goes to the report for the ID
  goToReport(id) {
  	axios.post('/update_clicked_report', {
      data: id
    })
    .then(function (res) {
      console.log("Successfully posted after run");
    })
    .catch(function (err) {
      console.log(err);
    });

  	this.setState({ redirect: true });
  }

  // Redirects the page to the next page
  renderRedirect = () => {
    if (this.state.redirect) {
      return <Redirect to='/report' />
    }
  }

  // Updates the front-end selection with our past run information
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
                <CustomTableCell>Report</CustomTableCell>
                <CustomTableCell>Delete</CustomTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.rows.map(row => (
                <TableRow className={classes.row} key={row.id}>
                  <CustomTableCell component="th" scope="row">
                    {row.name}
                  </CustomTableCell>
                  <CustomTableCell>{row.date_ran}</CustomTableCell>
                  <CustomTableCell><Link component={RouterLink} onClick={() => this.goToReport(row.id)}>{row.link}</Link></CustomTableCell>
                  <CustomTableCell>
                    <IconButton onClick={() => this.askDeleteRow(row.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </CustomTableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
        {this.renderRedirect()}
        <Dialog
          open={this.state.deleteOpen}
          onClose={this.handleDeleteRowClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Are you sure you want to delete this run?"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              Deleting the run cannot be undone.
            </DialogContentText>
          </DialogContent>
          <DialogActions>
            <Button onClick={this.handleDeleteRowClose} color="primary">
              Cancel
            </Button>
            <Button onClick={this.deleteRow} color="primary" autoFocus>
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </div>
    );
  }
}

PastRuns.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(PastRuns);
