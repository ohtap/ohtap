
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
from lxml import etree

# Months
months = {
	1: "January",
	2: "February",
	3: "March",
	4: "April",
	5: "May",
	6: "June",
	7: "July",
	8: "August",
	9: "September",
	10: "October",
	11: "November",
	12: "December"
}

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

# Reads the metadata to collect information on each of the files.
def read_metadata(file):
	df = pd.read_csv(file, encoding = "utf-8", header = None)

	info = {}
	for i, r in df.iterrows():
		if r[3] == "WOL":
			interviewee = r[7]
			info[interviewee] = {}
			info[interviewee]["interviewee"] = interviewee
			info[interviewee]["filename"] = r[6]
			info[interviewee]["interviewee_init"] = create_initials(r[7])
			info[interviewee]["interviewer"] = r[8]
			info[interviewee]["interviewer_init"] = create_initials(r[8])
			info[interviewee]["date"] = r[9]
			info[interviewee]["language_id"] = "eng"
			info[interviewee]["language"] = "English"
			info[interviewee]["publisher"] = "Oklahoma State University Library"

	return info

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

# Parses the XML file.
def parse_file(file, info):
	doc = etree.parse(file)
	interviews = doc.xpath("/metadata/record")

	num = 0
	for interview in interviews:
		done = False
		interviewee = interview.find("unmapped").text
		int_info = info[interviewee]
		int_info["title"] = interview.find("title").text
		root = ET.Element("TEI.2")
		header = ET.SubElement(root, "teiHeader", name = "Women of the Oklahoma Legislature")
		extent = write_file_description(header, int_info)

		# Creates the text itself
		text = ET.SubElement(root, "text")
		body = ET.SubElement(text, "body")
		div1 = ET.SubElement(body, "div1", type = "about_interview")
		div2 = ET.SubElement(body, "div2")

		nodes = interview.find("structure").find("node").findall("node")
		total_pages = 0
		for n in nodes:
			pages = n.findall("page")
			for i in range(1, len(pages) + 1):
				pb = ET.SubElement(div2, "pb", id = "p{}".format(total_pages + i), n = str(total_pages + i))
			total_pages += len(pages)
			if n.find("nodetitle").text != "Transcript": continue
			transcript = n.find("page").find("pagetext").text
			interviewer = int_info["interviewer"].split(",")

			date_parts = int_info["date"].split("/")
			boilerplate_sep = [
				"Today is {} {}, {}".format(months[int(date_parts[0])], date_parts[1], date_parts[2]),
				"My name is {} {}".format(interviewer[1].strip(), interviewer[0].strip()),
				"I   m {} {}".format(interviewer[1].strip(), interviewer[0].strip()),
				"This is {} {}, {}".format(months[int(date_parts[0])], date_parts[1], date_parts[2]),
				"I   m at the Capitol in Oklahoma City, and  my name is Tanya Finchum.",
				"Okay, today is October 10, 2007 and I   m in Oklahoma City at the  Capitol."
			]
			text = transcript
			for sep in boilerplate_sep:
				if sep in transcript:
					parts = transcript.split(sep)
					head = ET.SubElement(div1, "head")
					head.text = parts[0]
					text = "{}{}".format(sep, sep.join(parts[1:]))
					num += 1
					done = True
					break
			paragraph = ET.SubElement(div2, "p")
			paragraph.text = text

		extent.text = str(total_pages)

		tree = ET.ElementTree(root)
		tree.write("{}.tei".format(int_info["filename"].replace(".txt", "")))

def main():
	info = read_metadata("metadata.csv")
	parse_file("wol_export.xml", info)

if __name__ == '__main__':
	main()