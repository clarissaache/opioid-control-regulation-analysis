# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Difference in Difference Prescriptions

# %%
import pandas as pd
import numpy as np

Prescriptions = pd.read_csv(
    "/Users/clarissaache/IDS720/spaceX/pds2021-opioids-team-three/20_intermediate_files/Prescription-Pop-merge.csv"
)
Prescriptions


# %%
import altair as alt

base = (
    alt.Chart(Prescriptions)
    .mark_point(clip=True)
    .encode(
        alt.X("Year", scale=alt.Scale(zero=False)),
        alt.Y("Prescr_rate", scale=alt.Scale(domain=(0, 50000000))),
        color="Treatment:N",
    )
)

base + base.transform_loess("Year", "Prescr_rate", groupby=["Treatment"]).mark_line()

# This is alright (can se an inflection point in 2010)
# but I want to see if by putting transforming makes it look better


# %%
# lets try transforming the rate to log_rate
Prescriptions["log_rate"] = np.log(Prescriptions["Prescr_rate"])
Prescriptions


# %%
import altair as alt

base = (
    alt.Chart(Prescriptions)
    .mark_point(clip=True)
    .encode(
        alt.X("Year", scale=alt.Scale(zero=False)),
        alt.Y("log_rate", scale=alt.Scale(zero=False)),
        color="Treatment:N",
    )
)

base + base.transform_loess("Year", "log_rate", groupby=["Treatment"]).mark_line()


# %%
P_treatment = Prescriptions[Prescriptions.loc[:, "Treatment"] == "Treatment"]
P_control = Prescriptions[Prescriptions.loc[:, "Treatment"] == "Control"]
P_control


# %%
# forget about this... I cant make the two plots into one
