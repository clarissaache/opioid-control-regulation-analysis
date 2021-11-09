#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import os


# In[73]:


userhome = os.path.expanduser('~')

column_names = [
    "Notes",
    "County",
    "County Code",
    "Year",
    "Year Code",
    "Drug/Alcohol Induced Cause",
    "Drug/Alcohol Induced Cause Code",
    "Deaths",
]
rows = []
drug_code=['D1', 'D9', 'D2', 'D4']
for i in range(3,10):
    csvfile = userhome + r'/Documents/IDS 720/Mid-Sem-Proj/pds2021-opioids-team-three/00-source-data/US_VitalStatistics/Underlying Cause of Death, 200'+str(i)+'.txt'
    death_year = pd.read_table(csvfile)
    final=death_year[death_year['Drug/Alcohol Induced Cause Code'].isin(drug_code)]
    for row in final.to_numpy():
        rows.append(row)
for i in range(10,16):
    csvfile = userhome + r'/Documents/IDS 720/Mid-Sem-Proj/pds2021-opioids-team-three/00-source-data/US_VitalStatistics/Underlying Cause of Death, 20'+str(i)+'.txt'
    death_year = pd.read_table(csvfile)
    final=death_year[death_year['Drug/Alcohol Induced Cause Code'].isin(drug_code)]
    for row in final.to_numpy():
        rows.append(row)
deaths=pd.DataFrame(rows,columns=['Notes', 'County', 'County Code', 'Year', 'Year Code',
       'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code',
       'Deaths'])[['County', 'County Code', 'Year',
       'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code',
       'Deaths']]


# In[74]:


deaths1=deaths.groupby(['County', 'County Code', 'Year'])['Deaths'].sum().reset_index()
deaths1['State']=[i.split(',')[1] for i in deaths1.County]
deaths1['County']=[i.split(',')[0] for i in deaths1.County]


# In[81]:


deaths1.State.unique()


# In[87]:


deaths1.head()


# In[68]:


deaths1= deaths1.to_csv("deaths.csv", index=False)


# In[ ]:




