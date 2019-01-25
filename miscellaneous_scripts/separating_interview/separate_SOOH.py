
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
		if new_interviewee == "Van Deman": new_interviewee = "Van Deman, Jim"
		if interviewee in interviewees_done:
			new_interviewee = "{}{}".format(interviewee, interviewees_done[interviewee])
			interviewees_done[interviewee] += 1
		else:
			interviewees_done[interviewee] = 1
		int_info = info[new_interviewee]
		int_info["title"] = interview.find("title").text

		nodes = interview.find("structure").find("node").findall("node")
		for n in nodes:
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
			final_interview = ""
			m = None
			for regex in regexes:
				for i in regex_interviewers:
					new_regex = "{} {}".format(regex, i.strip())
					all_matches = re.findall(new_regex, transcript)
					if len(all_matches) > 0:
						m = all_matches[0]
						break
			if m is None: 
				final_interview = transcript
			else:
				sep = m[0]
				parts = transcript.split(sep)
				final_interview = sep.join(parts[1:])

			with open(int_info["filename"], "w", encoding = "utf-8") as f:
				f.write(final_interview.replace("End of interview", ""))

def main():
	info = read_metadata("metadata.csv")
	parse_file("sok_export.xml", info)

if __name__ == '__main__':
	main()