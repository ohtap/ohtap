# from argparse import ArgumentParser
import sys

# directory, words, metadata = read_arguments(ArgumentParser())
# parser.add_argument("-d", "--directory", default = "corpus", help = "Directory corpora files are")
# 	parser.add_argument("-w", "--words", default = "keywords.txt", help = "File of keywords")
# 	parser.add_argument("-m", "--metadata", default = "metadata.csv", help = "CSV file with metadata")
# 	args = parser.parse_args()
# parser = ArgumentParser()
# parser.add_argument("-m", "--me")
# args = parser.parse_args()
# args.me = "hi"
# print("HELLO PYTHON IS RUNNING LEN " + args.me)
print("Metadata file is: " + sys.argv[1])
print("Collection is: " + sys.argv[2])
print("Keyword list is: " + sys.argv[3])