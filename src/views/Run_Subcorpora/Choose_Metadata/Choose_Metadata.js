import React, { Component } from 'react';
import { Button, FormGroup, Label, Input, Progress, Card, CardHeader, CardBody, CardFooter, Form } from 'reactstrap';
import axios from 'axios';

class Choose_Metadata extends Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedFile: null,
      loaded: 0,
      disabledNext: true,
    };

    this.routeChangeNext = this.routeChangeNext.bind(this);
  };

  // Event to update state when form inputs change
  onChange = (e) => {
    switch (e.target.name) {
      case 'metadata-file':
        this.setState({
          selectedFile: e.target.files[0],
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
    formData.append('metadataFile', this.state.selectedFile);
    axios.post('/upload-metadata', formData, {
      onUploadProgress: ProgressEvent => {
        this.setState({ loaded: (ProgressEvent.loaded / ProgressEvent.total * 100) });
      },
    }).then((result) => {
      this.setState({ disabledNext: false });
    });
  }

  // Event to change to the next page to choose keywords
  routeChangeNext() {
    let path = `/run_subcorpora/running_tool`;
    this.props.history.push(path);
  }

  render() {
    return (
        <div class="animated fadeIn">
          <Card>
            <CardHeader>
              <strong>Upload Metadata Files</strong>
            </CardHeader>
            <CardBody>
              <Form onSubmit = { this.onSubmit } className = "form-horizontal">
                <FormGroup row>
                  <Label htmlFor = "metadataUpload">Upload File</Label>
                  <Input type = "file" name = "metadata-file" id = "metadataUpload" onChange = { this.onChange } />
                </FormGroup>
                <Progress max  = "100" color = "success" value = { this.state.loaded } > { Math.round(this.state.loaded, 2) }%</Progress>
                <Button type = "submit" size = "sm" color = "primary">Submit</Button>
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

export default Choose_Metadata;