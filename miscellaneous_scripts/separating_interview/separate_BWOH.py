
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
from lxml import etree

def main():
	for f in os.listdir("BWOH"):
		transcript = []
		with open("BWOH/{}".format(f), "r", encoding = "utf-8") as file:
			lines = [l.strip() for l in file.readlines()]
			add = False
			for l in lines:
				if "INTERVIEW WITH" in l: 
					add = True
				elif l == "Index":
					add = False
				elif add:
					transcript.append(l)
		with open(f, "w", encoding = "utf-8") as file:
			for l in transcript: file.write("{}\n".format(l))

if __name__ == '__main__':
	main()