
# NOTE: It is the historian's job to make sure that keywords are not repetitive (they are
# otherwise double-counted into counts).

from collections import defaultdict
from collections import OrderedDict
from argparse import ArgumentParser
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

nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('punkt')

NUM_TOP_WORDS = 20 # The number of top words that we want from each file
CONTEXT_WORDS_AROUND = 50
MAX_EXCLUDE_REGEX_LENGTH = 50
punctuation = ['\.', '/', '\?', '\-', '"', ',', '\\b'] # Punctuation we use within our regexes

keyword_to_dates = defaultdict(lambda: defaultdict(lambda :0))

# Helper function to write the beginning of the HTML document.
def write_beginning_of_html(report_name):
	text = """ <!DOCTYPE html>\n
		<html>\n
		<head>\n
		<style>\n
		.title {
			font-weight: bold;
		}
		</style>\n
		</head>\n
		<body>\n """
	with open(report_name, "w", encoding = "utf-8") as f:
		f.write(text)

# Helper function to write a h3 header in HTML format
def write_header_line(report_name, title):
	text = "<h3>{}</h3>".format(title)
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(text)

# Helper function to write a span line in HTML format
def write_span_line(report_name, title, content):
	text = """<span><span class="title">{}: </span>{}<br></span>""".format(title, content)
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(text)

# Helper function to write a list in HTML format
def write_list_lines(report_name, title, content):
	inner_text = "".join(["<li>{}</li>".format(c) for c in content])
	text = "<span>{}</span><ul>{}</ul>".format(title, inner_text)
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(text)

# Helper function to write the end of the HTML document
def write_end_of_html(report_name):
	text = " </body>\n</html>"
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(text)

# Reads in arguments into the directory, words, and metadata.
def read_arguments(parser):
	parser.add_argument("-d", "--directory", default = "corpus", help = "Directory corpora files are")
	parser.add_argument("-w", "--words", default = "keywords.txt", help = "File of keywords")
	parser.add_argument("-m", "--metadata", default = "metadata.csv", help = "CSV file with metadata")
	args = parser.parse_args()

	return args.directory, args.words, args.metadata

# Creates a new name that will be used for the subcorpora report,
# folder, etc. Bases it upon whatever already exists; so if there is
# already a folder or report with the same name, it adds a number to it.
def create_new_name(directory, words):
	collection_name = directory.split("/")[-1]
	keywords_name = words.replace(".txt", "")

	name = "{}_{}".format(collection_name, keywords_name)
	num_existing = 0
	while True:
		if not os.path.isfile("{}_report.html".format(name)) and not os.path.isdir(name) and not os.path.isfile("{}_keyword_statistics.csv".format(name)): 
			break
		num_existing += 1
		name = "{}_{}_{}".format(collection_name, keywords_name, num_existing)

	return name

# Reads all the text from each text file in the corpus directory
# and writes corpus statistics to the report file.
# TODO: Have an automatic way to resolve utf-8 errors (maybe to read
# it in as utf-8).
def read_corpus(directory, report_name):
	filenames = []
	content = []

	for file in os.listdir(directory):
		if ".txt" not in file: continue
		filenames.append(file)

		# If the encoding is not working with the files being read, comment out the
		# utf-8 encoding assumption and use these next three lines.
		with open("{}/{}".format(directory, file), "r", encoding = "ISO-8859-1") as f:
			print(file)
			content.append(f.read())

		# # Assumes the files are utf-8 encoding
		# with open("{}/{}".format(directory, file), "r", encoding = "utf-8") as f:
		# 	print(file)
		# 	content.append(f.read())
	
	write_header_line(report_name, "Collection Information")
	write_span_line(report_name, "Directory", directory)
	write_span_line(report_name, "Total number of files", len(filenames))

	return filenames, content

# Gets punctuation joined by bars (this is punctuation that we decide to count as separation!)
def get_punctuation_for_regex():
	return "|".join(punctuation)

