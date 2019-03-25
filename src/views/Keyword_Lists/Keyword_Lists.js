import React, { Component, lazy, Suspense } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Button,
  Col,
  Card,
  CardHeader,
  CardBody,
  Modal,
  Table,
} from 'reactstrap';
import axios from 'axios';

class Keyword_Lists extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showAdd: true,
      lists: {},
      tableBody: []
    };

    // Binds modal functions
    // this.handleShow = this.handleShow.bind(this);
    // this.handleClose = this.handleClose.bind(this);
    this.closeAddModal = this.closeAddModal.bind(this);
  }

  // Get our data once the component mounts
  componentDidMount() {
    axios.get('/get_keywords')
      .then(res => this.setState({ lists: res.data }))
      .then(data => this.updateTableBody(data))
      .catch(err => console.log("Error getting keywords: " + err));
  }

  // Fills the keyword list table with the relevant data
  updateTableBody() {
    const lists = this.state.lists;
    const tableBody = [];
    for (var k in lists) {
      const item = lists[k];
      tableBody.push(<tr id = { k }><td>{ item['name'] }</td><td>{ item['version'] }</td><td>{ item['date-added'] }</td><td><i id = "edit-{ k }" className="icon-pencil"></i><i id = "delete-{ k }" className="icon-trash"></i></td></tr>);
    }
    this.setState({ tableBody: tableBody });
  }

  // Closes the add modal
  closeAddModal() {
    this.setState({ showAdd: false });
  }

  // Shows the add modal
  openAddModal() {
    console.log("HELLO");
    this.setState({ showAdd: true });
  }

  // Closes the modal
  handleClose() {
    this.setState({ show: false });
  }

  // Shows the modal
  handleShow() {
    this.setState({ show: true });
  }

  // Opens the editing modal
  openEditingModal(id) {

  }

  render() {
    return (
      <div>
        <Modal show = "true" visible = "true">
          <div>
            <h1>Add New Keyword List</h1>
            <p>Hellooo</p>
            <Button variant = "primary" onClick = {() => this.closeAddModal()}>Close</Button>
          </div>
        </Modal>
        <Col>
          <Card>
            <CardHeader>Keyword Lists</CardHeader>
            <CardBody>
              <Button class="add-button" variant="primary" onClick={() => this.openAddModal()}>
                <i className="icon-plus"></i>Add New List
              </Button>
              <Table responsive>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Version</th>
                    <th>Date added</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  { this.state.tableBody }
                </tbody>
              </Table>
            </CardBody>
          </Card>
        </Col>
        <Col>
          <Card>
            <CardHeader>Edit List</CardHeader>
            <CardBody>

            </CardBody>
          </Card>
        </Col>
      </div>
    );
  }
}

export default Keyword_Lists;
