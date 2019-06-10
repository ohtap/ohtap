import pandas as pd
from collections import defaultdict

def get_interview_data(r, project_file_name, interview_num):
	data = {
		"interview_id": interview_num,
		"original_file_name": r["original_file_name"],
		"project_file_name": project_file_name,
		"av_file": r["av_file"],
		"is_incomplete_transcript": "" if str(r["is_incomplete_interview"]) == "nan" else str(r["is_incomplete_interview"]),
		"no_transcript": "" if str(r["no_transcript"]) == "nan" else str(r["no_transcript"]),
		"interviewer_name(s)": r["interviewer_name"],
		"researcher_assumed_race": r["researcher_assumed_race"],
		"date_of_first_interview": r["date_of_first_interview"],
		"interview_city": r["interview_city"],
		"interview_state": r["interview_state"],
		"interview_country": r["interview_country"],
		"collection_id": r["collection_ID"],
		"interviewee_ids": "",
		"is_in_rape_cluster": "" if str(r["is_in_rape_cluster"]) == "nan" else str(r["is_in_rape_cluster"]),
		"is_in_abortion_cluster": "" if str(r["is_in_abortion_cluster"]) == "nan" else str(r["is_in_abortion_cluster"]),
		"interview_location_geonames_id": r["interview_location_geonames_ID"],
		"notes": r["Notes"]
	}

	return data

def get_interviewee_data(r, interviewee_num):
	data = {
		"interviewee_id": interviewee_num,
		"interviewee_name": r["interviewee_name"],
		"interviewee_class_year": r["interviewee_class_year"],
		"class_year_type": r["Class_year_type"],
		"approximate_age_at_time_of_interview": r["approx_age_at_time_of_interview"],
		"real_interviewee_birth_year": r["real_interviewee_birth_year"],
		"approximate_interviewee_birth_year": r["approximate_interviewee_birth_year"],
		"birth_decade": r["birth_decade"],
		"interviewee_birth_city": r["interviewee_birth_city"],
		"interviewee_birth_state": r["interviewee_birth_state"],
		"interviewee_birth_country": r["interviewee_birth_country"],
		"birthplace_type": r["birthplace_type"],
		"place_of_significant_residence": r["place_of_significant_residence"],
		"sex": r["sex"],
		"identified_race": r["identified_race"],
		"other_race": r["other_race"],
		"marital_status (at time of interview)": r["marital_status (at time of interview)"],
		"children": r["children"],
		"education": r["education"],
		"past_occupations": r["Past_Occupations"],
		"current_or_most_recent_occupation": r["Current_or_most_Recent_Occupation"],
		"eeo-1_job_category": r["EEO-1_job_category"],
		"eeo-1_job_title": r["EEO-1_job_title"],
		"soc_job_description": r["SOC_job_description"],
		"soc_job_code": r["SOC_job_code"],
		"census_code": r["census_code"],
		"spouse_occupation": r["Spouse_Occupation"],
		"birth_place_geonames_id": r["birth_place_geonames_ID"],
		"residence_geonames_id": r["residence_geonames_ID"]
	}

	return data

# Keeps track of files that have already been done for multiple files (for _1, _2, etc.)
done_multiple_files = {}

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

def write_interviews_to_file(interviews):
	df = pd.DataFrame([])
	for k, v in interviews.items():
		df = df.append(pd.DataFrame(v, index=[0]), ignore_index=True)

	df.to_csv("ohtap_interviews.csv", encoding="utf-8")

def write_interviewees_to_file(interviewees):
	df = pd.DataFrame([])
	for k, v in interviewees.items():
		for interviewee in v:
			df = df.append(pd.DataFrame(interviewee, index=[0]), ignore_index=True)

	df.to_csv("ohtap_interviewees.csv", encoding="utf-8")

def main():
	interview_num = 0 # Keeps track of universal interview ID
	interviewee_num = 0 # Keeps track of universal interviewee ID
	interviewees = defaultdict(lambda: []) # Interview --> interviewees
	interviews = defaultdict(lambda: {}) # Interview --> interview information

	df = pd.read_csv("ohtap_metadata_6102019.csv", header=0) # Reads in the data

	# Loops through data, storing the interview data and interviewee data
	for i, r in df.iterrows():
		project_file_name = r["project_file_name"]
		original_file_name = r["original_file_name"]
		if pd.isnull(project_file_name):
			print("NO PROJECT FILE NAME: {}".format(original_file_name))
			continue
		new_filename = remove_end(project_file_name)
		if new_filename not in interviews:
			interview_data = get_interview_data(r, new_filename, interview_num)
			interviews[new_filename] = interview_data
			interview_num += 1
		
		interviewee_data = get_interviewee_data(r, interviewee_num)
		interviewees[new_filename].append(interviewee_data)
		interviewee_num += 1

	# Loops back through the interviewee data, storing the interviewee IDs into the interview data
	for k, v in interviewees.items():
		ids = []
		for interviewee in v:
			ids.append(str(interviewee["interviewee_id"]))
		if len(ids) == 0: 
			continue
		interviews[k]["interviewee_ids"] = "; ".join(ids)

	# Writes to CSV files
	write_interviews_to_file(interviews)
	write_interviewees_to_file(interviewees)

if __name__ == '__main__':
	main()
