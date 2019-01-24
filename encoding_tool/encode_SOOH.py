
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
import re
from lxml import etree

regexes = [
	"(4  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+).  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z\s]+), ([A-Za-z\s]+)  ([A-Za-z]+ [0-9]+, [0-9]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z\s]+), ([A-Za-z\s]+)  ([A-Za-z]+ [0-9]+, [0-9]+) )",
	"(4  O-State Stories  An Oral History Project of the OSU Library  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Muskogee African American Heritage Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Anthrax in Oklahoma Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Oklahoma Native Artists  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-]+)  A conversation with  ([A-Za-z\s\.\-]+)  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+/ [A-Za-z]+ [0-9]+, [0-9]+/  [A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Life in the 1930s Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Women Agricultural Extension Educators Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+ / [A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))",
	"(4  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+) ([A-Za-z\s]+))",
	"(5  Spotlighting Oklahoma  Oral History Project  ([A-Za-z\s\.\-,]+)  Oral History Interview  Interviewed by ([A-Za-z\s\.\-]+)  ([A-Za-z]+ [0-9]+, [0-9]+)  ([A-Za-z\s]+), ([A-Za-z\s]+))"
]

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
		if r[3] == "SOOH":
			interviewee = r[7]
			num = 1
			new_interviewee = interviewee
			while new_interviewee in info: 
				new_interviewee = "{}{}".format(interviewee, num)
				num += 1
			info[new_interviewee] = {}
			info[new_interviewee]["interviewee"] = interviewee
			info[new_interviewee]["filename"] = r[6]
			info[new_interviewee]["interviewee_init"] = create_initials(r[7])
			info[new_interviewee]["interviewer"] = r[8]
			info[new_interviewee]["interviewer_init"] = create_initials(r[8])
			info[new_interviewee]["date"] = r[9]
			info[new_interviewee]["language_id"] = "eng"
			info[new_interviewee]["language"] = "English"
			info[new_interviewee]["publisher"] = "Oklahoma State University Library"

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
	interviewees_done = {}
	for interview in interviews:
		done = False
		interviewee = interview.find("creator").text

		interviewee_parts = []
		for part in interviewee.split(";")[0].split(","):
			if "19" not in part: interviewee_parts.append(part)
		interviewee = ",".join(interviewee_parts).strip()
		new_interviewee = interviewee
		if interviewee in interviewees_done:
			new_interviewee = "{}{}".format(interviewee, interviewees_done[interviewee])
			interviewees_done[interviewee] += 1
		else:
			interviewees_done[interviewee] = 1
		int_info = info[new_interviewee]
		int_info["title"] = interview.find("title").text
		root = ET.Element("TEI.2")
		header = ET.SubElement(root, "teiHeader", name = "Spotlighting Oklahoma Oral History Project")
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

			interviewers = int_info["interviewer"].split(";")
			regex_interviewers = []
			for i in interviewers:
				if i.replace("-", " ") == "Pearson Little Thunder, Julie": i = "Little Thunder, Julie"
				parts = i.split(", ")
				last_name = parts[0]
				regex_interviewers.append(last_name.strip())
				if len(parts) > 1: regex_interviewers.append("{}. {}".format(parts[1].strip()[0].upper(), last_name))

			# Special cases
			if interviewee == "Tygart, Karen": regex_interviewers = ["Kyle Bryan"]

			transcript = n.find("page").find("pagetext").text
			m = None
			for regex in regexes:
				for i in regex_interviewers:
					new_regex = "{} {}".format(regex, i.strip())
					all_matches = re.findall(new_regex, transcript)
					if len(all_matches) > 0:
						m = all_matches[0]
						break
			if interviewee == "Steinle, Alice":
				head = ET.SubElement(div1, "head")
				paragraph = ET.SubElement(div2, "p")
				paragraph.text = transcript
			elif m is None: 
				head = ET.SubElement(div1, "head")
				head.text = transcript
			else:
				sep = m[0]
				parts = transcript.split(sep)
				head = ET.SubElement(div1, "head")
				head.text = parts[0]
				text = "{}{}".format(sep, sep.join(parts[1:]))
				paragraph = ET.SubElement(div2, "p")
				paragraph.text = text

			d = int_info["date"].strip()
			date_parts = d.split("/")

		extent.text = str(total_pages)

		tree = ET.ElementTree(root)
		tree.write("{}.tei".format(int_info["filename"].replace(".txt", "")))

def main():
	info = read_metadata("metadata.csv")
	parse_file("sok_export.xml", info)

if __name__ == '__main__':
	main()