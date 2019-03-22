import React, { Component } from 'react';
import { Card, CardHeader, CardBody, Form, Label, Input, CardFooter, Button, FormGroup } from 'reactstrap'
import axios from 'axios'

class Choose_Keywords extends Component {
  constructor(props) {
    super(props);

    this.state = {
      keywordList: '',
    };

    this.routeChangeNext = this.routeChangeNext.bind(this);
  }

  // Event to update state when form inputs change
  onChange = (e) => {
    switch (e.target.name) {
      case 'keyword-list':
        this.setState({ keywordList: e.target.value });
    }
  }

  // Create options for keyword selection
  createSelectItems() {
    let keyword_list = ["rape keywords", "sex keywords"];
    let items = [];
    for (let i = 0; i < keyword_list.length; i++) {
      items.push(<option key = {i} value = { keyword_list[i] }>{ keyword_list[i] }</option>);
    }
    return items;
  }

  // Event to change to the next page to choose metadata
  routeChangeNext() {
    let formData = new FormData();
    formData.append('keywordList', this.state.keywordList);
    axios.post('/choose-keywords', formData).then((result) => {
        // Access results
      }); 

    let path = `/run_subcorpora/choose_metadata`;
    this.props.history.push(path);
  }

  render() {
    return (
        <div class="animated fadeIn">
          <Card>
            <CardHeader>
              <strong>Choose Keyword List</strong>
            </CardHeader>
            <CardBody>
              <Form className = "form-horizontal">
                <FormGroup>
                  <Label htmlFor = "keyword-list">Keyword List</Label>
                  <Input type = "select" name = "keyword-list" id = "keyword-list" required>
                    { this.createSelectItems() }
                  </Input>
                </FormGroup>
              </Form>
            </CardBody>
            <CardFooter>
              <Button onClick = { this.routeChangeNext } size = "sm" color = "secondary">Next</Button>
            </CardFooter>
          </Card>
        </div>
      );
  }
}

export default Choose_Keywords;