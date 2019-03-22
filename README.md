# OHTAP Subcorpora Tool
Hilary Sun (hsun3@cs.stanford.edu), Stanford Computer Science, Winter/Spring 2019

## About

A web application to generation subcorporas for oral history analyses. 

### Design Document

Please see our design document [here](https://docs.google.com/document/d/1Y2Y7lZVFSKBxc57EO8zOrN_WNm-I7aYD5-6W2gl3GNA/edit).

## Use Cases

Can be used locally by downloading the repository and running it.

## Sample Application

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

### Usage

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

We used some aspects of CoreUI for the frontend, which is copyright 2018 creativeLabs Łukasz Holeczek and released under [the MIT license](https://github.com/coreui/coreui-free-bootstrap-admin-template/blob/master/LICENSE).

Library icon made by [Icon Pond]("https://www.flaticon.com/authors/popcorns-arts") from [Flaticon]("https://www.flaticon.com/"). It is licensed by [CC 3.0 BY]("http://creativecommons.org/licenses/by/3.0/").