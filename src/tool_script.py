# NOTE: It is the historian's job to make sure that keywords are not repetitive (they are
# otherwise double-counted into counts).

from collections import defaultdict
from collections import OrderedDict
import os
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from unidecode import unidecode
import csv
from bs4 import BeautifulSoup, Tag
import sys
import json

NUM_TOP_WORDS = 20 # The number of top words that we want from each file
CONTEXT_WORDS_AROUND = 50
MAX_EXCLUDE_REGEX_LENGTH = 50
punctuation = ['\.', '/', '\?', '\-', '"', ',', '\\b'] # Punctuation we use within our regexes

# Communicates with the Node.js backend with a JSON string
def print_message(_type, content):
	message = {
		"type": _type,
		"content": content
	}
	print(json.dumps(message))

# Downloads the NLTK libraries
def download_nltk():
	print_message("progress-message", "Downloading relevant libraries...")
	nltk.download('averaged_perceptron_tagger')
	nltk.download('stopwords')
	nltk.download('punkt')

	print_message("progress", 2)

# Reads in arguments into the directories, words, and metadata file needed for the runs
def read_arguments():
	print_message("progress_message", "Reading in run data...")
	data = json.loads(sys.argv[1])
	collections = data['collections']
	keywords = data['keywordList']
	metadata = data['metadata']
	runId = data['id']

	print_message("progress", 4)

	return runId, collections, keywords, metadata

# Creates a new folder to store the final data for the current run
def create_run_directory(runId):
	print_message("progress-message", "Creating a directory to store run results...")
	dirname = os.getcwd() + "/data/runs/" + runId
	os.mkdir(dirname)
	print_message("progress", 5)

	return dirname

# Downloads relevant libraries and otherwise sets us up for a successful run
def set_up():
	print_message("progress-message", "Setting up the run...")
	# download_nltk()
	runId, collections, keywords, metadata = read_arguments()
	runDirname = create_run_directory(runId)

	return runId, collections, keywords, metadata, runDirname

# Does one run with one collection and one keyword list
def create_new_run(c, k, metadata):
	print_message("progress-message", "Starting the run for collection " + c["id"] + " and keywords " + k["name"] + " v" + k["version"] + "...")

def main():
	print_message("progress-message", "")
	runId, collections, keywords, metadata, runDirname = set_up()

	progressPerRun = int(95/(len(c) * len(k)))
	totalProgress = 5
	for c in collections:
		for k in keywords:
			create_new_run(c, k, metadata)
			totalProgress += progressPerRun
			print_message("progress", totalProgress)

	print_message("progress", 100)

if __name__ == '__main__':
	main()
