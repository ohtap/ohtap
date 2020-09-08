import pandas as pd
import xml.etree.ElementTree as ET
import os
import sys

# =============================================================================
# ==                             WRITE HEADER                                ==
# =============================================================================
# Purpose: Extracts the needed data from the metadata spreadsheets
# Parameters: metatadata_folder - path to the folder containing the metadata spreadsheets
#                    Should contain files: Interviews.csv, Interviewees.csv, Collections.csv
# Returns: A dictionary info containing the needed information
# NOTE: If the metadata folder contains the appropriate files, this should work for
#       all of the collections
def ReadMetadata(file_name, metatadata_folder):
    # Read in metadata from spread sheets
    # TODO: Add a check for if those files are even there...
    interviews = pd.read_csv(metatadata_folder+"/Interviews.csv").set_index("project_file_name")
    interviewees = pd.read_csv(metatadata_folder + "/Interviewees.csv").set_index("interviewee_id")
    collections = pd.read_csv(metatadata_folder + "/Collections.csv").set_index("collection_id")

    # Initialize the dictionary that will contain the data needed for the header
    info = {}

    # Fill in the info from the opened spread sheets
    # Add interviewer
    info.update({"interviewer" : []})
    interviewer_names = interviews.loc[file_name].at["interviewer_names"]
    interviewer_names = interviewer_names.split(";")
    for name in interviewer_names:
        info["interviewer"].append(name.strip())

    # Add laguage, NOTE: hardcoded
    info.update({"language_id":"eng"})

    # Add date
    info.update({"date" : interviews.loc[file_name].at["date_of_first_interview"]})

    # Add collection id
    info.update({"collection_id" : interviews.loc[file_name].at["collection_id"]})
    info.update({"collection_name" : collections.loc[info["collection_id"]].at["collection_name"]})

    # Add Publisher
    info.update({"publisher" : collections.loc[info["collection_id"]].at["institution_name"]})

    # Add interviewees.
    # NOTE: interviewees value is a list because there may be more than one
    interviewee_ids = interviews.loc[file_name].at["interviewee_ids"]
    interviewee_ids = interviewee_ids.replace(" ", "").split(";")

    # build a list of interviewee names
    interviewee_names = []
    for id in interviewee_ids:
        interviewee_names.append(interviewees.loc[id].at["interviewee_name"])

    info.update({"interviewees" : interviewee_names})

    # Add the Title of the interview

    # NOTE: COLLECTION SPECIFIC!!!
    # This is a place holder title, the actual title is added
    # later in the fix title function
    for name in interviewee_names:
        title += ReverseName(name).upper() + ", "
    title = title.rstrip(", ")

    if pd.notna(info["date"]):
        title += " " + FormatDate(info["date"])

    info.update({"title" : title})      # Add title to info

    return info

# Purpose: turns a date in format MM/DD/YYYY into a more verbose format
def FormatDate(date):
    import datetime
    
    #Create a date object with the given date
    date = date.split("/")
    intermediary = datetime.date(int(date[2]), int(date[0]), int(date[1]))

    # Reformat and return it
    intermediary = intermediary.strftime("%B %d,%Y")
    return intermediary

# Purpose: change name from LAST, FIRST format to FIRST LAST
# Credit: Hillary Sun
def ReverseName(name):
	if pd.isnull(name): return ""
	parts = name.split(",")
	final_name = []
	for p in parts[1:]:
		final_name.append(p.strip())
	final_name.append(parts[0].strip())
	return " ".join(final_name)


# Purpose: find the initials of a name
# Note: can handle names in format FIRST LAST and LAST, FIRST and LAST, FIRST MIDDLE
#       and FIRST MIDDLE LAST
def CreateInitials(name):
    if pd.isnull(name): return ""

    if name.count(","):
        name = ReverseName(name)

    name = name.split(" ")
    initials = ""
    for part in name:
        if len(part) > 0:
            initials += part[0]

    return initials.upper()


# Purpose: Writes a TEI style header in XML for the given interview
# Parameters: info – a dictionary created by the ReadMetadata function containing
#                    information about the interview
# Returns: an ElementTree element representing the xml header element
def WriteHeader(info):
    # NOTE: there are a lot of calls to ET.SubElement, this function adds a new
    #       child to the element specified in the first parameter, the second
    #       parameter specifies what child will be called.
    
    # Set up teiHeader as the root
    teiHeader = ET.Element("teiHeader", type = info["collection_name"])
    fileDesc = ET.SubElement(teiHeader, "fileDesc")

    ##### Create the Title statement #####
    titleStmt = ET.SubElement(fileDesc, "titleStmt")       # titleStmt is child of header
    ET.SubElement(titleStmt, "title").text = info["title"]
    author = ET.SubElement(titleStmt, "author")
    # Add each interviewee to the authors section
    for interviewee in info["interviewees"]:
        nameElem = ET.SubElement(author, "name", {"id" : CreateInitials(interviewee), "reg" : interviewee, "type" : "interviewee"})
        nameElem.text = interviewee
        nameElem.tail = ", interviewee"
    
    # Add responsibility statement for Interviewer
    respStmt = ET.SubElement(titleStmt, "respStmt")
    ET.SubElement(respStmt, "resp").text = "Interview conducted by "
    for interviewer in info["interviewer"]:
        ET.SubElement(respStmt, "name", {"id" : CreateInitials(interviewer), "reg" : interviewer, "type" : "interviewer"}).text = interviewer

    # Add resposibility statement for Encoder
    respStmt = ET.SubElement(titleStmt, "respStmt")
    ET.SubElement(respStmt, "resp").text = "Text encoded by "
    ET.SubElement(respStmt, "name", id = "MS").text = "Madeleine Street"

    ##### Create Source description #####
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    biblFull = ET.SubElement(sourceDesc, "biblFull")

    # Create second title statement
    titleStmt = ET.SubElement(biblFull, "titleStmt")
    ET.SubElement(titleStmt, "title").text = info["title"]
    author = ET.SubElement(titleStmt, "author")
    # Add the authors names to the text section of the authors tag
    author.text = ""
    for interviewee in info["interviewees"]:
        author.text += ReverseName(interviewee) + ", "
    author.text = author.text.strip(", ")               # for cleaning up

    ET.SubElement(biblFull, "extent")

    # Create publication statement
    publicationStmt = ET.SubElement(biblFull, "publicationStmt")
    ET.SubElement(publicationStmt, "publisher").text = info["publisher"]
    ET.SubElement(publicationStmt, "pubPlace")
    if pd.notna(info["date"]):
        ET.SubElement(publicationStmt, "date"). text = FormatDate(info["date"])
    ET.SubElement(publicationStmt, "authority")

    ##### Create Profile Description #####
    profileDesc = ET.SubElement(teiHeader, "profileDesc")
    # Add Language Description
    langUsage = ET.SubElement(profileDesc, "langUsage")
    ET.SubElement(langUsage, "language", id = "eng").text = "english"

    return teiHeader


# Purpose: Changes the title field to the appropriate title based on the interview
# Parameters: header — the ElementTree Element representing the header
#             interview_path – path to the interview to being parsed
# Returns: An updated version of the header element
# Does: Updates the header element passed to it
def FixTitle(header, interview_path):
    # Read in interview as an ElementTree
    interview = ET.parse(interview_path)
    interview_root = interview.getroot()

    # Exctract the title from the interview
    title = interview_root.find(".*{https://www.weareavp.com/nunncenter/ohms}title")
    title = title.text

    # Update the header with the new title
    for elem in header.iter():
        if elem.tag == "title":
            elem.text = title

    return header


