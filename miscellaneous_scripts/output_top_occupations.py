
from collections import defaultdict
import pandas as pd

# Reads the metadata to collect information on each of the files.
def read_metadata(file):
	df = pd.read_csv(file, encoding = "utf-8", header = None)

	occupations = defaultdict(lambda:0)
	for i, r in df.iterrows():
		past_occupations = r[32]
		current_occupations = r[33]
		if not pd.isnull(past_occupations):
			for p in past_occupations.split(";"):
				p = p.strip().lower()
				occupations[p] += 1
		if not pd.isnull(current_occupations):
			for p in current_occupations.split(";"):
				p = p.strip().lower()
				occupations[p] += 1

	return occupations

def main():
	occupations = read_metadata("metadata.csv")
	with open("occupations.csv", "w") as f:
		for k, v in sorted(occupations.items(), key = lambda x:x[1], reverse = True):
			f.write("{}: {}\n".format(k, v))

if __name__ == '__main__':
	main()