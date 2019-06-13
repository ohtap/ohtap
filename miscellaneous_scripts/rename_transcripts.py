import os
import pandas as pd
import shutil

current_dir = os.getcwd() # current directory you're in
# EDIT THIS SECTION #
collection = "UNCSW" # path to your collections folder
interview_metadata = "interviews.csv" # name of the metadata file
#####################

# Removes the _a, _b, etc. associated with multiple interviewees.
def remove_end(filename):
	modified_filename = filename.replace(".txt", "")
	parts = modified_filename.split("_")

	last_part = str(parts[-1])
	num = None

	# Checks first to see if it's _1, _2, etc. and stores that number
	if last_part.isdigit():
		num = int(last_part)
		parts = parts[:-1]

	# Removes the _a, _b, etc. at the end
	new_filename = modified_filename
	last_part = str(parts[-1])
	if len(last_part) == 1 and last_part.isalpha():
		new_filename = "_".join(parts[0:-1])

		# Adds in the _1, _2, etc.
		if num is not None:
			new_filename = "{}_{}".format(new_filename, num)

	return "{}.txt".format(new_filename.replace("__", "_"))

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

# Copies and creates a new file with new name
def create_and_rename(filename, new_filename):
	full_filename = os.path.join(current_dir, collection, filename)
	full_new_filename = os.path.join(current_dir, new_collection, new_filename)
	if os.path.exists(full_new_filename):
		raise Exception("{} already exists--either you haven't cleared the folder or the code has an error.".format(new_filename))
	shutil.copy(full_filename, full_new_filename)

# Makes the new folder where the new files are going to be stored
new_collection = "{}_new".format(collection)
if not os.path.exists(new_collection):
	os.mkdir(new_collection)

# Reads in the metadata
df = pd.read_csv(interview_metadata)
all_files = {}
for i, r in df.iterrows():
	all_files[r["project_file_name"]] = 1

# Reads through all the files
full_num = 0
for filename in sorted(os.listdir(collection)):
	full_num += 1
	new_filename = filename

	if new_filename not in all_files:
		new_filename = remove_end(filename)
		if new_filename not in all_files:
			check_filename = "{}_1.txt".format(new_filename.replace(".txt", ""))
			if check_filename in all_files:
				new_filename = check_filename
		else:
			num, modified_file_name = remove_number(new_filename)
			if num is not None:
				check_filename = "{}_{}.txt".format(modified_file_name.replace(".txt", ""), num + 1)
				if check_filename in all_files:
					new_filename = check_filename

	if new_filename not in all_files:
		raise Exception("{} not in metadata! Error with code!".format(new_filename))

	create_and_rename(filename, new_filename)
	print("{}->{}".format(filename, new_filename))

# Final check
new_full_num = 0
for filename in os.listdir(new_collection):
	new_full_num += 1

print("Old directory count: {}".format(full_num))
print("New directory count: {}".format(new_full_num))
