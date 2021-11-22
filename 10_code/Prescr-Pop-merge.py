#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# get all data
deaths=pd.read_csv('deaths.csv')
populations=pd.read_csv('CountyPopulations.csv')
prescriptions=pd.read_csv('prescriptions3')


# ## FLORIDA

# In[3]:


prescriptions['County']=prescriptions['BUYER_COUNTY'] 
florida=prescriptions[prescriptions.State=='Florida'][['County','T_DATE','MME','State']] # only picking Florida related rows
flcounties=prescriptions[prescriptions.State=='Florida']['County'].unique() #getting all counties from Florida (67 of them)
missing=[]
for j in range(2006,2015):
    for i in flcounties:
        if i not in[l for l in florida[(florida.County==i)&(florida.T_DATE==j)]['County']]:
            missing.append([i,j,'NA','Florida']) # giving NA for the counties with no prescription related info
missing_dataframe=pd.DataFrame(missing,columns=['County','T_DATE','MME','State'])
updated_prescr=pd.concat([florida,missing_dataframe],axis=0) #contains all FL counties across the years. the ones with NA do not have any prescriptions info
updated_prescr['Treatment']='Treatment' #this new column is to make sure we know which state is the control or treatment group
updated_prescr.groupby(['T_DATE'])['County'].count() #double checking that all florida counties are included for each year


# ## Georgia

# In[4]:


Georgia=prescriptions[prescriptions.State=='Georgia'][['County','T_DATE','MME','State']].copy() #getting Georgia rows
Georgia_counties=prescriptions[(prescriptions.State=='Georgia')&(prescriptions.T_DATE==2013)]['BUYER_COUNTY'].unique() #getting Georgia counties (151 of them)
Georgiafinal=Georgia.loc[Georgia.County.isin(Georgia_counties),].copy()
Georgiafinal['Treatment']='Control' 
Georgia.loc[Georgia.County.isin(Georgia_counties),].groupby('T_DATE')['County'].count() #double checking that all georgia counties are included for each year


# ## North Carolina

# In[5]:


#similar analysis done on Georgia is repeated
NC=prescriptions[prescriptions.State=='North Carolina'][['County','T_DATE','MME','State']]
NC_counties=prescriptions[(prescriptions.State=='North Carolina')&(prescriptions.T_DATE==2013)]['BUYER_COUNTY'].unique()
NCfinal=NC.loc[NC.County.isin(NC_counties),]
NCfinal['Treatment']='Control'
NC.loc[NC.County.isin(NC_counties),].groupby('T_DATE')['County'].count() # confirm all years have the same counties


# ## Kentucky

# In[6]:


#similar analysis done on Georgia is repeated
KY=prescriptions[prescriptions.State=='Kentucky'][['County','T_DATE','MME','State']]
KY_counties=prescriptions[(prescriptions.State=='Kentucky')&(prescriptions.T_DATE==2013)]['BUYER_COUNTY'].unique()
KYfinal=KY.loc[KY.County.isin(KY_counties),]
KYfinal['Treatment']='Control'
KY.loc[KY.County.isin(KY_counties),].groupby('T_DATE')['County'].count() # confirm all years have the same counties


# ## Putting the treatment and control states in one dataframe

# In[7]:


all_prescriptions=pd.concat([updated_prescr,KYfinal,Georgiafinal,NCfinal],axis=0) #concatenating treatment and control states in one dataframe


# In[8]:


states=['Florida', 'Georgia', 'North Carolina', 'Kentucky']
subset=populations.loc[populations.State.isin(states),].copy() #only getting population info on the above states
subset['County']=[i.split(' County')[0] for i in subset.County] #renaming values to go from: "A County" to just "A". 
all_prescriptions['County']=(all_prescriptions['County'].str.lower()).str.capitalize()
all_prescriptions['Year']=all_prescriptions['T_DATE'] #renaming the Year column to match for mergin


# In[9]:


rectifying = { #these are the outlier counties that do not match the names in the census data. I renamed them to help with the merge.
    "De soto": "DeSoto",
    "Indian river": "Indian River",
    "Miami-dade": "Miami-Dade",
    "Palm beach": "Palm Beach",
    "Saint johns": "St. Johns",
    "Saint lucie": "St. Lucie",
    "Saint Johns": "St. Johns",
    "Saint Lucie": "St. Lucie",
    "Santa rosa": "Santa Rosa",
    "Mccracken": "McCracken",
    "Mccreary": "McCreary",
    "Mclean": "McLean",
    "Ben hill": "Ben Hill",
    "Dekalb": "DeKalb",
    "Jeff davis": "Jeff Davis",
    "Mcduffie": "McDuffie",
    "Mcintosh": "McIntosh",
    "Mcdowell": "McDowell",
    "New hanover": "New Hanover",
}
p=[]
for i in all_prescriptions['County']:
    if i in rectifying.keys():
        p.append(rectifying[i])
    else:
        p.append(i)
all_prescriptions['County']=p #updating the county column for prescriptions to match with census county names 


# # Merging census and prescr data +dealing with NA data

# In[10]:


prescr_merge=pd.merge(all_prescriptions,subset,on=['County','Year','State'],how='left',indicator=True)[['State','County','MME','Population','Year','Treatment','_merge']]
prescr_merge[prescr_merge["_merge"] != "both"] #everything merged properly


# In[11]:


prescr_merge['MME']=prescr_merge['MME'].replace('NA',np.NaN) 
prescr_merge['Prescr_rate']=prescr_merge['MME']/prescr_merge['Population'] 


# In[12]:


prescr_merge=prescr_merge[prescr_merge.County=='Glades'].sort_values(by=['State','County','Year']).interpolate(method='bfill') #using interpolation to fill in  missing values for Glades.


# In[13]:


prescr_merge[prescr_merge.isnull().any(axis=1)] #as expected, no missing values!! Yay!  


# In[14]:


prescr_pop=prescr_merge.to_csv("Prescription-Pop-merge.csv",index=False)

