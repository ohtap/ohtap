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
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import TextField from '@material-ui/core/TextField';
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

function createData(id, name, version, date_added, included, excluded) {
  return { id, name, version, date_added, included, excluded };
}

class KeywordLists extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      keywords: {},
      rows: [],
      deleteOpen: false,
      currRowId: null,
      editOpen: false,
      addOpen: false,
    };

    this.updateTable = this.updateTable.bind(this);

    this.askAddRow = this.askAddRow.bind(this);
    this.handleAddRowClose = this.handleAddRowClose.bind(this);
    this.addRow = this.addRow.bind(this);

    this.editRow = this.editRow.bind(this);
    this.askEditRow = this.askEditRow.bind(this);
    this.handleEditRowClose = this.handleEditRowClose.bind(this);

    this.askDeleteRow = this.askDeleteRow.bind(this);
    this.handleDeleteRowClose = this.handleDeleteRowClose.bind(this);
    this.deleteRow = this.deleteRow.bind(this);
  }

  // Gets our data once the component mounts
  componentDidMount() {
    axios.get('/get_keywords')
      .then(res => this.setState({ keywords: res.data }))
      .then(data => this.updateTable())
      .catch(err => console.log("Error getting keywords (" + err + ")"));
  }

  // Handles closing the "Add Row" dialog
  handleAddRowClose() {
    this.setState({ addOpen: false });
  }

  // Opens a modal to add a new row
  askAddRow() {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    today = mm + "/" + dd + "/" + yyyy;

    this.setState({
      addOpen: true,
      currRowId: null,
      currRowName: "",
      currRowVersion: "",
      currRowDateAdded: today,
      currRowIncluded: "",
      currRowExcluded: "",
    });
  }

  // Adds a row
  addRow() {
    axios.post('/add_keyword_list', {
      id: this.state.currRowName + "-" + this.state.currRowVersion,
      name: this.state.currRowName,
      version: this.state.currRowVersion,
      date_added: this.state.currRowDateAdded,
      included: this.state.currRowIncluded,
      excluded: this.state.currRowExcluded
    })
    .then(res => {
      axios.get('/get_keywords')
        .then(data => this.updateTable())
        .catch(err => console.log("Error getting keywords (" + err + ")"));
    })
    .catch(function (err) {
      console.log(err);
    });

    this.updateTable();
    this.handleAddRowClose();
  }

   // Handles closing the "Delete Row" dialog
  handleDeleteRowClose() {
    this.setState({ deleteOpen: false, currRowId: null });
  }

  // Opens a modal to check if the user really wants to delete the row
  askDeleteRow(id) {
    this.setState({ deleteOpen: true, currRowId: id });
  }

  // Deletes the current row
  deleteRow(id) {
    axios.post('/delete_keyword_list', {
      id: this.state.currRowId
    })
    .then(res => {
      axios.get('/get_keywords')
        .then(res => this.setState({ keywords: res.data }))
        .then(data => this.updateTable())
        .catch(err => console.log("Error getting keywords (" + err + ")"));
    })
    .catch(function (err) {
      console.log(err);
    });

    this.handleDeleteRowClose();
  }

  // Handles closing the "Edit Row" dialog
  handleEditRowClose() {
    this.setState({ editOpen: false, currRowId: null });
  }

  askEditRow(id) {
    this.setState({
      editOpen: true,
      currRowId: id,
      currRowName: this.state.keywords[id]["name"],
      currRowVersion: this.state.keywords[id]["version"],
      currRowDateAdded: this.state.keywords[id]["date-added"],
      currRowIncluded: this.state.keywords[id]["include"],
      currRowExcluded: this.state.keywords[id]["exclude"]
    });
  }

  editRow() {
    console.log(this.state.currRowIncluded);


    axios.post("/edit_keyword_list", {
      id: this.state.currRowId,
      name: this.state.currRowName,
      version: this.state.currRowVersion,
      date_added: this.state.currRowDateAdded,
      included: this.state.currRowIncluded,
      excluded: this.state.currRowExcluded
    })
    .then(res => {
      axios.get("/get_keywords")
        .then(res => this.setState({ keywords: res.data }))
        .then(data => this.updateTable())
        .catch(err => console.log("Error getting keywords (" + err + ")"));
    })
    .catch(function (err) {
      console.log(err);
    });

    this.updateTable();
    this.handleEditRowClose();
  }

  // Updates the front-end selection with our past run information
  updateTable() {
    var rows = [];
    for (var id in this.state.keywords) {
      var v = this.state.keywords[id];
      var name = v["name"];
      var version = v["version"];
      var date_added = v["date-added"];
      var included = v["include"];
      var excluded = v["exclude"];
      var data = createData(id, name, version, date_added, included, excluded);
      rows.push(data);
    }
    this.setState({ rows: rows });
  }

  render() {
    const { classes } = this.props;

    return (
      <div>
        <Typography variant="h4">
          Keyword Lists
        </Typography>
        <Typography paragraph>
          Add, edit, and delete keyword lists. On this demo version, all editing functionality is not allowed.
        </Typography>
        <br />
        <Button onClick={this.askAddRow} color="primary" autoFocus>
            Add Keyword List
        </Button>
        <br />
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <CustomTableCell>Keyword List Name</CustomTableCell>
                <CustomTableCell>Version</CustomTableCell>
                <CustomTableCell>Date added</CustomTableCell>
                <CustomTableCell>Included Keywords</CustomTableCell>
                <CustomTableCell>Excluded Keywords</CustomTableCell>
                <CustomTableCell>Modify/Delete</CustomTableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.state.rows.map(row => (
                <TableRow className={classes.row} key={row.id}>
                  <CustomTableCell component="th" scope="row">
                    {row.name}
                  </CustomTableCell>
                  <CustomTableCell>{row.version}</CustomTableCell>
                  <CustomTableCell>{row.date_added}</CustomTableCell>
                  <CustomTableCell>{row.included.join()}</CustomTableCell>
                  <CustomTableCell>{row.excluded.join()}</CustomTableCell>
                  <CustomTableCell>
                    <IconButton onClick={() => this.askEditRow(row.id)}>
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
          <DialogTitle id="alert-dialog-title">{"Are you sure you want to delete this keyword list?"}</DialogTitle>
          <DialogContent>
            <DialogContentText id="alert-dialog-description">
              Deleting the keyword list cannot be undone.
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
        <Dialog
          open={this.state.addOpen}
          onClose={this.handleAddRowClose}
          aria-labelledby="form-dialog-title-add"
        >
          <DialogTitle id="form-dialog-title-add">Add keyword list</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Add a keyword list.
              <br />
              <TextField
                label="Name"
                value={ this.state.currRowName }
                onChange={(e) => this.setState({ currRowName: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Version"
                value={ this.state.currRowVersion }
                onChange={(e) => this.setState({ currRowVersion: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                disabled
                label="Date Added"
                value={ this.state.currRowDateAdded }
                onChange={(e) => this.setState({ currRowDateAdded: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Included keywords (comma separated)"
                value={ this.state.currRowIncluded }
                onChange={(e) => this.setState({ currRowIncluded: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Excluded keywords (comma separated)"
                value={ this.state.currRowExcluded }
                onChange={(e) => this.setState({ currRowExcluded: e.target.value })}
                margin="normal"
              />
            </DialogContentText>
            <DialogActions>
              <Button onClick={this.handleAddRowClose} color="primary">
                Cancel
              </Button>
              <Button onClick={this.addRow} color="primary">
                Save
              </Button>
            </DialogActions>
          </DialogContent>
        </Dialog>
        <Dialog
          open={this.state.editOpen}
          onClose={this.handleEditRowClose}
          aria-labelledby="form-dialog-title-edit"
        >
          <DialogTitle id="form-dialog-title-edit">Edit keyword list</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Edit the keyword list.<br />
              <TextField
                id={ this.state.currRowId + "-edit-name"}
                label="Name"
                value={ this.state.currRowName }
                onChange={(e) => this.setState({ currRowName: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-version"}
                label="Version"
                value={ this.state.currRowVersion }
                onChange={(e) => this.setState({ currRowVersion: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                disabled
                id={ this.state.currRowId + "-edit-date-added"}
                label="Date Added"
                value={ this.state.currRowDateAdded }
                onChange={(e) => this.setState({ currRowDateAdded: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-included"}
                label="Included keywords (comma separated)"
                value={ this.state.currRowIncluded }
                onChange={(e) => this.setState({ currRowIncluded: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-excluded"}
                label="Excluded keywords (comma separated)"
                value={ this.state.currRowExcluded }
                onChange={(e) => this.setState({ currRowExcluded: e.target.value })}
                margin="normal"
              />
            </DialogContentText>
            <DialogActions>
              <Button onClick={this.handleEditRowClose} color="primary">
                Cancel
              </Button>
              <Button onClick={this.editRow} color="primary">
                Save
              </Button>
            </DialogActions>
          </DialogContent>
        </Dialog>
      </div>
    );
  }
}

KeywordLists.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(KeywordLists);
