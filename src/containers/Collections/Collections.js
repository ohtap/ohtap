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
      editOpen: false,
      addOpen: false,
    }

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
    axios.get('/get_collections')
      .then(res => this.setState({ collections: res.data }))
      .then(data => this.updateTable())
      .catch(err => console.log("Error getting collections (" + err + ")"));
  }

  // Handles closing the "Add Row" dialog
  handleAddRowClose() {
    this.setState({ addOpen: false });
  }

  // Opens a modal to add a new row
  askAddRow() {
    this.setState({ 
      addOpen: true,
      currRowId: null,
      currRowName: "",
      currRowShortenedName: "",
      currRowCollectionCount: "",
      currRowDescription: "",
      currRowThemes: "",
      currRowNotes: ""
    });
  }

  addRow() {
    axios.post('/add_collection', {
      id: this.state.currRowId,
      name: this.state.currRowName,
      shortenedName: this.state.currRowShortenedName,
      description: this.state.currRowDescription,
      themes: this.state.currRowThemes,
      notes: this.state.currRowNotes
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

  // Handles closing the "Edit Row" dialog
  handleEditRowClose() {
    this.setState({ editOpen: false, currRowId: null });
  }

  askEditRow(id) {
    this.setState({ 
      editOpen: true, 
      currRowId: id,
      currRowName: this.state.collections[id]["name"],
      currRowShortenedName: this.state.collections[id]["shortened-name"],
      currRowCollectionCount: this.state.collections[id]["collection-count"],
      currRowDescription: this.state.collections[id]["description"],
      currRowThemes: this.state.collections[id]["themes"],
      currRowNotes: this.state.collections[id]["notes"]
    });
  }

  editRow() {
    axios.post("/edit_collection", {
      id: this.state.currRowId,
      name: this.state.currRowName,
      shortenedName: this.state.currRowShortenedName,
      description: this.state.currRowDescription,
      themes: this.state.currRowThemes,
      notes: this.state.currRowNotes
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

    this.updateTable();
    this.handleEditRowClose();
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
          Add, upload, edit, and delete collections.
        </Typography>
        <br />
        <Button onClick={this.askAddRow} color="primary" autoFocus>
            Add Collection
        </Button>
        <br />
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
        <Dialog
          open={this.state.addOpen}
          onClose={this.handleAddRowClose}
          aria-labelledby="form-dialog-title-add"
        >
          <DialogTitle id="form-dialog-title-add">Add collection</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Add a collection.<br />
              <TextField
                label="ID"
                value={ this.state.currRowId }
                onChange={(e) => this.setState({ currRowId: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Name"
                value={ this.state.currRowName }
                onChange={(e) => this.setState({ currRowName: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Collection Count"
                value={ this.state.currRowCollectionCount }
                onChange={(e) => this.setState({ currRowCollectionCount: e.target.value })}
                margin="normal"
              />
              <br />
              <input
                style={{ display: 'none '}}
                id="raised-button-file"
                multiple
                type="file"
              />
              <label htmlFor="raised-button-file">
                <Button variant="raised" component="span">
                  Upload Files
                </Button>
              </label>
              <br />
              <TextField
                label="Shortened Name"
                value={ this.state.currRowShortenedName }
                onChange={(e) => this.setState({ currRowShortenedName: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Description"
                value={ this.state.currRowDescription }
                onChange={(e) => this.setState({ currRowDescription: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Themes"
                value={ this.state.currRowThemes }
                onChange={(e) => this.setState({ currRowThemes: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                label="Notes"
                value={ this.state.currRowNotes }
                onChange={(e) => this.setState({ currRowNotes: e.target.value })}
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
          <DialogTitle id="form-dialog-title-edit">Edit collection</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Edit the collection.<br />
              <TextField
                id={ this.state.currRowId + "-edit-name"}
                label="Name"
                value={ this.state.currRowName }
                onChange={(e) => this.setState({ currRowName: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                disabled
                id={ this.state.currRowId + "-edit-collection-count"}
                label="Collection Count"
                value={ this.state.currRowCollectionCount }
                onChange={(e) => this.setState({ currRowCollectionCount: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-shortened-name"}
                label="Shortened Name"
                value={ this.state.currRowShortenedName }
                onChange={(e) => this.setState({ currRowShortenedName: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-description"}
                label="Description"
                value={ this.state.currRowDescription }
                onChange={(e) => this.setState({ currRowDescription: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-themes"}
                label="Themes"
                value={ this.state.currRowThemes }
                onChange={(e) => this.setState({ currRowThemes: e.target.value })}
                margin="normal"
              />
              <br />
              <TextField
                id={ this.state.currRowId + "-edit-notes"}
                label="Notes"
                value={ this.state.currRowNotes }
                onChange={(e) => this.setState({ currRowNotes: e.target.value })}
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

Collections.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Collections);
