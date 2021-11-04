#!/usr/bin/env python
# coding: utf-8

# ### Merging data **by Larissa**
# Here we will merge the following cleaned datasets:
# - prescription from Florida, Kenntucky, North Carolina,
# - death data from all states
# - census data from all states
#
# ---

# Import first dataset containing prescription data

# In[28]:


import pandas as pd

df_prescriptions = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-three/main/20_intermediate/prescriptions?token=AI3GZDZGWG25Z2T5V2RXQGDBRO3WS",
    index_col=0,
)
df_prescriptions.head()


# Renaming the column T_DATE to have it the same everywhere:

# In[29]:


df_prescriptions = df_prescriptions.rename(
    {"T_DATE": "Year", "BUYER_COUNTY": "County"}, axis=1
)


# Changing the values in County to be capitalized and lowercase to be the same as in the other dataframes:

# In[30]:


df_prescriptions["County"] = df_prescriptions["County"].str.lower()
df_prescriptions["County"] = df_prescriptions["County"].str.capitalize()
df_prescriptions.head()


# Checking missing data

# In[31]:


df_prescriptions.isna().sum()


# Importing thr second dataset containing the death data

# In[32]:


df_deaths = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-three/main/20_intermediate_files/deaths.csv?token=AI3GZD6NJFVWRHJMICW5FSTBRO4Z2"
)
df_deaths.head()


# Changing the datatype of Year from float to int to have the same data format for Year in all dataframes

# In[33]:


df_deaths["Year"] = df_deaths["Year"].astype("int64")
df_deaths.head()


# Checking missing data

# In[34]:


df_deaths.isna().sum()


# Importing the third datasset containing census data

# In[36]:


df_census = pd.read_csv(
    "https://raw.githubusercontent.com/MIDS-at-Duke/pds2021-opioids-team-three/main/MidSemester/20_intermediates/CountyPopulations.csv?token=AI3GZD36R6FVBM277DEVPB3BRRDSC",
    index_col=0,
)
df_census.head()


# Checking missing data

# In[37]:


df_census.isna().sum()


# ### Next step merging
# I willbe merging all three datasets into one via a left join on prescription because that is the table where we want all the rows from
#
# ---

# Because we have multiple dataframes and not only 2 we can't just simply merge. First, we create a list with our three dataframes.

# In[46]:


# compile  list of dataframes we want to merge
data_frames = [df_prescriptions, df_deaths, df_census]


# Function merging the three dataframes, outer join to not loose any data. Merging on County, Year, State  which can be found in every of the three datasets.

# In[54]:


from functools import reduce

df_merged = reduce(
    lambda left, right: pd.merge(
        left, right, on=["County", "Year", "State"], how="outer", validate="one_to_one"
    ),
    data_frames,
)


# Looking at the merged data, and the missing data.

# In[58]:


df_merged.head()
df_merged.isna().sum()


# In[49]:


df_merged.describe()


# Creating a csv file in case we need that

# In[52]:


pd.DataFrame.to_csv(df_merged, "merged_data.csv", sep=",", na_rep=".", index=False)
