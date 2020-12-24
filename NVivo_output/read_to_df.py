'''
DESCRIPTION-------
Example code for reading NVivo coded content from an NVivo extract into a pandas dataframe. 
Here we read in two files, one containing an extract of all NVivo coding except errors, and another containing only the error coding.
The code itself is trivial and the important points are contained in NOTES.

NOTES-------
1) dependencies: the df.read_excel() in pandas uses the xlrd package internally, so you need to pip or conda install xlrd
2) need to export the NVivo extract as an .xls file 
  - NOT .xlsx, because for some reason xlrd now only supports the older .xls file type
  - NOT .csv because some cell values (description, coded text, maybe others) can contain commas and it is a hassle to work around this
3) df.read_excel() cannot read the .xls file as directly exported from NVivo (NVivo's exported .xls file is malformed according to .read_excel()'s requirements)
So as a workaround, you can "repair" NVivo's .xls file by doing the following:
   -open up the .xls file that was exported from NVivo in some spreadsheet software (I used mac's Numbers application, but Google Sheets or Excel would probably work too)
   -re-export the opened file as another .xls file (which will now be well-formed for .read_excel()). In the Numbers application, what you do precisely is
     + navigate to File -> Export To -> Excel...
     + under "Advanced Options" change file type to .xls
     + in the Excel Worksheets field, select "One Per Table" and nothing else (in particular, unselect "Include a summary worksheet" if that was selected by default")
     + click next and save the repaired file where you want

-

'''

import os
import pandas as pd


#Set up directory structure however you want. Here the 'repaired' (as described above) .xls files are assumed to reside in the directory ./data/nvivo_content
NVIVO_CONTENT_FP = os.path.join(".", "data", "nvivo_content")
NOT_ERRORS_FP = os.path.join(NVIVO_CONTENT_FP, "everything_but_errors_12-22-20.xls")
ERRORS_FP = os.path.join(NVIVO_CONTENT_FP, "errors_12-22-20.xls")

everything_df = pd.read_excel(NOT_ERRORS_FP)
errors_df = pd.read_excel(ERRORS_FP)
