import React from 'react';
import DefaultLayout from './containers/DefaultLayout';

const Keyword_Lists = React.lazy(() => import('./views/Keyword_Lists'));
const Collections = React.lazy(() => import('./views/Collections'));
const Choose_Files = React.lazy(() => import('./views/Run_Subcorpora/Choose_Files'));
const Choose_Keywords = React.lazy(() => import('./views/Run_Subcorpora/Choose_Keywords'));
const Choose_Metadata = React.lazy(() => import('./views/Run_Subcorpora/Choose_Metadata'));
const Subcorpora_Report = React.lazy(() => import('./views/Run_Subcorpora/Subcorpora_Report'));
const Running_Tool = React.lazy(() => import('./views/Run_Subcorpora/Running_Tool'));
const Past_Runs = React.lazy(() => import('./views/Past_Runs'));

const routes = [
	{ path: '/run_subcorpora/choose_files', name: 'Choose Files', component: Choose_Files },
	{ path: '/run_subcorpora/choose_keywords', name: 'Choose Keyword List', component: Choose_Keywords },
	{ path: '/run_subcorpora/choose_metadata', name: 'Choose Metadata', component: Choose_Metadata },
	{ path: '/run_subcorpora/subcorpora_report', name: 'Subcorpora_Report', component: Subcorpora_Report },
	{ path: '/keyword_lists', exact: true, name: 'Keyword Lists', component: Keyword_Lists },
	{ path: '/collections', exact: true, name: 'Collections', component: Collections },
	{ path: '/run_subcorpora/running_tool', name: 'Running Tool', component: Running_Tool },
	{ path: '/past_runs', exact: true, name: 'Past Runs', component: Past_Runs },
];

export default routes;
