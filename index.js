const express = require('express');
const path = require('path');
const app = express();
var bodyParser = require('body-parser');
const multer = require('multer');
const cors = require('cors');
var fs = require('fs');
var axios = require('axios');

// Serve static files from the React app
app.use(express.static(path.join(__dirname, '/build')));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors());

// Current variables
var corpus = [];
var keywords = "";
var metadata = "";

// Specifies storage for multer upload
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
		corpus.push(currDir);
		cb(null, currDir);
	},
	filename: (req, file, cb) => {
		cb(null, file.originalname);
	},
});
const corpusUpload = multer({ storage }).array('file');
const metadataUpload = multer({ storage }).single('metadata');

// The "catchall" handler: for any request that doesn't
// match one above, send back React's index.html file.
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname+'/build/index.html'));
});

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

// Uploads metadata
app.post('/upload-metadata', function (req, res) {
	metadataUpload(req, res, function (err) {
		if (err instanceof multer.MulterError) {
			return res.status(500).json(err);
		} else if (err) {
			return res.status(500).json(err);
		}
		return res.status(200).send(req.file);
	});
});


// Chooses the keyword list
app.post('/choose-keywords', function (req, res) {
	console.log(req.body);
});


const port = process.env.PORT || 5000;
app.listen(port);

console.log(`OHTAP Subcorpora Tool launched at localhost:${port}`);