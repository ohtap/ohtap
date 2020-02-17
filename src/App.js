import React, { Component } from 'react';
import loadable from '@loadable/component';

const DefaultLayout = loadable(() => import('./containers/DefaultLayout'));

class App extends Component {
  render() {
    return (
      <div className="App">
        <DefaultLayout />
      </div>
    );
  }
}

export default App;
