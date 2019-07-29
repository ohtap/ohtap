# OHTAP Subcorpora Tool
Hilary Sun (hsun3@cs.stanford.edu), Stanford Computer Science, Winter/Spring 2019

## About

A web application to generation subcorporas for oral history analyses. 

### Design Document

Please see our design document [here](https://docs.google.com/document/d/1Y2Y7lZVFSKBxc57EO8zOrN_WNm-I7aYD5-6W2gl3GNA/edit).

## Use Cases

Can be used locally by downloading the repository and running it.

## Sample Application (TBD)

A sample static web application is running at [https://ohtap-subcorpora-tool.herokuapp.com](https://docs.google.com/document/d/1Y2Y7lZVFSKBxc57EO8zOrN_WNm-I7aYD5-6W2gl3GNA/edit). This contains a few sample transcripts for you to play around with and explore the functionality of the subcorpora tool.

## Installation

### Clone repository

To clone the repository and install relevant packages onto your local machine, run:

```
# Clone the repository
$ git clone git@github.com:ohtap/subcorpora-tool.git

# Go into the project main folder
$ cd subcorpora-tool
```

You only need to clone it once.

## Usage

### Running the application

In order to build the static HTML files, run:

```
$ npm run build
```

You only need to run this once if you don't edit any of the files.

To run the local web application:

```
$ node index.js
```

You should see the line `OHTAP Subcorpora Tool launched` in the terminal after running this command if the web application is successfully running locally.

Open up your web browser to [https://localhost:5000](https://localhost:5000).

### Running the subcorpora tool

Navigate to the tab "Create a new run."

#### (1) vNaming your run

Give your run a name. It will automatically create a new run with the ID composed of the name, date, and time. This should be unique to each run, unless you somehow miraculously create multiple reports in the same second (or if you switch time zones and happen to do a run at the same time). The code for this page is in `/src/containers/CreateRun/CreateRun.js`.

#### (2) Selecting collections

Here you will select the collections that will be included in the run. There is a multiple selection tool. The code for this page is in `/src/containers/CreateRun/SelectCollections/SelectCollections.js`.

#### (3) Selecting keyword lists

Here you will select the keyword lists that will be included in the run. There is a multiple selection tool. The code for this page is in `/src/containers/CreateRun/SelectKeywords/SelectKeywords.js`.

#### (4) Selecting metadata

#### (5) Running the Python script

The subcorpora folder formed will be within the folder `data/subcorpora`.

### Adding, editing, and deleting keyword lists

Navigate to the tab "Keyword Lists." Add by clicking on the button "Add New Keyword List," edit by clicking on the pencil icon beside the relevant list, and delete by clicking on the trash can icon beside the relevant list.

### Viewing and clearing past runs

Navigate to the tab "Past Runs." Clear the list by clicking on the button "Clear past runs."

### Sharing data

All session data will be stored in `data/session.json`. This contains all the keyword lists, reports, collection names, etc. This is meant to be shareable between people to restore sessions.

They will not, however, be able to see the subcorpora formed.

## Directory structure
```
.
|	+--
+-- build		# Contains the built static HTML files
+-- public		# Contains default HTML
|	+--
+-- src 		# Contains all the React files
+-- .gitignore	# List of files and folders to ignore
+-- index.js 	# Main entry point
+-- README.md 	# Instructions the web app
+-- 
```

## Acknowledgements

