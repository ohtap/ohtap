
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
from lxml import etree

def main():
	for f in os.listdir("UNCSW"):
		transcript = []
		with open("UNCSW/{}".format(f), "r", encoding = "utf-8") as file:
			lines = [l.strip() for l in file.readlines()]
			add = False
			for l in lines:
				if l == "Online.": add = True
				# if "[START OF TAPE 1, SIDE A]" in l:
				# 	parts = l.split("[START OF TAPE 1, SIDE A]")
				# 	transcript.append("[START OF TAPE 1, SIDE A]".join(parts[1:]))
				# 	add = True
				# elif "END OF INTERVIEW" in l: add = False
				# if "For the Southern Oral History Program" in l:
				# 	parts = l.split("For the Southern Oral History Program")
				# 	transcript.append("For the Southern Oral History Program".join(parts[1:]))
				# 	add = True
				# if "START OF INTERVIEW" in l:
				# 	add = True
				elif add:
					transcript.append(l)
		
		if len(transcript) > 0:
			print(f)
			os.remove("UNCSW/{}".format(f))
			with open(f, "w", encoding = "utf-8") as file:
				for l in transcript: file.write("{}\n".format(l))

if __name__ == '__main__':
	main()