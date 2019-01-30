
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
HIGHLIGHTED_WORDS_AROUND = 100 # The number of words we want before and after (separate) for in-context
CONTEXT_WORDS_AROUND = 100
MAX_EXCLUDE_REGEX_LENGTH = 10
punctuation = ['\.', '/', '\?', '\-', '"', ',', '\\b'] # Punctuation we use within our regexes

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

# Gets punctuation joined by bars
def get_punctuation_for_regex():
	return "|".join(punctuation)

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
				punc = get_punctuation_for_regex()
				r = r'(?:{})({})(?:{})'.format(punc, w.replace("*", "[a-zA-Z]*"), punc)
				include_regexes.append(r)
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

	return words, include_regexes, exclude_regexes

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
		with open("{}/{}".format(directory, file), "r", encoding = "utf-8") as f:
			print(file)
			content.append(f.read())
	
	write_header_line(report_name, "Collection Information")
	write_span_line(report_name, "Directory", directory)
	write_span_line(report_name, "Total number of files", len(filenames))

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

# Reads in arguments into the directory, words, and metadata.
def read_arguments(parser):
	parser.add_argument("-d", "--directory", default = "corpus", help = "Directory corpora files are")
	parser.add_argument("-w", "--words", default = "keywords.txt", help = "File of keywords")
	parser.add_argument("-m", "--metadata", default = "metadata.csv", help = "CSV file with metadata")
	args = parser.parse_args()

	return args.directory, args.words, args.metadata

# Parses through the data to get counts.
def get_metadata_counts(df, filenames):
	include = {} # Information about the files in this subcorpus
	for f in filenames: include[f] = 0
	people = {} # Information about individual people (only females or unknown)
	male_interviews = {} # Keeps track of which interviews have males
	male_and_female_interviews = {} # Keeps track of which interviews have male and non-male interviewees

	for i, r in df.iterrows():
		f = r[6]
		if f in include:
			interviewee_name = r[7]
			if not pd.isnull(r[25]) and r[25].strip() == "Male": 
				male_interviews[f] = 1
				continue
			if f in male_interviews: male_and_female_interviews[f] = 1
			include[f] = 1

			# Adds the interviewee (assumes that the first entry contains all the complete information)
			if interviewee_name not in people: 
				people[interviewee_name] = {}
				people[interviewee_name]["birth_year"] = r[17] if not pd.isnull(r[17]) else ""
				people[interviewee_name]["birth_decade"] = r[19] if not pd.isnull(r[19]) else ""
				people[interviewee_name]["education"] = r[31] if not pd.isnull(r[31]) else ""
				people[interviewee_name]["identified_race"] = r[26] if not pd.isnull(r[26]) else ""
				people[interviewee_name]["sex"] = r[25] if not pd.isnull(r[25]) else ""
				people[interviewee_name]["birth_country"] = r[22] if not pd.isnull(r[22]) else ""

			# Adds the file information
			# TODO: Not sure if needed

	return include, people, male_and_female_interviews

# Reads the metadata to collect statistics. Excludes any interview with males only.
def read_metadata(file, filenames, report_name):
	df = pd.read_csv(file, encoding = "utf-8", header = None)
	include, people, male_and_female_interviews = get_metadata_counts(df, filenames)

	# Metadata information to output for individual interviewees
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
	write_span_line(report_name, "Number of interviews included", str(len(include.keys())))
	write_span_line(report_name, "Number of interviews included that have both male and non-male interviewees", str(len(male_and_female_interviews.keys())))
	write_span_line(report_name, "Total unique interviewees", str(len(people.keys())))

	birth_decade_arr = []
	for k, v in birth_decade.items():
		k = "Not given" if (k == "" or k == "Unknown") else int(k)
		birth_decade_arr.append("{}: {}".format(k, v))
	write_list_lines(report_name, "Interviewees' birth decade counts", birth_decade_arr)

	education_arr = []
	for k, v in education.items():
		if k == "": k = "Not given"
		education_arr.append("{}: {}".format(k, v))
	write_list_lines(report_name, "Interviewees' education counts", education_arr)

	identified_race_arr = []
	for k, v in identified_race.items():
		if k == "": k = "Not given"
		identified_race_arr.append("{}: {}".format(k, v))
	write_list_lines(report_name, "Interviewees' identified race counts", education_arr)

	sex_arr = []
	for k, v in sex.items():
		if k == "": k = "Not given"
		sex_arr.append("{}: {}".format(k, v))
	write_list_lines(report_name, "Interviewees' sex counts", sex_arr)

	birth_country_arr = []
	for k, v in birth_country.items():
		if k == "": k = "Not given"
		birth_country_arr.append("{}: {}".format(k, v))
	write_list_lines(report_name, "Interviewees' birth country counts", birth_country_arr)


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

def is_punctuation(ch):
	for p in punctuation:
		if p == "\\b": continue
		if p[0] == "\\": p = p[1:]
		if ch == p: return True
	return False

# Gets n words before and after the match and returns them as arrays
def get_words_around(m_text, m_loc, content, n):
	new_m_text = m_text

	# Skips over the punctuation in the beginning if necessary
	start_loc = m_loc
	if is_punctuation(content[m_loc]):
		new_m_text = "{}{}".format(content[start_loc], new_m_text)
		start_loc += 1
	
	# Skip over the punctuation in the end if necessary
	after_loc = start_loc + len(m_text)
	if len(content) > after_loc and is_punctuation(content[after_loc]):
		new_m_text = "{}{}".format(new_m_text, content[after_loc])
		after_loc += 1

	before_text = content[:m_loc].split()
	before = []
	before_text.reverse()
	num = 0
	for w in before_text:
		if num >= n: break
		before.append(w)
		if is_punctuation(w): continue # Doesn't count punctuation as words
		num += 1
	before.reverse()
			
	after_text = content[after_loc:].split()
	after = []
	num = 0
	for w in after_text:
		if num >= n: break
		after.append(w)
		if is_punctuation(w): continue # Doesn't count punctuation as words
		num += 1

	return before, new_m_text, after

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

# Bolds keyword matches.
def bold_keyword_matches(c, sorted_matches):
	bolded_content = ""
	last_char = 0 # NOT included in the last round
	add_on = 0
	bolds_added = 0
	for sm in sorted_matches:
		loc = sm[0]
		match = sm[1]
		if "</b>" in bolded_content[(loc + (bolds_added * len("<b>"))):]: continue
		bolded_content = "{}{}<b>{}</b>".format(bolded_content, c[last_char:loc], c[loc:(loc + len(match))])
		bolds_added += 1
		last_char = loc + len(match)
	if last_char < len(c): bolded_content = "{}{}".format(bolded_content, c[last_char:len(c)])
	
	return bolded_content

# Highlights the context.
def highlight_context(c):
	all_words = c.split(" ")
	modified_words = []
	start = False
	count = 0
	for w in all_words:
		if start: count += 1
		if "</b>" in w:
			count = 0
			start = True
		if count == HIGHLIGHTED_WORDS_AROUND:
			count = 0
			w = "{}</mark>".format(w)
			start = False
		modified_words.append(w)
	if start: modified_words[-1] = "{}</mark>".format(modified_words[-1])
	all_words = modified_words
	all_words.reverse()

	modified_words = []
	start = False
	count = 0
	for w in all_words:
		if start: count += 1
		if "<b>" in w:
			count = 0
			start = True
		if count == HIGHLIGHTED_WORDS_AROUND:
			count = 0
			w = "<mark>{}".format(w)
			start = False
		modified_words.append(w)
	if start: modified_words[-1] = "<mark>{}".format(modified_words[-1])
	modified_words.reverse()

	new_c = " ".join(modified_words)

	return new_c

# Highlight the context and returns a list of the contexts.
def get_context_lists(c):
	all_words = c.split(" ")
	all_new_words = []
	curr_words = []
	include = False
	for w in all_words:
		if "<mark>" in w: include = True
		if include: 
			curr_words.append(w)
		if "</mark>" in w: 
			include = False
			all_new_words.append(" ".join(curr_words))
			curr_words = []

	return "...{}...".format("... ... ...".join(all_new_words)).replace("<mark>", "").replace("</mark>", "")

# Writes out subcorpora with highlighted information
def write_highlighted_subcorpora(subcorpora_dirname, filenames, content, all_matches):
	all_contexts = {}

	highlighted_subcorpora_dirname = "{}_highlighted".format(subcorpora_dirname)
	os.mkdir(highlighted_subcorpora_dirname)	
	for i in range(len(filenames)):
		file = filenames[i]
		c = content[i]
		if file not in all_matches: continue
		sorted_matches = sorted(all_matches[file], key=lambda x: x[0])
		bolded_content = bold_keyword_matches(c, sorted_matches)
		highlighted_content = highlight_context(bolded_content)
		contexts = get_context_lists(highlighted_content)
		all_contexts[file] = contexts
		new_file = "{}/{}".format(highlighted_subcorpora_dirname, file).replace(".txt", ".html")
		with open(new_file, "w", encoding = "utf-8") as f:
			f.write("<html><head></head><body>")
			f.write(highlighted_content)
			f.write("</body></html>")

	return all_contexts

# Finds the keywords within the files and outputs the relevant information.
def find_keywords(filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname):
	# Stores the frequency of each keyword across all files
	keyword_freq = defaultdict(lambda:0)
	keyword_counts_name = "{}_keyword_counts.csv".format(name)

	# Stores the frequency of each keyword by file
	keyword_freq_files = {}
	keyword_counts_file_name = "{}_keyword_counts_by_file.csv".format(name)

	# Stores keyword collocations
	keyword_collocations = defaultdict(lambda:0)
	keyword_collocations_name = "{}_keyword_collocations.csv".format(name)
	keyword_collocations_format_name = "{}_keyword_collocations_formats.csv".format(name)
	keyword_collocations_format = defaultdict(lambda: [])

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

	# Loops through each file
	for i in range(len(content)):
		file = filenames[i]
		c = " {}.".format(" ".join(content[i].split()))

		curr_keywords = defaultdict(lambda:0)
		curr_matches = []

		# Loops through each keyword
		for j in range(len(include_regexes)):
			curr_r = include_regexes[j]
			regex = re.compile(curr_r, re.IGNORECASE) # Currently ignores the case
			for m in regex.finditer(c):
				m_loc = m.start()
				m_text = m.group(1)
				before, new_m_text, after = get_words_around(m_text, m_loc, c, MAX_EXCLUDE_REGEX_LENGTH)

				if need_to_exclude(before, after, new_m_text, exclude_regexes): continue

				keyword_freq[words[j]] += 1
				curr_keywords[words[j]] += 1
				keyword_formats[words[j]].append(m_text)
				curr_matches.append([m_loc, m_text])

				collocations, collocations_f = check_for_collocations(before, after, m_text, new_m_text, j, include_regexes)
				for l in range(len(collocations)):
					col = collocations[l]
					col_f = collocations_f[l]
					k = "{};{}".format(words[col[0]], words[col[1]])
					keyword_collocations[k] += 0.5
					keyword_collocations_format[k].append("{} {}".format(col_f[0], col_f[1]))

		if len(curr_keywords.keys()) > 0: 
			num_with_keywords += 1
			keyword_freq_files[file] = curr_keywords
			total_keywords += len(curr_keywords)
			all_matches[file] = curr_matches
			content[i] = c

	get_multiple_keyword_counts(curr_keywords, multiple_keyword)
	write_keyword_basic_statistics(report_name, subcorpora_dirname, multiple_keyword_name, keyword_counts_name, num_with_keywords, total_keywords, len(content))
	write_keyword_counts_to_csv(keyword_freq, keyword_counts_name, keyword_freq_files, keyword_counts_file_name)
	write_keyword_collocations_to_csv(keyword_collocations, keyword_collocations_name, keyword_collocations_format, keyword_collocations_format_name)
	write_multiple_keyword_to_csv(multiple_keyword, multiple_keyword_name)
	write_keyword_formats_to_csv(keyword_formats, keyword_format_name)
	write_subcorpora(subcorpora_dirname, filenames, content, keyword_freq_files)
	all_contexts = write_highlighted_subcorpora(subcorpora_dirname, filenames, content, all_matches)
	write_header_line(report_name, "Contexts")
	for file, contexts in all_contexts.items():
		write_list_lines(report_name, file, [contexts])

# Sets up directory and filenames and reads in data.
def set_up():
	directory, words, metadata = read_arguments(ArgumentParser())
	name = create_new_name(directory, words)
	subcorpora_dirname = name
	report_name = "{}_report.html".format(name)
	write_beginning_of_html(report_name)

	filenames, content = read_corpus(directory, report_name)
	words, include_regexes, exclude_regexes = read_keywords(words, report_name)
	metadata = read_metadata(metadata, filenames, report_name)

	return directory, words, metadata, name, subcorpora_dirname, report_name, filenames, content, words, include_regexes, exclude_regexes, metadata

def main():
	directory, words, metadata, name, subcorpora_dirname, report_name, filenames, content, words, include_regexes, exclude_regexes, metadata = set_up()
	get_top_words(filenames, content, name)
	find_keywords(filenames, content, words, include_regexes, exclude_regexes, report_name, name, subcorpora_dirname)
	write_end_of_html(report_name)

if __name__ == '__main__':
	main()