# Gets the words from the keywords file and turns them into Python regex form. Returns
# the full list of words and the include and exclude regexes.
def read_keywords(file, report_name):
	words = []
	include_words = []
	exclude_words = []
	include_regexes = []
	exclude_regexes = []

	include = True
	with open(file, "r") as f:
		words = [x.strip().lower() for x in f.readlines()]
		for w in words:
			w = w.strip()
			if w == "":
				include = False
				continue

			if include:
				include_words.append(w)
			else:
				r = r"\b{}\b".format(w.replace("*", "[a-zA-Z]*"))
				exclude_regexes.append(r)
				exclude_words.append(w)

		write_header_line(report_name, "Keyword Information"),
		write_span_line(report_name, "Filename", file),
		write_span_line(report_name, "Total number of keywords", len(include_regexes) + len(exclude_regexes)),
		write_span_line(report_name, "Keywords to include", "; ".join(include_words)),
		write_span_line(report_name, "Keywords to exclude", "; ".join(exclude_words))

	# Sorts the include words backwards to make sure we get the longer words first later
	include_words.sort(reverse=True) # Sorts it alphabetically backwards
	include_words.sort(key=len, reverse=True) # Sorts it lengthwise backwards

	for w in include_words:
		punc = get_punctuation_for_regex()
		r = r'(?:{})({})(?:{})'.format(punc, w.replace("*", "[a-zA-Z]*"), punc)
		include_regexes.append(r)

	return include_words + exclude_words, include_regexes, exclude_regexes

# Gets the files for inclusion--excludes any files that are only male interviewees or 
# interviewws with no transcripts.
def get_included_files(df, filenames):
	filenames_map = {}
	for f in filenames:
		filenames_map[f] = 0

	# Statistics about file inclusion/exclusion
	num_files_no_transcript = 0 # Total number of files in collection with no transcript
	people = {} # Information about individual people (only "Sex" == "Female" and "Sex" == "Unknown"); we match people based on first and last name
	male_interviews = {} # Interviews that include males
	male_plus_interviews = {} # Interviews with both male and non-male interviewees
	interview_years = defaultdict(lambda:0)
	interview_years_by_file = {}

	files_for_inclusion = {} # Final list of files for inclusion
	multiple_file_tracker = {} # Keeps track of filenames already done without the _a, _b, etc. at the end (which we used for multiple interviewees)

	for i, r in df.iterrows():
		f = r["project_file_name"]

		# Skips files with no project filename (shouldn't happen)
		if pd.isnull(f):
			continue

		# Skips files not in collection
		if f not in filenames_map:
			continue

		# Skips files with no transcript
		no_transcript = r["no_transcript"]
		if not pd.isnull(no_transcript) and (no_transcript or no_transcript.strip() == "TRUE"):
			num_files_no_transcript += 1
			continue

		# Removes the multiple interviewee indication (_a, _b, etc.) to avoid repeated counts (TODO: Remove this when it's no longer an issue)
		nonmultiple_f = f
		file_front = f.replace(".txt", "")
		parts = file_front.split("_")
		if len(parts[-1]) == 1 and parts[-1].isalpha():
			nonmultiple_f = "{}.txt".format("_".join(parts[0:-1]))

		# Skips files with multiple interviewees that were already included
		if nonmultiple_f in multiple_file_tracker:
			continue

		# If the interviewee is male, marks it and continues (as there may be the same file later with a non-male interviewee, which means we need it)
		sex = r["sex"]
		if not pd.isnull(sex) and sex.strip() == "Male":
			male_interviews[f] = 1
			if f in files_for_inclusion:
				male_plus_interviews[f] = 1 # Means it contains both male and non-male interviewees
			continue

		# If the current interviewee is non-male and the interview has a male, mark it
		if f in male_interviews:
			male_plus_interviews[f] = 1
			male_interviews[f] = 0

		# At this point, we have a new interview (not previously added) with at least one non-male interviewee we want to add!
		# This assumes first entry contains the complete information and that names are the same.
		interviewee_name = r["interviewee_name"]
		if interviewee_name not in people:
			birth_decade = r["birth_decade"]
			education = r["education"]
			identified_race = r["identified_race"]
			interviewee_birth_country = r["interviewee_birth_country"]

			people[interviewee_name] = {}
			people[interviewee_name]["birth_decade"] = birth_decade if not pd.isnull(birth_decade) else ""
			people[interviewee_name]["education"] = education if not pd.isnull(education) else ""
			people[interviewee_name]["identified_race"] = identified_race if not pd.isnull(identified_race) else ""
			people[interviewee_name]["sex"] = sex if not pd.isnull(sex) else ""
			people[interviewee_name]["birth_country"] = interviewee_birth_country if not pd.isnull(interviewee_birth_country) else ""

		files_for_inclusion[f] = 1
		multiple_file_tracker[f] = 1

		date_of_first_interview = r["date_of_first_interview"]
		if pd.isnull(date_of_first_interview):
			interview_years["Not given"] += 1
			interview_years_by_file[f] = "Not given"
		else:
			year = date_of_first_interview.split("/")[2]

			# Attempts to fix the two numbered ones; assumes anything that is 00-19 is in 2000s (otherwise in 1900s)
			if len(year) == 2:
				if int(year) <= 19:
					year = "20{}".format(year)
				else:
					year = "19{}".format(year)

			interview_years[year] += 1
			interview_years_by_file[f] = year

	return files_for_inclusion, people, num_files_no_transcript, male_interviews, male_plus_interviews, interview_years, interview_years_by_file

# Sorts and writes metadata list information into the file
def sort_write_metadata_list(d, description, report_name):
	# Standardizes the keys
	new_d = {}
	for k, v in d.items():
		k = str(k)
		if k == "" or k == "Unknown":
			k = "Not given"
		new_d[k] = v

	arr = []
	for k, v in sorted(new_d.items()):
		arr.append("{}: {}".format(k, v))
	write_list_lines(report_name, description, arr)

# Aggregates the interviewee/interview information and writes it to the HTML report
def aggregate_interview_metadata(files_for_inclusion, people, report_name, total_num_files, num_files_no_transcript, male_interviews, male_plus_interviews, interview_years):
	# Gets metadata counts for interviewees
	birth_decade = defaultdict(lambda:0)
	education = defaultdict(lambda:0)
	identified_race = defaultdict(lambda:0)
	sex = defaultdict(lambda:0)
	birth_country = defaultdict(lambda:0)
	for k, v in people.items():
		birth_decade[v["birth_decade"]] += 1
		education[v["education"]] += 1
		identified_race[v["identified_race"]] += 1
		sex[v["sex"]] += 1
		birth_country[v["birth_country"]] += 1

	# Writes the relevant information to the file
	write_header_line(report_name, "Metadata Statistics")
	write_span_line(report_name, "Total number of interviews included", str(len(files_for_inclusion.keys())))
	write_span_line(report_name, "Total number of interviews", str(total_num_files))
	write_span_line(report_name, "Total number of interviews with no transcript", str(num_files_no_transcript))
	write_span_line(report_name, "Total number of interviews with only male interviewees", str(len([k for k, v in male_interviews.items() if v == 1])))
	write_span_line(report_name, "Total number of interviews with both male and non-male interviewees", str(len(male_plus_interviews.keys())))
	write_span_line(report_name, "Total unique interviewees", str(len(people.keys())))

	sort_write_metadata_list(interview_years, "Years interviews conducted", report_name)
	sort_write_metadata_list(birth_decade, "Interviewees' birth decade counts", report_name)
	sort_write_metadata_list(education, "Interviewees' education counts", report_name)
	sort_write_metadata_list(identified_race, "Interviewees' identified race counts", report_name)
	sort_write_metadata_list(sex, "Interviewees' sex counts", report_name)
	sort_write_metadata_list(birth_country, "Interviewees' birth country counts", report_name)

# Reads in the metadata to collect statistics and exclude any files that are only male
# interviewees or interviews with no transcripts. Returns the list of included files + their years.
def read_metadata(file, filenames, report_name):
	df = pd.read_csv(file, encoding = "utf-8", header = 0)
	files_for_inclusion, people, num_files_no_transcript, male_interviews, male_plus_interviews, interview_years, interview_years_by_file = get_included_files(df, filenames)
	total_num_files = len(filenames)
	aggregate_interview_metadata(files_for_inclusion, people, report_name, total_num_files, num_files_no_transcript, male_interviews, male_plus_interviews, interview_years)

	return files_for_inclusion, interview_years_by_file

# Sets up directory and filenames and reads in data.
def set_up():
	directory, words, metadata = read_arguments(ArgumentParser())
	name = create_new_name(directory, words)
	subcorpora_dirname = name
	report_name = "{}_report.html".format(name)
	write_beginning_of_html(report_name)

	filenames, content = read_corpus(directory, report_name)
	words, include_regexes, exclude_regexes = read_keywords(words, report_name)
	files_for_inclusion, interview_years_by_file = read_metadata(metadata, filenames, report_name)

	return directory, words, files_for_inclusion, name, subcorpora_dirname, report_name, filenames, content, words, include_regexes, exclude_regexes, metadata, interview_years_by_file

# Gets the top words in each transcript, writing them into a CSV. Exclude stopwords,
# punctuation, and common verbs.
def get_top_words(filenames, content, name):
	dont_include = [] # Can be used later to add more words to exclude
	stop_words = set(stopwords.words("english") + list(string.punctuation) + list(dont_include))
	verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]
	stats_name = "{}_file_top_words.csv".format(name)

	all_words = []
	for i in range(len(filenames)):
		file = filenames[i]
		c = unidecode(content[i].lower())
		word_tokens = nltk.pos_tag(word_tokenize(c)) # Tags the type of word
		filtered = []
		for w, tag in word_tokens:
			# Takes out stopwords
			if w in stop_words:
				continue

			# Takes out verbs
			if tag in verb_tags:
				continue

			# Excludes any that has punctuation
			has_punc = False
			for ch in w:
				if ch in string.punctuation: has_punc = True
			if has_punc:
				continue

			filtered.append(w)

		word_map = defaultdict(lambda:0)
		for w in filtered: word_map[w] += 1

		num = 0
		for k, v in sorted(word_map.items(), key = lambda kv: kv[1], reverse = True):
			if num >= NUM_TOP_WORDS: break
			all_words.append([file, k, v])
			num += 1

	# Writes the top words of each file into a CSV
	df = pd.DataFrame(all_words)
	df.to_csv(stats_name, index = False, header = ["filename", "word", "count"])

# Returns true if character is considered "punctuation"
def is_punctuation(ch):
	for p in punctuation:
		if p == "\\b": continue
		if p[0] == "\\": p = p[1:]
		if ch == p: return True
	return False

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

# Checks for collocations for the words before and after
def check_for_collocations(before, after, m_text, new_m_text, curr_i, include_regexes):
	collocations = []
	collocations_formats = []
	for i in range(len(include_regexes)):
		r = include_regexes[i]
		r_len = len(r.split(" "))

		# Checks if there is a collocation before
		if not is_punctuation(new_m_text[0]) and len(before) >= r_len:
			prev = before[(len(before)-r_len):]
			prev_text = " ".join(prev).strip()
			if prev_text == "": break
			if not is_punctuation(prev_text[len(prev_text)-1]) and re.match(r, prev_text, re.IGNORECASE): 
				collocations.append([i, curr_i])
				collocations_formats.append([prev_text, m_text])

		# Checks if there is a collocation after
		if not is_punctuation(new_m_text[len(new_m_text)-1]) and len(after) >= r_len:
			af = after[:r_len]
			af_text = " ".join(af).strip()
			if not is_punctuation(af_text[0]) and re.match(r, af_text, re.IGNORECASE): 
				collocations.append([curr_i, i])
				collocations_formats.append([m_text, af_text])

	return collocations, collocations_formats

# Checks if we already included the current match before (unfortunately this is super slow...)
# TODO: Maybe speed it up with some set theory or something.
def check_already_included(curr_matches, m_loc_curr, curr_len):
	curr_end = m_loc_curr + curr_len
	for prev_match in curr_matches:
		m_loc_prev = prev_match[0]
		prev_len = len(prev_match[2])
		prev_end = m_loc_prev + prev_len

		# Checks if the current word is inside the previous word using location data
		if m_loc_curr >= m_loc_prev and curr_end <= prev_end:
			return True

	return False

# Counts the total number of multiple keyword pairs within the same document.
def get_multiple_keyword_counts(curr_keywords, multiple_keyword):
	for k1 in curr_keywords.keys():
		for k2 in curr_keywords.keys():
			if k1 == k2: continue
			curr = [k1, k2]
			curr.sort()
			multiple_keyword["{};{}".format(curr[0], curr[1])] += 1

# Writes out some basic keyword statistics within the report.
def write_keyword_basic_statistics(report_name, subcorpora_dirname, multiple_keyword_name, keyword_counts_name, num_with_keywords, total_keywords, content_length):
	# Writes some basic statistics into the report
	write_header_line(report_name, "Keyword Statistics")
	write_span_line(report_name, "Subcorpora written into directory", subcorpora_dirname)
	write_span_line(report_name, "Multiple keyword counts written into file", multiple_keyword_name)
	write_span_line(report_name, "Keyword counts written into file", keyword_counts_name)
	write_span_line(report_name, "Total number of files at least one keyword", num_with_keywords)
	write_span_line(report_name, "Total number of keywords found", total_keywords)
	write_span_line(report_name, "Percentage of files", "{}%".format(100 * round(float(num_with_keywords)/float(content_length), 5)))

# Writes the keyword counts in total and by file into a CSV.
def write_keyword_counts_to_csv(keyword_freq, keyword_counts_name, keyword_freq_files, keyword_counts_file_name):
	all_keyword_freq = []
	for k, v in sorted(keyword_freq.items(), key = lambda kv: kv[1], reverse = True):
		all_keyword_freq.append([k, v])
	df = pd.DataFrame(all_keyword_freq)
	if len(all_keyword_freq) > 0: df.to_csv(keyword_counts_name, index = False, header = ["keyword", "count"])
	all_keyword_file_freq = []
	for k, v in keyword_freq_files.items():
		for k_1, v_1 in sorted(v.items(), key = lambda kv: kv[1], reverse = True):
			all_keyword_file_freq.append([k, k_1, v_1])
	df = pd.DataFrame(all_keyword_file_freq)
	if len(all_keyword_file_freq) > 0: df.to_csv(keyword_counts_file_name, index = False, header =  ["filename", "keyword", "count"])

# Writes the keyword collocations and formats into a CSV.
def write_keyword_collocations_to_csv(keyword_collocations, keyword_collocations_name, keyword_collocations_format, keyword_collocations_format_name):
	all_keyword_collocations = []
	for k, v in sorted(keyword_collocations.items(), key = lambda kv: kv[1], reverse = True):
		w = k.split(";")
		all_keyword_collocations.append([w[0], w[1], v])
	df = pd.DataFrame(all_keyword_collocations)
	if len(all_keyword_collocations) > 0: df.to_csv(keyword_collocations_name, index = False, header = ["word_1", "word_2", "count"])
	all_keyword_collocations_format = []
	for k, v in keyword_collocations_format.items():
		w = k.split(";")
		new_v = []
		for v_1 in v:
			parts = v_1.split(" ")
			w1 = parts[0].lower()
			if is_punctuation(w1[0]):
				w1 = w1[1:]
			w2 = parts[1].lower()
			if is_punctuation(w2[-1]):
				w2 = w2[:-1]
			new_v.append("{} {}".format(w1, w2))
		new_v = list(set(new_v))
		all_keyword_collocations_format.append([w[0], w[1], "; ".join(new_v)])
	df = pd.DataFrame(all_keyword_collocations_format)
	if len(all_keyword_collocations_format) > 0: df.to_csv(keyword_collocations_format_name, index = False, header = ["word_1", "word_2", "formats"])

# Writes the multiple keyword statistics into a CSV.
def write_multiple_keyword_to_csv(multiple_keyword, multiple_keyword_name):
	all_multiple_keyword = []
	for k, v in sorted(multiple_keyword.items(), key = lambda kv: kv[1], reverse = True):
		w = k.split(";")
		all_multiple_keyword.append([w[0], w[1], v])
	df = pd.DataFrame(all_multiple_keyword)
	if len(all_multiple_keyword) > 0: df.to_csv(multiple_keyword_name, index = False, header = ["word_1", "word_2", "count"])

# Writes the keyword formats into a CSV.
def write_keyword_formats_to_csv(keyword_formats, keyword_format_name):
	all_keyword_formats = []
	for k, v in keyword_formats.items():
		if len(v) == 0: continue
		v.sort()
		for i in range(len(v)):
			w = v[i]
			w = w.lower()
			if is_punctuation(w[0]): w = w[1:]
			if is_punctuation(w[-1]): w = w[:-1]
			v[i] = w
		v = list(set(v))
		all_keyword_formats.append([k, "; ".join(v)])
	df = pd.DataFrame(all_keyword_formats)
	if len(all_keyword_formats) > 0: df.to_csv(keyword_format_name, index = False, header = ["keyword", "formats"])

# Writes all the original interviews that have keywords into a subdirectory.
def write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files):
	os.mkdir(subcorpora_dirname)
	for i in range(len(filenames)):
		file = filenames[i]
		if file not in keyword_freq_files: continue
		new_file = "{}/{}".format(subcorpora_dirname, file)
		with open(new_file, "w", encoding = "utf-8") as f:
			f.write(content[i])

# TODO: Not sure if we need to combine these together...
def bold_keywords(matches, c):
	# First goes through and combines the ranges that need to be combined
	# combined_lists = []
	# curr_start = None
	# curr_end = None
	# curr_list_of_indices = []
	# for i in len(matches):
	# 	m = matches[i]
	# 	loc = m[0]
	# 	before = m[1]
	# 	word = m[2]
	# 	after = m[3]
	# 	before_loc = loc - len(before) # Inclusive
	# 	after_loc = loc + len(word) + len(after) # Exclusive

	# 	if curr_start is None:
	# 		curr_start = before_loc
	# 		curr_end = after_loc
	# 		curr_list_of_indices.append(i)
	# 	else:
	# 		if before_loc >= curr_start and before_loc < curr_end:
	# 			curr_end = after_loc
	# 			curr_list_of_indices.append(i)
	# 		else:
	# 			combined_lists.append([curr_start, curr_end, curr_list_of_indices])
	# 			curr_start = None
	# 			curr_end = None
	# 			curr_list_of_indices = []

	# if curr_start is not None:
	# 	combined_lists.append([curr_start, curr_end, curr_list_of_indices])

	# Then goes through the combined lists and reconstructs the texts
	# for cl in combined_lists:
	# 	start = cl[0]
	# 	end = cl[1]
	# 	list_of_indices = cl[2]

	# 	curr_text = ""
	# 	for i in len(list_of_indices):
	# 		index = list_of_indices[i]
	# 		if i == 0:
	# 			curr_text = "{}<b>{}</b>".format()
	# 		elif i == len(list_of_indices) - 1:

	# 		else:

	all_bolded = []
	for m in matches:
		loc = m[0]
		before = m[1]
		word = m[2]
		after = m[3]

		bold_word = "<b>{}</b>".format(word)
		curr_context = "{}{}{}".format(before, bold_word, after)
		all_bolded.append(curr_context)

	return all_bolded

# Gets all the surrounding context for keywords
def get_all_contexts(subcorpora_dirname, filenames, content, all_matches):
	all_contexts = {}

	for i in range(len(filenames)):
		f = filenames[i]
		if f not in all_matches: continue

		matches = all_matches[f]
		matches = sorted(matches, key=lambda x: x[0])
		c = content[i]
		all_contexts[f] = bold_keywords(matches, c)

	return all_contexts

