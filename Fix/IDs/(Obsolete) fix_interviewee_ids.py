import pandas as pd

"""
Finds the highest interviewee ids used in each collection in the DataFrame
"""
def getHighestIds(df):
    ids = []

    newIds = None
    previousCollection = df.loc[0]["collection_id"]
    for index, row in df.iterrows():
        collection = row["collection_id"]

        #Update the list of ranges
        if (collection != previousCollection):
            ids.append(int(newIds.split(';')[-1]))

            newIds = row["interviewee_ids"]
            previousCollection = collection
        else:
            newIds = row["interviewee_ids"]

    newIds = row["interviewee_ids"]
    ids.append(int(newIds.split(";")[-1]))

    return ids

"""
Maps all old interviewee IDs to new IDs
"""
def makeIDDict(interviewsDf, intervieweesDf, alteredIntervieweesDf):
    idDict = {}

    # Dict of names to new IDs; cleared after each collection is processed
    nameDict = {}

    highestIds = getHighestIds(interviewsDf)

    nameSet = {""}
    highID = highestIds.pop(0)
    currentVEENum = 0

    dropped = 0
    for index, row in intervieweesDf.iterrows():
        # Collection changed
        if index > highID:
            nameSet = {""}
            highID = highestIds.pop(0)

        # New interviewee
        if row["interviewee_name"] not in nameSet:
            nameSet.add(row["interviewee_name"])
            newID = "VEE" + str(currentVEENum)
            nameDict[row["interviewee_name"]] = newID
            currentVEENum += 1
        # Repeat interviewee
        else:
            dropped += 1
            newID = nameDict[row["interviewee_name"]]
            alteredIntervieweesDf.drop([index], inplace=True)

        # Update the dictionary
        idDict[row["interviewee_id"]] = newID

    return idDict

"""
Fix the interviewee IDs in each of the supplied DataFrames according to the mapping in hte supplied idDict
"""
def fixIDs(interviewsDf, alteredIntervieweesDf, idDict):

    #Fix the IDs in the interviews DataFrame
    for index, row in interviewsDf.iterrows():
        idsToChange = []
        temp = row["interviewee_ids"].split(';')
        for num in temp: idsToChange.append(num.strip())

        changedIDs = []
        for idNum in idsToChange:
            changedIDs.append(idDict[idNum])

        changedIDString = changedIDs[0]

        for i in range(1, len(changedIDs)):
            changedIDString += "; " + changedIDs[i]
        interviewsDf.at[index, "interviewee_ids"] = changedIDString


    #Fix the IDs in the interviewees DataFrame
    for index, row in alteredIntervieweesDf.iterrows():
        alteredIntervieweesDf.at[index, "interviewee_id"] = idDict[row["interviewee_id"]]

    # Save the altered csv files
    alteredIntervieweesDf.to_csv("interviewees_new.csv")
    interviewsDf.to_csv("interviews_new.csv")

"""
MUST MANUALLY DELETE THE INDEX COLUMN FROM THE OUTPUT .CSV FILES
"""

def main():
    intervieweesDf = pd.read_csv("interviewees.csv", dtype={"interviewee_id": "object"})
    alteredIntervieweesDf = intervieweesDf.copy()
    interviewsDf = pd.read_csv("interviews.csv")

    #Dict of old IDs to new IDs
    idDict = makeIDDict(interviewsDf, intervieweesDf, alteredIntervieweesDf)

    fixIDs(interviewsDf, alteredIntervieweesDf, idDict)


if __name__ == '__main__':
    main()