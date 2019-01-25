
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
from lxml import etree

def main():
	for f in os.listdir("ROHA"):
		transcript = []
		with open("ROHA/{}".format(f), "r", encoding = "utf-8") as file:
			lines = [l.strip() for l in file.readlines()]
			add = False
			skip_next = False
			for l in lines:
				if "END OF TAPE" in l: continue
				elif skip_next:
					skip_next = False
					continue
				elif "TRANSCRIPT BY" in l: 
					add = True
					skip_next = True
				elif "END OF INTERVIEW" in l:
					add = False
					break
				elif add:
					transcript.append(l)
		with open(f, "w", encoding = "utf-8") as file:
			for l in transcript: file.write("{}\n".format(l))

if __name__ == '__main__':
	main()