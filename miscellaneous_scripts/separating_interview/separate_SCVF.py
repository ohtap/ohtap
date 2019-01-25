
import xml.etree.ElementTree as ET
from collections import defaultdict
import os
import pandas as pd
from lxml import etree

def main():
	for f in os.listdir("SCVF"):
		transcript = []
		with open("SCVF/{}".format(f), "r", encoding = "utf-8") as file:
			lines = [l.strip() for l in file.readlines()]
			add = False
			for l in lines:
				if "by:" in l: 
					add = True
				elif "filmed by:" in l:
					add = True
				elif "END OF INTERVIEW" in l:
					add = False
				elif add:
					transcript.append(l)
		if len(transcript) == 0: print(f)
		with open(f, "w", encoding = "utf-8") as file:
			for l in transcript: file.write("{}\n".format(l))

if __name__ == '__main__':
	main()