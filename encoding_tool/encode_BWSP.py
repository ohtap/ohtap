
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd

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
def read_metadata(file, filenames):
	df = pd.read_csv(file, encoding = "utf-8", header = None)

	info = {}
	for f in filenames: info[f] = {}
	for i, r in df.iterrows():
		f = r[6]
		if f in info:
			info[f] = {}
			info[f]["interviewee"] = r[7]
			info[f]["interviewee_init"] = create_initials(r[7])
			info[f]["interviewer"] = r[8]
			info[f]["interviewer_init"] = create_initials(r[8])
			info[f]["date"] = r[9]
			info[f]["language_id"] = "eng"
			info[f]["language"] = "English"
			info[f]["pub_place"] = "Providence, Rhode Island"
			info[f]["publisher"] = "Brown University"

	return info

# Reverses the comma for a name.
def reverse_name(name):
	if pd.isnull(name): return ""
	parts = name.split(",")
	final_name = []
	for p in parts[1:]:
		final_name.append(p.strip())
	final_name.append(parts[0].strip())
	return " ".join(final_name)

# Separates the boilerplate and the pages for the file.
def separate_boilerplate(content, info):
	for file, lines in content.items():
		print(file)
		interviewee = reverse_name(info[file]["interviewee"])
		interviewer = reverse_name(info[file]["interviewer"])
		interviewee_init = info[file]["interviewee_init"].upper()
		interviewer_init = info[file]["interviewer_init"].upper()

		is_boilerplate = True
		boilerplate = []
		pages = []
		curr_page = []
		num_pages = 0
		for l in lines:
			l = l.strip()
			if l == "": continue

			# Checks to see if we're still in the boilerplate. A few cases
			# that we are not in.
			# (1) It says "Track 1"
			if l == "Track 1": is_boilerplate = False
			# (2) It says "[Part 1]"
			if l == "[Part 1]": is_boilerplate = False
			# (3) It start with the interviewee or interviewer's full name/initials
			# (We are assuming that this format doesn't appear in boilerplate.)
			if "{}:".format(interviewee) in l or "{}:".format(interviewee_init) in l.lower() or ("{}:".format(interviewer) in l and interviewer != "") or ("{}:".format(interviewer_init) in l.lower() and interviewer_init != ""):
				is_boilerplate = False
			# (4) Unique cases
			if "Derria Byrd:" in l: is_boilerplate = False
			if l == "Q: – first woman in the English department, at least, weren’t you?": is_boilerplate = False
			if l == "SAR: Well, I guess we should start with how you grew up and where you grew up.": is_boilerplate = False

			if is_boilerplate:
				boilerplate.append(l)
			else:
				# Adds the lines for the current page onto the page
				# since this signals the end of the page.
				if l.isdigit(): 
					num_pages = int(l)
					pages.append(curr_page)
					curr_page = []
				else:
					curr_page.append(l)

		print(boilerplate[-1])
		print()
	
	return boilerplate, pages, num_pages

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
	author.text = ", interviewee"

	# Interviewer
	resp_stmt = ET.SubElement(title_stmt, "respStmt")
	resp = ET.SubElement(resp_stmt, "resp")
	resp.text = "Interview conducted by "
	interviewer = ET.SubElement(title_stmt, "name", id = info["interviewer_init"], reg = info["interviewer"], type = "interviewer")
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
	extent.text = info["num_pages"]
	publisher_stmt = ET.SubElement(bibl_full, "publicationStmt")
	publisher = ET.SubElement(publisher_stmt, "publisher")
	publisher.text = info["publisher"]
	pub_place = ET.SubElement(publisher_stmt, "pubPlace")
	pub_place.text = info["pub_place"]
	date = ET.SubElement(publisher_stmt, "date")
	date.text = info["date"]

# Writes the "fileDesc" section of the TEI file, which is under "teiHeader."
def write_file_description(header, info):
	file_desc = ET.SubElement(header, "fileDesc")
	write_title_section(file_desc, info)
	write_source_description(file_desc, info)
	
# Writes the "profileDesc" section of the TEI file, which is under "teiHeader."
def write_profile_description(header, info):
	profile_desc = ET.SubElement(header, "profileDesc")
	lang_usage = ET.SubElement(profile_desc, "langUsage")
	language = ET.SubElement(lang_usage, "language", id = info["language_id"])
	language.text = info["language"]

# Writes the "revisionDesc" section of the TEI file, which is under "teiHeader."
def write_revision_description(header, info):
	revision_desc = ET.SubElement(header, "revisionDesc")

# Creates the "about_interview" div section of the TEI file, which is under "body."
def write_about_interview(body, info):
	div1 = ET.SubElement(body, "div1", type = "about_interview")
	head = ET.SubElement(div1, "head")
	head.text = info["title"]
	li = ET.SubElement(div1, "list", type = "simple")
	curr = None
	for l in info["boilerplate"]:
		if "Narrator: " in l:
			item = ET.SubElement(li, "item")
			item.text = "Subject:"
			name = ET.SubElement(item, "name", id = "spk1", key = info["interviewee_init"], reg = info["interviewee"], type = "interviewer")
			name.text = l.replace("Narrator: ")
		elif "Interviewer: " in l:
			item = ET.SubElement(li, "item")
			item.text = "Interviewer:"
			name = ET.SubElement(item, "name", id = "spk2", key = info["interviewer_init"], reg = info["interviewer"], type = "interviewer")
			name.text = l.replace("Interviewer: ")
		elif "Interview Date: " in l:
			item = ET.SubElement(li, "item")
			item.text = "Date:"
			date = ET.SubElement(item, "date")
			date.text = l.replace("Interview Date: ")
		else:
			if ":" in l:
				if curr is not None: curr = ET.SubElement(li, "item")
			if curr is None:
				p = ET.SubElement(curr, "p")
				p.text = l
			else:
				p = ET.SubElement(li, "item")
				p.text = l

# Creates the TEI tree and writes it to a TEI file.
def create_tei(info):
	root = ET.Element("TEI.2")

	# Creates the header
	header = ET.SubElement(root, "teiHeader", name = "Brown Women Speak: Pembrooke Center Transcripts")
	write_file_description(header, info)
	write_profile_description(header, info)
	write_revision_description(header, info)
	
	# Creates the text itself
	text = ET.SubElement(root, "text")
	body = ET.SubElement(text, "body")

	tree = ET.ElementTree(root)
	tree.write("test.tei")

def main():
	filenames = []
	content = {}
	for file in os.listdir("BWSP"):
		if ".txt" not in file: continue
		with open("BWSP/{}".format(file), "r", encoding = "utf-8") as f:
			filenames.append(file)
			lines = f.readlines()
			content[file] = lines

	info = read_metadata("metadata.csv", filenames)
	separate_boilerplate(content, info)
	# create_tei(info)

if __name__ == '__main__':
	main()