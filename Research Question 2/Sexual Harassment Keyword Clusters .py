#!/usr/bin/env python
# coding: utf-8

# In[1]:


#WHAT THIS NOTEBOOK DOES:  
#Develop a canonical grouping of keywords 
#Develop a Regular Expression to Use Keyword Clusters to designate events as "Sexual Harassment" 
#Return Frequency Statistics of Sexual Harassment Events  


# In[22]:


from collections import defaultdict
import pandas as pd
import os
import re


# In[3]:


#LOADS NVivo extracts into dataframes 
print(os.getcwd()) 
everything_but = os.path.join(".", "Desktop", "everything_but_errors_12-22-20.xls")
errors = os.path.join(".", "Desktop", "errors_12-22-20.xls") 

everything_but_df = pd.read_excel(everything_but)
errors_df = pd.read_excel(errors)


# In[4]:


coding_types = everything_but_df["Hierarchical Name"].unique()
coding_types


# In[5]:


everything_but_df["Hierarchical Name"].value_counts() 


# In[10]:


sexual_harassment_events = everything_but_df[ everything_but_df['Hierarchical Name'] == 'Nodes\\\\Topic\\Sexual harassment']
sexual_harassment_events["Folder Location"].value_counts() 


# In[11]:


#events coded as sexual harrassment

list_of_sexual_harrassment_events = sexual_harassment_events["Hierarchical Name.1"]
list_of_sexual_harrassment_events


# In[12]:


#Counts by collection 
list_of_interviews_with_atl_one_sexual_harassment_event = list(sexual_harassment_events["Hierarchical Name.1"].unique())
s_counts_by_collection = defaultdict(lambda:0) 


for s_interview in list_of_interviews_with_atl_one_sexual_harassment_event: 
    s_collection = s_interview.split('\\\\')[1] 
    s_counts_by_collection[s_collection] += 1 


# In[13]:


#Number of Interviews in collection coded as sexual harassment events
s_counts_by_collection 


# In[15]:


#Counts by interview
s_counts_by_interview = list(sexual_harassment_events["Hierarchical Name.1"].value_counts())


# In[38]:


#Sexual Harassment Cluster 
#Loads contents of txt file containing keywords into a string
sexual_harassment_keywords_string = "" 
sexual_harassment_keywords_txt_file = os.path.join(".", "Desktop", "ohtap", "sexual_harassment_cluster_keywords.txt") 
with open(sexual_harassment_keywords_txt_file, "r+") as ack: #opens as read and write
    sexual_harassment_keywords_string = ack.read() 

print(sexual_harassment_keywords_string)
print("\n")

#clusters created with the "OR" regex metacharacter    
regex_version_sexual_harassment_keywords = sexual_harassment_keywords_string.replace(",", "|") 
print(regex_version_sexual_harassment_keywords) 
regex_version_sexual_harassment = re.compile(regex_version_sexual_harassment_keywords)
print(regex_version_sexual_harassment)  
    #NOTE: The regex compile all of the keywords, it just doesn't show below


# In[39]:


#Testing the regex 
#(note: .findall() returns all values, .match() just returns the first) 

testing_different_keywords = regex_version_sexual_harassment.findall("statutory offense, passed the football, cat calling us he exposed himself blueberry pie fondle molest") 
testing_different_keywords


# In[40]:


#Collects data on all interviews coded from NVivo as sexual harassment 

interviews_with_sexual_harassment_events = sexual_harassment_events["Hierarchical Name.1"]


events_of_sexual_harassment_dictionary = {'Interview Name': interviews_with_sexual_harassment_events, 'Interview Text': text_of_interviews_with_sexual_harassment_events}   
for event in events_of_sexual_harassment_dictionary: 
    print(event, events_of_sexual_harassment_dictionary[event])


# In[41]:


#Event extent of Interviews Coded as Sexual Harassment 
interviews_with_sexual_harassment_events = sexual_harassment_events["Hierarchical Name.1"]
text_of_interviews_with_sexual_harassment_events = sexual_harassment_events["Coded Text"]


events_of_sexual_harassment_dictionary = {'Interview Name': interviews_with_sexual_harassment_events, 'Interview Text': text_of_interviews_with_sexual_harassment_events}   
for event in events_of_sexual_harassment_dictionary: 
    print(events_of_sexual_harassment_dictionary['Interview Name'] + " " + events_of_sexual_harassment_dictionary['Interview Text'])


# In[42]:


#Keyword Cluster through events  

for content_of_event in events_of_sexual_harassment_dictionary:  
    ahh = events_of_sexual_harassment_dictionary['Interview Text']
    for a in ahh: 
        print(str(a)) 
        sexual_harassment_keyword_hits_per_sexual_harassment_event = regex_version_sexual_harassment.findall(a) 
        frequency_of_sexual_harassment_keyword_per_event = len(sexual_harassment_keyword_hits_per_sexual_harassment_event)
        print(sexual_harassment_keyword_hits_per_sexual_harassment_event)
        print(frequency_of_sexual_harassment_keyword_per_event) 


# In[ ]:




