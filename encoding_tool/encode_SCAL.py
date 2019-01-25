
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
import re
from lxml import etree

# Creates initials from a name. If the name has a comma in it, it splits the comma
# and then puts the first part of the first comma behind everything else. It then takes
# the first letter of each part of the name for the initials.
def create_initials(name):
	if pd.isnull(name): return ""
	if "(" in name:
		name = name.replace("(", "").replace(")", "").replace(",", "")
	name = name.lower()
	if "," in name:
		parts = name.split(",")
		for i in range(0, len(parts)): parts[i] = parts[i].strip()
		name = "{} {}".format(" ".join(parts[1:]), parts[0])
	initials = ""
	parts = name.split(" ")
	for p in parts:
		initials = "{}{}".format(initials, p[0])
	
	return initials

# Writes the "titleStmt" section of the TEI file, which is under "fileDesc."
def write_title_section(file_desc, info):
	title_stmt = ET.SubElement(file_desc, "titleStmt")

	# Title of the interview
	title = ET.SubElement(title_stmt, "title")
	title.text = info["title"]

	# Interviewee
	author = ET.SubElement(title_stmt, "author")
	interviewee = ET.SubElement(author, "name", id = info["interviewee_init"], reg = info["interviewee"], type = "interviewee")
	interviewee.text = info["interviewee"]

	# Interviewer
	resp_stmt = ET.SubElement(title_stmt, "respStmt")
	resp = ET.SubElement(resp_stmt, "resp")
	resp.text = "Interview conducted by "
	interviewer = ET.SubElement(resp_stmt, "name", id = info["interviewer_init"], reg = info["interviewer"], type = "interviewer")
	interviewer.text = info["interviewer"]

	# Encoder (me!) -- I just hard-coded this in
	resp_stmt2 = ET.SubElement(title_stmt, "respStmt")
	resp2 = ET.SubElement(resp_stmt2, "resp")
	resp2.text = "Text encoded by "
	encoder = ET.SubElement(resp_stmt2, "name", id = "hs")
	encoder.text = "Hilary Sun"

# Writes the "sourceDesc" section of the TEI file, which is under "fileDesc."
def write_source_description(file_desc, info):
	source_desc = ET.SubElement(file_desc, "sourceDesc")
	bibl_full = ET.SubElement(source_desc, "biblFull")
	title_stmt2 = ET.SubElement(bibl_full, "titleStmt")
	title2 = ET.SubElement(title_stmt2, "title")
	title2.text = info["title"]
	author2 = ET.SubElement(title_stmt2, "author")
	author2.text = info["interviewee"]
	extent = ET.SubElement(bibl_full, "extent")
	publisher_stmt = ET.SubElement(bibl_full, "publicationStmt")
	publisher = ET.SubElement(publisher_stmt, "publisher")
	publisher.text = info["publisher"]
	pub_place = ET.SubElement(publisher_stmt, "pubPlace")
	date = ET.SubElement(publisher_stmt, "date")
	date.text = info["date"]

	return extent

# Writes the "fileDesc" section of the TEI file, which is under "teiHeader."
def write_file_description(header, info):
	file_desc = ET.SubElement(header, "fileDesc")
	write_title_section(file_desc, info)
	extent = write_source_description(file_desc, info)

	return extent

# Writes the "profileDesc" section of the TEI file, which is under "teiHeader."
def write_profile_description(header, info):
	profile_desc = ET.SubElement(header, "profileDesc")
	lang_usage = ET.SubElement(profile_desc, "langUsage")
	language = ET.SubElement(lang_usage, "language", id = info["language_id"])
	language.text = info["language"]

# Writes the "revisionDesc" section of the TEI file, which is under "teiHeader."
def write_revision_description(header, info):
	revision_desc = ET.SubElement(header, "revisionDesc")

def write_speaker_information(div1, int_info):
	li = ET.SubElement(div1, "list", type = "simple")
	spk1 = ET.SubElement(li, "item")
	spk1.text = "Interviewer:"
	interviewer_node = ET.SubElement(spk1, "name", id = "spk1", key = int_info["interviewer_init"], reg = int_info["interviewer"], type = "interviewer")
	interviewer_node.text = int_info["interviewer"]
	spk2 = ET.SubElement(li, "item")
	spk2.text = "Subject:"
	interviewee_node = ET.SubElement(spk2, "name", id = "spk2", key = int_info["interviewee_init"], reg = int_info["interviewee"], type = "interviewee")
	interviewee_node.text = int_info["interviewee"]

# Writes the lines of the current speaker into div2.
def write_speaker(div2, spk, spkn, last_name, lines):
	sp = ET.SubElement(div2, "sp", who = spk)
	speaker = ET.SubElement(sp, "speaker", n = spkn)
	speaker.text = "{}:".format(last_name.upper())
	for l in lines:
		p = ET.SubElement(sp, "p")
		p.text = l

# Parses the XML file.
def parse_files(info):
	for f in os.listdir("SCAARJ"):
		int_info = info[f]

		int_info["title"] = "Asian American Reproductive Justice Oral History Project"
		root = ET.Element("TEI.2")
		header = ET.SubElement(root, "teiHeader", name = "Smith College AARJ")
		extent = write_file_description(header, int_info)

		# Creates the text itself
		text = ET.SubElement(root, "text")
		body = ET.SubElement(text, "body")
		div1 = ET.SubElement(body, "div1", type = "about_interview")
		div2 = ET.SubElement(body, "div2")

		with open("SCAARJ/{}".format(f), "r", encoding = "utf-8") as file:
			lines = file.readlines()
			last_name = f.replace("SCAARJ_", "").split("_")[0]
			
			boilerplate = []
			is_interviewer = True
			curr_speaker = []
			is_boilerplate = True
			for l in lines:
				l = l.strip()
				if l == "": continue
				if l.startswith("KWON:") or l.startswith("GOOGLE VOICE:"):
					is_boilerplate = False
					if not is_interviewer and len(curr_speaker) > 0:
						write_speaker(div2, "spk2", "2", last_name, curr_speaker)
						curr_speaker = []
					is_interviewer = True
					curr_speaker.append(l.replace("KWON:", "").replace("GOOGLE VOICE:", "").strip())
				elif l.startswith("{}:".format(last_name.upper())):
					is_boilerplate = False
					if is_interviewer and len(curr_speaker) > 0:
						write_speaker(div2, "spk1", "1", "Kwon", curr_speaker)
						curr_speaker = []
					is_interviewer = False
					curr_speaker.append(l.replace("{}:".format(last_name.upper()), "").strip())
				elif not is_boilerplate:
					curr_speaker.append(l)
				if is_boilerplate: boilerplate.append(l)

			head = ET.SubElement(div1, "head")
			for l in boilerplate:
				p = ET.SubElement(head, "p")
				p.text = l
			write_speaker_information(div1, int_info)

		tree = ET.ElementTree(root)
		tree.write("{}.tei".format(f.replace(".txt", "")), encoding = "utf-8")

# Reads the metadata to collect information on each of the files.
def read_metadata(file):
	df = pd.read_csv(file, encoding = "utf-8", header = None)

	info = {}
	for i, r in df.iterrows():
		if r[3] == "SCAL":
			filename = r[6]
			info[filename] = {}
			info[filename]["interviewee"] = r[7]
			info[filename]["interviewee_init"] = create_initials(r[7])
			info[filename]["interviewer"] = r[8]
			info[filename]["interviewer_init"] = create_initials(r[8])
			info[filename]["date"] = r[9]
			info[filename]["language_id"] = "eng"
			info[filename]["language"] = "English"
			info[filename]["publisher"] = "Smith College"

	return info

def main():
	info = read_metadata("metadata.csv")
	parse_files(info)

if __name__ == '__main__':
	main()