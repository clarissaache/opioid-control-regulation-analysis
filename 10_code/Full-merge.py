#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


# get all data
deaths=pd.read_csv('deaths.csv')
populations=pd.read_csv('CountyPopulations.csv')


# ## FLORIDA

# In[3]:


names={' LA':'Louisiana', ' ID':'Idaho', ' CO':'Colorado', ' IL':'Illinois', ' OH':'Ohio' ,' PA':'Pennsylvania', ' SC':'South Carolina', ' FL':'Florida', ' NC':'North Carolina',
       ' CA':'California', ' NY':'New York', ' VA':'Virginia', ' MI':'Michigan', ' MD':'Maryland', ' IN':'Indiana', ' AK':'Alaska', ' TN':'Tennessee', ' TX':'Texas',
       ' ME':'Maine', ' MN':'Minnesota', ' NJ':'New Jersey', ' AL':'Alabama', ' MA':'Massachusetts', ' GA':'Georgia', ' KY':'Kentucky', ' NH':'New Hampshire', ' AR':'Arkansas',
       ' WA':'Washington', ' WV':'West Virginia', ' NM':'New Mexico', ' MO':'Missouri', ' RI':'Rhode Island', ' WI':'Wisconsin', ' OK':'Oklahoma', ' KS':'Kansas', ' UT':'Utah',
       ' NV':'Nevada', ' MT':'Montana', ' ND':'North Dakota', ' VT':'Vermont', ' OR':'Oregon', ' AZ':'Arizona', ' MS':'Mississippi', ' DC':'District of Columbia', ' NE':'Nebraska',
       ' CT':'Connecticut', ' WY':'Wyoming', ' HI':'Hawaii', ' IA':'Iowa', ' DE':'Delaware', ' SD':'South Dakota'}


# In[4]:


state = deaths["State"].apply(lambda x: x.replace(x, names[x])) #updated state names from abbreviations to full names
deaths["State"] = state  
deaths['Year']=deaths['Year'].astype('int64')
populations['County']=[i.split(' County')[0] for i in populations.County]
deaths=deaths[deaths.State!='Alaska'] #removing Alaska per Nick's instructions


# In[5]:


lol=[]
for i in [i.split(' County') for i in deaths.County]:
    if len(i)==1:
        for j in i:
            lol.append(j)
    else:
        lol.append(i[0])
deaths['County']=lol #removing the word county in column
name={'Dona Ana':'Doña Ana', 'La Porte':'LaPorte', 'Mc Kean':'McKean'} #renaming names similar to census data
deaths['County']=[name[i] if i in name.keys() else i for i in deaths['County']]


# In[6]:


fldeaths = deaths[deaths.State == "Florida"][["State", "County", "Year", "Deaths"]]
flcounties = populations[populations.State=='Florida']['County'].unique() #67 counties  
missing = []
for j in range(2003, 2016):
    for i in flcounties:
        if i not in [
            l for l in fldeaths[(fldeaths.County == i) & (fldeaths.Year == j)]["County"]
        ]:
            missing.append(
                ["Florida", i, j, np.nan]
            )  # giving NA for the ones with no drugs stuff
missing_dataframe = pd.DataFrame(missing, columns=["State", "County", "Year", "Deaths"])
updated_deaths = pd.concat([fldeaths, missing_dataframe], axis=0)#contains all FL counties across the years. the ones with NA do not have any drug related deaths info
updated_deaths["Treatment"] = "Treatment" #this new column is to make sure we know which state is the control or treatment group
updated_deaths.groupby(["Year"])[
    "County"
].count()  # double checking that all florida counties are included


# ## Texas 

# In[7]:


#similar analysis as Florida is done on Texas
Txdeaths = deaths[deaths.State == "Texas"][["State", "County", "Year", "Deaths"]]
Txcounties=populations[populations.State=='Texas']['County'].unique() #254 counties
missing = []
for j in range(2003, 2016):
    for i in Txcounties:
        if i not in [
            l for l in Txdeaths[(Txdeaths.County == i) & (Txdeaths.Year == j)]["County"]
        ]:
            missing.append(
                ["Texas", i, j, np.nan]
            )  # giving NA for the ones with no drugs stuff
missing_dataframe = pd.DataFrame(missing, columns=["State", "County", "Year", "Deaths"])
updated_Tx = pd.concat([Txdeaths, missing_dataframe], axis=0)
updated_Tx["Treatment"] = "Treatment"
updated_Tx.groupby(["Year"])[
    "County"
].count()  # double checking that all Texas counties are included


# ## Washington

# In[8]:


#similar analysis as Florida is done on Washington
Wadeaths = deaths[deaths.State == "Washington"][["State", "County", "Year", "Deaths"]]
Wacounties=populations[populations.State=='Washington']['County'].unique() #39 counties
missing = []
for j in range(2003, 2016):
    for i in Wacounties:
        if i not in [
            l for l in Wadeaths[(Wadeaths.County == i) & (Wadeaths.Year == j)]["County"]
        ]:
            missing.append(
                ["Washington", i, j, np.nan]
            )  # giving NA for the ones with no drugs stuff
missing_dataframe = pd.DataFrame(missing, columns=["State", "County", "Year", "Deaths"])
updated_Wa = pd.concat([Wadeaths, missing_dataframe], axis=0)
updated_Wa["Treatment"] = "Treatment"
updated_Wa.groupby(["Year"])[
    "County"
].count()  # double checking that all Texas counties are included


# # Adding the above info from the 3 states in one df

# In[9]:


treat_updated=pd.concat([updated_deaths,updated_Tx,updated_Wa],axis=0) #the number of rows are expected
treat_updated


# # Merging deaths and census data for Wa,Tx and FL

# In[10]:


treat_updated=treat_updated[treat_updated.Year>=2006] 
merge_deaths=pd.merge(treat_updated,populations,on=['State','County','Year'],how='left',validate="1:1",indicator=True) 
merge_deaths[merge_deaths['_merge']!='both'] # everything merged right


# ## Dealing with Nas from Counties with no mortality info.

# In[11]:


missing=[]
for i in merge_deaths["Deaths"]:
    if pd.isna(i):
        missing.append(np.random.randint(0,10)) #picking this way to randomly give a value between 0 and 10 deaths. we could decide on another better way later.
    else:
        missing.append(i)
merge_deaths['Deaths']=missing
merge_deaths['death_prop']=merge_deaths['Deaths'].astype('float64')/merge_deaths['Population'] #calculates the death rate per county


# In[12]:


merge_deaths[merge_deaths.isnull().any(axis=1)]  #This confirms that there is now no deaths NA's in Texas,Washington and Florida 


# In[13]:


merge_deaths.head()


# ## The rest of the country states (will be our control group)

# In[14]:


rest_deaths=deaths.loc[~deaths['State'].isin(['Washington','Texas','Florida']),]
rest_deaths=rest_deaths[rest_deaths.Year>=2006]
restmerge=pd.merge(rest_deaths,populations,on=['State','County','Year'],how='left',indicator=True)
restmerge[restmerge['_merge']!='both']# this looks for the rows that did't merge properly. Only District of Columbia pops up. 


# In[15]:


restmerge=restmerge.loc[restmerge['Deaths']!='MissingMissingMissingMissing',].copy()
restmerge=restmerge.loc[restmerge.County!='District of Columbia'].copy()
restmerge['Treatment']='Control'
restmerge['death_prop']=restmerge['Deaths'].astype('float64')/restmerge['Population']
restmerge=restmerge[['State','County','Year','Deaths','Population','death_prop','Treatment','_merge']]


# In[16]:


restmerge[restmerge.isnull().any(axis=1)] #No more Nas! yay!


# In[17]:


deaths_pop=pd.concat([merge_deaths,restmerge],axis=0) #putting treatment and control groups together
final=deaths_pop[['State','County','Year','Deaths','Population','Treatment','death_prop']].to_csv('deaths-pop-merge.csv')

