import React, { Component } from 'react';

class Home extends Component {
  render() {
    return (
      <div class="animated fadeIn">
        <div class="card">
          <div class="card-body">
            <h1 class="docs-title" id="main-title">San Onofre Nuclear Generating Station</h1>
            <p class="docs-lead">We are conducting a case study of SONGS using the social multi-criteria decision-making process.</p>
            <form method="post" action="/api/addstakeholder">
              <label>Enter a stakeholder</label><br />
              <input type="text" name="name" placeholder="Enter name..." required></input>
              <input type="submit" value="Add Stakeholder"></input>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
