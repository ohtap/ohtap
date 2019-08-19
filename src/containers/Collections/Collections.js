import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
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
      collections: [],
      rows: [
        {
          id: "SHS", 
          name: "Stanford Interviews", 
          shortened_name: "Stanford", 
          collection_count: 46, 
          description: "Interviews from various alumni, faculty, staff, and others.", 
          themes: "Experiences as a Stanford student; career aspirations; life stories leading up to success", 
          notes: "This is only a subset of our current Stanford collection for demo purposes."
        }
      ],
    }

    this.editRow = this.editRow.bind(this);
    this.deleteRow = this.deleteRow.bind(this);
  }

  // TODO: Fix data retrieval
  componentDidMount() {}

  editRow(id) {
    console.log("Edit " + id);
  }

  deleteRow(id) {
    console.log("Delete " + id);
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
                    <IconButton onClick={() => this.deleteRow(row.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </CustomTableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      </div>
    );
  }
}

Collections.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Collections);
