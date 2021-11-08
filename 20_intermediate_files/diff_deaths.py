#!/usr/bin/env python
# coding: utf-8

# # Difference in Difference Deaths

# In[1]:


import pandas as pd
import numpy as np
Deaths = pd.read_csv('deaths-pop-merge.csv')
Deaths


# ## For Florida

# In[2]:


states=['Washington','Texas'] 
Floridadf=Deaths[~Deaths.State.isin(states)] # removing Washington and texas and keeping: Florida vs the rest of the country 
pre_FL=Floridadf[(Floridadf.State=='Florida')&(Floridadf.Year<2010)] # filtering for pre policy years for Florida 
post_FL=Floridadf[(Floridadf.State=='Florida')&(Floridadf.Year>=2010)] #post policy years for Florida
pre_contr=Floridadf[(Floridadf.Treatment=='Control')&(Floridadf.Year<2010)] # pre policy years for all the other control states 
post_contr=Floridadf[(Floridadf.Treatment=='Control')&(Floridadf.Year>=2010)] #post policy years for all the other control states


# In[3]:


from plotnine import *
def diffIndiff(prepolicy_contr,postpolicy_contr,prepolicy_treatment,postpolicy_treatment,xvar,yvar,policyyear):
    m=(
    ggplot()
    # plot all chosen states,  pre policy year
    + geom_smooth(
        prepolicy_contr,
        aes(x=xvar, y=yvar,color="Treatment"),
        method="lm",
    )
    # plot all chosen states, post policy year
    + geom_smooth(
        postpolicy_contr,
        aes(x=xvar, y=yvar,color="Treatment"),
        method="lm",
    )
    # plot treatment, pre policy year
    + geom_smooth(
        prepolicy_treatment,
        aes(x=xvar, y=yvar, color="Treatment"),
        method="lm",
    )
    # plot treatment, post policy year
    + geom_smooth(
        postpolicy_treatment,
        aes(x=xvar, y=yvar, color="Treatment"),
        method="lm",
    )
    + geom_vline(xintercept=policyyear, linetype="dotted")
    + xlab("Year")
    + ylab("Mortality rate")
    + theme_classic(base_family="Times")
    + scale_x_continuous(breaks=[2006, 2008, 2010, 2012,2014], limits=[2006, 2014])
    )
    return m


# In[5]:


m=diffIndiff(pre_contr,post_contr,pre_FL,post_FL,'Year','death_prop',2010)+ labs(title="Mortality rate for Florida vs. Other States", color="State")
#ggsave(plot=m,filename='Mortality-rate-FL.png')
m


# # Washington

# In[6]:


states=['Florida','Texas']
Wadf=Deaths[~Deaths.State.isin(states)] # removing Florida and texas and keeping Washington vs the rest of the country 
pre_Wa=Wadf[(Wadf.State=='Washington')&(Wadf.Year<2012)]
post_Wa=Wadf[(Wadf.State=='Washington')&(Wadf.Year>=2012)]
pre_contr=Wadf[(Wadf.Treatment=='Control')&(Wadf.Year<2012)]
post_contr=Wadf[(Wadf.Treatment=='Control')&(Wadf.Year>=2012)]


# In[7]:


m=diffIndiff(pre_contr,post_contr,pre_Wa,post_Wa,'Year','death_prop',2012)+ labs(title="Mortality rate for Washington vs. Other States", color="Treatment")
#ggsave(plot=m,filename='Mortality-rate-Wa.png')
m


# ## Texas

# In[8]:


states=['Florida','Washington']
Txdf=Deaths[~Deaths.State.isin(states)] # removing Florida and Washington and keeping Washington vs the rest of the country 
pre_Tx=Txdf[(Txdf.State=='Texas')&(Txdf.Year<2007)]
post_Tx=Txdf[(Txdf.State=='Texas')&(Txdf.Year>=2007)]
pre_contr=Txdf[(Txdf.Treatment=='Control')&(Txdf.Year<2007)]
post_contr=Txdf[(Txdf.Treatment=='Control')&(Txdf.Year>=2007)]


# In[9]:


m=diffIndiff(pre_contr,post_contr,pre_Tx,post_Tx,'Year','death_prop',2007)+ labs(title="Mortality rate for Texas vs. Other States", color="Treatment")
#ggsave(plot=m,filename='Mortality-rate-Tx.png') #saves it as a png 
m

