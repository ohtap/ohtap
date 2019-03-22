import React, { Component } from 'react';
import { Button, FormGroup, Label, Input, Progress, Card, CardHeader, CardBody, CardFooter, Form } from 'reactstrap';
import axios from 'axios';

class Choose_Files extends Component {
  constructor(props) {
    super(props);

    this.state = {
      corpusName: '',
      selectedFiles: null,
      loaded: 0,
      disabledNext: true,
    }; 

    this.routeChangeNext = this.routeChangeNext.bind(this);
  }

  // Event to update state when form inputs change
  onChange = (e) => {
    switch (e.target.name) {
      case 'file':
        this.setState({
          selectedFiles: e.target.files,
        });
        break;
      default:
        this.setState({ [e.target.name]: e.target.value });
    }
  }

  // Event to submit the data to the server
  onSubmit = (e) => {
    e.preventDefault();
    let formData = new FormData();
    formData.append('corpusName', this.state.corpusName);
    for (var i = 0; i < this.state.selectedFiles.length; i++) {
      formData.append('file', this.state.selectedFiles[i]);
    }
    axios.post('/upload-corpus', formData, {
      // Updates the progress of the upload
      onUploadProgress: ProgressEvent => {
        this.setState({ loaded: (ProgressEvent.loaded / ProgressEvent.total * 100) });
      },
    }).then((result) => {
        // Access results
        this.setState({ disabledNext: false });
    });
  }

  // Event to change to the next page to choose keywords
  routeChangeNext() {
    let path = `/run_subcorpora/choose_keywords`;
    this.props.history.push(path);
  }

  render() {
    return (
      <div class="animated fadeIn">
        <Card>
          <CardHeader>
            <strong>Upload Corpus Files</strong>
          </CardHeader>
          <CardBody>
            <Form onSubmit = { this.onSubmit } className = "form-horizontal">
              <FormGroup row>
                <Label htmlFor = "corpusName">Corpus Name</Label>
                <Input type = "text" id = "corpusName" name = "corpusName" onChange = { this.onChange } placeholder = "Enter corpus name" required />
              </FormGroup>
              <FormGroup row>
                <Label htmlFor = "corpusUpload">Upload Files</Label>
                <Input type = "file" name = "file" id = "corpusUpload" onChange = { this.onChange } webkitdirectory multiple />
              </FormGroup>
              <Progress max = "100" color = "success" value = { this.state.loaded } > { Math.round(this.state.loaded, 2) }%</Progress>
              <Button type = "submit" size = "sm" color = "primary">Submit</Button>
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