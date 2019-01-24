# Oral History Text Analysis Project (OHTAP)
### Stanford University

#### Estelle Freedman, Natalie Marine-Street
#### w/ Katie McDonough
#### Research Assistants:
* Hilary Sun (2018-19)
* Cheng-Hau Kee (Summer 2018)

## Creating subcorpora

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

### Phase I

#### Black Women Oral History Project (BWOH)

#### Brown Women Speak: Pembrooke Center Transcripts (BWSP)

#### Rutgers Oral History Archives (ROHA)

#### Rosie the Riveter WWII American Homefront Project - Bancroft (RTRB)

#### Smith College Alumnae Oral History Project (SCAP)

#### Stanford Nurse Alumni Interviews (SNAI)

#### Stanford Historical Society Alumni Interviews (SHSA)

#### Stanford Historical Society Faculty and Staff and Misc Interviews (SHSF)

### Phase II

#### Oklahoma Centennial Farm Families (OCFF)

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

#### Smith College Activist Life (SCAL)

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

#### UNC The Long Civil Rights Movement: Gender and Sexuality (UNCGAS)

#### UNC Southern Women (UNCSW)

#### UNC The Long Civil Rights Movement: The Women's Movement in the South (UNCTWMS)

### Women of the Oklahoma Legislature (WOL)

Run `py encoding_tool/encode_WOL.py`. You need to have `metadata.csv` and `wol_export.xml` in the folder `encoding_tool`.

Challenges:

* The transcripts is really nicely formatted into XML, but the transcript is incorrect. The speaker is not specified correctly during their line--it seems like they used a PDF reader and it incorrectly read the format.
* Another special note about this one--it's really hard to distinguish the boilerplate from the text--I first found the most common ways the interviewer started the interview ("I am [interviewer name]", etc. It's listed under `boilerplate_sep` in the code) and used those, then looked at each other file individually.

TODO:

* Separate speakers. For now, I just put it all into the `<div2>`.
* Add in the images and other artifacts. For now, I just have empty pages.