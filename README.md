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

Run `python subcorpora_tool/find_subcorpora_v2.py`.

You need to pass in three arguments: 
* `-d`: The directory where the corpora files are located. The folder should be the name of the corpus. If no folder is specified, the default is `corpora`.
* `-w`: The text file for the keywords. If no file is specified, the default is `keywords.txt`.
* `-m`: The CSV file where the metadata for all of the corpora is located. This file should be in the format noted in the metadata document in the Drive folder. If no file is specified, the default is `metadata.csv`.

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