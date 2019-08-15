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
	runId = data['id']
	runName = data['name']
	runDate = data['date']
	collections = data['collections']
	keywords = data['keywordList']
	metadata_file = data['metadata']

	print_message("progress", 4)

	return runId, runName, runDate, collections, keywords, metadata_file

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
def get_included_files(collections, df, runJSON):
	files_for_inclusion = {} # Final list of files for inclusion

	# Statistics about file inclusion/exclusion
	num_files_no_transcript = {} # Total number of files in collection with no transcript
	people = {} # Information about individual people (only "Sex" == "Female" and "Sex" == "Unknown")
	male_interviews = {} # Interviews that include males
	male_plus_interviews = {} # Interviews with both male and non-male interviews
	interview_years = {}
	interview_years_by_file = {}

	# Needed information across all collections
	interview_years_all_collections = defaultdict(lambda:0)
	interviewee_metadata_all_collections = defaultdict(lambda:defaultdict(lambda:0))

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
		if interviewee_name not in people:
			birth_decade = r["birth_decade"]
			education = r["education"]
			identified_race = r["identified_race"]
			interviewee_birth_country = r["interviewee_birth_country"]

			curr_person = {}
			curr_person["birth_decade"] = birth_decade if not pd.isnull(birth_decade) else "Not given"
			curr_person["education"] = education if not pd.isnull(education) else "Not given"
			curr_person["identified_race"] = identified_race if not pd.isnull(identified_race) else "Not given"
			curr_person["sex"] = sex if not pd.isnull(sex) else "Not given"
			curr_person["birth_country"] = interviewee_birth_country if not pd.isnull(interviewee_birth_country) else "Not given"

			people[interviewee_name] = curr_person

			interviewee_metadata_all_collections["birth_decade"][curr_person["birth_decade"]] += 1
			interviewee_metadata_all_collections["education"][curr_person["education"]] += 1
			interviewee_metadata_all_collections["race"][curr_person["identified_race"]] += 1
			interviewee_metadata_all_collections["sex"][curr_person["sex"]] += 1
			interviewee_metadata_all_collections["birth_country"][curr_person["birth_country"]] += 1

		files_for_inclusion[curr_c][f] = 1

		date_of_first_interview = r["date_of_first_interview"]
		if pd.isnull(date_of_first_interview):
			interview_years[curr_c]["Not given"] += 1
			interview_years_by_file[curr_c][f] = "Not given"
			interview_years_all_collections["Not given"] += 1
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
				interview_years_all_collections[year] += 1

	# Updates the summary report data
	runJSON["summary-report"]["total-interviewees"] = len(people)
	runJSON["summary-report"]["time-range-interviews"] = interview_years_all_collections
	runJSON["summary-report"]["time-range-birth-year"] = interviewee_metadata_all_collections["birth_decade"]
	runJSON["summary-report"]["race"] = interviewee_metadata_all_collections["race"]
	runJSON["summary-report"]["sex"] = interviewee_metadata_all_collections["sex"]
	runJSON["summary-report"]["education"] = interviewee_metadata_all_collections["education"]
	runJSON["summary-report"]["birth_country"] = interviewee_metadata_all_collections["birth_country"]

	metadata = {
		"files_for_inclusion": files_for_inclusion,
		"people": people,
		"num_files_no_transcript": num_files_no_transcript,
		"male_interviews": male_interviews,
		"male_plus_interviews": male_plus_interviews,
		"interview_years": interview_years,
		"interview_years_by_file": interview_years_by_file
	}

	return metadata

# Reads in the metadata to collect statistics and excludes any files that are only male
# interviewees or interviews with no transcripts for each collection.
def read_metadata(collections, metadata_file, runJSON):
	df = pd.read_csv(data_dirname + metadata_file, encoding = "utf-8", header = 0)
	return get_included_files(collections, df, runJSON)

# Downloads relevant libraries and otherwise sets us up for a successful run.
def set_up(runJSON):
	print_message("progress-message", "Setting up the subcorpora run...")

	# download_nltk()
	runId, runName, runDate, collections, keywords, metadata_file = read_arguments()
	runJSON["id"] = runId
	runJSON["name"] = runName
	runJSON["date"] = runDate
	runJSON["metadata"] = metadata_file
	runJSON["collections"] =  [c["id"] for c in collections]
	runJSON["keyword-lists"] = [k["name"] + "-" + k["version"] for k in keywords]

	runDirname = create_run_directory(runId)
	runJSON["runDirname"] = runDirname

	runJSON["summary-report"] = {
		"total-collections": len(collections),
		"total-keywords": sum([len(k["include"]) for k in keywords]),
		"total-collections-with-keywords": 0,
		"total-interviews-with-keywords": 0
	}
	keyword_regexes = convert_keywords(keywords)
	collections = read_corpuses(collections)

	metadata = read_metadata(collections, metadata_file, runJSON)

	return collections, keywords, keyword_regexes, metadata, runDirname

# Gets n words before and after the match and returns them
def get_words_around(m_text, m_loc, content, n):
	before_text = content[:m_loc].split(" ")
	after_loc = m_loc + len(m_text)
	after_text = content[after_loc:].split(" ")

	before_len = len(before_text) - n
	if before_len < 0: 
		before_len = 0
	after_len = n if n <= len(after_text) else len(after_text)

	return " ".join(before_text[before_len:]), m_text, " ".join(after_text[:after_len])

