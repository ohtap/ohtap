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
data_dirname = os.getcwd() + "/data/"

# Prints out a JSON string that is then read by the Node.js backend.
def print_message(_type, content):
	message = {
		"type": _type,
		"content": content
	}
	print(json.dumps(message))

# Downloads the NLTK libraries.
def download_nltk():
	print_message("progress-message", "Downloading relevant libraries...")

	nltk.download('averaged_perceptron_tagger')
	nltk.download('stopwords')
	nltk.download('punkt')

	print_message("progress", 2)

# Reads in arguments into the directories, words, and metadata file needed for the runs.
def read_arguments():
	print_message("progress_message", "Reading in run data...")

	data = json.loads(sys.argv[1])
	collections = data['collections']
	keywords = data['keywordList']
	metadata_file = data['metadata']
	runId = data['id']

	print_message("progress", 4)

	return runId, collections, keywords, metadata_file

# Creates a new folder to store the final data for the current run.
def create_run_directory(runId):
	print_message("progress-message", "Creating a directory to store run results...")
	dirname = data_dirname + "runs/" + runId
	os.mkdir(dirname)
	print_message("progress", 5)

	return dirname

# Gets punctuation joined by bars (this is punctuation that we decide to count as separation!)
def get_punctuation_for_regex():
	return "|".join(punctuation)

# Converts the keyword list to Python regex form. Returns the full list of words and the 
# included and excluded regexes.
def convert_keywords(keywords):
	converted_keywords = []

	for k in keywords:
		# Sorts the included words backwards to make sure we get the longer words first
		included_words = k["include"]
		included_words = sorted(included_words, key=lambda l: (len(l), l), reverse=True)
		punc = get_punctuation_for_regex()
		included_regexes = []
		for w in included_words:
			r = r'(?:{})({})(?:{})'.format(punc, w.replace("*", "[a-zA-Z]*"), punc)
			included_regexes.append(r)

		excluded_words = k["exclude"]
		excluded_regexes = []
		for w in excluded_words:
			r = r"\b{}\b".format(w.replace("*", "[a-zA-Z]*"))
			excluded_regexes.append(w)

		k["included_regexes"] = included_regexes
		k["include"] = included_words
		k["excluded_regexes"] = excluded_regexes
		converted_keywords.append(k)

	return converted_keywords

# Reads all the text from each text file in the corpus directory. TODO: Resolve utf-8.
def read_corpuses(collections):
	new_collections = []
	for c in collections:
		directory = data_dirname + "corpus-files/" + c["id"]
		filenames = []
		content = []

		for file in os.listdir(directory):
			if ".txt" not in file: continue
			filenames.append(file)

			with open("{}/{}".format(directory, file), "r", encoding = "ISO-8859-1") as f:
				content.append(f.read())

		c["filenames"] = filenames
		c["content"] = content
		new_collections.append(c)

	return new_collections

