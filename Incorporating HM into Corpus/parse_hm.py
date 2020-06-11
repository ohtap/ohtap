import pandas as pd
import os
from os import path
import sys

colsToUse = ["Accession#", "Name", "Story_ID", "Story_Transcript"] # Columns to access from the data file
intervieweeSet = {""} # Set of interviewee names

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

"""
Given a string containing the name of an interviewee (the output of parseName() ), create the name of the file that will contain
the current interview, appending numbers to the end if there are multiple interviews with the same interviewee
Note: will change previously created filenames by appending numbers, if the same interviewee has another interview

Return a string in the form "HM_lastName_firstName{_#}.txt"
"""
def makeFilename(name, accessionNum, previousAccessionNum, previousFilename):
    #Keep accessing the same file
    if accessionNum == previousAccessionNum:
        return previousFilename

    if name in intervieweeSet:
        #Check if unnumbered file exists
        if path.exists("txt/HM_" + name + ".txt"):
            os.rename("txt/HM_" + name + ".txt", "txt/HM_" + name + "_1.txt")

        #Assign this transcript the next smallest number
        i = 1
        while path.exists("txt/HM_" + name + "_" + str(i) + ".txt"):
            i += 1
        return "HM_" + name + "_" + str(i) + ".txt"

    #New file and new interviewee
    else:
        intervieweeSet.add(name)
        return "HM_" + name + ".txt"

"""
Given a string, remove useless unicode characters from it and return the cleaned line
"""

def cleanLine(line):
    line = line.replace("\x81", "")
    line = line.replace("\x8d", "")
    line = line.replace("\x8f", "")
    return line


"""
Given a file to write to, and a row of data, append the transcript to the file with the following formatting:
1. Speaker Change tags
2. Story IDs
3. Ending the writing with a newline
(Later: add interviewer and interviewee names, or Speaker 1 and Speaker 2 on a story-by-story basis)
"""
def writeTranscriptToFile(file, row):
    #Story Header
    file.write("Story_ID: " + str(row["Story_ID"]) + "\n")

    transcript = row["Story_Transcript"]
    transcriptList = list(filter(None, transcript.split("\n")))

    #Write the transcript, listing the current speaker
    i = 0
    for line in transcriptList:
        if line.split()[0][-1] == ':':
            i -= 1
        else:
            if i % 2 == 0:
                file.write("Speaker 1: ")
            else:
                file.write("Speaker 2: ")
            i+=1

        file.write(cleanLine(line) + "\n")


def main():
    dataFrame = pd.read_csv("history_makers.csv", usecols=colsToUse)

    previousAccessionNum = ""
    previousFilename = ""
    f = None

    for index, row in dataFrame.iterrows():
        intervieweeName = parseName(row["Name"])
        accessionNum = row["Accession#"]

        filename = makeFilename(intervieweeName, accessionNum, previousAccessionNum, previousFilename)
        previousAccessionNum = accessionNum

        if (filename != previousFilename):
            #print(filename)
            if f is not None: f.close()
            f = open(r"txt/" + filename, "a")
            previousFilename = filename

        writeTranscriptToFile(f, row)

    f.close()

if __name__ == '__main__':
    main()