# Checks to see if there's anything it needs to exclude
def need_to_exclude(before, after, m_text, exclude_regexes):
	m_len = len(m_text.split(" "))
	for r in exclude_regexes:
		r_len = len(r.split(" "))
		leftover_len = r_len - m_len
		if leftover_len < 0: leftover_len = 0

		# Checks if the adding on the before has the regex
		prev = before[(len(before)-leftover_len):]
		prev_text = "{} {}".format(" ".join(prev), m_text).strip()
		if re.match(r, prev_text, re.IGNORECASE): return True

		# Checks if the adding on the after has the regex
		af = after[:leftover_len]
		af_text = "{} {}".format(m_text, " ".join(af)).strip()
		if re.match(r, af_text, re.IGNORECASE): return True

	return False

# Finds the keywords in each file.
def find_keywords(files_for_inclusion, filenames, content, words, included_regexes, excluded_regexes, interview_years_by_file, currRunJSON):
	# Stores the frequency of each keyword across all files (keyword --> count)
	keyword_freq = defaultdict(lambda:0)

	keyword_to_dates = defaultdict(lambda:defaultdict(lambda:0))

	# Basic statistics
	num_with_keywords = 0
	total_keywords = 0 # Total number of keywords found in all files
	all_matches = {}
	time_range_interviews = defaultdict(lambda:0)

	# Loops through each file, looking for keywords, and stores the matches
	for i in range(len(content)):
		file = filenames[i]
		if file not in files_for_inclusion or files_for_inclusion[file] == 0: 
			continue

		# TODO: Figure out why this is wrong...
		date_of_interview = "Not given"
		if file in interview_years_by_file:
			date_of_interview = interview_years_by_file[file]

		c = " {}.".format(" ".join(content[i].split())) # Splits the content by spaces (combines newlines, etc.)

		# Stores the file's keyword counts and matches
		curr_keywords = defaultdict(lambda:0)
		curr_matches = []

		time_range_interviews[date_of_interview] += 1

		# Loops through the regexes
		for j in range(len(included_regexes)):
			curr_r = included_regexes[j]
			regex = re.compile(curr_r, re.IGNORECASE) # Currently ignores the case
			for m in regex.finditer(c):
				m_loc = m.start()
				m_text = m.group(1)
				w = words[j]

				before, new_m_text, after = get_words_around(m_text, m_loc, c, MAX_EXCLUDE_REGEX_LENGTH)
				if need_to_exclude(before, after, new_m_text, excluded_regexes):
					continue

				# Updates the statistics
				keyword_freq[w] += 1
				curr_keywords[w] += 1
				
				keyword_to_dates[w][date_of_interview] += 1
				total_keywords += 1

				# Adds it onto the matches
				curr_matches.append([m_loc, before, new_m_text, after])

		if len(curr_keywords) > 0:
			num_with_keywords += 1
			all_matches[file] = curr_matches

	currRunJSON["total-keywords"] = total_keywords
	currRunJSON["total-interviews-with-keywords"] = num_with_keywords
	currRunJSON["time-range-interviews"] = time_range_interviews
	currRunJSON["keyword-counts"] = keyword_freq
	currRunJSON["keywords-over-time"] = keyword_to_dates

	return all_matches

# Gets all the surrounding contexts for keyword matches in files.
def get_all_contexts(filenames, content, all_matches, currRunJSON):
	keywordJSON = {}

	for i in range(len(filenames)):
		f = filenames[i]
		if f not in all_matches:
			continue

		bolded_contexts = []
		matches = all_matches[f]
		c = content[i]
		matches = sorted(matches, key=lambda x: x[0])

		for j in range(len(matches)):
			m = matches[j]
			loc = m[0]
			before = m[1]
			word = m[2]
			after = m[3]

			bold_word = "<b>{}</b>".format(word)
			curr_context = "...{}{}{}...".format(before, bold_word, after)
			cJSON = {
				"id": str(j) + "-" + f,
				"keywordContext": curr_context,
				"flagged": False,
				"falseHit": False
			}
			bolded_contexts.append(cJSON)

		keywordJSON[f] = bolded_contexts

	currRunJSON["keyword-contexts"] = keywordJSON

# Creates one new run with one collection and one keyword list
def create_new_run(c, k, metadata, runJSON):
	k["id"] = k["name"] + "-" + k["version"]
	print_message("progress-message", "Creating run for " + c["id"] + " and " + k["id"])
	currRunId = c["id"] + "-" + k["id"]
	currRunJSON = {
		"id": currRunId,
		"collection": c["id"],
		"keyword-list": k["id"]
	}

	print_message("m", metadata)

	all_matches = find_keywords(metadata["files_for_inclusion"][c["id"]], c["filenames"], c["content"], k["include"], k["included_regexes"], k["excluded_regexes"], metadata["interview_years_by_file"][c["id"]], currRunJSON)
	get_all_contexts(c["filenames"], c["content"], all_matches, currRunJSON)

	num_with_keywords = currRunJSON["total-interviews-with-keywords"]
	if num_with_keywords > 0:
		runJSON["summary-report"]["total-collections-with-keywords"] += 1
		runJSON["summary-report"]["total-interviews-with-keywords"] += num_with_keywords



	runJSON["individual-reports"][currRunId] = currRunJSON

def main():
	runJSON = {} # Final JSON object that contains this run information
	collections, keywords, keyword_regexes, metadata, runDirname =  set_up(runJSON)

	runJSON["individual-reports"] = {}
	progressPerRun = int(95/(len(collections) * len(keywords)))
	totalProgress = 5
	for c in collections:
		for k in keywords:
			create_new_run(c, k, metadata, runJSON)
			totalProgress += progressPerRun
			print_message("progress", totalProgress)

	with open(data_dirname + "run.json", "w") as f:
		f.write(json.dumps(runJSON))

	print_message("progress", 100)

if __name__ == '__main__':
	main()
