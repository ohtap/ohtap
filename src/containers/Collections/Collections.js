import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
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

function createData(id, name, shortened_name, collection_count, description, themes, notes) {
  return { id, name, shortened_name, collection_count, description, themes, notes };
}

class Collections extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      collections: {},
      rows: [],
      deleteOpen: false,
      currRowId: null,
    }

    this.updateTable = this.updateTable.bind(this);

    this.editRow = this.editRow.bind(this);

    this.askDeleteRow = this.askDeleteRow.bind(this);
    this.handleDeleteRowClose = this.handleDeleteRowClose.bind(this);
    this.deleteRow = this.deleteRow.bind(this);
  }

  // Gets our data once the component mounts
  componentDidMount() {
    axios.get('/get_collections')
      .then(res => this.setState({ collections: res.data }))
      .then(data => this.updateTable())
      .catch(err => console.log("Error getting collections (" + err + ")"));
  }

  // Handles closing the "Delete Row" dialog
  handleDeleteRowClose() {
    this.setState({ deleteOpen: false, currRowId: null });
  }

  // Opens a modal to check if the user really wants to delete the row
  askDeleteRow(id) {
    this.setState({ deleteOpen: true, currRowId: id });
  }

  editRow(id) {
    console.log("Edit " + id);
  }

  // Deletes the current row
  deleteRow(id) {
    axios.post("/delete_collection", {
      id: this.state.currRowId
    })
    .then(res => {
      axios.get('/get_collections')
        .then(res => this.setState({ collections: res.data }))
        .then(data => this.updateTable())
        .catch(err => console.log("Error getting collections (" + err + ")"));
    })
    .catch(function (err) {
      console.log(err);
    });

    this.handleDeleteRowClose();
  }

  // Updates the front-end selection with our past run information
  updateTable() {
    var rows = [];
    for (var id in this.state.collections) {
      var v = this.state.collections[id];
      var name = v["name"];
      var shortened_name = v["shortened-name"];
      var collection_count = v["collection-count"];
      var description = v["description"];
      var themes = v["themes"];
      var notes = v["notes"];
      var data = createData(id, name, shortened_name, collection_count, description, themes, notes);
      rows.push(data);
    }

    this.setState({ rows: rows });
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Typography variant="h4">
          Collections
        </Typography>
        <Typography paragraph>
          Add, upload, edit, and delete collections. On this demo version, all editing functionality is not allowed.
        </Typography>
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <CustomTableCell>Collection ID</CustomTableCell>
                <CustomTableCell>Collection Name</CustomTableCell>
                <CustomTableCell>Collection Count</CustomTableCell>
                <CustomTableCell>Description</CustomTableCell>
                <CustomTableCell>Themes</CustomTableCell>
                <CustomTableCell>Notes</CustomTableCell>
                <CustomTableCell>Modify/Delete</CustomTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.rows.map(row => (
                <TableRow className={classes.row} key={row.id}>
                  <CustomTableCell component="th" scope="row">
                    {row.id}
                  </CustomTableCell>
                  <CustomTableCell>{row.name}</CustomTableCell>
                  <CustomTableCell>{row.collection_count}</CustomTableCell>
                  <CustomTableCell>{row.description}</CustomTableCell>
                  <CustomTableCell>{row.themes}</CustomTableCell>
                  <CustomTableCell>{row.notes}</CustomTableCell>
                  <CustomTableCell>
                    <IconButton onClick={() => this.editRow(row.id)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton onClick={() => this.askDeleteRow(row.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </CustomTableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
        <Dialog
          open={this.state.deleteOpen}
          onClose={this.handleDeleteRowClose}
          aria-labelledby="alert-dialog-title"
          aria-describedby="alert-dialog-description"
        >
          <DialogTitle id="alert-dialog-title">{"Are you sure you want to delete this collection?"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              Deleting the collection cannot be undone.
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

Collections.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Collections);
