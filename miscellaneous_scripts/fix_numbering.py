# There was an error with our numbering system. All files starting from UNCSW and
# afterwards that were multiple files for one interviewee didn't start with _1 but
# instead was the plain filename and then started numbering (going against our original)
# metadata schema. This python file fixes it.
# Hilary (hilary@cs.stanford.edu) on 6/10/2019

import pandas as pd
from collections import defaultdict

# Removes the last number (if there is one)
def remove_number(project_file_name):
	modified_file_name = project_file_name.replace(".txt", "")
	parts = modified_file_name.split("_")
	last_part = str(parts[-1])
	num = None
	if last_part.isdigit():
		modified_file_name = "{}".format("_".join(parts[:-1]))
		num = int(last_part)
	modified_file_name = "{}.txt".format(modified_file_name)

	return num, modified_file_name

# Reads in the data
df = pd.read_csv("ohtap_metadata.csv", header=0)

# Counts up the files in each filename
filenames = defaultdict(lambda:0)
for i, r in df.iterrows():
	project_file_name = r["project_file_name"]
	if pd.isnull(project_file_name):
		continue

	_, modified_file_name = remove_number(project_file_name)
	filenames[modified_file_name] += 1

new_df = df.copy() # Deep copies the dataframe

# Modifies the filenames is there are multiple
for i, r in df.iterrows():
	if r["UID"] < 100772: continue
	project_file_name = r["project_file_name"]
	if pd.isnull(project_file_name):
		continue

	num, modified_file_name = remove_number(project_file_name)
	if filenames[modified_file_name] > 1:
		if num is None:
			modified_file_name = "{}_1.txt".format(modified_file_name.replace(".txt", ""))
		else:
			modified_file_name = "{}_{}.txt".format(modified_file_name.replace(".txt", ""), num + 1)
		print("{} -> {}".format(project_file_name, modified_file_name))
		new_df.loc[i, "project_file_name"] = modified_file_name

new_df.to_csv("ohtap_metadata_revised.csv", encoding="utf-8")
