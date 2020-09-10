# Oral History Text Analysis Project (OHTAP)
### Stanford University

#### Estelle Freedman, Natalie Marine-Street
#### w/ Katie McDonough
#### Research Assistants:
* Nick Gardner (Fall 2020 -)
* Yibing Du (Fall 2020 - )
* Jade Lintott (Fall 2020 - )
* Anika Asthana (Summer 2020 - )
* Natalie Sada (Summer 2020)
* Maddie Street (Summer 2020)
* Jenny Hong (2019-20)
* Preston Carlson (2019-20)
* Hilary Sun (2018-19)
* Cheng-Hau Kee (Summer 2018)

## Winnow Subcorpus Creation Tool
### Version 1

This can only handle one corpus and one file of keywords.

Run `python subcorpora_tool/find_subcorpora_v1.py -d corpus_directory_name -w keywords_file.txt -m metadata_file.csv`.

You need to pass in three arguments: 
* `-d`: The directory where the corpora files are located.
* `-w`: The text file that contains the list of keywords.
* `-m`: The CSV file where the metadata for all of the corpora is located. This file should be in the format noted in the metadata document in the Drive folder.

### Version 2

Run `python find_subcorpora_v2.py` with `subcorpora_tool`. It must be run within the directory `subcorpora_tool`. Make sure that all text files are utf-8 encoded to avoid any encoding errors.

You need to pass in three arguments: 
* `-d`: The directory where the corpora files are located. The folder should be the name of the corpus. If no folder is specified, the default is `corpus`.
* `-w`: The text file for the keywords. These are currently assumed to be all lowercase. If no file is specified, the default is `keywords.txt`.
* `-m`: The CSV file where the metadata for all of the corpora is located. This file should be in the format noted in the metadata document in the Drive folder. We assume the CSV has a header, and that its encoding is utf-8. If no file is specified, the default is `metadata.csv`.

For the keywords file, the keywords can be specified using the following rules:
* Using the `*` symbol means that any number of letters can be be replaced.
* Keywords are to be separated by a newline (each one should be on a separate line). Those that are to be included should be the first lines of the file; those that are to be ignored should be in the last half of the file, separated from the included keywords with a newline. An examples is as follows:

```
rape
rap*

rapport
rapping
```

In this example, rape and rap* are included, and rapport and rapping are excluded.

The following files and folders will be output:
* `corpus_keywords_report.html`: Contains the basic report about the keywords and corpus.
* `corpus_keywords_file_top_words.csv`: Contains the top words of each file in the corpus in the following format: filename, word, count.
* `corpus_keywords_keyword_collocations.csv`: Contains the keyword collocations and their counts from all the files in the following format: word_1, word_2, count. If there are no collocations, there is no file.
* `corpus_keywords_keyword_collocations_formats.csv`: Contains the keyword collocations and their formats. If there are no collocations, there is no file.
* `corpus_keywords_multiple_keywords.csv`: Contains how many times keywords appeared together in the same document in the following format: word_1, word_2, count. If none is output, then there are no multiple keywords.
* `corpus_keywords_keyword_counts.csv`: Contains the keyword counts in all in the following format: keyword, count.
* `corpus_keywords_keyword_counts_by_file.csv`: Contains the keyword counts in each file in the following format: filename, keyword, count.
* `corpus_keywords_keyword_formats.csv`: Contains all the different formats of each keyword. If none is output, then there are no keywords at all.

## Encoding files

For now, we have different scripts to encode different collections. I made some notes on problems/patterns with the files.

We are currently separating it as follows (it is not complete yet; just enough to separate basic information). We still need to do the following:

* Include page numbers for those that don't have it ().
* Figure out what to do with additional information that isn't currently covered in encoding.
* Figure out what to do with images (WOL).

```
<!DOCTYPE TEI.2>
<TEI.2>
	<teiHeader type = "[Collection Name]">
		<fileDesc>
			<titleStmt>
				<title>[Title of Interview]</title>
				<author>
					<name id = "[Interviewee1 Initials]" reg = "[Interviewee Name]" type = "interviewee">[Interviewee Name]</name>, interviewee
						...
				</author>
				<respStmt>
					<resp>Interview conducted by </resp><name id = "[Interviewer1 Initials]" reg = "[Interviewer1 Name]" type = "interviewer">[Interviewer1 Name]</name>
				</respStmt>
				<respStmt>
					<resp>Text encoded by </resp><name id = "[Encoder Initials]">[Encoder Name]</name>
				</respStmt>
			</titleStmt>
			<sourceDesc>
				<biblFull>
					<titleStmt>
						<title>[Title of Interview]</title>
						<author>[Interviewees]</author>
					</titleStmt>
					<extent></extent>
					<publicationStmt>
						<publisher>[Institution]</publisher>
						<pubPlace></pubPlace>
						<date>[Interview Date]</date>
						<authority/>
					</publicationStmt>
				</biblFull>
			</sourceDesc>
		</fileDesc>
		<profileDesc>
			<langUsage>
				<language id = "[Language Abbr.]">[Language]</language>
			</langUsage>
		</profileDesc>
	</teiHeader>
	<text>
		<body>
			<div1 type = "about_interview">
				<head>[Interview Boilerplate]</head>
				<list type = "simple">
					<item>Interviewer:<name id = "spk1" key = "[Interviewer1 Initials]" reg = "[Interviewer1 Name]" type = "interviewer">[Interviewer1 Name]</item>
					...
					<item>Subject:<name id = "spk?" key = "[Interviewee1 Initials]" reg = "[Interviewee1 Name]" type = "interviewee">[Interviewee1 Name]</item>
					...
					<item>Date:<date>[Interview Date]</date></item>
				</list>
			</div1>
			<div2>
				<pb id = "p[Page Number]" n = [Page Number] />
				<sp who = "spk1">
					<speaker n = "1">...</speaker>
				</sp>
			</div2>
		</body>
	</text>
</TEI.2>
```

## Phase I Oral History Collections

#### Black Women Oral History Project (BWOH)

#### Brown Women Speak: Pembrooke Center Transcripts (BWSP)

#### Rutgers Oral History Archives (ROHA)

#### Rosie the Riveter WWII American Homefront Project - Bancroft (RTRB)

In order to run, you need:
	- the path for a folder for Metadata with the following files:
		- "Interviews.csv" a csv version of the Interviews metadata sheet
		- "Interviewees.csv" a csv version of the Interviewees metadata sheet
		- "Collections.csv" a csv version of the Collections metadata sheet
	- the path for a folder containing all of the transcripts
	- a "name map" of the appropriate format (should be in the github), can also
		be generated using `map_names_RTRB.py`
	- the pandas library (included with the anacondas distribution)

Run with `py encode_RTRB.py [transcript folder path] [metadata folder path] [name map path]`


#### Smith College Alumnae Oral History Project (SCAP)

#### Stanford Nurse Alumni Interviews (SNAI)

#### Stanford Historical Society Alumni Interviews (SHSA)

#### Stanford Historical Society Faculty and Staff and Misc Interviews (SHSF)

### Phase II

#### Oklahoma Centennial Farm Families (OCFF)

In order to run, you need:
	- the path for a folder for Metadata with the following files:
		- "Interviews.csv" a csv version of the Interviews metadata sheet
		- "Interviewees.csv" a csv version of the Interviewees metadata sheet
		- "Collections.csv" a csv version of the Collections metadata sheet
	- the path for a folder containing all of the transcripts
	- a "name map" of the appropriate format (should be in the github), can also
		be generated using `map_names_OFCC.py`
	- the pandas library (included with the anacondas distribution)

Run with `py encode_OCFF.py [transcript folder path] [metadata folder path] [name map path]`

NOTE: In order for this script to work, all of the transcripts but be preprocessed
      manually by adding the following "tags" to each transcript:
      	- `<<BOILERPLATE START>>`, `<<BOILERPLATE END>>`
	- `<<INTRODUCTION START>>`, `<<INTRODUCTION END>>`
	- `<<INTERVIEW START>>`, `<<INTERVIEW END>>`

#### Oklahoma One Hundred Year Life Collection (OOHYLC)

#### O-STATE Stories (OSS)

Run `py encoding_tool/encode_OSS.py`. You need to have `metadata.csv` and `oss_export.xml` in the folder `encoding_tool`.

Challenges:

* There are multiple interviewees, multiple dates, and multiple interviewers for the interviews.
* The transcripts are really nicely formatted into XML, but the transcript is incorrect. The speaker is not specified correctly during their line--it seems like they used a PDF reader and it incorrectly read the format.
* Another special note about this one--it's really hard to distinguish the boilerplate from the text--I first found the most common ways the interviewer started the interview ("I am [interviewer name]", etc. It's listed under `boilerplate_sep` in the code) and used those, then looked at each other file individually.

TODO:

* Separate speakers. For now, I just put it all into the `<div2>`.
* Add in the images and other artifacts. For now, I just have empty pages.

#### Dust, Drought and Dreams Gone Dry: Oklahoma Women and the Dust Bowl (OWDB)

#### Inductees of the Oklahoma Women's Hall of Fame Oral History Project (OWHF)

#### Smith College AARJ (SCAARJ)

Run `py encoding_tool/encode_SCAARJ.py`. You need to have `metadata.csv` and a folder `SCAARJ` containing the `.txt` files within it (download from the Drive). Make sure that the `.txt` files are encoded in `utf-8`.

This one was definitely one of the cleaner transcript sets to work with. It had one interviewer, one interviewee per transcript, and each transcript was written out the same way.

Challenges:

* `.docx`, the original format of the interviews, are difficult to work with in python. I just took the `.txt` files that I had already copied and pasted to work with for this code.
* I did a GOOGLE VOICE speaker manually for Nguyen, Tu-Uyen's transcript. I called GOOGE VOICE speaker 3 and designated it as an interviewer.

TODO:

* Add in page numbers...which has to be done manually unfortunately.

#### Smith College Activist Life (SCAL)

NEED TO COMPLETE!

Challenges:

* Not all of the interviews are the same, but these can be done manually since there aren't a lot of interviews in here anyways.

TODO:

* Add in page numbers...which has to be done manually unfortunately.

#### Smith College Voices of Feminism (SCVF)

#### Spotlighting Oklahoma Oral History Project (SOOH)

Run `py encoding_tool/encode_SOOH.py`. You need to have `metadata.csv` and `sok_export.xml` in the folder `encoding_tool`.

Challenges:

* There are multiple interviewees.
* There was a bug in one of the transcripts where the `creator` tag for Van Deman, Jim, doesn't contain his full name (so I manually added it in).
* For interviewer Julie Pearson Little Thunder, there were random hyphens in her name during the transcription.
* Some do not have a full interview (specifically, Steinle, Alice).
* There were a lot of manual checks I had to do to separate the boilerplate and to write regexes.

TODO:

* Separate speakers. For now, I just put it all into the `<div2>`.
* Take out End of Interview. For now, it doesn't affect the results.

#### UNC The Long Civil Rights Movement: Gender and Sexuality (UNCGAS)

#### UNC Southern Women (UNCSW)

#### UNC The Long Civil Rights Movement: The Women's Movement in the South (UNCTWMS)

#### Women of the Oklahoma Legislature (WOL)

Run `py encoding_tool/encode_WOL.py`. You need to have `metadata.csv` and `wol_export.xml` in the folder `encoding_tool`.

Challenges:

* The transcripts is really nicely formatted into XML, but the transcript is incorrect. The speaker is not specified correctly during their line--it seems like they used a PDF reader and it incorrectly read the format.
* Another special note about this one--it's really hard to distinguish the boilerplate from the text--I first found the most common ways the interviewer started the interview ("I am [interviewer name]", etc. It's listed under `boilerplate_sep` in the code) and used those, then looked at each other file individually.

TODO:

* Separate speakers. For now, I just put it all into the `<div2>`.
* Add in the images and other artifacts. For now, I just have empty pages.

## Miscellaneous Pre-processing Scripts

### Helping to categorize occupations.

The script `miscellaneous_scripts/output_top_occupations.py` reads in `metadata.csv` (in the same folder) and outputs the top occupations listed under `Past Occupations` and `Current Occupation` in our metadata spreadsheet. This is to help categorize them under job categories. It outputs an `occupations.csv` file that lists all of the occupations by how often they appear.

### Helping to isolate the transcript

#### RTRB

Run `miscellaneous_scripts/separating_interview/separate_RTRB.py` with `RTRB` of `.txt` files within the `separating_interview` folder.

#### ROHA

Run `miscellaneous_scripts/separating_interview/separate_ROHA.py` with `ROHA` of `.txt` files within the `separating_interview` folder.

#### SOOH

Run `miscellaneous_scripts/separating_interview/separate_SOOH.py` with the `sok_export.xml` file within the `separating_interview` folder.

#### BWOH

Run `miscellaneous_scripts/separating_interview/separate_BWOH.py` with the `BWOH` of `.txt` files within the `separating_interview` folder. Some had to be manually checked.

#### SCAP

Run `miscellaneous_scripts/separating_interview/separate_SCAP.py` with the `SCAP` of `.txt` files within the `separating_interview` folder. Some had to be manually checked.

#### SCVF

Run `miscellaneous_scripts/separating_interview/separate_SCVF.py` with the `SCVF` of `.txt` files within the `separating_interview` folder. A lot of interviews were blank so they didn't have interview transcripts.
