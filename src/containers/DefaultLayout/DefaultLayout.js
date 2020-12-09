import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import HomeIcon from '@material-ui/icons/Home';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import ListRoundedIcon from '@material-ui/icons/ListRounded';
import AssessmentRoundedIcon from '@material-ui/icons/AssessmentRounded';
import DescriptionRoundedIcon from '@material-ui/icons/DescriptionRounded';
import loadable from '@loadable/component';
import Typography from '@material-ui/core/Typography';
import { Route, BrowserRouter, Link } from 'react-router-dom';

const drawerWidth = 240;

const Home = loadable(() => import('../Home'));
const KeywordLists = loadable(() => import('../KeywordLists'));
const Collections = loadable(() => import('../Collections'));
const CreateRun = loadable(() => import('../CreateRun'));
const PastRuns = loadable(() => import('../PastRuns'));

const SelectCollections = loadable(() => import('../CreateRun/SelectCollections'));
const SelectKeywords = loadable(() => import('../CreateRun/SelectKeywords'));
const SelectMetadata = loadable(() => import('../CreateRun/SelectMetadata'));
const SelectMetadataSecondSheet = loadable(() => import('../CreateRun/SelectMetadataSecondSheet'));

const Report = loadable(() => import('../Report'));
const PastRunsReport = loadable(() => import("../Report/PastRunsReport"));

const styles = theme => ({
  root: {
    display: 'flex',
  },
  appBar: {
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginLeft: 12,
    marginRight: 20,
  },
  hide: {
    display: 'none',
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    padding: '0 8px',
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: -drawerWidth,
  },
  contentShift: {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  },
});

class DefaultLayout extends React.Component {
  state = {
    open: false,
  };

  handleDrawerOpen = () => {
    this.setState({ open: true });
  };

  handleDrawerClose = () => {
    this.setState({ open: false });
  };  

  render() {
    const { classes, theme } = this.props;
    const { open } = this.state;

    return (
      
      <div className={classes.root}>
        <CssBaseline />
        <BrowserRouter>
        <AppBar
          position="fixed"
          className={classNames(classes.appBar, {
            [classes.appBarShift]: open,
          })}
        >
          <Toolbar disableGutters={!open}>
            <IconButton
              color="inherit"
              aria-label="Open drawer"
              onClick={this.handleDrawerOpen}
              className={classNames(classes.menuButton, open && classes.hide)}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" color="inherit" noWrap>
              
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          className={classes.drawer}
          variant="persistent"
          anchor="left"
          open={open}
          classes={{
            paper: classes.drawerPaper,
          }}
        >
          <div className={classes.drawerHeader}>
            <IconButton onClick={this.handleDrawerClose}>
              {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
            </IconButton>
          </div>
          <Divider />
          <List>
            <ListItem button key='Home' component={Link} to='/'>
              <ListItemIcon><HomeIcon /></ListItemIcon>
              <ListItemText primary='Home' />
            </ListItem>
            <ListItem button key='Create a new run' component={Link} to='/create_run'>
              <ListItemIcon><AddCircleIcon /></ListItemIcon>
              <ListItemText primary='Create a new run' />
            </ListItem>
            <ListItem button key='Keyword lists' component={Link} to='/keyword_lists'>
              <ListItemIcon><ListRoundedIcon /></ListItemIcon>
              <ListItemText primary='Keyword lists' />
            </ListItem>
            <ListItem button key='Collections' component={Link} to='/collections'>
              <ListItemIcon><DescriptionRoundedIcon /></ListItemIcon>
              <ListItemText primary='Collections' />
            </ListItem>
            <ListItem button key='Past runs' component={Link} to='/past_runs'>
              <ListItemIcon><AssessmentRoundedIcon /></ListItemIcon>
              <ListItemText primary='Past runs' />
            </ListItem>
          </List>
          <Divider />
        </Drawer>
        <main
          className={classNames(classes.content)}
        >
          <div className={classes.drawerHeader} />
            <Route exact path='/' component={Home} />
            <Route exact path='/keyword_lists' component={KeywordLists} />
            <Route exact path='/collections' component={Collections} />
            <Route exact path='/create_run' component={CreateRun} />
            <Route exact path='/create_run/select_collections' component={SelectCollections} />
            <Route exact path='/create_run/select_keywords' component={SelectKeywords} />
            <Route exact path='/create_run/select_metadata' component={SelectMetadata} />
            <Route exact path='/create_run/select_metadata_second_sheet' component={SelectMetadataSecondSheet} />
            <Route exact path='/report' component={Report} />
            <Route exact path='/past_runs' component={PastRuns} />
            <Route exact path='/past_runs_report' component={PastRunsReport} />
        </main>
        </BrowserRouter>
      </div>
    );
  }
}

DefaultLayout.propTypes = {
  classes: PropTypes.object.isRequired,
  theme: PropTypes.object.isRequired,
};

export default withStyles(styles, { withTheme: true })(DefaultLayout);