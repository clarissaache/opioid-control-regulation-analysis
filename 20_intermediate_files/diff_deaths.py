# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Difference in Difference Deaths

# %%
import pandas as pd
import numpy as np

Deaths = pd.read_csv(
    "/Users/clarissaache/IDS720/spaceX/pds2021-opioids-team-three/20_intermediate_files/deaths-pop-merge.csv"
)
Deaths


# %%
Deaths.loc[Deaths.State == "Florida", "Treatment"] = "Florida"
Deaths.loc[Deaths.State == "Washington", "Treatment"] = "Washington"
Deaths.loc[Deaths.State == "Texas", "Treatment"] = "Texas"
Deaths.Treatment.value_counts()


# %%
alt.data_transformers.disable_max_rows()


# %%
import altair as alt

base = (
    alt.Chart(Deaths)
    .mark_point(clip=True)
    .encode(
        alt.X("Year", scale=alt.Scale(zero=False)),
        alt.Y("death_prop", scale=alt.Scale(domain=(-0.5, 1.5))),
        color="Treatment:N",
    )
)

base + base.transform_loess("Year", "death_prop", groupby=["Treatment"]).mark_line()


# %%
Deaths_by_state = Deaths.groupby(
    [Deaths["Year"], Deaths["Treatment"]], as_index=False
).mean()
Deaths_by_state


# %%
import altair as alt

base = (
    alt.Chart(Deaths_by_state)
    .mark_point()
    .encode(
        alt.X("Year", scale=alt.Scale(zero=False)),
        alt.Y("death_prop", scale=alt.Scale(zero=False)),
        color="Treatment:N",
    )
)

base + base.transform_loess("Year", "death_prop", groupby=["Treatment"]).mark_line()

# %% [markdown]
# Looks like this aggregation makes the policy makers in Texas and Florida look good.
# Note that the differnces in rates are so very subtil from one year to the next

# %%
# lets try transforming the rate to log_rate
Deaths["log_rate"] = np.log(Deaths["death_prop"])
Deaths


# %%
base = (
    alt.Chart(Deaths)
    .mark_point(clip=True)
    .encode(
        alt.X("Year", scale=alt.Scale(zero=False)),
        alt.Y("log_rate", scale=alt.Scale(domain=(-12, 5))),
        color="Treatment:N",
    )
)

base + base.transform_loess("Year", "log_rate", groupby=["Treatment"]).mark_line()

# THOUGHTS:
# so, in this graph we can see that death rates did not change much after policies went in effect
# however, the explosion of the crisis in 2015 sort of did not affect Florida and Texas the way it did the rest of the states
# (including Washington)


# %%
# SAME PLOT, THIS IS JUST A CLOSEUP VIEW
base = (
    alt.Chart(Deaths)
    .mark_point(clip=True)
    .encode(
        alt.X("Year", scale=alt.Scale(zero=False)),
        alt.Y("log_rate", scale=alt.Scale(domain=(-12, -5))),
        color="Treatment:N",
    )
)

base + base.transform_loess("Year", "log_rate", groupby=["Treatment"]).mark_line()
