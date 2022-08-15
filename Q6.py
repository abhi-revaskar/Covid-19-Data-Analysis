#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime,timedelta, date
from dateutil.relativedelta import relativedelta

f=open("neighbor-districts-modified.json")
Dist=json.load(f)

census=pd.read_excel("DDW_PCA0000_2011_Indiastatedist.xlsx")
vaccine=pd.read_csv("cowin_vaccine_data_districtwise.csv")

vacc_dist=list(vaccine["District_Key"])
mdos=list(vaccine["14/08/2021.5"])
mdos=mdos[1:]
fdos=list(vaccine["14/08/2021.6"])
fdos=fdos[1:]
pop_dist=list(census["Name"])
tru=list(census["TRU"])
pop_fem=list(census["TOT_F"])
pop_male=list(census["TOT_M"])

vaccine_ratio_dist={"districtid":[],"ratio":[]}
dist_id=[]
vacc_ratio=[]

for i in Dist:
    idx=[j for j in range(len(vacc_dist)) if vacc_dist[j]==i]
    dist_id.append(i)
    femdos=fdos[idx[0]-1]
    maledos=mdos[idx[0]-1]
    rat=int(femdos)/int(maledos)
    vacc_ratio.append(rat)
    
vaccine_ratio_dist["districtid"]=dist_id
vaccine_ratio_dist["ratio"]=vacc_ratio

popul_ratio_dist={"districtid":[],"ratio":[]}
dist_id=[]
pop_ratio=[]

for i in Dist:
    dist=i[3:]
    if dist not in pop_dist:
        continue
    idx=[j for j in range(len(pop_dist)) if pop_dist[j]==dist]
    dist_id.append(i)
    males=pop_male[idx[0]]
    females=pop_fem[idx[0]]
    rat=int(females)/int(males)
    pop_ratio.append(rat)
    
popul_ratio_dist["districtid"]=dist_id
popul_ratio_dist["ratio"]=pop_ratio


# In[7]:


vaccine_popul_ratio={"districtid":[], "vaccinationratio":[], "populationratio":[], "ratioofratios":[]}

distid=[]
vacc_ratio_val=[]
popul_ratio_val=[]
tot_ratio=[]

vacc_dist=list(vaccine_ratio_dist["districtid"])
vacc_ratio=list(vaccine_ratio_dist["ratio"])
pop_ratio=list(popul_ratio_dist["ratio"])
dist_id=list(popul_ratio_dist["districtid"])

for i in range(len(dist_id)):
    dist=dist_id[i]
    idx=vacc_dist.index(dist)
    distid.append(dist)
    ratio=vacc_ratio[idx]/pop_ratio[i]
    vacc_ratio_val.append(vacc_ratio[idx])
    popul_ratio_val.append(pop_ratio[i])
    tot_ratio.append(ratio)
    
vaccine_popul_ratio["districtid"]=distid
vaccine_popul_ratio["vaccinationratio"]=vacc_ratio_val
vaccine_popul_ratio["populationratio"]=popul_ratio_val
vaccine_popul_ratio["ratioofratios"]=tot_ratio
    
df=pd.DataFrame.from_dict(vaccine_popul_ratio)
df.sort_values(by="ratioofratios",inplace=True)
df.to_csv("vaccination-population-ratio-district.csv") #vaccination-population-ratio-district.csv


# In[17]:


state_map={"JK":"JAMMU & KASHMIR","HP":"HIMACHAL PRADESH","PB":"PUNJAB","CH":"CHANDIGARH","UT":"UTTARAKHAND","HR":"HARYANA",
           "RJ":"RAJASTHAN","UP":"UTTAR PRADESH","BR":"BIHAR","SK":"SIKKIM","AR":"ARUNACHAL PRADESH","NL":"NAGALAND",
          "MN":"MANIPUR","MZ":"MIZORAM","TR":"TRIPURA","ML":"MEGHALAYA","AS":"ASSAM","WB":"WEST BENGAL","JH":"JHARKHAND",
          "OR":"ODISHA","CT":"CHHATTISGARH","MP":"MADHYA PRADESH","GJ":"GUJARAT","MH":"MAHARASHTRA","DN":"DAMAN & DIU",
          "AP":"ANDHRA PRADESH","KA":"KARNATAKA","GA":"GOA","KL":"KERALA","TN":"TAMIL NADU",
           "PY":"PUDUCHERRY","DL":"NCT OF DELHI"}

