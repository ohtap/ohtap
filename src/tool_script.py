
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

NUM_TOP_WORDS = 20 # The number of top words that we want from each file
CONTEXT_WORDS_AROUND = 50
MAX_EXCLUDE_REGEX_LENGTH = 50
punctuation = ['\.', '/', '\?', '\-', '"', ',', '\\b'] # Punctuation we use within our regexes

keyword_to_dates = defaultdict(lambda: defaultdict(lambda :0))

# Reads in arguments into the directory, words, and metadata.
def read_arguments():
	return sys.argv[1], sys.argv[2], sys.argv[3]

# Sets up directory and filenames and reads in data.
def set_up():
	nltk.download('averaged_perceptron_tagger')
	nltk.download('stopwords')
	nltk.download('punkt')
	directory, words, metadata = read_arguments()
	print(directory, words, metadata)

def main():
	print("PROGRESS: 50")
	# directory, words, files_for_inclusion, name, subcorpora_dirname, report_name, filenames, content, words, include_regexes, exclude_regexes, metadata, interview_years_by_file = set_up()
	set_up()

if __name__ == '__main__':
	main()
