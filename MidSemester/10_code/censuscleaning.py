#!/usr/bin/env python
# coding: utf-8

# In[165]:


import numpy as np
import pandas as pd 


# In this file I will be merging US Population data taken from the US census website into one single data frame. This data fram will contain the populations in all states, by county for 2006-2012. We have to merge two separate data files, one with pre-2010 information and one with post-2010 information.

# In[166]:


Census20102012 = pd.read_csv("https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-three/censusdata/MidSemester/00_data/co-est2015-alldata-1.csv?token=AVVHZRVBT2T5NJYQ73KTJJLBRLTFG", encoding="ISO-8859-1")
Census20102012.sample(5)


# In[167]:


for col in Census20102012.columns:
        print(col)


# From this, we know that the relevant columns to keep are:
# REGION
# DIVISION
# STNAME
# CTYNAME
# CENSUS2010POP
# POPESTIMATE2011
# POPESTIMATE2012

# In[168]:


Census20102012sub = Census20102012[['STNAME', 'CTYNAME', 'CENSUS2010POP', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014', 'POPESTIMATE2015']]
Census20102012sub


# In[169]:


Census20102012sub.rename({'STNAME': 'STATE', 'CTYNAME': 'COUNTY', 'CENSUS2010POP': '2010', 'POPESTIMATE2011': '2011', 'POPESTIMATE2012': '2012', 'POPESTIMATE2013': '2013', 'POPESTIMATE2014': '2014', 'POPESTIMATE2015': '2015'}, axis=1, inplace=True)

Census20102012sub


# In[170]:


Census20002009 = pd.read_csv("https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-three/censusdata/MidSemester/00_data/co-est2009-alldata.csv?token=AVVHZRXAAUHE3DNX32FWTELBRLTMG", encoding="ISO-8859-1")
Census20002009.sample(5)


# Same format as previous file so we can use same format except we are using Pop. estimates from 2006-2009

# In[171]:


Census20002009sub = Census20002009[['STNAME', 'CTYNAME', 'POPESTIMATE2006', 'POPESTIMATE2007','POPESTIMATE2008', 'POPESTIMATE2009']]
Census20002009sub


# In[172]:


Census20002009sub.rename({'STNAME': 'STATE', 'CTYNAME': 'COUNTY', 'POPESTIMATE2006': '2006', 'POPESTIMATE2007': '2007', 'POPESTIMATE2008': '2008','POPESTIMATE2009': '2009'}, axis=1, inplace=True)

Census20002009sub


# In[173]:


Check = (Census20002009sub['STATE'] == Census20002009sub['COUNTY'])
Check.value_counts()


# Noticed that the total state populations are ALSO included so I will want to drop those from final clean data 

# Changing some of the county names for the data so that it will merge better (some county names were changed in the past few years)

# In[174]:


Census20002009sub.loc[Census20002009sub.COUNTY == "La Salle Parish", "COUNTY"] = 'LaSalle Parish'
Census20002009sub.loc[Census20002009sub.COUNTY == "Petersburg Census Area", "COUNTY"] = 'Petersburg Borough'
Census20102012sub.loc[Census20102012sub.COUNTY == "Oglala Lakota County", "COUNTY"] = 'Shannon County'
Census20002009sub.loc[Census20002009sub.COUNTY == "Wade Hampton Census Area", "COUNTY"] = 'Kusilvak Census Area'
Census20002009sub.loc[Census20002009sub.COUNTY == "Wade Hampton Census Area", "COUNTY"] = 'Kusilvak Census Area'


# In[175]:


Population = pd.merge(Census20002009sub, Census20102012sub, on = ['STATE', 'COUNTY'], how = 'outer', indicator = True)

Population.sample(20)


# In[176]:


Population[Population._merge != "both"]


# Only one unmatched column so will just drop it. 

# In[177]:


Population.dropna


# Data was merged so that it was the same on both sides (thanks to the changing of La Salle Parish to LaSalle Parish). Now to drop the state total populations. 

# In[178]:


CountyPopulations = Population[Population['COUNTY'] != Population["STATE"]]
CountyPopulations.sample(20)


# Checking that the state population was actually dropped: 

# In[179]:


Check2 = (CountyPopulations['STATE'] == CountyPopulations['COUNTY'])
Check2.value_counts()


# In[180]:


CountyPopulations = CountyPopulations.drop('_merge', axis=1)
CountyPopulations


# In[181]:


CountyPopulations = CountyPopulations.melt(id_vars=['STATE', 'COUNTY'])
CountyPopulations


# In[182]:


CountyPopulations.rename({'STATE': 'State', 'COUNTY': 'County', 'variable': 'Year', 'value': 'Population'}, axis=1, inplace=True)
CountyPopulations


# In[193]:


CountyPopulations.to_csv('CountyPopulations.csv')

