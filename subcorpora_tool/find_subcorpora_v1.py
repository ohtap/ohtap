
from collections import defaultdict
from argparse import ArgumentParser
import os
import pandas as pd
import re
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from unidecode import unidecode

# Reads all the text from each text file in the directory
def read_corpus(directory, final_filename):
	filenames = []
	content = []
	for file in os.listdir(directory):
		if ".txt" not in file: continue
		filenames.append(file)
		with open("{}/{}".format(directory, file), "r", encoding = "utf-8") as f:
			content.append(f.read())

	with open(final_filename, "a") as f:
		f.write("COLLECTION INFORMATION\n")
		f.write("Directory: {}\n".format(directory))
		f.write("Total number of files: {}\n".format(len(filenames)))

	return filenames, content

def turn_to_regex(w):
	return r"\b{}\b".format(w.replace("*", "[a-zA-Z]*"))

# Reads in the keywords
def read_keywords(file, final_filename):
	words = []
	regexes = []

	with open(final_filename, "a") as f:
		f.write("KEYWORD INFORMATION\n")

	with open(file, "r") as f:
		words = [x.strip().lower() for x in f.readlines()]
		for w in words:
			r = turn_to_regex(w)
			regexes.append(r)

	with open(final_filename, "a") as f:
		f.write("Filename: {}\n".format(file))
		f.write("Total number of keywords: {}\n".format(len(regexes)))
		f.write("Keywords: {}\n".format("; ".join(words)))
		f.write("\n")

	return words, regexes

# Reads in the metadata to collect statistics
def read_metadata(file, filenames, final_filename):
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

	with open(final_filename, "a") as f:
		f.write("Interviewees' birth decade counts:\n")
		for k, v in birth_decade.items():
			if k == "": k = "Not given"
			f.write("\t{}: {}\n".format(k, v))
		f.write("Interviewees' education counts:\n")
		for k, v in education.items():
			if k == "": k = "Not given"
			f.write("\t{}: {}\n".format(k, v))
		f.write("Interviewees' identified race counts:\n")
		for k, v in identified_race.items():
			if k == "": k = "Not given"
			f.write("\t{}: {}\n".format(k, v))
		f.write("Interviewees' sex counts:\n")
		for k, v in sex.items():
			if k == "": k = "Not given"
			f.write("\t{}: {}\n".format(k, v))
		f.write("Interviewees' birth country counts:\n")
		for k, v in birth_country.items():
			if k == "": k = "Not given"
			f.write("\t{}: {}\n".format(k, int(v)))
		f.write("\n")

	return info

# Finds the keywords within the files and outputs relevant information
def find_keywords(filenames, content, words, regexes, final_filename, final_dirname):
	keyword_frequencies = defaultdict(lambda:0)
	keyword_frequencies_files = {}
	num_files_with_keywords = 0
	num_files_with_one_keyword = 0
	total_keywords = 0
	keyword_collocations = defaultdict(lambda:0)

	for i in range(len(content)):
		f = filenames[i]
		c = content[i].lower()
		appeared_keywords = defaultdict(lambda:0)
		for j in range(len(regexes)):
			matches = re.findall(regexes[j], c)
			for m in matches:
				total_keywords += 1
				keyword_frequencies[words[j]] += 1
				appeared_keywords[words[j]] += 1
		if len(appeared_keywords.keys()) == 1: num_files_with_one_keyword += 1
		if len(appeared_keywords.keys()) > 1: 
			num_files_with_keywords += 1
			for k1 in appeared_keywords.keys():
				for k2 in appeared_keywords.keys():
					if k1 == k2: continue
					curr = [k1, k2]
					curr.sort()
					keyword_collocations[", ".join(curr)] += 1
		if len(appeared_keywords.keys()) > 0: keyword_frequencies_files[f] = appeared_keywords	

	with open(final_filename, "a") as f:
		f.write("KEYWORD STATISTICS\n")
		f.write("Subcorpora written into directory: {}\n".format(final_dirname))
		f.write("Total number of files with one keyword: {}\n".format(num_files_with_one_keyword))
		f.write("Total number of files with more than one keyword: {}\n".format(num_files_with_keywords))
		f.write("Total number of keywords found: {}\n".format(total_keywords))
		f.write("\n")

		f.write("KEYWORD COLLOCATION STATISTICS\n")
		for k, v in sorted(keyword_collocations.items(), key=lambda kv: kv[1], reverse=True):
			f.write("{}: {}\n".format(k, v))
		f.write("\n")

		f.write("KEYWORD BY FILE STATISTICS\n")
		for k, v in keyword_frequencies_files.items():
			f.write("{}: ".format(k))
			items = ["{} ({})".format(k_1, v_1) for k_1, v_1 in sorted(v.items(), key=lambda kv: kv[1], reverse=True)]
			f.write("{}\n".format(", ".join(items)))
		f.write("\n")

	write_subcorpora(final_dirname, filenames, content, keyword_frequencies_files)

	return keyword_frequencies_files

# Writes the subcorpora into a subdirectory
def write_subcorpora(final_dirname, filenames, content, keyword_frequencies_files):
	os.mkdir(final_dirname)
	for i in range(len(filenames)):
		file = filenames[i]
		if file not in keyword_frequencies_files: continue
		new_f = "{}/{}".format(final_dirname, file)
		with open(new_f, "w", encoding = "utf-8") as f:
			f.write(content[i])

# Writes the top words in each file, minus stopwords and punctuation
def get_top_words(filenames, content, final_filename):
	dont_include = [] # Can be used to add stopwords
	with open(final_filename, "a") as f:
			f.write("TOP WORDS BY FILE STATISTICS\n")

	stop_words = set(stopwords.words("english") + list(string.punctuation) + list(dont_include))
	for i in range(len(filenames)):
		file = filenames[i]
		c = unidecode(content[i].lower())
		word_tokens = word_tokenize(c)
		filtered = []
		for w in word_tokens:
			if w in stop_words: continue
			has_punc = False
			for c in w:
				if c in string.punctuation: has_punc = True
			if has_punc: continue

			filtered.append(w)
		
		word_map = defaultdict(lambda:0)
		for w in filtered:
			word_map[w] += 1

		num = 0
		all_words = []
		for k, v in sorted(word_map.items(), key=lambda kv: kv[1], reverse=True):
			if num >= 20: break
			all_words.append("{} ({})".format(k, v))
			num += 1
		
		with open(final_filename, "a", encoding = "utf-8") as f:
			f.write("{}: {}\n".format(file, ", ".join(all_words)))

	with open(final_filename, "a") as f:
		f.write("\n")

# Splits into sentences
def split_into_sentences(c):
	return re.split('\.|\!|\?', c)

# Writes out the context in which these keywords appear
def get_context(filenames, content, keyword_frequencies_files, final_filename):
	with open(final_filename, "a", encoding = "utf-8") as f:
		f.write("KEYWORD CONTEXTS\n")

	for i in range(len(filenames)):
		file = filenames[i]
		if file not in keyword_frequencies_files: continue
		freq = keyword_frequencies_files[file]
		sentences = split_into_sentences(content[i])
		has_keyword = []
		for s in sentences:
			s = s.replace("\n", " ").replace("\t", " ")
			s = re.sub('\s+', ' ', s).strip()
			for k in freq.keys():
				matches = re.findall(turn_to_regex(k), s)
				if len(matches) > 0:
					has_keyword.append(s)
					break

		with open(final_filename, "a", encoding = "utf-8") as f:
			f.write("{}:\n".format(file))
			for s in has_keyword:
				f.write("\t...{}...\n".format(s))

	with open(final_filename, "a", encoding = "utf-8") as f:
		f.write("\n")

def main():
	# Gets arguments using parser
	parser = ArgumentParser()
	parser.add_argument("-d", "--directory", help = "Directory where files are")
	parser.add_argument("-w", "--words", help = "File with keywords")
	parser.add_argument("-m", "--metadata", help = "File with metadata")
	args = parser.parse_args()

	# Creates a new file where we'll store the report
	collection_name = args.directory.split("/")[-1]
	final_filename = "{}_report.txt".format(collection_name)
	final_dirname = "{}_subcorpora".format(collection_name)
	num_existing = 0
	while True:
		if not os.path.isfile(final_filename): break
		num_existing += 1
		final_filename = "{}_report_{}.txt".format(collection_name, num_existing)
		final_dirname = "{}_subcorpora_{}".format(collection_name, num_existing)


	filenames, content = read_corpus(args.directory, final_filename)
	metadata = read_metadata(args.metadata, filenames, final_filename)
	words, regexes = read_keywords(args.words, final_filename)
	keyword_frequencies_files = find_keywords(filenames, content, words, regexes, final_filename, final_dirname)
	get_top_words(filenames, content, final_filename)
	get_context(filenames, content, keyword_frequencies_files, final_filename)
	

if __name__ == '__main__':
	main()