import pandas as pd
import os

output_csv_header = ["interviewee_name", "collection_id", "real_interviewee_birth_year",
                     "birth_decade", "researcher_assumed_birth_decade", "researcher_assumed_race",
                     "identified race"]

def main():
    old_metadata = pd.read_csv("Interviewees.csv")

    new_metadata = pd.read_csv("missing_priority_metadata.csv")

    updated_metadata = []

    new_metadata_dict = {}

    #Generate new_metadata_dict
    for index, row in new_metadata.iterrows():
        current_key = row["project_file_name"]
        current_key = os.path.splitext(current_key)[0]
        current_key = current_key.format("_1", "")
        current_key = current_key.format("_2", "")


        # Get the interviewee's name
        current_key_words = current_key.split("_")
        if len(current_key_words) == 4:
            current_key = current_key_words[1] + ", " + current_key_words[2] + " " + current_key_words[3]
        elif len(current_key_words) == 3:
            current_key = current_key_words[1] + ", " + current_key_words[2]
        else:
            print("This is a serious problem: " + current_key)

        collection_id = row["collection_id"]
        real_interviewee_birth_year, birth_decade, researcher_assumed_birth_decade, researcher_assumed_race, identified_race = "", "", "", "", ""

        #Get birth year/decade
        if not pd.isnull(row["year of birth"]):
            real_interviewee_birth_year = row["year of birth"]
            birth_decade = int(real_interviewee_birth_year) - int(real_interviewee_birth_year)%10
        elif not pd.isnull(row["birth_decade"]):
            birth_decade = row["birth_decade"]
        elif not pd.isnull(row["researcher_assumed_birth_decade"]):
            researcher_assumed_birth_decade = row["researcher_assumed_birth_decade"]

        #Get race
        if not pd.isnull(row["researcher_assumed_race OR identified_race"]):
            race_words = row["researcher_assumed_race OR identified_race"].split(" ")
            if "[stated]" in race_words:
                identified_race = row["researcher_assumed_race OR identified_race"].format(" [stated", "")
            else:
                researcher_assumed_race = row["researcher_assumed_race OR identified_race"]

        new_metadata_dict[current_key] = [collection_id,
                                          real_interviewee_birth_year,
                                          birth_decade,
                                          researcher_assumed_birth_decade,
                                          researcher_assumed_race,
                                          identified_race]

    for index, row in old_metadata.iterrows():
        if row["interviewee_name"] not in new_metadata_dict.keys() or new_metadata_dict[row["interviewee_name"]][0] != row["collection_id"]:
            print("Updating: " + row["interviewee_name"])
            updated_metadata.append([row["interviewee_name"], row["collection_id"], row["real_interviewee_birth_year"],
                                     row["birth_decade"], row["researcher_assumed_birth_decade"], row["researcher_assumed_race"],
                                     row["identified_race"]])
        else:
            real_interviewee_birth_year, birth_decade, researcher_assumed_birth_decade, researcher_assumed_race, identified_race = "", "", "", "", ""

            # Get birth year/decade
            if not pd.isnull(row["real_interviewee_birth_year"]):
                real_interviewee_birth_year = row["real_interviewee_birth_year"]
                birth_decade = int(real_interviewee_birth_year) - int(real_interviewee_birth_year) % 10
            elif new_metadata_dict[row["interviewee_name"]][1] != "":
                #print("Updating: " + row["interviewee_name"])
                real_interviewee_birth_year = new_metadata_dict[row["interviewee_name"]][1]
                birth_decade = new_metadata_dict[row["interviewee_name"]][2]
            elif not pd.isnull(row["birth_decade"]):
                birth_decade = row["birth_decade"]
            elif new_metadata_dict[row["interviewee_name"]][2] != "":
                birth_decade = new_metadata_dict[row["interviewee_name"]][2]
            elif not pd.isnull(row["researcher_assumed_birth_decade"]):
                researcher_assumed_birth_decade = row["researcher_assumed_birth_decade"]
            elif new_metadata_dict[row["interviewee_name"]][3] != "":
                researcher_assumed_birth_decade = new_metadata_dict[row["interviewee_name"]][3]

            # Get race
            if not pd.isnull(row["identified_race"]):
                identified_race = row["identified_race"]
            elif new_metadata_dict[row["interviewee_name"]][5] != "":
                identified_race = new_metadata_dict[row["interviewee_name"]][5]
            elif not pd.isnull(row["researcher_assumed_race"]):
                researcher_assumed_race = row["researcher_assumed_race"]
            elif new_metadata_dict[row["interviewee_name"]][4] != "":
                researcher_assumed_race = new_metadata_dict[row["interviewee_name"]][4]

            updated_metadata.append([row["interviewee_name"], row["collection_id"], real_interviewee_birth_year,
                                     birth_decade, researcher_assumed_birth_decade, researcher_assumed_race, identified_race])

    updated_metadata_df = pd.DataFrame(updated_metadata)
    updated_metadata_df.to_csv("updated_metadata.csv", index=False, header=output_csv_header)

if __name__ == '__main__':
    main()