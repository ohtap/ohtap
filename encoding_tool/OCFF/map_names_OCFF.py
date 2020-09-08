# Creates a map of how speakers are refered to

import pandas as pd
import sys
import os

transcript_folder = "PATH OF TRANSCRIPT FOLDER GOES HERE"

# Get data for the interviews
interview_md = "INTERVIEW METADATA CSV SHEET PATH GOES HERE"
interview_md = pd.read_csv(interview_md).set_index("project_file_name")

# Get data for the interviewees
interviewees_md = "INTERVIEWEE METADATA CSV SHEET PATH GOES HERE"
interviewees_md = pd.read_csv(interviewees_md).set_index("interviewee_id")

# Set up the csv
speaker_map = {"file_name" : [], "spk_1" : [], "spk_2" : [], "spk_3" : [], "spk_4" : [], "spk_5" : [], "spk_6" : []}
num_spk_cols = 6                # Tracks the number of columns for speakers thus far
num_done = 0                    # Tracks the number of interviews already mapped

# Iterate through each transcript
for entry in os.scandir(transcript_folder):
    if entry.name.endswith(".txt") and entry.name.startswith("OCFF"):
        # Add name of file
        speaker_map["file_name"].append(entry.name)

        # Get Interviewer names
        interviewers = interview_md.loc[entry.name].at["interviewer_names"].split(";")

        # Get Interviewee names
        interviewee_ids = interview_md.loc[entry.name].at["interviewee_ids"].split(";")
        interviewees = []
        for id in interviewee_ids:
            interviewees.append(interviewees_md.loc[id.strip()].at["interviewee_name"])

        # Add speakers to name map
        current_col = 1
        for speaker in interviewers:
            text = "interviewer;" + speaker

            # Check for speaker references
            lines = open(entry.path).read().splitlines()
            found_ref = False
            for line in lines:
                # Extract first and last name from expected format of Last, First
                last_name = speaker.split(",")[0].strip().lower()
                first_name = speaker.split(",")[1].strip().lower()
                if line.strip().lower() == last_name:
                    found_ref = last_name
                    break
                if line.strip().lower() == first_name[0] + ". " + last_name:
                    found_ref = first_name[0] + ". " + last_name
                    break
                if line.strip().lower() == first_name:
                    found_ref = first_name
                    break
            
            # Add reference to table if found and MISSING if not
            if found_ref:
                text += ";" + found_ref
            else:
                text += ";" + "MISSING"

            speaker_map["spk_" + str(current_col)].append(text)
            current_col += 1

        for speaker in interviewees:
            text = "interviewee;" + speaker

            # Check for speaker references
            lines = open(entry.path).read().splitlines()
            found_ref = False
            for line in lines:
                # Extract first and last name from expected format of Last, First
                last_name = speaker.split(",")[0].strip().lower()
                first_name = speaker.split(",")[1].strip().lower()
                if line.strip().lower() == last_name:
                    found_ref = last_name
                    break
                if line.strip().lower() == first_name[0] + ". " + last_name:
                    found_ref = first_name[0] + ". " + last_name
                    break
                if line.strip().lower() == first_name:
                    found_ref = first_name
                    break
            
            # Add reference to table if found and MISSING if not
            if found_ref:
                text += ";" + found_ref
            else:
                text += ";" + "MISSING"

            speaker_map["spk_" + str(current_col)].append(text)
            current_col += 1

        while current_col <= num_spk_cols:
            speaker_map["spk_" + str(current_col)].append("")
            current_col += 1


# Print/return the csv
speaker_map = pd.DataFrame.from_dict(speaker_map)
print(speaker_map.to_csv())
