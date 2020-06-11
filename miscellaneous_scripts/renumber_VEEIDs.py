import pandas as pd

"""
Purpose: reassign interviewee_ids to interviewees in increasing numerical order, and replace all instances of a given
interviewee's old id in the "Interviews" sheet's "interviewee_ids" column with that interviewee's new id

Input: a .csv file with two columns, "Interviewee IDs" and "Interviews' Interviewee IDs"
The "Interviewee IDs" will be from the "interviewee_id" column of the "Interviewees" sheet from the "OHTAP_Metadata" Google sheet
The "Interviews' Interviewee IDs" will be from the "interviewee_ids" column of the "Interviews" sheet from the same Google sheet

Output: a csv file with two columns
The "Interviewee IDs" column should be copied and pasted into the "interviewee_id" column of the "Interviewees" sheet of the "OHTAP_Metadata" Google sheet
The "Interviews' Interviewee IDs" column should be copied and pasted into the "interviewee_ids" column of the "Interviews" sheet of the same Google sheet

"""
new_csv_header = ["Interviewee IDs", "Interviews' Interviewee IDs"]

def main():
    df = pd.read_csv("old_interviewee_ids.csv")

    oldToNewIDMap = dict()

    #Build the map from the old interviewee IDs to the new interviewee IDs
    for i, r in df.iterrows():
        if pd.isnull((r["Interviewee IDs"])):
            break

        oldToNewIDMap[r["Interviewee IDs"]] = "VEE" + str(i)


    newInterviewIntervieweeIDsList = []

    #Build the new list of Interviews' Interviewee IDs
    for i, r in df.iterrows():
        if pd.isnull((r["Interviews' Interviewee IDs"])):
            break

        oldVEEIDsList = str(r["Interviews' Interviewee IDs"]).split("; ")

        newVEEIDs = ""

        for oldVEEID in oldVEEIDsList:
            newVEEIDs += oldToNewIDMap[oldVEEID]
            newVEEIDs += "; "

        newVEEIDs = newVEEIDs[:-len("; ")]

        newInterviewIntervieweeIDsList.append(newVEEIDs)

    newIntervieweeIDsList = list(oldToNewIDMap.values())
    #Pad the smaller list
    if (len(newIntervieweeIDsList) != len(newInterviewIntervieweeIDsList)):
        if (len(newIntervieweeIDsList) < len(newInterviewIntervieweeIDsList)):
            while (len(newIntervieweeIDsList) < len(newInterviewIntervieweeIDsList)):
                newIntervieweeIDsList.append("")
        else:
            while (len(newInterviewIntervieweeIDsList) < len(newIntervieweeIDsList)):
                newInterviewIntervieweeIDsList.append("")

    new_csv_dict = {"Interviewee IDs": newIntervieweeIDsList, "Interviews' Interviewee IDs": newInterviewIntervieweeIDsList}
    new_csv_df = pd.DataFrame(new_csv_dict)

    new_csv_name = "new_interviewee_ids.csv"
    new_csv_df.to_csv(new_csv_name, index=False)


if __name__ == '__main__':
    main()