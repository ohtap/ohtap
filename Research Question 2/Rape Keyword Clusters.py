#!/usr/bin/env python
# coding: utf-8

# In[1]:


#WHAT THIS NOTEBOOK DOES:  
#Develop a canonical grouping of keywords 
#Develop a Regular Expression to Use Keyword Clusters to designate events as "Rape or Sexual Assault" 
#Return Frequency Statistics of Rape


# In[3]:


from collections import defaultdict
import pandas as pd
import os
import re


# In[4]:


#LOADS NVivo extracts into dataframes 
print(os.getcwd()) 
everything_but = os.path.join(".", "Desktop", "everything_but_errors_12-22-20.xls")
errors = os.path.join(".", "Desktop", "errors_12-22-20.xls") 

everything_but_df = pd.read_excel(everything_but)
errors_df = pd.read_excel(errors)


# In[5]:


coding_types = everything_but_df["Hierarchical Name"].unique()
coding_types


# In[6]:


everything_but_df["Hierarchical Name"].value_counts() 


# In[7]:


#extract all events pertaining to clusters
rape_events = everything_but_df[ everything_but_df['Hierarchical Name'] == 'Nodes\\\\Topic\\Sexual assault or rape']
sexual_harassment_events = everything_but_df[ everything_but_df['Hierarchical Name'] == 'Nodes\\\\Topic\\Sexual harassment']
rape_events["Folder Location"].value_counts()
rape_events["Hierarchical Name.1"].value_counts()
rape_events["Coded Text"]  


# In[8]:


list_of_interviews_with_rape_event = rape_events["Hierarchical Name.1"]
list_of_interviews_with_rape_event


# In[9]:


rape_events["Folder Location"].value_counts() 


# In[10]:


#Counts by collection 
#counts by collection 

#number of interviews with at least one rape event
list_of_interviews_with_atl_one_rape_event = list(rape_events["Hierarchical Name.1"].unique())
list_of_interviews_with_atl_one_sexual_harassment_event = list(sexual_harassment_events["Hierarchical Name.1"].unique())
r_counts_by_collection = defaultdict(lambda:0)

for r_interview in list_of_interviews_with_atl_one_rape_event: 
    #interview["Coded Text"]
    r_collection = r_interview.split('\\\\')[1]
    r_counts_by_collection[r_collection] += 1 

#defaultdict - creates items with default values instead of throwing an error 

#for key, value in counts_by_collection.items(): 
  #  print(counts_by_collection[key])


# In[11]:


#Number of Interviews in collection coded as sexual harassment events
r_counts_by_collection 


# In[15]:


#Counts by interview
r_counts_by_interview = list(rape_events["Hierarchical Name.1"].value_counts())


# In[38]:


#Rape Cluster
#Loads contents of txt file containing keywords into a string
rape_keywords_string = ""
rape_keywords_txt_file = os.path.join(".", "Desktop", "ohtap", "rape_cluster_keywords.txt")
with open(rape_keywords_txt_file, "r+") as ack: #opens as read and write
    rape_keywords_string = ack.read()

print(rape_keywords_string)
print("\n")

#clusters created with the "OR" regex metacharacter
regex_version_rape_keywords = rape_keywords_string.replace(",", "|")
print(regex_version_rape_keywords)
regex_version_rape = re.compile(regex_version_rape_keywords)
print(regex_version_rape)
    #NOTE: The regex compile all of the keywords, it just doesn't show below


# In[39]:


#Testing the regex
#(note: .findall() returns all values, .match() just returns the first)

testing_different_keywords = regex_version_rape.findall("statutory offense, raped, raping passed the football, cat calling us he exposed himself blueberry pie fondle molest")
testing_different_keywords


# In[40]:


#Collects data on all interviews coded from NVivo as Rape

interviews_with_rape_events = rape_events["Hierarchical Name.1"]
text_of_interviews_with_rape_events = rape_events["Coded Text"]

events_of_rape_dictionary = {'Interview Name': interviews_with_rape_events, 'Interview Text': text_of_interviews_with_rape_events}
for event in events_of_rape_dictionary:
    print(event, events_of_rape_dictionary[event])


# In[41]:


#Event extent of Interviews Coded as Sexual Harassment 
interviews_with_rape_events = rape_events["Hierarchical Name.1"]
text_of_interviews_with_rape_events = rape_events["Coded Text"]


events_of_rape_dictionary = {'Interview Name': interviews_with_rape_events, 'Interview Text': text_of_interviews_with_rape_events}
for event in events_of_rape_dictionary:
    print(events_of_rape_dictionary['Interview Name'] + " " + events_of_rape_dictionary['Interview Text'])


# In[42]:


#Keyword Cluster through events  

for content_of_event in events_of_rape_dictionary:
    ahh = events_of_rape_dictionary['Interview Text']
    for a in ahh: 
        print(str(a)) 
        rape_keyword_hits_per_rape_event = regex_version_rape.findall(a)
        frequency_of_sexual_harassment_keyword_per_event = len(rape_keyword_hits_per_rape_event)
        print(rape_keyword_hits_per_rape_event)
        print(frequency_of_rape_keyword_per_event)


# In[ ]:




