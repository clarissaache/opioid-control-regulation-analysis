#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[11]:


# get all data
deaths = pd.read_csv("deaths.csv")
populations = pd.read_csv("CountyPopulations.csv")
prescriptions = pd.read_csv("prescriptions3")


# In[12]:


prescriptions


# ## FLORIDA

# In[13]:


prescriptions["County"] = prescriptions["BUYER_COUNTY"]
florida = prescriptions[prescriptions.State == "Florida"][
    ["County", "T_DATE", "MME", "State"]
]
flcounties = prescriptions[prescriptions.State == "Florida"]["County"].unique()
missing = []
for j in range(2006, 2015):
    for i in flcounties:
        if i not in [
            l for l in florida[(florida.County == i) & (florida.T_DATE == j)]["County"]
        ]:
            missing.append(
                [i, j, "NA", "Florida"]
            )  # giving NA for the counties with no prescription related info
missing_dataframe = pd.DataFrame(missing, columns=["County", "T_DATE", "MME", "State"])
updated_prescr = pd.concat([florida, missing_dataframe], axis=0)
updated_prescr["Treatment"] = "Treatment"
updated_prescr.groupby(["T_DATE"])[
    "County"
].count()  # double checking that all florida counties are included for each year


# ## Georgia

# In[14]:


Georgia = prescriptions[prescriptions.State == "Georgia"][
    ["County", "T_DATE", "MME", "State"]
].copy()
Georgia_counties = prescriptions[
    (prescriptions.State == "Georgia") & (prescriptions.T_DATE == 2013)
]["BUYER_COUNTY"].unique()
Georgiafinal = Georgia.loc[
    Georgia.County.isin(Georgia_counties),
].copy()
Georgiafinal["Treatment"] = "Control"
Georgia.loc[Georgia.County.isin(Georgia_counties),].groupby("T_DATE")[
    "County"
].count()  # double checking that all georgia counties are included for each year


# ## North Carolina

# In[15]:


NC = prescriptions[prescriptions.State == "North Carolina"][
    ["County", "T_DATE", "MME", "State"]
]
NC_counties = prescriptions[
    (prescriptions.State == "North Carolina") & (prescriptions.T_DATE == 2013)
]["BUYER_COUNTY"].unique()
NCfinal = NC.loc[
    NC.County.isin(NC_counties),
]
NCfinal["Treatment"] = "Control"
NC.loc[NC.County.isin(NC_counties),].groupby("T_DATE")[
    "County"
].count()  # confirm all years have the same counties


# ## Kentucky

# In[16]:


KY = prescriptions[prescriptions.State == "Kentucky"][
    ["County", "T_DATE", "MME", "State"]
]
KY_counties = prescriptions[
    (prescriptions.State == "Kentucky") & (prescriptions.T_DATE == 2013)
]["BUYER_COUNTY"].unique()
KYfinal = KY.loc[
    KY.County.isin(KY_counties),
]
KYfinal["Treatment"] = "Control"
KY.loc[KY.County.isin(KY_counties),].groupby("T_DATE")[
    "County"
].count()  # confirm all years have the same counties


# ## Putting all States together+ population

# In[17]:


all_prescriptions = pd.concat([updated_prescr, KYfinal, Georgiafinal, NCfinal], axis=0)
all_prescriptions.head()


# In[18]:


states = ["Florida", "Georgia", "North Carolina", "Kentucky"]
subset = populations.loc[
    populations.State.isin(states),
].copy()  # only getting population info on those states
subset["County"] = [i.split(" County")[0] for i in subset.County]
all_prescriptions["County"] = (all_prescriptions["County"].str.lower()).str.capitalize()
all_prescriptions["Year"] = all_prescriptions["T_DATE"]  # renaming the column


# In[19]:


rectifying = {
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
p = []
for i in all_prescriptions["County"]:
    if i in rectifying.keys():
        p.append(rectifying[i])
    else:
        p.append(i)
all_prescriptions["County"] = p


# # Dealing with NA data

# In[20]:


prescr_merge = pd.merge(
    all_prescriptions,
    subset,
    on=["County", "Year", "State"],
    how="left",
    indicator=True,
)[["State", "County", "MME", "Population", "Year", "Treatment", "_merge"]]
prescr_merge[prescr_merge["_merge"] != "both"]


# In[21]:


prescr_merge["MME"] = prescr_merge["MME"].replace("NA", np.NaN)
# prescr_merge['MME']=[np.random.randint(0,10) if nfor i in prescr_merge['MME']] #should we just remove this row
prescr_merge["Prescr_rate"] = prescr_merge["MME"] / prescr_merge["Population"]


# In[22]:


prescr_merge[
    prescr_merge.isnull().any(axis=1)
]  # will need to talk about how to deal with these 2 Counties. Not a big deal!


# In[23]:


prescr_pop = prescr_merge.to_csv("Prescription-Pop-merge.csv", index=False)
