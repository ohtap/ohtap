
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

NUM_TOP_WORDS = 20 # The number of top words that we want from each file
NUM_WORDS_AROUND = 50 # The number of words we want before and after (separate) for in-context

def write_header_line(title):
	return "<h3>{}</h3>".format(title)

def write_span_line(title, content):
	text = """<span><span class="title">{}: </span>{}<br></span>""".format(title, content)
	return text

def write_list_lines(title, content):
	inner_text = "".join(["<li>{}</li>".format(c) for c in content])
	text = "<span>{}</span><ul>{}</ul>".format(title, inner_text)
	return text

# Gets around words before and after the match
def get_words_around(m, content, around):
	parts = content.split(" {} ".format(m))
	results = []

	for i in range(len(parts) - 1):
		before = []
		after = []

		# Adds the words before
		words = []
		for j in range(i+1):
			for w in parts[j].split(): words.append(w)
		words.reverse()
		num = 0
		while num < len(words) and len(before) < around:
			before.append(words[num])
			num += 1
		before.reverse()

		# Adds the words after
		words = []
		for j in range(i+1, len(parts)):
			for w in parts[i+1].split(): words.append(w)
		num = 0
		while num < len(words) and len(after) < around:
			after.append(words[num])
			num += 1

		results.append([before, m, after])

	return results

def needs_to_be_excluded(before, after, around_len, m, regex):
	trimmed_before = before if len(before) < around_len else before[(len(before) - around_len):]
	trimmed_after = after if len(after) < around_len else after[:around_len]
	content = " {} {} {} ".format(" ".join(trimmed_before), m, " ".join(trimmed_after))
	matches = re.findall(regex, " {} ".format(content))
	for sub_m in matches:
		if len(re.findall(" {} ".format(m), " {} ".format(sub_m))) > 0: return True
	return False

# Finds the keywords within the files and outputs the relevant information.
def find_keywords(filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname):
	# Stores the frequency of each keyword across all files
	keyword_freq = defaultdict(lambda:0)

	# Stores the frequency of each keyword by file
	keyword_freq_files = {}
	keyword_counts_name = "{}_keyword_counts.csv".format(name)

	# Stores keyword collocations
	keyword_collocations = defaultdict(lambda:0)
	keyword_collocations_name = "{}_keyword_collocations.csv".format(name)

	# Stores data on how many times pairs of keywords appear together in the same file
	multiple_keyword = defaultdict(lambda:0)
	multiple_keyword_name = "{}_multiple_keywords.csv".format(name)

	# Stores data on keyword formats
	keyword_formats = defaultdict(lambda:[])
	keyword_format_name = "{}_keyword_formats.csv".format(name)

	all_contexts = {}

	# Basic statistics
	num_with_keywords = 0 # Number of files that have at least one keyword
	total_keywords = 0 # The total number of keywords found in all file

	for i in range(len(content)):
		file = filenames[i]
		c = " {} ".format(" ".join(content[i].lower().split())) # Adds a space before and after to distinguish for \b in regex
		print(c)
		curr_contexts = []
		curr_keywords = defaultdict(lambda:0)

		for j in range(len(include_regexes)):
			matches = re.findall(include_regexes[j], c)
			if len(matches) > 0: print("Searching for {}".format(include_regexes[j]))
			matches = list(set(matches)) # Removes duplicate matches
			for m in matches:
				results = get_words_around(m, c, NUM_WORDS_AROUND)
				match_len = len(m.split(" "))
				for before, m, after in results:
					print("Before: {}".format(" ".join(before)))
					print(m)
					print("After: {}".format(" ".join(after)))
					skip = False
					for r in exclude_regexes:
						regex_len = len(r.split(" "))
						around_len = regex_len - match_len
						if around_len < 0: continue
						if needs_to_be_excluded(before, after, around_len, m, r):
							skip = True
							print("EXCLUDE")
							break

					if skip: continue
					context = "...{} <b>{}</b> {}...".format(" ".join(before), m, " ".join(after))
					curr_contexts.append(context)
					keyword_freq[words[j]] += 1
					curr_keywords[words[j]] += 1

		if len(curr_keywords.keys()) > 0:
			curr_keywords_name = list(set(curr_keywords.keys()))
			num_with_keywords += 1
			keyword_freq_files[file] = curr_keywords
			for k1 in curr_keywords_name:
				total_keywords += curr_keywords[k1]
				for k2 in curr_keywords_name:
					if k1 == k2: continue
					curr = [k1, k2]
					curr.sort()
					multiple_keyword["{};{}".format(curr[0], curr[1])] += 1
		
		all_contexts[file] = curr_contexts

	# Writes some basic statistics into the report
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(write_header_line("Keyword Statistics"))
		f.write(write_span_line("Subcorpora written into directory", subcorpora_dirname))
		f.write(write_span_line("Multiple keyword counts written into file", multiple_keyword_name))
		f.write(write_span_line("Keyword counts written into file", keyword_counts_name))
		f.write(write_span_line("Total number of files at least one keyword", num_with_keywords))
		f.write(write_span_line("Total number of keywords found", total_keywords))

	# Writes the keyword counts by file into a CSV
	all_keyword_freqs = []
	for k, v in keyword_freq_files.items():
		for k_1, v_1 in sorted(v.items(), key = lambda kv: kv[1], reverse = True):
			all_keyword_freqs.append([k, k_1, v_1])
	df = pd.DataFrame(all_keyword_freqs)
	if len(all_keyword_freqs) > 0: df.to_csv(keyword_counts_name, index = False, header = ["filename", "keyword", "count"])

	# Writes the multiple keyword statistics into a CSV
	all_multiple_keyword = []
	for k, v in sorted(multiple_keyword.items(), key = lambda kv: kv[1], reverse = True):
		w = k.split(";")
		all_multiple_keyword.append([w[0], w[1], v])
	df = pd.DataFrame(all_multiple_keyword)
	if len(all_multiple_keyword) > 0: df.to_csv(multiple_keyword_name, index = False, header = ["word_1", "word_2", "count"])

	# Writes the keyword formats into a CSV
	all_keyword_formats = []
	for k, v in keyword_formats.items():
		if len(v) == 0: continue
		v.sort()
		all_keyword_formats.append([k, "; ".join(v)])
	df = pd.DataFrame(all_keyword_formats)
	if len(all_keyword_formats) > 0: df.to_csv(keyword_format_name, index = False, header = ["keyword", "formats"])

	# Writes the keyword contexts into the report
	with open(report_name, "a", encoding = "utf-8") as f:
		f.write(write_header_line("Keyword Contexts"))
		for k, v in all_contexts.items():
			f.write(write_list_lines(k, list(set(v))))

	write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files)

# Writes the subcorpora into the directory.
def write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files):
	os.mkdir(subcorpora_dirname)
	for i in range(len(filenames)):
		file = filenames[i]
		if file not in keyword_freq_files: continue
		new_file = "{}/{}".format(subcorpora_dirname, file)
		with open(new_file, "w", encoding = "utf-8") as f:
			f.write(content[i])

# Writes the top words in each file, minus stopwords and punctuation,
# into a CSV.
def get_top_words(filenames, content, name):
	dont_include = [] # Can be later used to add more words to exclude
	stop_words = set(stopwords.words("english") + list(string.punctuation) + list(dont_include))
	stats_name = "{}_file_top_words.csv".format(name)

	verb_tags = ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]

	all_words = []
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
		for k, v in sorted(word_map.items(), key = lambda kv: kv[1], reverse = True):
			# if v >= 50 or v <= 20: continue
			if num >= NUM_TOP_WORDS: break
			all_words.append([file, k, v])
			num += 1

	# Writes the top words of each file into a CSV
	df = pd.DataFrame(all_words)
	df.to_csv(stats_name, index = False, header = ["filename", "word", "count"])

# Reads in arguments into the directory, words, and metadata.
def read_arguments(parser):
	parser.add_argument("-d", "--directory", default = "corpus", help = "Directory corpora files are")
	parser.add_argument("-w", "--words", default = "keywords.txt", help = "File of keywords")
	parser.add_argument("-m", "--metadata", default = "metadata.csv", help = "CSV file with metadata")
	args = parser.parse_args()

	return args.directory, args.words, args.metadata

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
		f.write(write_header_line("Metadata Statistics"))

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

			if include:
				r = r"\b{}\b".format(w.replace("*", "[a-zA-Z]*"))
				include_regexes.append(r)
				include_words.append(w)
			else:
				r = r"\b{}\b".format(w.replace("*", "[a-zA-Z]*"))
				exclude_regexes.append(r)
				exclude_words.append(w)

	with open(report_name, "a", encoding = "utf-8") as f:
		text = "{}{}{}{}{}".format(
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
	report_name = "{}_report.html".format(name)
	write_beginning_of_html(report_name)

	filenames, content = read_corpus(directory, report_name)
	words, include_regexes, exclude_regexes = read_keywords(words, report_name)
	metadata = read_metadata(metadata, filenames, report_name)
	get_top_words(filenames, content, name)
	find_keywords(filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname)

	write_end_of_html(report_name)

if __name__ == '__main__':
	main()