# Gets the files for inclusion--excludes any files that are only male interviewees or
# interviews with no transcripts.
def get_included_files(collections, df):
	files_for_inclusion = {} # Final list of files for inclusion

	# Statistics about file inclusion/exclusion
	num_files_no_transcript = {} # Total number of files in collection with no transcript
	people = {} # Information about individual people (only "Sex" == "Female" and "Sex" == "Unknown")
	male_interviews = {} # Interviews that include males
	male_plus_interviews = {} # Interviews with both male and non-male interviews
	interview_years = {}
	interview_years_by_file = {}

	filenames_map = {}
	for c in collections:
		curr_id = c["id"]
		files_for_inclusion[curr_id] = {}
		num_files_no_transcript[curr_id] = 0
		people[curr_id] = {}
		male_interviews[curr_id] = {}
		male_plus_interviews[curr_id] = {}
		interview_years[curr_id] = defaultdict(lambda:0)
		interview_years_by_file = defaultdict(lambda:{})

		for f in c["filenames"]:
			filenames_map[f] = curr_id

	for i, r in df.iterrows():
		f = r["project_file_name"]

		# Skips files with no project filename (shouldn't happen)
		if pd.isnull(f):
			continue

		# SKips files not in collection
		if f not in filenames_map:
			continue

		curr_c = filenames_map[f]

		# Skips files with no transcript
		no_transcript = r["no_transcript"]
		if not pd.isnull(no_transcript) and (no_transcript or no_transcript.strip() == "TRUE"):
			num_files_no_transcript[curr_c] += 1
			continue

		# If the interviewee is male, marks it and continues (as there may be the same file later on with a non-male interviewee)
		sex = r["sex"]
		if not pd.isnull(sex) and sex.strip() == "Male":
			male_interviews[curr_c][f] = 1
			if f in files_for_inclusion:
				male_plus_interviews[curr_c][f] = 1 # Means it contains both male and non-male
			continue

		# If the current interviewee is non-male and the interview has a male, mark it
		if f in male_interviews[curr_c]:
			male_plus_interviews[curr_c][f] = 1
			male_interviews[curr_c][f] = 0

		# At this point, we have a new interview (not previously added) with at least one non-male
		# interviewee we want to add!
		interviewee_name = r["interviewee_name"]
		if interviewee_name not in people[curr_c]:
			birth_decade = r["birth_decade"]
			education = r["education"]
			identified_race = r["identified_race"]
			interviewee_birth_country = r["interviewee_birth_country"]

			curr_person = {}
			curr_person["birth_decade"] = birth_decade if not pd.isnull(birth_decade) else ""
			curr_person["education"] = education if not pd.isnull(education) else ""
			curr_person["identified_race"] = identified_race if not pd.isnull(identified_race) else ""
			curr_person["sex"] = sex if not pd.isnull(sex) else ""
			curr_person["birth_country"] = interviewee_birth_country if not pd.isnull(interviewee_birth_country) else ""

			people[curr_c][interviewee_name] = curr_person

		files_for_inclusion[curr_c][f] = 1

		date_of_first_interview = r["date_of_first_interview"]
		if pd.isnull(date_of_first_interview):
			interview_years[curr_c]["Not given"] += 1
			interview_years_by_file[curr_c][f] = "Not given"
		else:
			year = date_of_first_interview.split("/")[2]

			# Attempts to fix the two numbered ones; assumes anything that is 00-19 is in 2000s
			if len(year) == 2:
				if int(year) <= 19:
					year = "20{}".format(year)
				else:
					year = "19{}".format(year)

				interview_years[curr_c][year] += 1
				interview_years_by_file[curr_c][f] = year

	print_message("files_for_inclusion", files_for_inclusion)
	print_message("people", people)
	print_message("num_files_no_transcript", num_files_no_transcript)
	print_message("male_interviews", male_interviews)
	print_message("male_plus_interviews", male_plus_interviews)
	print_message("interview_years", interview_years)
	print_message("interview_years_by_file", interview_years_by_file)

	return files_for_inclusion, people, num_files_no_transcript, male_interviews, male_plus_interviews, interview_years, interview_years_by_file

# Reads in the metadata to collect statistics and excludes any files that are only male
# interviewees or interviews with no transcripts for each collection.
def read_metadata(collections, metadata_file):
	df = pd.read_csv(data_dirname + metadata_file, encoding = "utf-8", header = 0)
	files_for_inclusion, people, num_files_no_transcript, male_interviews, male_plus_interviews, interview_years, interview_years_by_file = get_included_files(collections, df)

	return files_for_inclusion

# Downloads relevant libraries and otherwise sets us up for a successful run.
def set_up():
	print_message("progress-message", "Setting up the run...")

	# download_nltk()
	runId, collections, keywords, metadata_file = read_arguments()
	runDirname = create_run_directory(runId)
	converted_keywords = convert_keywords(keywords)
	collections = read_corpuses(collections)
	metadata = read_metadata(collections, metadata_file)

	return runId, collections, keywords, metadata, runDirname

# Does one run with one collection and one keyword list.
def create_new_run(c, k, metadata):
	print_message("progress-message", "Starting the run for collection " + c["id"] + " and keywords " + k["name"] + " v" + k["version"] + "...")

def main():
	runId, collections, keywords, metadata, runDirname = set_up()

	progressPerRun = int(95/(len(collections) * len(keywords)))
	totalProgress = 5
	for c in collections:
		for k in keywords:
			create_new_run(c, k, metadata)
			totalProgress += progressPerRun
			print_message("progress", totalProgress)

	print_message("progress", 100)

if __name__ == '__main__':
	main()
