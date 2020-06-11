import pandas as pd
import math

outputCSVHeader = ["Accession#", "original_file_name", "project_file_name", "date_of_first_interview", "approx_age_at_time_of_interview", "interview_city", "interview_state",
                   "interviewee_birth_state"]
#Questions about occupations, eeoc, and education
#State is the acronym
intervieweeSet = {""}
filenames = []

"""
Given a string containing the name of an interviewee, remove extraneous titles, middle names, and suffixes such as "Jr.", "Reverend", or "The Honorable"

Return a string in the form "lastName_firstName", or "firstName" if there is no last name
"""
def parseName(name):
    notFirstNames = ["The", "Honorable", "Reverend", "Minister", "Sister", "Father", "Bishop", "Dr.", "Capt.", "Col.", "Lt.", "Maj.", "Gen.", "Sgt.", "Radm.", "Cdr.", "Brig."]
    notLastNames = ["Sr.", "Jr.", "jr", "II", "III"]
    splitName = name.split()
    firstName = ""
    lastName = ""

    foundFirst = False
    # Find first and last names
    for i in range(len(splitName)):
        if not foundFirst:
            firstName = splitName[i]
            if firstName not in notFirstNames:
                foundFirst = True
        else:
            if splitName[i] not in notLastNames:
                lastName = splitName[i]


    # Trim trailing comma
    if lastName.find(",") != -1:
        lastName = lastName[:-1]

    if lastName != "":
        return lastName + "_" + firstName
    else:
        return firstName

def makeFilename(name, accessionNum, previousAccessionNum, previousFilename):
    #Keep accessing the same file
    if accessionNum == previousAccessionNum:
        return previousFilename

    if name in intervieweeSet:
        #Check if unnumbered file exists and rename it if so
        if ("HM_" + name + ".txt") in filenames:
            nameIndex = filenames.index("HM_" + name + ".txt")
            filenames[nameIndex] = ("HM_" + name + "_1.txt")

        #Assign this transcript the next smallest number
        i = 1
        while ("HM_" + name + "_" + str(i) + ".txt") in filenames:
            i += 1
        return "HM_" + name + "_" + str(i) + ".txt"

    #New file and new interviewee
    else:
        intervieweeSet.add(name)
        return "HM_" + name + ".txt"

#Return an empty string if not one of the fifty states
def stateNameToAcronym(stateName):
    nameToAcronymMap = {"alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
                        "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
                        "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
                        "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD", "massachusetts": "MA",
                        "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
                        "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM",
                        "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
                        "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC", "south dakota": "SD",
                        "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
                        "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY"}

    if not isinstance(stateName, str) or stateName.lower() not in nameToAcronymMap: return ""
    else: return nameToAcronymMap[stateName.lower()]

def processMetadata(accessionNums):
    accessionNumToMetadataMap = {}

    # Map Accession#'s to filenames
    for i in range(len(accessionNums)):
        accessionNumToMetadataMap[accessionNums[i]] = [accessionNums[i], "Digital Archive Stories(1).xlsx", filenames[i]]

    metadataDF = pd.read_csv("hm_metadata.csv")

    for index, row in metadataDF.iterrows():
        currentMetadata = accessionNumToMetadataMap[row["Accession#"]]
        date_of_first_interview = ""
        approx_age_at_time_of_interview = ""
        if not isinstance(row["Interview Dates"], float):
            date_of_first_interview = row["Interview Dates"].split("|")[0].strip()
            if not math.isnan(row["DateBirth_Year"]):
                approx_age_at_time_of_interview = int(date_of_first_interview.split("/")[-1]) - int(row["DateBirth_Year"])
        interview_city = row["Interview Locations"].split("|")[0].split(",")[0].strip()
        interview_state = stateNameToAcronym(row["Interview Locations"].split("|")[0].split(",")[1].strip())
        interviewee_birth_state = stateNameToAcronym(row["BirthState"])

        accessionNumToMetadataMap[row["Accession#"]] = [currentMetadata[0], currentMetadata[1], currentMetadata[2], date_of_first_interview,
                                                        approx_age_at_time_of_interview, interview_city, interview_state, interviewee_birth_state]

    return list(accessionNumToMetadataMap.values())

def main():
    accessionNums = []

    dataDF = pd.read_csv("history_makers.csv", usecols=["Accession#", "Name"])

    #Generate a list of filenames
    previousAccessionNum = ""
    previousFilename = ""
    for index, row in dataDF.iterrows():
        intervieweeName = parseName(row["Name"])
        accessionNum = row["Accession#"]

        filename = makeFilename(intervieweeName, accessionNum, previousAccessionNum, previousFilename)
        previousAccessionNum = accessionNum

        if filename != previousFilename:
            accessionNums.append(accessionNum)
            filenames.append(filename)
            previousFilename = filename

    accessionNumToMetadata = processMetadata(accessionNums)

    outputDF = pd.DataFrame(accessionNumToMetadata)
    outputDF.to_csv("accession#_filename_map.csv", index=False, header=outputCSVHeader)


if __name__ == '__main__':
    main()