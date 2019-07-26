import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';
import {Line, Bar, Doughnut} from 'react-chartjs-2';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

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
	table: {
    minWidth: 700,
  },
  row: {
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.background.default,
    },
  },
});

class IndividualReport extends React.Component {
	constructor(props) {
		super(props);

		this.state = {
			data: this.props.parentData, // Passed from the parent report
			timeRangeInterviewsData: {},
			timeRangeBirthYearData: {},
			keywordCounts: {},
			intervieweeRaceData: {},
	  }
	}

	componentDidMount() {
		this.generateTimeRangeInterviewsData();
  	this.generateTimeRangeBirthYear();
  	this.generateKeywordCountsData();
  	this.generateIntervieweeRaceData();
  	this.generateTables();
  }

  generateIntervieweeRaceData = () => {
  	var labels = [];
  	var values = [];

  	const data = this.state.data['summary-report']['race'];
  	for (var key in data) {
  		const value = data[key];
  		labels.push(key);
  		values.push(value);
  	}

  	const newData = {
			labels: labels,
			datasets: [{
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
			}]
		};

  	this.setState({ intervieweeRaceData: newData });
  }

  generateKeywordCountsData = () => {
  	var labels = [];
  	var values = [];
  	const data = this.state.data['summary-report']['keyword-counts'];
  	for (var key in data) {
  		const value = data[key]
  		labels.push(key);
  		values.push(value);
  	}

  	const newData = {
		  labels: labels,
		  datasets: [
		    {
		      label: 'Counts of Keyword Found',
		      backgroundColor: 'rgba(255,99,132,0.2)',
		      borderColor: 'rgba(255,99,132,1)',
		      borderWidth: 1,
		      hoverBackgroundColor: 'rgba(255,99,132,0.4)',
		      hoverBorderColor: 'rgba(255,99,132,1)',
		      data: values
		    }
		  ]
		};

  	this.setState({ keywordCounts: newData });
  }

  generateTimeRangeInterviewsData = () => {
		var labels = [];
		var values = [];
  	const data = this.state.data['summary-report']['time-range-interviews'];
  	for (var key in data) {
  		const value = data[key]
  		labels.push(key);
  		values.push(value);
  	}

  	const newData = {
		  labels: labels,
		  datasets: [
		    {
		      label: 'Time Range of Interviews (by decade)',
		      fill: false,
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
		    }
		  ]
		};

		this.setState({ timeRangeInterviewsData: newData });
	};

	generateTables = () => {
		// var tables = [];

		// const data = this.state.data['individual-reports']['SHS-rape-3']['keyword-contexts'];
		// for (var key in data) {
		// 	const values = data[key];
		// 	const currTable = (
  //           <TableBody>
  //             {values.map(row => (
  //               <TableRow className={styles.row}>
  //                 <CustomTableCell component="th" scope="row">
  //                   <Checkbox checked={values.incorrect} />
  //                 </CustomTableCell>
  //                 <CustomTableCell><Checkbox checked={values.flagged} /></CustomTableCell>
  //                 <CustomTableCell>{values['keyword-context']}</CustomTableCell>
  //               </TableRow>
  //             ))}
  //           </TableBody>
  //         );
		// 	tables.push({title: key, tableBody: currTable});
		// }

		// this.setState({ tables: tables });
	};

	generateTimeRangeBirthYear = () => {
		// TODO: Sort them by the key
		const newData = [];
		const data = this.state.data['summary-report']['time-range-birth-year'];
		for (var key in data) {
			const value = data[key];
			newData.push({lineValue: value, argument: parseInt(key)});
		}

		this.setState({ timeRangeBirthYearData: newData });
	};

	render() {
		const { classes } = this.props;
		const { intervieweeRaceData: irData, timeRangeInterviewsData: triData, timeRangeBirthYearData: trbyData, keywordCounts: kcData } = this.state;
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
	          <b>Total keywords: </b>{ summaryData['total-keywords'] }<br />
	          <b>Total keywords found: </b>{ summaryData['total-keywords-found'] }<br />
	        </Typography>
	      </Paper>
	      <br />
	      <Paper className={classes.paper} elevation={1}>
	      	<Typography variant="h5" component="h3">
	          Keyword Counts
	        </Typography>
	      	<Bar
	      		data = {kcData}
	      	/>
	      </Paper>
	      <Paper className={classes.paper} elevation={1}>
	      	<Typography variant="h5" component="h3">
	          Time Range of Interviews
	        </Typography>
	      	<Line data={triData} />
	      </Paper>
	      <br />
	      <Paper className={classes.paper} elevation={1}>
	      	<Typography variant="h5" component="h3">
	          Race of Interviewees
	        </Typography>
	      	<Doughnut data={irData} />
	      </Paper>
	      <br />
	      <Paper className={classes.paper} elevation={1}>
	      	<Typography variant="h5" component="h3">
	          Keywords in Context
	        </Typography>
	        <br />
        	<Typography paragraph>
        		SHSA_Dodge_Judith.txt
        	</Typography>
        	<Table className={classes.table}>
        		<TableHead>
              <TableRow>
                <CustomTableCell>Incorrect</CustomTableCell>
                <CustomTableCell>Flagged</CustomTableCell>
                <CustomTableCell>Context</CustomTableCell>
              </TableRow>
            </TableHead>
        		<TableBody>
        			<TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
                <CustomTableCell>...quarterback. But Stanford lost to UCLA seventy-two to nothing. I imagine that's the worst one that they've ever had. Shortly after that, it was the old Pacific Coast Conference, and it was disbanded because there were penalties against Washington, USC, UCLA--I forget. Anyway, there were a lot of <b>abuses</b>. And two years later, I went down to L.A. on the train, so it was my junior year, and I had a friend that went to UCLA, so I stayed with her and saw them. But at halftime at the game, UCLA, who had been penalized, referred to Stanford as...</CustomTableCell>
              </TableRow>
        		</TableBody>
        	</Table>
        	<br />
        	<Typography paragraph>
        		SHSA_Gartrell_Nanette.txt
        	</Typography>
        	<Table className={classes.table}>
        		<TableHead>
              <TableRow>
                <CustomTableCell>Incorrect</CustomTableCell>
                <CustomTableCell>Flagged</CustomTableCell>
                <CustomTableCell>Context</CustomTableCell>
              </TableRow>
            </TableHead>
        		<TableBody>
        			<TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
                <CustomTableCell>...and author Nanette Gartrell (BA Human Biology 1972) discusses her family and educational background and traces the trajectory of a career devoted to overturning stereotypes and scientific misconceptions about homosexuality, providing non-homophobic healthcare, and preventing sexual misconduct by physicians. Topics include the ramifications of her personal experience of <b>sexual abuse</b> as a child; the emergence of her identity as a lesbian; Stanford student life in the late 1960s, including the meeting of the first organized campus group of lesbians; lesbian communities in Davis, California, and Washington, DC; and the womens music cultural movement. Gartrell also highlights her work on various...</CustomTableCell>
              </TableRow>
              <TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
                <CustomTableCell>...APA taskforces related to women and/or sexuality; the organizations Dyke Docs and Women in Medicine; her efforts to ensure the profession treated <b>sexual abuse</b> of patients by psychiatrists as a serious ethical violation; and the National Longitudinal Lesbian Family Study, an investigation of American lesbian mothers and their children. Part 1 p. 15 [00:00:00 00:31:12] Growing up in Santa Barbara, California, and learning about the existence of gay people from a homophobic uncle...</CustomTableCell>
              </TableRow>
        		</TableBody>
        	</Table>
        	<br />
        	<Typography paragraph>
        		SHSF_Strober_Myra.txt
        	</Typography>
        	<Table className={classes.table}>
        		<TableHead>
              <TableRow>
                <CustomTableCell>Incorrect</CustomTableCell>
                <CustomTableCell>Flagged</CustomTableCell>
                <CustomTableCell>Context</CustomTableCell>
              </TableRow>
            </TableHead>
        		<TableBody>
        			<TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
                <CustomTableCell>...became its founding director. She discusses fundraising for the center and the lecture series that attracted overflowing crowds from the campus and neighboring areas. In addition, she discusses her service on the Committee on Recruitment and Retention of Women Faculty at Stanford and her experience as a sexual <b>harassment</b> advisor counselling female faculty members. She shares her perspectives on the challenges facing women in academia, such as a low percentage of women on the tenured faculty, salary disparity, and a lack of support. Strober also relates the story of how Stanford successfully competed to host and edit the preeminent...</CustomTableCell>
              </TableRow>
              <TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
                <CustomTableCell>...a member of the Board of Trustees of Mills College. Strober has consulted with several corporations on improved utilization of women in management and on work-family issues. She has also been an expert witness in cases involving the valuation of work in the home, sex discrimination, and <b>sexual harassment</b>. At the School of Education, Strober was director of the Joint Degree Program, a master's program in which students receive both an MA in education and an MBA from the Graduate School of Business. She also served as the chair of the Program in Administration and Policy Analysis, associate dean...</CustomTableCell>
              </TableRow>
              <TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
               <CustomTableCell>...and also Francine Gordon, who was my colleague. But she was also having a tough time. This was her first teaching experience. I had had five years of teaching experience, so I had that going for me, but as a brand new assistant professor with all of the <b>sexism</b>, it was really a hard time for her. Arjay Miller, who was the Dean of the Business School, was a prince. He was extremely supportive. He had been the CEO of Ford Motor Company. He was not an academic. Francine and I wanted to create and host a conference on..."</CustomTableCell>
        			</TableRow>
 							<TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
 								<CustomTableCell>..Series at noon was one of the main events of the campus, and eventually the center hired Margo Davis, who was in charge of the lecture series and got outside money for it. One of the most interesting debates at CROW was whether to take money from the <b>Playboy</b> Foundation, which wanted to fund one of our lecture series on Women and the Media. I thought we should take the money, and the provost, Bill Miller, thought we should take it. Bill Miller said he thought we should be like the Catholic Church and figure that the money was...</CustomTableCell>
        			</TableRow>
        			<TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
        				<CustomTableCell>...cleansed in the giving. But other people argued that we should not take the money. Nan [Nannerl] Keohane, who ultimately became president of Wellesley and president of Duke, felt we should not take the money, that we didn't want the <b>Playboy</b> Foundation to advertise that they were supporting us, because that made them look good. So in the end, we didn't take the money, and I had to go to Bill Miller and explain why we didn't take the money. That was hard. Stanford was not used to faculty turning down...</CustomTableCell>
        			</TableRow>
        			<TableRow className={classes.row}>
                <CustomTableCell component="th" scope="row">
                  <Checkbox />
                </CustomTableCell>
                <CustomTableCell><Checkbox /></CustomTableCell>
        				<CustomTableCell>...to ignore them. There were faculty who told us they couldn't even get senior people in their department to read their work, and they didn't feel supported. This was men and women. Then a lot of women told us they felt underpaid. And there were problems with sexual <b>harassment</b>, particularly in the Medical School. We recommended that Stanford pay attention to this culture of nonsupport and try to create a new culture of support, and that the university look pretty carefully at the salary system to figure out what to do about these grave disparities in salaries between women...</CustomTableCell>
        			</TableRow>
        		</TableBody>
        	</Table>
	       </Paper>
		</div>
		);
	}
}

IndividualReport.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(IndividualReport);