# Finds the keywords in each file.
def find_keywords(files_for_inclusion, filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname, interview_years_by_file):
	# Stores the frequency of each keyword across all files (keyword --> count)
	keyword_freq = defaultdict(lambda:0)
	keyword_counts_name = "{}_keyword_counts.csv".format(name)

	# Stores the frequency of each keyword by file (filename --> keyword --> count)
	keyword_freq_files = defaultdict(lambda:0)
	keyword_counts_file_name = "{}_keyword_counts_by_file.csv".format(name)

	# Stores keyword collocations
	keyword_collocations = defaultdict(lambda:0)
	keyword_collocations_name = "{}_keyword_collocations_formats.csv".format(name)
	keyword_collocations_format_name = "{}_keyword_collocations_formats.csv".format(name)
	keyword_collocations_format = defaultdict(lambda:[])
	
	# Stores data on how many times pairs of keywords appear together in the same file
	multiple_keyword = defaultdict(lambda:0)
	multiple_keyword_name = "{}_multiple_keywords.csv".format(name)

	# Stores data on keyword formats
	keyword_formats = defaultdict(lambda:[])
	keyword_format_name = "{}_keyword_formats.csv".format(name)

	# Basic statistics
	num_with_keywords = 0 # Number of files that have at least one keyword
	total_keywords = 0 # The total number of keywords found in all file
	all_matches = {}

	# Loops through each file, looking for keywords, and stores the matches as 
	# (m_loc: location of start of text in content[i], before: text that comes before, m_text: the actual text, after: text that comes after)
	for i in range(len(content)):
		file = filenames[i]
		if file not in files_for_inclusion or files_for_inclusion[file] == 0: continue
		c = " {}.".format(" ".join(content[i].split())) # Splits the content by spaces (combines newlines, etc.)

		# Stores the file's keyword counts and matches
		curr_keywords = defaultdict(lambda:0)
		curr_matches = []

		# Loops through the regexes
		for j in range(len(include_regexes)):
			curr_r = include_regexes[j]
			regex = re.compile(curr_r, re.IGNORECASE) # Currently ignores the case
			for m in regex.finditer(c):
				m_loc = m.start()
				m_text = m.group(1)
				w = words[j]

				before, new_m_text, after = get_words_around(m_text, m_loc, c, MAX_EXCLUDE_REGEX_LENGTH)
				if need_to_exclude(before, after, new_m_text, exclude_regexes): 
					continue

				# If it is already included with a previous regex, continue
				if check_already_included(curr_matches, m_loc, len(new_m_text)):
					continue

				# Updates the statistics
				keyword_freq[w] += 1
				curr_keywords[w] += 1
				keyword_formats[w].append(m_text)
				date_of_interview = interview_years_by_file[file]
				keyword_to_dates[w][date_of_interview] += 1
				collocations, collocations_f = check_for_collocations(before, after, m_text, new_m_text, j, include_regexes)
				for l in range(len(collocations)):
					col = collocations[l]
					col_f = collocations_f[l]
					k = "{};{}".format(words[col[0]], words[col[1]])
					keyword_collocations[k] += 0.5
					keyword_collocations_format[k].append("{} {}".format(col_f[0], col_f[1]))	

				# Adds it onto the matches
				curr_matches.append([m_loc, before, new_m_text, after])

		if len(curr_keywords.keys()) > 0:
			num_with_keywords += 1
			keyword_freq_files[file] = curr_keywords
			total_keywords += len(curr_matches) # Total number of keywords found overall
			all_matches[file] = curr_matches
			content[i] = c
			get_multiple_keyword_counts(curr_keywords, multiple_keyword)

	# Writes out keyword statistics and our final files to the subcorpora directory
	write_keyword_basic_statistics(report_name, subcorpora_dirname, multiple_keyword_name, keyword_counts_name, num_with_keywords, total_keywords, len(content))
	write_keyword_counts_to_csv(keyword_freq, keyword_counts_name, keyword_freq_files, keyword_counts_file_name)
	write_keyword_collocations_to_csv(keyword_collocations, keyword_collocations_name, keyword_collocations_format, keyword_collocations_format_name)
	write_multiple_keyword_to_csv(multiple_keyword, multiple_keyword_name)
	write_keyword_formats_to_csv(keyword_formats, keyword_format_name)
	write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files)

	# Writes out the context to the report
	write_header_line(report_name, "Contexts")
	all_contexts = get_all_contexts(subcorpora_dirname, filenames, content, all_matches)
	for file, contexts in all_contexts.items():
		write_list_lines(report_name, file, contexts)

def main():
	directory, words, files_for_inclusion, name, subcorpora_dirname, report_name, filenames, content, words, include_regexes, exclude_regexes, metadata, interview_years_by_file = set_up()
	get_top_words(filenames, content, name)
	find_keywords(files_for_inclusion, filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname, interview_years_by_file)
	write_end_of_html(report_name)

if __name__ == '__main__':
	main()
