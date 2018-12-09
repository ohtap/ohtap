
from collections import defaultdict
from argparse import ArgumentParser
import os
import pandas as pd
import re
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from unidecode import unidecode

def read_keywords(file, report_name):
	

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

	with open(report_name, "a") as f:
		f.write("COLLECTION INFORMATION\n")
		f.write("Directory: {}\n".format(directory))
		f.write("Total number of files: {}\n".format(len(filenames)))

	return filenames, content

# Reads in arguments into the directory, words, and metadata.
def read_arguments(parser):
	parser.add_argument("-d", "--directory", default = "corpora", help = "Directory corpora files are")
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
		if not os.path.isfile("{}_report.txt".format(name)) and not os.path.isdir(name) and not os.path.isfile("{}_keyword_statistics.csv".format(name)): 
			break
		num_existing += 1
		name = "{}_{}_{}".format(collection_name, keywords_name, num_existing)

	return name

def main():
	directory, words, metadata = read_arguments(ArgumentParser())
	name = create_new_name(directory, words)
	report_name = "{}_report.txt".format(name)
	subcorpora_dirname = name
	keyword_stats_name = "{}_keyword_stats.csv".format(name)

	filenames, content = read_corpus(directory, report_name)

if __name__ == '__main__':
	main()