import React, { Component } from 'react';
import { 
  Card, 
  CardHeader, 
  CardBody, 
  Form, 
  Label, 
  Input, 
  CardFooter, 
  Button, 
  FormGroup 
} from 'reactstrap';
import axios from 'axios';

class Choose_Keywords extends Component {
  constructor(props) {
    super(props);

    this.state = {
      keywords: [],
      selectedKeywords: [],
      selectionBody: [],
    };

    this.updateSelection = this.updateSelection.bind(this);
    this.routeChangeNext = this.routeChangeNext.bind(this);
    this.selectionChange = this.selectionChange.bind(this);
  }

  // Updates the selection UI
  updateSelection() {
    const keywords = this.state.keywords;
    var selectionBody = [];
    for (var k in keywords) {
      const item = keywords[k];
      const name = item['name'] + '-' + item['version'];
      selectionBody.push(<option>{ name }</option>);
    }

    this.setState({ selectionBody: selectionBody });
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

    this.setState({ selectedKeywords: selected });
  }

  // Get our data once the component mounts
  componentDidMount() {
    axios.get('/get_keywords')
      .then(res => this.setState({ keywords: res.data }))
      .then(data => this.updateSelection(data))
      .catch(err => console.log("Error getting collections (" + err + ")"));
  }

  // Event to change to the next page to choose metadata
  routeChangeNext() {
    // Updates the backend collections information based on what was selected
    axios.post('/choose_keywords', {
      data: this.state.selectedKeywords
    })
    .then(function (res) {
      console.log("Successfully posted keywords");
    })
    .catch(function (err) {
      console.log(err);
    });

    // Move on!
    let path = `/run_subcorpora/choose_metadata`;
    this.props.history.push(path);
  }

  render() {
    return (
        <div class="animated fadeIn">
        <Card>
          <CardHeader>
            <strong>Select Keyword Lists</strong>
          </CardHeader>
          <CardBody>
            <Form className = "form-horizontal">
              <FormGroup>
                <Label for="selectKeywords">Select Keyword Lists</Label>
                <Input type="select" name="selectKeywords" id="selectKeywords" onChange = { this.selectionChange } multiple>
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

export default Choose_Keywords;