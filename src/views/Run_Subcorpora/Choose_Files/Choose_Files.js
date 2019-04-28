import React, { Component } from 'react';
import { Button, FormGroup, Label, Input, Progress, Card, CardHeader, CardBody, CardFooter, Form } from 'reactstrap';
import axios from 'axios';

class Choose_Files extends Component {
  constructor(props) {
    super(props);

    this.state = {
      collections: [],
      selectedCollections: [],
      selectionBody: [],
    }; 

    this.updateSelection = this.updateSelection.bind(this);
    this.routeChangeNext = this.routeChangeNext.bind(this);
    this.selectionChange = this.selectionChange.bind(this);
  }

  // Updates the selected values as the selection UI changes
  selectionChange(event) {
    var options = event.target.options;
    var selected = [];
    for (var i = 0; i < options.length; i++) {
      if (options[i].selected) {
        selected.push(options[i].value)
      }
    }
    this.state.selectedCollections = selected;
  }

  // Get our data once the component mounts
  componentDidMount() {
    axios.get('/get_collections')
      .then(res => this.setState({ collections: res.data }))
      .then(data => this.updateSelection(data))
      .catch(err => console.log("Error getting collections (" + err + ")"));
  }

  // Updates the selection UI
  updateSelection() {
    const collections = this.state.collections;
    var selectionBody = [];
    for (var k in collections) {
      const item = collections[k];
      selectionBody.push(<option>{ item['id'] }</option>);
    }

    this.setState({ selectionBody: selectionBody });
  }

  // Event to change to the next page to choose keywords
  routeChangeNext() {
    // Updates the backend collections information based on what was selected
    axios.post('/choose_collections', {
      data: this.state.selectedCollections
    })
    .then(function (res) {
      console.log("Successfully posted collections");
    })
    .catch(function (err) {
      console.log(err);
    });

    // Moves on!
    let path = `/run_subcorpora/choose_keywords`;
    this.props.history.push(path);
  }

  render() {
    return (
      <div class="animated fadeIn">
        <Card>
          <CardHeader>
            <strong>Select Collections</strong>
          </CardHeader>
          <CardBody>
            <Form className = "form-horizontal">
              <FormGroup>
                <Label for="selectCollections">Select Collections</Label>
                <Input type="select" name="selectCollections" id="selectCollections" onChange = { this.selectionChange } multiple>
                  { this.state.selectionBody }
                </Input>
              </FormGroup>
            </Form>
          </CardBody>
          <CardFooter>
            <Button onClick = { this.routeChangeNext } size = "sm" color = "secondary" disabled = { this.state.disabledNext }>Next</Button>
          </CardFooter>
        </Card>
      </div>
    );
  }
}

export default Choose_Files;