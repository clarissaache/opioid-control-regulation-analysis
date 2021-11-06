# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np

# %% [markdown]
# # GEORGIA

# %%
df = pd.read_csv("/Users/clarissaache/Downloads/arcos-ga-statewide-itemized.csv")

# df['BUYER_COUNTY'] = df['BUYER_COUNTY'].replace(np.nan, 'Unknown')
# replaced with Unknown

# df['BUYER_COUNTY']=np.where(df['BUYER_ADDRESS1']=='1000 FIRST AVE NE', 'GRADY')
# df['BUYER_COUNTY']=df['BUYER_COUNTY'].fillna('GRADY')


# %%
# fixing unknowns
df[df["BUYER_COUNTY"].isna()][
    [
        "BUYER_ADDRESS1",
        "BUYER_ADDRESS2",
        "BUYER_CITY",
        "BUYER_STATE",
        "BUYER_ZIP",
        "BUYER_COUNTY",
    ]
]


# %%
df["BUYER_COUNTY"] = df["BUYER_COUNTY"].replace(np.nan, "GRADY")

df[df["BUYER_COUNTY"].isna()][
    [
        "BUYER_ADDRESS1",
        "BUYER_ADDRESS2",
        "BUYER_CITY",
        "BUYER_STATE",
        "BUYER_ZIP",
        "BUYER_COUNTY",
    ]
]


# %%
df["T_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format="%m%d%Y", errors="coerce")
df["T_DATE"] = pd.DatetimeIndex(df["T_DATE"]).year
df_by_county = df.groupby(["BUYER_COUNTY", "T_DATE"]).sum().reset_index()
df_by_county["MME"] = (
    df_by_county["CALC_BASE_WT_IN_GM"] * 1000 * df_by_county["MME_Conversion_Factor"]
)

finalcolumns = ["BUYER_COUNTY", "T_DATE", "MME"]
df_final_GA = df_by_county[finalcolumns].copy()


# %%
df_final_GA["State"] = "Georgia"
df_final_GA


# %%
df_final_GA.isna().any()

# %% [markdown]
# # North Carolina

# %%
df2 = pd.read_csv("/Users/clarissaache/Downloads/arcos-nc-statewide-itemized.csv")


# %%
# fixing unknowns: googling address to find out which County they are in
df2[df2["BUYER_COUNTY"].isna()][
    [
        "BUYER_ADDRESS1",
        "BUYER_ADDRESS2",
        "BUYER_CITY",
        "BUYER_STATE",
        "BUYER_ZIP",
        "BUYER_COUNTY",
    ]
]
# no unknowns!!


# %%
df2["T_DATE"] = pd.to_datetime(
    df2["TRANSACTION_DATE"], format="%m%d%Y", errors="coerce"
)
df2["T_DATE"] = pd.DatetimeIndex(df2["T_DATE"]).year
df_by_county = df2.groupby(["BUYER_COUNTY", "T_DATE"]).sum().reset_index()
df_by_county["MME"] = (
    df_by_county["CALC_BASE_WT_IN_GM"] * 1000 * df_by_county["MME_Conversion_Factor"]
)
finalcolumns = ["BUYER_COUNTY", "T_DATE", "MME"]
df_final_NC = df_by_county[finalcolumns].copy()
# Quick sense check: looks like the TRANSACTION DATE and new T DATE columns match!


# %%
df_final_NC["State"] = "North Carolina"
df_final_NC


# %%
df_final_NC.isna().any()

# %% [markdown]
# # Kentucky

# %%
df3 = pd.read_csv("/Users/clarissaache/Downloads/arcos-ky-statewide-itemized.csv")


# %%
# fixing unknowns: googling address to find out which County they are in
df3[df3["BUYER_COUNTY"].isna()]
# no unknowuns!


# %%
df3["T_DATE"] = pd.to_datetime(
    df3["TRANSACTION_DATE"], format="%m%d%Y", errors="coerce"
)
df3["T_DATE"] = pd.DatetimeIndex(df3["T_DATE"]).year
df_by_county = df3.groupby(["BUYER_COUNTY", "T_DATE"]).sum().reset_index()
df_by_county["MME"] = (
    df_by_county["CALC_BASE_WT_IN_GM"] * 1000 * df_by_county["MME_Conversion_Factor"]
)
finalcolumns = ["BUYER_COUNTY", "T_DATE", "MME"]
df_final_KY = df_by_county[finalcolumns].copy()
# Quick sense check: looks like the TRANSACTION DATE and new T DATE columns match!


# %%
df_final_KY["State"] = "Kentucky"
df_final_KY


# %%
df_final_KY.isna().any()

# %% [markdown]
# # Florida

# %%
df4 = pd.read_csv("/Users/clarissaache/Downloads/arcos-fl-statewide-itemized.csv")


# %%
# which counties are unknown
df4[df4["BUYER_COUNTY"].isna()][
    [
        "BUYER_ADDRESS1",
        "BUYER_ADDRESS2",
        "BUYER_CITY",
        "BUYER_STATE",
        "BUYER_ZIP",
        "BUYER_COUNTY",
    ]
]


# %%
# fix unknowns
df4["BUYER_COUNTY"] = df4["BUYER_COUNTY"].replace(np.nan, "PINELLAS")


# %%
df4[df4["BUYER_COUNTY"].isna()][
    [
        "BUYER_ADDRESS1",
        "BUYER_ADDRESS2",
        "BUYER_CITY",
        "BUYER_STATE",
        "BUYER_ZIP",
        "BUYER_COUNTY",
    ]
]


# %%
df4["T_DATE"] = pd.to_datetime(
    df4["TRANSACTION_DATE"], format="%m%d%Y", errors="coerce"
)
df4["T_DATE"] = pd.DatetimeIndex(df4["T_DATE"]).year
df_by_county = df4.groupby(["BUYER_COUNTY", "T_DATE"]).sum().reset_index()
df_by_county["MME"] = (
    df_by_county["CALC_BASE_WT_IN_GM"] * 1000 * df_by_county["MME_Conversion_Factor"]
)

finalcolumns = ["BUYER_COUNTY", "T_DATE", "MME"]
df_final_FL = df_by_county[finalcolumns].copy()
df_final_FL["State"] = "Florida"
df_final_FL


# %%
df_final_FL.isna().any()


# %%
prescriptions2 = pd.concat((df_final_FL, df_final_GA, df_final_NC, df_final_KY), axis=0)


# %%
prescriptions2


# %%
prescriptions2.isna().any()


# %%
prescriptions2.to_csv(
    "/Users/clarissaache/IDS720/spaceX/pds2021-opioids-team-three/20_intermediate/prescriptions3"
)
