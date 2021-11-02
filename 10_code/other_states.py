#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np


# # GEORGIA

# In[4]:


df = pd.read_csv('/Users/clarissaache/Downloads/arcos-ga-statewide-itemized.csv')
df['BUYER_COUNTY'] = df['BUYER_COUNTY'].replace(np.nan, 'Unknown')
#replaced with Unknown


# In[6]:


df['T_DATE'] = pd.to_datetime(df['TRANSACTION_DATE'], format='%m%d%Y', errors='coerce')
df['T_DATE']=pd.DatetimeIndex(df['T_DATE']).year
df_by_county = df.groupby(['BUYER_COUNTY', 'T_DATE']).sum().reset_index()
df_by_county['MME']=df_by_county['CALC_BASE_WT_IN_GM']*1000*df_by_county['MME_Conversion_Factor']
finalcolumns=['BUYER_COUNTY', 'T_DATE', 'MME']
df_final_GA=df_by_county[finalcolumns]
# Quick sense check: looks like the TRANSACTION DATE and new T DATE columns match!
df


# In[9]:


df_final_GA["State"]='Georgia'


# # North Carolina

# In[10]:


df2 = pd.read_csv('/Users/clarissaache/Downloads/arcos-nc-statewide-itemized.csv')
df2['BUYER_COUNTY'] = df2['BUYER_COUNTY'].replace(np.nan, 'Unknown')
#replaced with Unknown
df2['T_DATE'] = pd.to_datetime(df2['TRANSACTION_DATE'], format='%m%d%Y', errors='coerce')
df2['T_DATE']=pd.DatetimeIndex(df2['T_DATE']).year
df_by_county = df2.groupby(['BUYER_COUNTY', 'T_DATE']).sum().reset_index()
df_by_county['MME']=df_by_county['CALC_BASE_WT_IN_GM']*1000*df_by_county['MME_Conversion_Factor']
finalcolumns=['BUYER_COUNTY', 'T_DATE', 'MME']
df_final_NC=df_by_county[finalcolumns]
# Quick sense check: looks like the TRANSACTION DATE and new T DATE columns match!
df2


# In[13]:


df_final_NC["State"]='North Carolina'
df_final_NC


# # Kentucky

# In[14]:


df2 = pd.read_csv('/Users/clarissaache/Downloads/arcos-ky-statewide-itemized.csv')
df2['BUYER_COUNTY'] = df2['BUYER_COUNTY'].replace(np.nan, 'Unknown')
#replaced with Unknown
df2['T_DATE'] = pd.to_datetime(df2['TRANSACTION_DATE'], format='%m%d%Y', errors='coerce')
df2['T_DATE']=pd.DatetimeIndex(df2['T_DATE']).year
df_by_county = df2.groupby(['BUYER_COUNTY', 'T_DATE']).sum().reset_index()
df_by_county['MME']=df_by_county['CALC_BASE_WT_IN_GM']*1000*df_by_county['MME_Conversion_Factor']
finalcolumns=['BUYER_COUNTY', 'T_DATE', 'MME']
df_final_KY=df_by_county[finalcolumns]
# Quick sense check: looks like the TRANSACTION DATE and new T DATE columns match!
df2


# In[15]:


df_final_KY["State"]='Kentucky'
df_final_KY


# # Florida

# In[17]:


df2 = pd.read_csv('/Users/clarissaache/Downloads/arcos-fl-statewide-itemized.csv')
df2['BUYER_COUNTY'] = df2['BUYER_COUNTY'].replace(np.nan, 'Unknown')
#replaced with Unknown
df2['T_DATE'] = pd.to_datetime(df2['TRANSACTION_DATE'], format='%m%d%Y', errors='coerce')
df2['T_DATE']=pd.DatetimeIndex(df2['T_DATE']).year
df_by_county = df2.groupby(['BUYER_COUNTY', 'T_DATE']).sum().reset_index()
df_by_county['MME']=df_by_county['CALC_BASE_WT_IN_GM']*1000*df_by_county['MME_Conversion_Factor']
finalcolumns=['BUYER_COUNTY', 'T_DATE', 'MME']
df_final_FL=df_by_county[finalcolumns]
df_final_FL["State"]='Florida'
df_final_FL


# In[23]:


prescriptions = pd.concat((df_final_FL, df_final_GA, df_final_NC, df_final_KY), axis=0)


# In[24]:


prescriptions


# In[27]:


prescriptions.to_csv('/Users/clarissaache/IDS720/pds2021-opioids-team-three/20_intermediate/prescriptions')

