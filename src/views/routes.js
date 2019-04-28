import React from 'react';
import DefaultLayout from './containers/DefaultLayout';

const Keyword_Lists = React.lazy(() => import('./views/Keyword_Lists'));
const Collections = React.lazy(() => import('./views/Collections'));

const routes = [
	{ path: '/keyword_lists', exact: true, name: 'Keyword Lists', component: Keyword_Lists },
	{ path: '/collections', exact: true, name: 'Collections', component: Collections },
];

export default routes;
