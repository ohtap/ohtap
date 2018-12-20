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

Run `python find_subcorpora_v2.py` with `subcorpora_tool`. It must be run within the directory

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