const express = require('express');
const path = require('path');
const app = express();
var bodyParser = require('body-parser');
const multer = require('multer');
const cors = require('cors');
var fs = require('fs');
var axios = require('axios');

/*** INITIALIZATION AND APPLICATION STARTUP ***/

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '/build')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

// Data files for session
const dataFile = './data/session.json';
var data = {};

// Current data for current run
var currRun = {
	collections: [],
	metadata: "",
	keywordList: {}
};

/*
 * Initializes the data into the session by reading in the current collections
 * located in data/corpus-files. It also reads in the data located in the data
 * file and keeps that in backend memory.
 */
 function initializeData() {
 	console.log("Initializing data from session.json...")
 	var rawData = fs.readFileSync(dataFile);
 	data = JSON.parse(rawData);

 	// Reads in current collections located in data/corpus-files
 	let collections = fs.readdirSync('./data/corpus-files').filter(function (file) {
		return fs.statSync('./data/corpus-files/' + file).isDirectory();
	});

	// Deletes any collections in the data JSON structure that don't appear
	// within our folder and prints a warning message.
	var remove = [];
	for (var c in data['collections']) {
		if (!collections.includes(c)) {
			remove.push(c);
		}
	}
	for (var i in remove) {
		delete data[remove[i]];
		console.log('WARNING: ' + remove[i] + ' collection doesn\'t exist in data/corpus-files. Please either add the files or delete the entry from session.json.');
	}

	console.log("Initialized data:");
	console.log(JSON.stringify(data) + '\n');
 }

// Serves the session
const port = process.env.PORT || 5000;
app.listen(port, function() {
	// Creates a session JSON file if one does not exist and writes to it
	const rawContents = `{ 
		'keyword-lists': {},
		'past-runs': {},
		'collections': {}
	}`;

	if (!fs.existsSync(dataFile)) {
		fs.writeFile(dataFile, rawContents, { flag: 'wx' }, function (err) {
		    if (err) throw err;
		});
		initializeData();
	} else {
		initializeData();
	}
});
console.log(`OHTAP Subcorpora Tool launched at localhost:${port}\n`);

/** FUNCTIONS FOR UPDATING SESSION.JSON **/

// Writes to the session.json file
function saveToSessionFile() {
	fs.writeFile(dataFile, JSON.stringify(data), function (err) {
		if (err) {
			console.log("ERROR: could not save to session.json (" + err + ")");
		}
	});
}

/** PYTHON PROCESS FOR RUNNING SUBCORPORA TOOL **/

/** UPLOADING METADATA FILES **/

/** GETTING AND UPDATING KEYWORD LISTS **/

// Retrieves all the keyword lists in JSON format
app.get("/get_keywords", function (req, res) {
	res.status(200).send(data["keyword-lists"]);
});

// Adds new keywords
app.post('/add_keywords', function (req, res) {
	var currData = req.body;
	data['keyword-lists'][currData.id] = currData.data;
	res.status(200).send();
	saveToSessionFile()
});

// Deletes the keyword list
app.post('/delete_keywords', function (req, res) {
	var currData = req.body;
	delete data['keyword-lists'][currData.id];
	saveToSessionFile()
});

/** GETTING, UPLOADING, AND UPDATING COLLECTIONS **/

// Specifies storage for multer uploads
var corpusDir = './data/corpus-files';
const storage = multer.diskStorage({
	destination: (req, file, cb) => {
		// Creates the directory that they are meant to exist in
		// TODO: Add error checking for duplicate in form
		var name = req.body.corpusName.toLowerCase().replace(" ", "_");
		var currDir = corpusDir.concat("/", name);
		if (!fs.existsSync(currDir)) {
			fs.mkdirSync(currDir);
		}
		cb(null, currDir);
	},
	filename: (req, file, cb) => {
		cb(null, file.originalname);
	},
});
const corpusUpload = multer({ storage }).array('file');

// Uploads file to data/corpus-files folder
app.post('/upload-corpus', function (req, res) {
	// Uploads the files
	corpusUpload(req, res, function (err) {
		if (err instanceof multer.MulterError) {
			return res.status(500).json(err);
		} else if (err) {
			return res.status(500).json(err);
		}
		return res.status(200).send(req.file);
	});
});

// Retrieves all the collections in JSON format
app.get("/get_collections", function (req, res) {
	res.status(200).send(data["collections"]);
});

/** GETTING PAST RUNS **/

app.get("/get_past_runs", function (req, res) {
	res.status(200).send(data["past-runs"]);
});

/** GENERAL PAGE SERVICE **/

// The "catchall" handler: for any request that doesn't
// match one route above, send back React's index.html file.
// This needs to be the last route in index.js.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname+'/build/index.html'));
});
