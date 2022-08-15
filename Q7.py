#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime,timedelta, date
from dateutil.relativedelta import relativedelta

f=open("neighbor-districts-modified.json")
Dist=json.load(f)

vaccine=pd.read_csv("cowin_vaccine_data_districtwise.csv")

vacc_dist=list(vaccine["District_Key"])
covax=list(vaccine["14/08/2021.8"])
covax=covax[1:]
shield=list(vaccine["14/08/2021.9"])
shield=shield[1:]

vaccine_ratio_dist={"districtid":[], "vaccineratio":[]}
vaccine_ratio_distx={"districtid":[], "vaccineratio":[]}
dist_id=[]
vacc_ratio=[]
dist_idx=[]
vacc_ratiox=[]

for i in Dist:
    idx=[j for j in range(len(vacc_dist)) if vacc_dist[j]==i]
    shieldn=shield[idx[0]-1]
    covaxn=covax[idx[0]-1]
    if(int(covaxn)==0):
        dist_idx.append(i)
        vacc_ratiox.append("NA")
    else:
        rat=int(shieldn)/int(covaxn)
        dist_id.append(i)
        vacc_ratio.append(rat)
    
vaccine_ratio_dist["districtid"]=dist_id
vaccine_ratio_dist["vaccineratio"]=vacc_ratio

vaccine_ratio_distx["districtid"]=dist_idx
vaccine_ratio_distx["vaccineratio"]=vacc_ratiox

df1=pd.DataFrame.from_dict(vaccine_ratio_dist)
df1.sort_values(by="vaccineratio",inplace=True)

df2=pd.DataFrame.from_dict(vaccine_ratio_distx)
df=pd.concat([df1,df2],axis=0,ignore_index=True)
df.to_csv("vaccine-type-ratio-district.csv") #vaccine-type-ratio-district.csv


# In[4]:


vacc_dist=vacc_dist[1:]
State=[]
for i in Dist:
    if i[:2] not in State:
        State.append(i[:2])
stateid=[]
covax_state=[]
shield_state=[]
vacc_ratio=[]
stateidx=[]
vacc_ratiox=[]
for i in State:
    idx=[j for j in range(len(vacc_dist)) if vacc_dist[j][:2]==i]
    covax_tot=0
    shield_tot=0
    for j in idx:
        covax_tot+=int(covax[j])
        shield_tot+=int(shield[j])
    covax_state.append(covax_tot)
    shield_state.append(shield_tot)
    if(covax_tot==0):
        stateidx.append(i)
        vacc_ratiox.append("NA")
    else:
        ratio=shield_tot/covax_tot
        stateid.append(i)
        vacc_ratio.append(ratio)
    
df1=pd.DataFrame.from_dict({"stateid":stateid, "vaccineratio":vacc_ratio})
df1.sort_values(by="vaccineratio",inplace=True)
df2=pd.DataFrame.from_dict({"stateid":stateidx, "vaccineratio":vacc_ratiox})
df=pd.concat([df1,df2],axis=0,ignore_index=True)
df.to_csv("vaccine-type-ratio-state.csv") #vaccine-type-ratio-state.csv


# In[5]:


covax_overall=0
shield_overall=0
for i in range(len(covax_state)):
    covax_overall+=covax_state[i]
    shield_overall+=shield_state[i]
    
ratio_overall=shield_overall/covax_overall
df=pd.DataFrame.from_dict({"id":["overall"], "vaccineratio":[ratio_overall]})
df.sort_values(by="vaccineratio",inplace=True)
df.to_csv("vaccine-type-ratio-overall.csv") #vaccine-type-ratio-overall.csv


# In[ ]:




