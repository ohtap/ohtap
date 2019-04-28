import React, { Component } from 'react';
import {
  Button,
  Col,
  Card,
  CardHeader,
  CardBody,
  Modal,
  Form,
  Input,
  Label,
  FormGroup,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Table,
} from 'reactstrap';
import axios from 'axios';

class Keyword_Lists extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showAdd: false,
      showEdit: false,
      showDelete: false,
      lists: {},
      tableBody: []
    };

    this.toggleAddModal = this.toggleAddModal.bind(this);
    this.openEditModal = this.openEditModal.bind(this);
    this.closeEditModal = this.closeEditModal.bind(this);
    this.openDeleteModal = this.openDeleteModal.bind(this);
    this.closeDeleteModal = this.closeDeleteModal.bind(this);

    this.addNewKeywordList = this.addNewKeywordList.bind(this);
    this.deleteKeywordList = this.deleteKeywordList.bind(this);
    this.editKeywordList = this.editKeywordList.bind(this);
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
      const name = item['name'] + "-" + item['version'];
      tableBody.push(<tr id = { name }><td>{ item['name'] }</td><td>{ item['version'] }</td><td>{ item['date-added'] }</td><td><Button class = "link" onClick = {() => this.openEditModal(name)}><i className = "icon-pencil"></i></Button><Button class = "link" onClick = {() => this.openDeleteModal(name)}><i className = "icon-trash"></i></Button></td></tr>);
    }

    this.setState({ tableBody: tableBody });
  }

  // Edits the keyword list in question
  editKeywordList = (e) => {
    e.preventDefault();

    var newLists = this.state.lists;
    var id = this.state.editListId;
    newLists[id]['name'] = this.state.editListName;
    newLists[id]['version'] = this.state.editListVersion;

    var includeList = this.state.editListInclude.split(","); // needs to be comma-separated
    var newIncludeList = [];
    for (var i = 0; i < includeList.length; i++) {
      var keyword = includeList[i].trim();
      if (keyword === '') continue;
      newIncludeList.push(keyword);
    }
    var excludeList = this.state.editListExclude.split(","); // needs to be comma-separated
    var newExcludeList = [];
    for (var i = 0; i < excludeList.length; i++) {
      var keyword = excludeList[i].trim();
      if (keyword == '') continue;
      newExcludeList.push(keyword);
    }

    newLists[id]['include'] = newIncludeList;
    newLists[id]['exclude'] = newExcludeList;

    var newData = {
      "name": newLists[id]['name'],
      "version": newLists[id]['version'],
      "date-added": newLists[id]['date-added'],
      "include": newLists[id]['include'],
      "exclude": newLists[id]['exclude']
    };

    // Sends it to the backend
    axios.post('/add_keywords', {
      id: id,
      data: newData
    })
    .then(function (res) {
      console.log("Successfully added keywords");
    })
    .catch(function (err) {

    });

    this.updateTableBody();

    this.setState({ 
      lists: newLists,
      showEdit: false
    });
  }

  // Delete the keyword list in question
  deleteKeywordList() {
    var id = this.state.deleteListId;
    var newLists = {};
    for (var k in this.state.lists) {
      if (k == id) continue;
      newLists[k] = this.state.lists[k];
    }
    this.setState({ 
      lists: newLists,
    });

    // Sends it to the backend
    axios.post('/delete_keywords', {
      id: id
    })
    .then(function (res) {
      console.log("Successfully deleted keywords");
    })
    .catch(function (err) {

    });

    this.updateTableBody();

    this.setState({ showDelete: false });
    window.location.reload();
  }

  // Opens the edit modal
  openEditModal(id) {
    var currData = this.state.lists[id];

    this.setState({
      editListId: id,
      editListName: currData['name'],
      editListVersion: currData['version'],
      editListInclude: currData['include'].join(', '),
      editListExclude: currData['exclude'].join(', '),
      showEdit: true
    });
  }

  // Closes the edit modal
  closeEditModal() {
    this.setState({ showEdit: false });
  }

  // Opens the delete modal
  openDeleteModal(id) {
    this.setState({ deleteListId: id });
    this.setState({ 
      showDelete: true
    });
  }

  // Closes the delete modal
  closeDeleteModal() {
    this.setState({ showDelete: false });
  }

  // Toggles the add modal
  toggleAddModal() {
    this.setState(prevState => ({
      showAdd: !prevState.showAdd
    }));
  }

  // onChange event to update state when form inputs change
  onChange = (e) => {
    switch (e.target.name) {
      case 'other':
        break;
      default:
        this.setState({ [e.target.name]: e.target.value });
    }
  }

  // Adds the new keyword list
  // TODO: Add verification
  addNewKeywordList = (e) => {
    e.preventDefault();
    
    // Gets current date
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    var date = mm + '/' + dd + '/' + yyyy;

    var includeList = this.state.addListInclude.split(","); // needs to be comma-separated
    var newIncludeList = [];
    for (var i = 0; i < includeList.length; i++) {
      var keyword = includeList[i].trim();
      if (keyword == '') continue;
      newIncludeList.push(keyword);
    }

    var newExcludeList = [];
    if (this.state.addListExclude != undefined) {
      var excludeList = this.state.addListExclude.split(","); // needs to be comma-separated
      
      for (var i = 0; i < excludeList.length; i++) {
        var keyword = excludeList[i].trim();
        if (keyword == '') continue;
        newExcludeList.push(keyword);
      }
    }

    var newData = {
      "name": this.state.addListName,
      "version": this.state.addListVersion,
      "date-added": date,
      "include": newIncludeList,
      "exclude": newExcludeList
    };

    var id = this.state.addListName + '-' + this.state.addListVersion;

    // Sends it to the backend
    axios.post('/add_keywords', {
      id: id,
      data: newData
    })
    .then(function (res) {
      console.log("Successfully added keywords");
    })
    .catch(function (err) {

    });

    // Updates the table
    var newLists = this.state.lists;
    newLists[id] = newData;
    this.setState({ lists: newLists });
    this.updateTableBody();

    // Closes modal
    this.setState(prevState => ({
      showAdd: !prevState.showAdd
    }));
  }

  render() {
    return (
      <div>
        
        <Col>
          <Card>
            <CardHeader>Keyword Lists</CardHeader>
            <CardBody>
              <Modal isOpen = { this.state.showEdit }>
                <ModalHeader>Edit Keyword List</ModalHeader>
                <ModalBody>
                  <Form onSubmit = { this.editKeywordList } className = "form-horizontal">
                    <FormGroup row>
                      <Label htmlFor = "editListName">Name</Label>
                      <Input type = "text" name = "editListName" id = "editListName" onChange = { this.onChange } value = { this.state.editListName } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editListVersion">Version</Label>
                      <Input type = "text" name = "editListVersion" id = "editListVersion" onChange = { this.onChange } value = { this.state.editListVersion } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editListInclude">Included keywords (comma separated)</Label>
                      <Input type = "textarea" name = "editListInclude" id = "editListInclude" onChange = { this.onChange } value = { this.state.editListInclude } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editListExclude">Excluded keywords (comma separated)</Label>
                      <Input type = "textarea" name = "editListExclude" id = "editListExclude" onChange = { this.onChange } value = { this.state.editListExclude } />
                    </FormGroup>
                    <Button type = "submit" size = "sm" color = "primary">Save</Button>
                  </Form>
                </ModalBody>
                <ModalFooter>
                  <Button size = "sm" color = "secondary" onClick = { this.closeEditModal }>Cancel</Button>
                </ModalFooter>
              </Modal>
              <Modal isOpen = { this.state.showDelete }>
                <ModalHeader>Delete Keyword List</ModalHeader>
                <ModalBody>
                  <p> Are you sure you want to delete the keyword list?</p>
                  <Button size = "sm" color = "secondary" onClick = { this.deleteKeywordList }>
                    Delete
                  </Button>
                  <Button size = "sm" color = "secondary" onClick = { this.closeDeleteModal }>
                    Cancel
                  </Button>
                </ModalBody>
              </Modal>
              <Button variant="primary" onClick={ this.toggleAddModal }>
                <i className="icon-plus"></i>&nbsp;Add New List
              </Button>
              <Modal isOpen = { this.state.showAdd } toggle = { this.toggleAddModal }>
                <ModalHeader toggle = { this.toggleAddModal }>Add New Keyword List</ModalHeader>
                <ModalBody>
                  <Form onSubmit = { this.addNewKeywordList } className = "form-horizontal">
                    <FormGroup row>
                      <Label htmlFor = "addListName">Name</Label>
                      <Input type = "text" name = "addListName" id = "addListName" onChange = { this.onChange } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addListVersion">Version</Label>
                      <Input type = "text" name = "addListVersion" id = "addListVersion" onChange = { this.onChange } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addListInclude">Included keywords (comma separated)</Label>
                      <Input type = "textarea" name = "addListInclude" id = "addListInclude" onChange = { this.onChange } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addListExclude">Excluded keywords (comma separated)</Label>
                      <Input type = "textarea" name = "addListExclude" id = "addListExclude" onChange = { this.onChange } />
                    </FormGroup>
                    <Button type = "submit" size = "sm" color = "primary">Save</Button>
                  </Form>
                </ModalBody>
                <ModalFooter>
                  <Button size = "sm" color = "secondary" onClick = { this.toggleAddModal }>Cancel</Button>
                </ModalFooter>
              </Modal>
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
      </div>
    );
  }
}

export default Keyword_Lists;
