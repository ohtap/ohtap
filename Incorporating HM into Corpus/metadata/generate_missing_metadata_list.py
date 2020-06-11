import pandas as pd


output_csv_header = ["project_file_name", "collection_id", "date_of_first_interview", "birth_decade",
                     "researcher_assumed_race OR identified_race", "education", "current_or_most_recent_occupation"]

def get_missing_metadata(filename, current_interview, interviewees_df):

    interviewees = current_interview["interviewee_ids"].split(";")
    for i in range(len(interviewees)):
        interviewees[i] = interviewees[i].strip()

    date_of_first_interview_presence = "Present" if isinstance(current_interview["date_of_first_interview"], str) else "Missing"

    birth_decade_presence, race_presence, education_presence, occupation_presence = "", "", "", ""

    for vee_id in interviewees:
        for i, row in interviewees_df.iterrows():
            if row["interviewee_id"] == vee_id:
                birth_decade_presence = "Present" if birth_decade_presence != "Missing" and not pd.isnull(row["birth_decade"]) else "Missing"
                race_presence = "Present" if race_presence != "Missing" and (not pd.isnull(row["researcher_assumed_race"]) or
                                                                             not pd.isnull(row["identified_race"])) else "Missing"
                education_presence = "Present" if education_presence != "Missing" and not pd.isnull(row["education"]) else "Missing"
                occupation_presence = "Present" if occupation_presence != "Missing" and not pd.isnull(row["current_or_most_recent_occupation"]) else "Missing"

                break

    return [filename, current_interview["collection_id"], date_of_first_interview_presence, birth_decade_presence,
            race_presence, education_presence, occupation_presence]

def main():
    files_df = pd.read_csv("fixed_duplicates.csv")
    filenames_list = list(files_df["project_file_name"])

    interviews_df = pd.read_csv("interviews.csv")
    interviewees_df = pd.read_csv("interviewees.csv")


    missing_metadata_list = []

    for i, r in interviews_df.iterrows():
        if r["project_file_name"] in filenames_list:
            missing_any = False
            missing_metadata = get_missing_metadata(r["project_file_name"], r, interviewees_df)
            for i in range(2, 7):
                if missing_metadata[i] == "Missing":
                    missing_any = True
                    break
            if missing_any: missing_metadata_list.append(missing_metadata)

    missing_metadata_df = pd.DataFrame(missing_metadata_list)
    missing_metadata_df.to_csv("missing_metadata.csv", index=False, header=output_csv_header)

if __name__ == '__main__':
    main()