# =============================================================================
# ==                              WRITE BODY                                 ==
# =============================================================================
def ParseText(interview_path, name_map_path, info):
    ##### Open and read in interview #####
    interview_name = interview_path.split("/")[-1]
    interview_xml = ET.parse(interview_path)

    ##### Separate Text #####

    # Get the text of the interview
    interview_text = interview_xml.find(".*{https://www.weareavp.com/nunncenter/ohms}transcript").text

    # NOTE: ask about the front matter for this particular collection

    ##### Parse the text #####
    text = ET.Element("text")

    # Create the body
    speaker_list = MakeSpeakerList(interview_path, name_map_path)

    body = ET.SubElement(text, "body")

    div2 = CreateDiv2(interview_text, speaker_list)
    div1 = CreateAbtInterview(interview_name, speaker_list, info)

    body.insert(0, div1)
    body.insert(1, div2)

    return text


# Purpose: Creates a list of the speakers
# Parameters: interview_path – path of the interview to look at
#             name_map_path – path to the name map
# Returns: a list of speakers
# NOTE: a speaker is represented as a dictionary with the following feilds:
#       name (last, first), role (interviewer/interviewee), references 
#       (a list of ways they are reffered to)
def MakeSpeakerList(interview_path, name_map_path):
    # Get the name of the interview from the path
    interview_name = interview_path.split("/")[-1]

    # Read in the name map and make it searchable by file name
    name_map = pd.read_csv(name_map_path).set_index("file_name")

    # initialize the speaker list
    speaker_list = []

    # Get the appropriate row from the name_map
    row = name_map.loc[interview_name].fillna(0).tolist()
    for speaker in row:
        if speaker != 0:
            speaker = speaker.split(";")
            to_add = {}
            to_add["name"] = speaker[1]
            to_add["role"] = speaker[0]
            to_add["references"] = speaker[2].lower()
            to_add["number"] = 0                # Number is set to zero and used to store the order of speakers later
            speaker_list.append(to_add)

    return speaker_list

# Purpose: Create and returns the div2 section of an encoded interview
#          NOTE: this is the part with the actual text of the interview
# Parameters: interview_text –  a string containing the text of the interview
#             name_map – a list of the speakers in the interview as created by
#                        the MakeSpeakerList Function
# Returns: The div2 as an ElementTree Element
def CreateDiv2(interview_text, name_map):
    # set up div2
    div2 = ET.Element("div2")

    #### Encode the interview text #####
    interview_text = interview_text.splitlines()

    prev_speaker = None             # Stores the name_map entry for the previous speaker
    prev_line = None
    turn_num = 0                    # Counts the conversational turns
    spk_so_far = 0                  # Counts the number of different people to speak so far

    # Go through each line of the interview and assign speaker tags
    for line in interview_text:
        lower_line = line.lower()
        has_speaker_tag = False

        # Check the "references" section of each speaker to see if the line
        # is a new speaker tag. For this collection, we assume that all
        # speaker tags are found on thier own line
        for speaker in name_map:
            if lower_line.strip().count(speaker["references"] + ":"):
                has_speaker_tag = speaker
                break
        
        # Case where the line has a speaker tag
        if has_speaker_tag:
            # Assign the speaker a number if they haven't spoken yet
            if speaker["number"] == 0:
                spk_so_far += 1
                speaker["number"] = spk_so_far

            # Case where the speaker tag indicates a new speaker
            if has_speaker_tag["name"] != prev_speaker:
                # Create speech sub element
                turn_num += 1
                prev_line = ET.SubElement(div2, "sp", {"who" : "spk_" + str(speaker["number"]), "id" : str(turn_num)})
                
                # Create speaker tag
                ET.SubElement(prev_line, "speaker", n = str(speaker["number"])).text = has_speaker_tag["references"].upper() + ":"
    
            # Add the line of text to the appropriate paragraph section of the speaker
            AddLineToParagraph(prev_line, line.replace(speaker["references"].upper() + ":", ""))
        
        # Otherwise, we assume the line is someone speaking
        else:
            if prev_line:
                AddLineToParagraph(prev_line, line)

    return div2
    

def AddLineToParagraph(speech_element, line):
    paragraph = speech_element.findall("./p")            # The list of paragraphs in the prev_line
    all_children = speech_element.findall(".*")          # All children of the current line
    # Case where a page break was inserted, start a new paragraph
    if len(all_children) != 0 and all_children[-1].tag == "pb":
        ET.SubElement(speech_element, "p").text = line
    # Case where there is already a paragraph sub element
    elif len(paragraph) == 0:
        ET.SubElement(speech_element, "p").text = line
    # Case where there is not already a paragraph sub element
    else:
        paragraph[-1].text += " " + line

# Purpose: Creates the about interview div1 of the body section
# Parameters: interview_name – a string representing the name of the file
#             name_map – a list of the speakers in the interview as created by
#                        the MakeSpeakerList Function
#             info – a dictionary created by the ReadMetadata function containing
#                    information about the interview
# Returns: The div1 as an ElementTree Element
def CreateAbtInterview(interview_name, name_map, info):
    # Set up the div1 and list
    div1 = ET.Element("div1", {"type" : "about_interview"})
    ET.SubElement(div1, "head").text = info["title"]
    list_elem = ET.SubElement(div1, "list", {"type" : "simple"})

    # Add Speakers to the list as items
    for speaker in name_map:
        item = ET.SubElement(list_elem, "item")         # item is the new element
        # Text of the item element differs based on the role of the speaker
        if speaker["role"] == "interviewer":
            item.text = "Interviewer:"
        else:
            item.text = "Subject:"
        # Add the name subelement to the item
        name = ET.SubElement(item, "name", {"id" : "spk" + str(speaker["number"]), "key" : CreateInitials(speaker["name"]), "reg" : speaker["name"], "type" : speaker["role"]})
        name.text = speaker["name"]

    # Add the interview date
    item = ET.SubElement(list_elem,"item")
    item.text = "Date:"
    if pd.notna(info["date"]):
        ET.SubElement(item, "date").text = FormatDate(info["date"])
    else:
        ET.SubElement(item, "date").text = "MISSING"

    return div1
# =============================================================================
# ==                            PARSE INTERVIEW                              ==
# =============================================================================
def ParseInterview(interview_path, metatadata_folder, name_map_path):
    # Write the header section
    interview_name = interview_path.split("/")[-1]
    info = ReadMetadata(interview_name, metatadata_folder)
    header = WriteHeader(info)
    FixTitle(header, interview_path)

    # Write the text section
    text = ParseText(interview_path, name_map_path, info)

    # Combine the pieces
    interview = ET.Element("TEI.2")
    interview.insert(0, header)
    interview.insert(1, text)

    return interview


# =============================================================================
# ==                                  MAIN                                   ==
# =============================================================================

def main():
    # Declaration of the needed path variables
    transcripts = ""
    metadata = ""
    name_map = ""

    # Set the path variables based on the command line args
    # if sys.argv.count("maddie_preset") != 0:
    #     transcripts = "../DATA/RTRB_Transcripts"
    #     metadata = "../DATA/metadata"
    #     name_map = "name_map.csv"
    if len(sys.argv) != 4:
        print("Usage: python parse_RTRB.py transcripts metadata_folder name_map")
        print("     transcripts: location of the folder of transcripts")
        print("     metadata_folder: location of the folder of metadata spread sheets")
        print("     name_map: location of the completed name map for the OCFF collection")
        exit()
    else:
        transcripts = sys.argv[1]
        metadata = sys.argv[2]
        name_map = sys.argv[3]

    # make new directory to hold transcripts
    dir_path = os.path.join(os.getcwd(), "tei")
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    # Parse all interviews and write the encoded versions to the tei folder
    for entry in os.scandir(transcripts):
        if entry.path.endswith(".txt"):
            interview = ParseInterview(entry.path, metadata, name_map)
            new_file_name = os.path.join(dir_path, entry.name.replace(".txt", "")+".tei")
            print(new_file_name)
            file = open(new_file_name, "w")
            interview = str(ET.tostring(interview,"unicode")).strip("'b")
            file.write(interview)

if __name__ == "__main__":
    main()