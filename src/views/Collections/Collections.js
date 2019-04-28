import React, { Component, lazy, Suspense } from 'react';
import { Bar, Line } from 'react-chartjs-2';
import {
  Button,
  Col,
  Card,
  CardHeader,
  CardBody,
  Modal,
  Form,
  Progress,
  Input,
  Label,
  FormGroup,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Table,
} from 'reactstrap';
import axios from 'axios';

class Collections extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showAdd: false,
      showEdit: false,
      showDelete: false,
      collections: {},
      tableBody: [],
      corpusName: '',       // name of corpus to be uploaded/added
      selectedFiles: null,  // selected files to upload
      loaded: 0,            // percentage of files that were uploaded

    };

    this.toggleAddModal = this.toggleAddModal.bind(this);
    this.openEditModal = this.openEditModal.bind(this);
    this.closeEditModal = this.closeEditModal.bind(this);
    this.openDeleteModal = this.openDeleteModal.bind(this);
    this.closeDeleteModal = this.closeDeleteModal.bind(this);

    this.addCollection = this.addCollection.bind(this);
    this.deleteCollection = this.deleteCollection.bind(this);
    this.editCollection = this.editCollection.bind(this);
  }

  // Get our data once the component mounts
  componentDidMount() {
    axios.get('/get_collections')
      .then(res => this.setState({ collections: res.data }))
      .then(data => this.updateTableBody(data))
      .catch(err => console.log("ERROR: cannot get collections (" + err + ")"));
  }

  // Fills the keyword list table with the relevant data
  updateTableBody() {
    const collections = this.state.collections;
    const tableBody = [];

    for (var k in collections) {
      const item = collections[k];
      tableBody.push(<tr id = { item['id'] }><tr>{ item['id'] }</tr><td>{ item['name'] }</td><td>{ item['collection-count'] }</td><td>{ item['description'] }</td><td>{ item['themes'] }</td><td>{ item['notes'] }</td><td><Button class = "link" onClick = {() => this.openEditModal(item['id'])}><i className = "icon-pencil"></i></Button><Button class = "link" onClick = {() => this.openDeleteModal(item['id'])}><i className = "icon-trash"></i></Button></td></tr>);
    }
    
    this.setState({ tableBody: tableBody });
  }

  // Edits the collection in question
  editCollection = (e) => {
    e.preventDefault();

    var newCollections = this.state.collections;
    var id = this.state.editCollectionID;
    newCollections[id]['name'] = this.state.editCollectionName;
    newCollections[id]['shortened-name'] = this.state.editCollectionShortenedName;
    newCollections[id]['description'] = this.state.editCollectionDescription;
    newCollections[id]['themes'] = this.state.editCollectionThemes;
    newCollections[id]['notes'] = this.state.editCollectionNotes;

    var newData = {
      "name": newCollections[id]['name'],
      "shortened-name": newCollections[id]['shortened-name'],
      "description": newCollections[id]['description'],
      "themes": newCollections[id]['themes'],
      "notes": newCollections[id]['notes']
    };

    // // Sends it to the backend
    // axios.post('/add_collection', {
    //   id: id,
    //   data: newData
    // })
    // .then(function (res) {
    //   console.log("Successfully added keywords");
    // })
    // .catch(function (err) {

    // });

    // this.updateTableBody();

    // this.setState({ 
    //   lists: newLists,
    //   showEdit: false
    // });
  }

  // Delete the keyword list in question
  deleteCollection() {
    var id = this.state.deleteListId;
    console.log(id);
  //   var newLists = {};
  //   for (var k in this.state.lists) {
  //     if (k == id) continue;
  //     newLists[k] = this.state.lists[k];
  //   }
  //   this.setState({ 
  //     lists: newLists,
  //   });

  //   // Sends it to the backend
  //   axios.post('/delete_keywords', {
  //     id: id
  //   })
  //   .then(function (res) {
  //     console.log("Successfully deleted keywords");
  //   })
  //   .catch(function (err) {

  //   });

  //   this.updateTableBody();

  //   this.setState({ showDelete: false });
  //   window.location.reload();
  }

  // Opens the edit modal
  openEditModal(id) {
    var currData = this.state.collections[id];

    this.setState({
      editCollectionID: id,
      editCollectionName: currData['name'],
      editCollectionShortenedName: currData['shortened-name'],
      editCollectionDescription: currData['description'],
      editCollectionThemes: currData['themes'],
      editCollectionNotes: currData['notes'],
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
      case 'file':
        this.setState({
          selectedFiles: e.target.files,
        });
        break;
      case 'other':
        break;
      default:
        this.setState({ [e.target.name]: e.target.value });
    }
  }

  // Event to submit the file upload data to the server
  onFileSubmit = (e) => {
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
        this.setState({ disabledNext: false });
    });
  }

  // Adds the new keyword list
  // TODO: Add verification
  addCollection = (e) => {
    e.preventDefault();
    
    // // Gets current date
    // var today = new Date();
    // var dd = String(today.getDate()).padStart(2, '0');
    // var mm = String(today.getMonth() + 1).padStart(2, '0');
    // var yyyy = today.getFullYear();
    // var date = mm + '/' + dd + '/' + yyyy;

    // var includeList = this.state.addListInclude.split(","); // needs to be comma-separated
    // var newIncludeList = [];
    // for (var i = 0; i < includeList.length; i++) {
    //   var keyword = includeList[i].trim();
    //   if (keyword == '') continue;
    //   newIncludeList.push(keyword);
    // }

    // var newExcludeList = [];
    // if (this.state.addListExclude != undefined) {
    //   var excludeList = this.state.addListExclude.split(","); // needs to be comma-separated
      
    //   for (var i = 0; i < excludeList.length; i++) {
    //     var keyword = excludeList[i].trim();
    //     if (keyword == '') continue;
    //     newExcludeList.push(keyword);
    //   }
    // }

    // var newData = {
    //   "name": this.state.addListName,
    //   "version": this.state.addListVersion,
    //   "date-added": date,
    //   "include": newIncludeList,
    //   "exclude": newExcludeList
    // };

    // var id = this.state.addListName + '-' + this.state.addListVersion;

    // // Sends it to the backend
    // axios.post('/add_keywords', {
    //   id: id,
    //   data: newData
    // })
    // .then(function (res) {
    //   console.log("Successfully added keywords");
    // })
    // .catch(function (err) {

    // });

    // // Updates the table
    // var newLists = this.state.lists;
    // newLists[id] = newData;
    // this.setState({ lists: newLists });
    // this.updateTableBody();

    // // Closes modal
    // this.setState(prevState => ({
    //   showAdd: !prevState.showAdd
    // }));
  }

  render() {
    return (
      <div>
        
        <Col>
          <Card>
            <CardHeader>Collections</CardHeader>
            <CardBody>
              <Modal isOpen = { this.state.showEdit }>
                <ModalHeader>Edit Collection</ModalHeader>
                <ModalBody>
                  <Form onSubmit = { this.editCollection } className = "form-horizontal">
                    <FormGroup row>
                      <Label htmlFor = "editCollectionName">Name</Label>
                      <Input type = "text" name = "editCollectionName" id = "editCollectionName" onChange = { this.onChange } value = { this.state.editCollectionName } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editCollectionShortenedName">Shortened Name</Label>
                      <Input type = "text" name = "editCollectionShortenedName" id = "editCollectionShortenedName" onChange = { this.onChange } value = { this.state.editCollectionShortenedName } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editCollectionDescription">Description</Label>
                      <Input type = "textarea" name = "editCollectionDescription" id = "editCollectionDescription" onChange = { this.onChange } value = { this.state.editCollectionDescription } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editCollectionThemes">Themes</Label>
                      <Input type = "textarea" name = "editCollectionThemes" id = "editCollectionThemes" onChange = { this.onChange } value = { this.state.editCollectionThemes } />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "editCollectionNotes">Notes</Label>
                      <Input type = "textarea" name = "editCollectionNotes" id = "editCollectionNotes" onChange = { this.onChange } value = { this.state.editCollectionNotes } />
                    </FormGroup>
                    <Button type = "submit" size = "sm" color = "primary">Save</Button>
                  </Form>
                </ModalBody>
                <ModalFooter>
                  <Button size = "sm" color = "secondary" onClick = { this.closeEditModal }>Cancel</Button>
                </ModalFooter>
              </Modal>
              <Modal isOpen = { this.state.showDelete }>
                <ModalHeader>Delete Collection</ModalHeader>
                <ModalBody>
                  <p> Are you sure you want to delete the keyword list?</p>
                  <Button size = "sm" color = "secondary" onClick = { this.deleteCollection }>
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
                <ModalHeader toggle = { this.toggleAddModal }>Add New Collection</ModalHeader>
                <ModalBody>
                  <Form onSubmit = { this.addCollection } className = "form-horizontal">
                    <FormGroup row>
                      <Label htmlFor = "corpusName">ID</Label>
                      <Input type = "text" id = "corpusName" name = "corpusName" onChange = { this.onChange } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addCollectionName">Name</Label>
                      <Input type = "text" name = "addCollectionName" id = "addCollectionName" onChange = { this.onChange } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addCollectionShortenedName">Shortened Name</Label>
                      <Input type = "text" name = "addCollectionShortenedName" id = "addCollectionShortenedName" onChange = { this.onChange } required />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addCollectionDescription">Description</Label>
                      <Input type = "textarea" name = "addCollectionDescription" id = "addCollectionDescription" onChange = { this.onChange } />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addCollectionThemes">Themes</Label>
                      <Input type = "textarea" name = "addCollectionThemes" id = "addCollectionThemes" onChange = { this.onChange } />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "addCollectionNotes">Themes</Label>
                      <Input type = "textarea" name = "addCollectionNotes" id = "addCollectionNotes" onChange = { this.onChange } />
                    </FormGroup>
                    <FormGroup row>
                      <Label htmlFor = "corpusUpload">Upload Files</Label>
                      <Input type = "file" name = "file" id = "corpusUpload" onChange = { this.onChange } webkitdirectory multiple />
                    </FormGroup>
                    <Button size = "sm" onClick = { this.onFileSubmit } color = "primary">Upload Files</Button>
                    <Progress max = "100" color = "success" value = { this.state.loaded } > { Math.round(this.state.loaded, 2) }%</Progress>
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
                    <th>ID</th>
                    <th>Name</th>
                    <th>Collection Count</th>
                    <th>Description</th>
                    <th>Themes</th>
                    <th>Notes</th>
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

export default Collections;
