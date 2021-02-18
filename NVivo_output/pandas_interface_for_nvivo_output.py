#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pandas interface/organization of the raw NVivo output for all RAs to eventually use on RQs


# In[2]:


import pandas as pd
import os


# In[3]:


#NVivo exports have to be in .xls format 
#for more information, see read_to_df.py

#  1. conda download xlrd within the notebook 
#  2. pull up NVivo extracts (ohtap --> NVivo output --> data --> "everything-1-21-2021.xls" ) 
#  3. load the .xlrd files into dataframes to access the content 
#  4. parse through the content (can load specific parts into dictionaries for easier viewing)


# In[5]:


#use os pathways to pull up .xls files 


everything = os.path.join(".", "Desktop", "everything-1-21-2021.xls")
false_hits = os.path.join(".", "Desktop", "errors_12-22-20.xls")
# NOTE: I moved my extracts from my the ohtap/NVivo Output/data folder to my desktop because it mitigates the pathway errors I was previously getting 

#load them into dataframes 
everything_df = pd.read_excel(everything) 
false_hits_df = pd.read_excel(false_hits) 


# In[6]:


everything_df


# In[10]:


#can access specific data from these dataframes 
#also see pandas documentation on DataFrames - there's a lot of interesting stuff you can do! 
print(everything_df["Hierarchical Name.1"])
everything_df["Coded Text"]


# In[16]:


#Access data for specific manual codes 

rape_events = everything_df[ everything_df['Hierarchical Name'] == 'Nodes\\\\Topic\\Sexual assault or rape']
rape_events


# In[19]:


#within this, you can access specific information by interview 
all_events_coded_as_rape = rape_events["Coded Text"]
all_events_coded_as_rape


# In[20]:


#load information into dictionaries (ex: interviews events coded as rape)
interviews_with_rape_events = rape_events["Hierarchical Name.1"]
text_of_interviews_with_rape_events = rape_events["Coded Text"]


events_of_rape_dictionary = {'Interview Name': interviews_with_rape_events, 'Interview Text': text_of_interviews_with_rape_events}   
for event in events_of_rape_dictionary: 
    print(events_of_rape_dictionary['Interview Name'] + " " + events_of_rape_dictionary['Interview Text'])


# In[ ]:




