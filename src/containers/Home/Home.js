import React from 'react';
import Typography from '@material-ui/core/Typography';

class Home extends React.Component {
	render() {
		return (
			<div>
				<Typography paragraph component='h2' variant='h1'>
		            Winnow
		          </Typography>
		          <Typography paragraph variant='h5'>
		            Generate relevant subcorpora from your oral history collections for easier analysis.
		          </Typography>
		          <Typography paragraph>
		          	We are OHTAP (Oral History Textual Analysis Project), a group at Stanford working on integrating quantitative and qualitative methodologies for oral history analysis. 
		          	We currently are analyzing around 2000 oral history transcripts to help map historical memories of sexual harassment, assault, abuse. During our process, we found that 
		          	it was hard to figure out which transcripts were relevant and what a collection looked in terms of what we wanted to be searching for. Enter Winnow, a tool that generates 
		          	relevant subcorpora based on your metadata and lists of relevant keywords you want to search for. Winnow gives you smaller subsets of your collections that you are then able 
		          	to either analyze by hand or plug into other textual analysis tools.
		          </Typography>
	        </div>
		);
	}
}

export default Home;