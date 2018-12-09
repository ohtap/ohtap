
from collections import defaultdict
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

# The number of top words that we want from each file
NUM_TOP_WORDS = 20

def write_header_line(title):
	return "<h3>{}</h3>".format(title)

def write_span_line(title, content):
	text = """<span><span class="title">{}: </span>{}<br></span>""".format(title, content)
	return text

def write_list_lines(title, content):
	inner_text = "".join(["<li>{}</li>".format(c) for c in content])
	text = "<span>{}</span><ul>{}</ul>".format(title, inner_text)
	return text

# Splits content into sentences based on punctuation.
def split_into_sentences(c):
	return re.split('\.|\!|\?', c)

# Writes out the context in which these keywords appear.
def get_context(filenames, content, keyword_freq_files, report_name):
	for i in range(len(filenames)):
		file = filenames[i]
		if file not in keyword_freq_files: continue
		freq = keyword_freq_files[file]
		sentences = split_into_sentences(content[i])
		has_keyword = []
		for s in sentences:
			s = s.replace("\n", " ").replace("\t", " ")
			s = re.sub('\s+', ' ', s).strip()
			for k in freq.keys():
				matches = re.findall(turn_to_regex(k), s)
				if len(matches) > 0:
					has_keyword.append([s, matches])
					break

		with open(report_name, "a", encoding = "utf-8") as f:
			f.write(write_header_line("Keyword Contexts"))

			all_s = []
			for s, matches in has_keyword:
				new_s = s
				for m in matches:
					parts = new_s.split(m)
					new_s = "<b>{}</b>".format(m).join(parts)
				all_s.append("...{}...".format(new_s))
			f.write(write_list_lines(file, all_s))

# Checks to see if the match m needs to be excluded and returns True if so.
def needs_to_be_excluded(m, exclude_regexes):
	for r in exclude_regexes:
		matches = re.findall(r, m)
		if len(matches) > 0: return True

	return False

# Writes the subcorpora into the directory.
def write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files):
	os.mkdir(subcorpora_dirname)
	for i in range(len(filenames)):
		file = filenames[i]
		if file not in keyword_freq_files: continue
		new_file = "{}/{}".format(subcorpora_dirname, file)
		with open(new_file, "w", encoding = "utf-8") as f:
			f.write(content[i])

# Finds the keywords within the files and outputs the relevant information.
def find_keywords(filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname):
	keyword_freq = defaultdict(lambda:0) # Stores the frequency of each keyword
	keyword_freq_files = {} # Stores the frequency of each keyword by file
	num_with_keywords = 0 # Number of files that have at least one keyword
	total_keywords = 0 # The total number of keywords found in all file
	keyword_collocations = defaultdict(lambda:0) # Stores counts of keyword collocations
	keyword_collocations_name = "{}_keyword_collocations.csv".format(name)
	keyword_counts_name = "{}_keyword_counts.csv".format(name)

	# Gets the counts of keywords within all the files
	for i in range(len(content)):
		file = filenames[i]
		c = content[i].lower()
		appeared_keywords = defaultdict(lambda:0)
		for j in range(len(include_regexes)):
			matches = re.findall(include_regexes[j], c)
			for m in matches:
				if not needs_to_be_excluded(m, exclude_regexes):
					total_keywords += 1
					keyword_freq[words[j]] += 1
					appeared_keywords[words[j]] += 1
		if len(appeared_keywords.keys()) > 0:
			num_with_keywords += 1
			keyword_freq_files[file] = appeared_keywords
			for k1 in appeared_keywords.keys():
				for k2 in appeared_keywords.keys():
					if k1 == k2: continue
					curr = [k1, k2]
					curr.sort()
					keyword_collocations["{};{}".format(curr[0], curr[1])] += 1

	# Writes the keyword collocation statistics into a CSV
	all_collocations = []
	for k, v in sorted(keyword_collocations.items(), key=lambda kv: kv[1], reverse=True):
		words = k.split(";")
		all_collocations.append([words[0], words[1], v])
	df = pd.DataFrame(all_collocations)
	df.to_csv(keyword_collocations_name, index = False, header = ["word_1", "word_2", "count"])

	# Writes the general statistics into the report
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(write_header_line("Keyword Statistics"))
		f.write(write_span_line("Subcorpora written into directory", subcorpora_dirname))
		f.write(write_span_line("Keyword collocations counts written into file", keyword_collocations_name))
		f.write(write_span_line("Keyword counts written into file", keyword_counts_name))
		f.write(write_span_line("Total number of files at least one keyword", num_with_keywords))
		f.write(write_span_line("Total number of keywords found", total_keywords))

	# Writes the keyword counts by file into a CSV
	all_keywords = []
	for k, v in keyword_freq_files.items():
		for k_1, v_1 in sorted(v.items(), key=lambda kv: kv[1], reverse=True):
			all_keywords.append([k, k_1, v_1])
	df = pd.DataFrame(all_keywords)
	df.to_csv(keyword_counts_name, index = False, header = ["filename", "keyword", "count"])

	write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files)

	return keyword_freq_files

# Writes the top words in each file, minus stopwords and punctuation,
# into a CSV.
def get_top_words(filenames, content, name):
	dont_include = [] # Can be later used to add more words to exclude
	stop_words = set(stopwords.words("english") + list(string.punctuation) + list(dont_include))
	stats_name = "{}_file_top_words.csv".format(name)

	verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

	for i in range(len(filenames)):
		file = filenames[i]
		c = unidecode(content[i].lower())
		word_tokens = nltk.pos_tag(word_tokenize(c))
		filtered = []
		for w, tag in word_tokens:
			if w in stop_words: continue
			if tag in verb_tags: continue # Removes verbs
			has_punc = False
			for ch in w:
				if ch in string.punctuation: has_punc = True
			if has_punc: continue
			filtered.append(w)

		word_map = defaultdict(lambda:0)
		for w in filtered: word_map[w] += 1

		num = 0
		all_words = []
		for k, v in sorted(word_map.items(), key = lambda kv: kv[1], reverse = True):
			if num >= NUM_TOP_WORDS: break
			all_words.append([file, k, v])
			num += 1

	# Writes the top words of each file into a CSV
	df = pd.DataFrame(all_words)
	df.to_csv(stats_name, index = False, header = ["filename", "word", "count"])

# Reads the metadata to collect statistics.
def read_metadata(file, filenames, report_name):
	df = pd.read_csv(file, encoding = "utf-8", header = None)

	info = {}
	for f in filenames: info[f] = {}
	for i, r in df.iterrows():
		f = r[6]
		if f in info:
			info[f]["birth_year"] = r[17] if not pd.isnull(r[17]) else ""
			info[f]["birth_decade"] = r[19] if not pd.isnull(r[19]) else ""
			info[f]["education"] = r[31] if not pd.isnull(r[31]) else ""
			info[f]["identified_race"] = r[26] if not pd.isnull(r[26]) else ""
			info[f]["sex"] = r[25] if not pd.isnull(r[25]) else ""
			info[f]["birth_country"] = r[22] if not pd.isnull(r[22]) else ""

	# Metadata information to output
	birth_decade = defaultdict(lambda:0)
	education = defaultdict(lambda:0)
	identified_race = defaultdict(lambda:0)
	sex = defaultdict(lambda:0)
	birth_country = defaultdict(lambda:0)

	for file in filenames:
		birth_decade[info[file]["birth_decade"]] += 1
		education[info[file]["education"]] += 1
		identified_race[info[file]["identified_race"]] += 1
		sex[info[file]["sex"]] += 1
		birth_country[info[file]["birth_country"]] += 1

	with open(report_name, "a", encoding = "utf-8") as f:
		write_header_line("Metadata Statistics")

		birth_decade_arr = []
		for k, v in birth_decade.items():
			k = "Not given" if k == "" else int(k)
			birth_decade_arr.append("{}: {}".format(k, v))
		f.write(write_list_lines("Interviewees' birth decade counts", birth_decade_arr))

		education_arr = []
		for k, v in education.items():
			if k == "": k = "Not given"
			education_arr.append("{}: {}".format(k, v))
		f.write(write_list_lines("Interviewees' education counts", education_arr))

		identified_race_arr = []
		for k, v in identified_race.items():
			if k == "": k = "Not given"
			identified_race_arr.append("{}: {}".format(k, v))
		f.write(write_list_lines("Interviewees' identified race counts", education_arr))

		sex_arr = []
		for k, v in sex.items():
			if k == "": k = "Not given"
			sex_arr.append("{}: {}".format(k, v))
		f.write(write_list_lines("Interviewees' sex counts", sex_arr))

		birth_country_arr = []
		for k, v in birth_country.items():
			if k == "": k = "Not given"
			birth_country_arr.append("{}: {}".format(k, v))
		f.write(write_list_lines("Interviewees' birth country counts", birth_country_arr))

	return info

# Turns a keyword format (within the keyword file) into a regex 
# that can be used with the re library.
def turn_to_regex(w):
	return r"\b{}\b".format(w.replace("*", "[a-zA-Z]*"))

# Gets the words from the keywords file and gets regexes for each.
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

			r =  turn_to_regex(w)
			if include:
				include_regexes.append(r)
				include_words.append(w)
			else:
				exclude_regexes.append(r)
				exclude_words.append(w)

	with open(report_name, "a", encoding = "utf-8") as f:
		text = "{}{}{}{}".format(
			write_header_line("Keyword Information"),
			write_span_line("Filename", file),
			write_span_line("Total number of keywords", len(include_regexes) + len(exclude_regexes)),
			write_span_line("Keywords to include", "; ".join(include_words)),
			write_span_line("Keywords to exclude", "; ".join(exclude_words))
		)
		f.write(text)

	return words, include_regexes, exclude_regexes

# Reads all the text from each text file in the corpus directory
# and writes corpus statistics to the report file.
def read_corpus(directory, report_name):
	filenames = []
	content = []

	for file in os.listdir(directory):
		if ".txt" not in file: continue
		filenames.append(file)
		with open("{}/{}".format(directory, file), "r", encoding = "utf-8") as f:
			content.append(f.read())
	
	with open(report_name, "a", encoding = "utf-8") as f:
		text = "{}{}{}".format(
			write_header_line("Collection Information"), 
			write_span_line("Directory", directory), 
			write_span_line("Total number of files", len(filenames))
		)
		f.write(text)

	return filenames, content

# Reads in arguments into the directory, words, and metadata.
def read_arguments(parser):
	parser.add_argument("-d", "--directory", default = "corpus", help = "Directory corpora files are")
	parser.add_argument("-w", "--words", default = "keywords.txt", help = "File of keywords")
	parser.add_argument("-m", "--metadata", default = "metadata.csv", help = "CSV file with metadata")
	args = parser.parse_args()

	return args.directory, args.words, args.metadata

# Creates a new name that will be used for the subcorpora report,
# folder, etc. Bases it upon whatever already exists.
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

def write_end_of_html(report_name):
	text = " </body>\n</html>"
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(text)

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

def main():
	directory, words, metadata = read_arguments(ArgumentParser())
	name = create_new_name(directory, words)
	subcorpora_dirname = name
	keyword_stats_name = "{}_keyword_stats.csv".format(name)
	report_name = "{}_report.html".format(name)
	write_beginning_of_html(report_name)

	filenames, content = read_corpus(directory, report_name)
	words, include_regexes, exclude_regexes = read_keywords(words, report_name)
	metadata = read_metadata(metadata, filenames, report_name)
	get_top_words(filenames, content, name)
	keyword_freq_files = find_keywords(filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname)
	get_context(filenames, content, keyword_freq_files, report_name)

	write_end_of_html(report_name)

if __name__ == '__main__':
	main()