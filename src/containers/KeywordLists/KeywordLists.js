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
      keywords: [],
      rows: [
        { 
          id:'rape-3', 
          name: 'rape', 
          version: 3, 
          date_added: '01/24/2019', 
          included: "rap*, sex* assault, outrage, attack, insult, ravish, harass*, sex* abuse, seduce, seduction, took advantage of, sex* violence, hanky panky, abus*, incest*, anti-rape, hit on me, hit on her, pedophilia, child abuse, molest*, brutality", 
          excluded: "rapport, rapping, rapidly, rappelling, Dr. Raper, heart attack, rapidly, rap, racist attack, under attack, sterilization abuse", 
        }
      ],
    };

    // this.updateTable = this.updateTable.bind(this);
  }

  // TODO: Fix data retrieval
  // Gets our data once the component mounts
  componentDidMount() {
    axios.get('/get_keywords')
      .then(res => this.setState({keywords: res.data}))
      .then(data => this.updateTable())
      .catch(err => console.log("Error getting keywords (" + err + ")"));
  }

  // Updates the front-end selection with our current keyword information
  // updateTable() {
  //   var rows = [];
  //   for (var id in this.state.keywords) {
  //     var k = this.state.keywords[id];
  //     console.log(k);
  //     var data = createData(id, k['name'], k['version'], k['date_added'], k['included'].join(", "), k['excluded'].join(", "));
  //     rows.push(data);
  //   }
  //   this.setState({ rows: rows });
  // }

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
        <Paper className={classes.root}>
          <Table className={classes.table}>
            <TableHead>
              <TableRow>
                <CustomTableCell>Keyword List Name</CustomTableCell>
                <CustomTableCell>Version</CustomTableCell>
                <CustomTableCell>Date added</CustomTableCell>
                <CustomTableCell>Included Keywords</CustomTableCell>
                <CustomTableCell>Excluded Keywords</CustomTableCell>
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
                  <CustomTableCell>{row.included}</CustomTableCell>
                  <CustomTableCell>{row.excluded}</CustomTableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      </div>
    );
  }
}

KeywordLists.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(KeywordLists);
