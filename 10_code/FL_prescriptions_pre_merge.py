#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
df = pd.read_csv('/Users/clarissaache/Downloads/arcos-fl-statewide-itemized.csv')
df.head


# # Columns
# A "REPORTER" is an entity that purchases drugs, usually distributors and manufacturers
# <br>
# A "BUYER" is an entity receiving shipments from reporter. Like retail and online pharmacies, practicitoners other smaller distributors
# <br>
# **We care about the Buyer columns**

# In[3]:


df.shape
# 15104983 obs, 33 columns
df.columns


# # Which columns do we need??
# I basically just went through the columns related to buyers one by one checking if the information needed to be cleaned

# In[4]:


# Lets get rid of the Reporter columns for now (faster to work with smaller dataset)
cols = ['REPORTER_COUNTY',
       'BUYER_DEA_NO', 'BUYER_BUS_ACT', 'BUYER_NAME', 'BUYER_ADDL_CO_INFO',
       'BUYER_ADDRESS1', 'BUYER_ADDRESS2', 'BUYER_CITY', 'BUYER_STATE',
       'BUYER_ZIP', 'BUYER_COUNTY', 'TRANSACTION_CODE', 'DRUG_CODE', 'NDC_NO',
       'DRUG_NAME', 'QUANTITY', 'UNIT', 'ACTION_INDICATOR', 'ORDER_FORM_NO',
       'CORRECTION_NO', 'STRENGTH', 'TRANSACTION_DATE', 'CALC_BASE_WT_IN_GM',
       'DOSAGE_UNIT', 'TRANSACTION_ID', 'Product_Name', 'Ingredient_Name',
       'Measure', 'MME_Conversion_Factor', 'Combined_Labeler_Name',
       'Reporter_family', 'dos_str', 'MME']
df1 = df[cols]


# # Exploring which columns do we care about
# I looked at the unique values of the columns that we might be interested in or that might require us to do some cleaning before grouping

# In[5]:


df1.DRUG_NAME.unique()
# we only have data for 'OXYCODONE', 'HYDROCODONE'
df1['BUYER_COUNTY'].nunique()
# we have data for 67 counties, which is the amount of counties that exist in FL 
df1['TRANSACTION_CODE'].nunique()
# all transactions are sales (not returns, so we are good here)


# In[6]:


df1['Measure'].nunique
# they are all 'tab' = tablet


# # What should we do about the ACTION INDICATOR column?
# These may be transactions that were modified, deleted, or adjusted, so basically, we cannot trust the data for these observations. Can we?
# There is an important ammount of observations with 'Adjusted' and 'Incert' flags, but only 5 with the 'Delete' flag. Most obs are NaN in this column

# In[7]:


df1[df['ACTION_INDICATOR']== 'I']
# This column is an indication of corrected shipments by reporter. 
# Values include A: adjust, D: Delete or I: insert(late-reporter shipment).


# In[8]:


df1['BUYER_NAME'].nunique()
# there are 9566 different buyers!


# # Subset 
# Now that we know more about the columns we actually care about, I created an even smaller subset

# In[9]:


df2 = df[['BUYER_NAME', 'BUYER_COUNTY',
       'DRUG_NAME', 'QUANTITY', 'UNIT', 'STRENGTH', 'TRANSACTION_DATE', 'CALC_BASE_WT_IN_GM',
       'DOSAGE_UNIT', 'Ingredient_Name','MME_Conversion_Factor', 'dos_str']]
df2.head


# # Clean the columns we need
# Now that we have a smaller subset of the data with the columns we may need, let's see if the data is complete

# In[10]:


df2['BUYER_COUNTY'].isna().sum()
# 16 observations do not have a county
df2['BUYER_COUNTY'] = df['BUYER_COUNTY'].replace(np.nan, 'Unknown')
#replaced with Unknown


# In[11]:


df2['TRANSACTION_DATE'].isna().sum()
# AMAZING
# All transactions have dates, but they are in this weird format


# In[19]:


# changing dates that look like 8252007 to date format
df2['T_DATE'] = pd.to_datetime(df2['TRANSACTION_DATE'], format='%m%d%Y', errors='coerce')
df2['T_DATE']=pd.DatetimeIndex(df2['T_DATE']).year

#Grouping
df_by_county = df2.groupby(['BUYER_COUNTY', 'T_DATE']).sum().reset_index()
df_by_county['MME']=df_by_county['CALC_BASE_WT_IN_GM']/1000*df_by_county['MME_Conversion_Factor']
finalcolumns=['BUYER_COUNTY', 'T_DATE', 'MME']
df_final=df_by_county[finalcolumns]
# Quick sense check: looks like the TRANSACTION DATE and new T DATE columns match!
df2


# did it work alright?
df2['T_DATE'].isnull().any()
# YES!

df_by_county
df_final


