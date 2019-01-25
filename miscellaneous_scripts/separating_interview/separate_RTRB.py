
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
from lxml import etree

def main():
	for f in os.listdir("RTRB"):
		transcript = []
		with open("RTRB/{}".format(f), "r", encoding = "utf-8") as file:
			lines = [l.strip() for l in file.readlines()]
			add = False
			for l in lines:
				if "<transcript>" in l:
					transcript.append(l.split("<transcript>")[1])
					add = True
				elif "end of interview" in l.lower():
					add = False
				elif add:
					transcript.append(l)
		with open(f, "w", encoding = "utf-8") as file:
			for l in transcript: file.write("{}\n".format(l))

if __name__ == '__main__':
	main()