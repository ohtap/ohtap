import pandas as pd
import os

def get_filename_from_line(line):
    first_word = line.split('>')[0]
    filename_word = first_word.split('\\\\')[-1]
    return filename_word + ".txt"


def main():
    interviews_df = pd.read_csv("interviews.csv")
    interviewees_df = pd.read_csv("interviewees.csv")
    # Parse the .txt file, creating map from filenames to text content
    filenames_to_event_extent_dict = {}
    with open("Event (Extent).txt", encoding="utf-8") as fp:
        text_lines = fp.readlines()
        current_filename = ""
        for line in text_lines:
            if "Reliability Subcorpus" in line and get_filename_from_line(line) in filenames_to_event_extent_dict.keys():
                current_filename = "Reliability"
            elif "<Files" in line:
                current_filename = get_filename_from_line(line)
            elif current_filename != "Reliability":
                if current_filename in filenames_to_event_extent_dict:
                    filenames_to_event_extent_dict[current_filename].append(line)
                else:
                    filenames_to_event_extent_dict[current_filename] = [line]


    #Create dict of interviewee IDs to filenames
    VEE_id_to_filename_dict = {}
    for i, r in interviews_df.iterrows():
        ids_list = r["interviewee_ids"].split("; ")
        for VEE_id in ids_list:
            if VEE_id not in VEE_id_to_filename_dict:
                VEE_id_to_filename_dict[VEE_id] = [r["project_file_name"]]
            else:
                VEE_id_to_filename_dict[VEE_id].append(r["project_file_name"])


    #Create dict of filenames to decades
    filename_to_decade_dict = {}
    for i, r in interviewees_df.iterrows():
        current_filename_list = VEE_id_to_filename_dict[r["interviewee_id"]]
        current_birth_decade = "None"
        if not pd.isnull(r["birth_decade"]):
            current_birth_decade = r["birth_decade"]
        elif not pd.isnull(r["researcher_assumed_birth_decade"]):
            current_birth_decade = r["researcher_assumed_birth_decade"]

        for current_filename in current_filename_list:
            #If there is not already a value, add it to the dict
            if current_filename not in filename_to_decade_dict or filename_to_decade_dict[current_filename] == "None":
                if current_birth_decade == "None":
                    filename_to_decade_dict[current_filename] = current_birth_decade
                else:
                    filename_to_decade_dict[current_filename] = int(current_birth_decade)
            else: #If there is already a value, take the later one
                if current_birth_decade != "None" and filename_to_decade_dict[current_filename] < current_birth_decade:
                    filename_to_decade_dict[current_filename] = int(current_birth_decade)
                    if current_filename in filenames_to_event_extent_dict:
                        print("There was a conflict on " + current_filename)

    print("-----------------------------")

    #Check that all filenames are accounted for
    none_total = 0
    for current_filename in filenames_to_event_extent_dict.keys():
        if filename_to_decade_dict[current_filename] == "None":
            print("There is no birth decade for " + current_filename)
            none_total += 1

    print("None total: " + str(none_total))
    print("All total: " + str(len(filenames_to_event_extent_dict.keys())))


    #Write the information to a text file in chronological order
    for current_filename in filenames_to_event_extent_dict.keys():
        f = open("Sorted Text/event_extent_" + str(filename_to_decade_dict[current_filename]) + ".txt", "a+", encoding="utf-8")
        f.write(current_filename + " - " + str(filename_to_decade_dict[current_filename]) + "\n")
        for line in filenames_to_event_extent_dict[current_filename]:
            f.write(line)
        f.close()

    #Consolidate the text
    f = open("event_extent_all.txt", "a+", encoding="utf-8")
    for filename in os.listdir("Sorted Text/"):
        with open("Sorted Text/" + filename, encoding="utf-8") as fp:
            all_lines = fp.readlines()
            for line in all_lines:
                f.write(line)
    f.close()

if __name__ == '__main__':
    main()