vacc_dist=list(vaccine["District_Key"])

vaccine_ratio_state={"stateid":[],"females":[],"males":[],"ratio":[]}
state_id=[]
vacc_ratio=[]
fem_vacc=[]
male_vacc=[]
dist_id=list(vaccine_popul_ratio["districtid"])

for i in state_map:
    idx=[j for j in range(len(dist_id)) if dist_id[j][:2]==i]
    dist_list=[]
    for j in idx:
        dist_list.append(dist_id[j])
    males=0
    females=0
    if len(dist_list)==0:
        continue
    for j in dist_list:
        distidx=vacc_dist.index(j)
        males+=int(mdos[distidx-1])
        females+=int(fdos[distidx-1])
    state_id.append(i)
    male_vacc.append(males)
    fem_vacc.append(females)
    ratio=females/males
    vacc_ratio.append(ratio)
    
vaccine_ratio_state["stateid"]=state_id
vaccine_ratio_state["ratio"]=vacc_ratio
vaccine_ratio_state["male"]=male_vacc
vaccine_ratio_state["female"]=fem_vacc

popul_ratio_state={"stateid":[],"ratio":[]}
state_id=[]
pop_ratio=[]
pop_state=list(census["Name"])

for i in state_map:
    idx=[j for j in range(len(pop_state)) if pop_state[j]==state_map[i]]
    males=pop_male[idx[0]]
    females=pop_fem[idx[0]]
    ratio=females/males
    state_id.append(i)
    pop_ratio.append(ratio)
    
popul_ratio_state["stateid"]=state_id
popul_ratio_state["ratio"]=pop_ratio


# In[19]:


vaccine_popul_ratio_state={"stateid":[], "vaccinationratio":[], "populationratio":[], "ratioofratios":[]}

stateid=[]
vacc_ratio_val=[]
popul_ratio_val=[]
tot_ratio=[]

vacc_state=list(vaccine_ratio_state["stateid"])
vacc_ratio=list(vaccine_ratio_state["ratio"])
pop_ratio=list(popul_ratio_state["ratio"])
state_id=list(popul_ratio_state["stateid"])

for i in range(len(state_id)):
    state=state_id[i]
    if(state not in vacc_state):
        continue
    idx=vacc_state.index(state)
    stateid.append(state)
    ratio=vacc_ratio[idx]/pop_ratio[i]
    vacc_ratio_val.append(vacc_ratio[idx])
    popul_ratio_val.append(pop_ratio[i])
    tot_ratio.append(ratio)
    

df=pd.DataFrame.from_dict({"stateid":stateid, "vaccinationratio":vacc_ratio_val, "populationratio":popul_ratio_val, "ratioofratios":tot_ratio})
df.sort_values(by="ratioofratios",inplace=True)
df.to_csv("vaccination-population-ratio-state.csv") #vaccination-population-ratio-state.csv


# In[10]:


male_vacc=list(vaccine_ratio_state["male"])
female_vacc=list(vaccine_ratio_state["female"])
states=list(vaccine_ratio_state["stateid"])

vacc_males=0
vacc_females=0
for i in stateid:
    idx=states.index(i)
    vacc_males+=male_vacc[idx]
    vacc_females+=female_vacc[idx]
    
overall_vacc_ratio=vacc_females/vacc_males

idx=pop_state.index("India")
overall_pop_ratio=pop_fem[idx]/pop_male[idx]

overall_tot_ratio=overall_vacc_ratio/overall_pop_ratio

df=pd.DataFrame.from_dict({"id":["overall"], "vaccinationratio":[overall_vacc_ratio], "populationratio":[overall_pop_ratio], "ratioofratios":[overall_tot_ratio]})
df.to_csv("vaccination-population-ratio-overall.csv") #vaccination-population-ratio-overall.csv


# In[ ]:




