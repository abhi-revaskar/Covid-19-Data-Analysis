#!/usr/bin/env python
# coding: utf-8

# In[16]:


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
vaccine_state=pd.read_csv("state-vaccinated-count-overall.csv")

vacc_dist=list(vaccine["District_Key"])
dos1=list(vaccine["14/08/2021.3"])
dos1=dos1[1:]
dos2=list(vaccine["14/08/2021.4"])
dos2=dos2[1:]
pop_dist=list(census["Name"])
pop_total=list(census["TOT_P"])

distid=[]
dos1ratio=[]
dos2ratio=[]
for i in Dist:
    dist=i[3:]
    if dist not in pop_dist:
        continue
    idx=[j for j in range(len(pop_dist)) if pop_dist[j]==dist]
    dist_pop=pop_total[idx[0]]
    dist_idx=vacc_dist.index(i)
    dos1_tot=dos1[dist_idx-1]
    dos2_tot=dos2[dist_idx-1]
    distid.append(i)
    dos1ratio.append(int(dos1_tot)/int(dist_pop))
    dos2ratio.append(int(dos2_tot)/int(dist_pop))
    
df=pd.DataFrame.from_dict({"districtid":distid, "vaccinateddose1ratio":dos1ratio, "vaccinateddose2ratio":dos2ratio})
df.sort_values(by="vaccinateddose1ratio",inplace=True)
df.to_csv("vaccinated-dose-ratio-district.csv") #vaccinated-dose-ratio-district.csv


# In[22]:


state_map={"JK":"JAMMU & KASHMIR","HP":"HIMACHAL PRADESH","PB":"PUNJAB","CH":"CHANDIGARH","UT":"UTTARAKHAND","HR":"HARYANA",
           "RJ":"RAJASTHAN","UP":"UTTAR PRADESH","BR":"BIHAR","SK":"SIKKIM","AR":"ARUNACHAL PRADESH","NL":"NAGALAND",
          "MN":"MANIPUR","MZ":"MIZORAM","TR":"TRIPURA","ML":"MEGHALAYA","AS":"ASSAM","WB":"WEST BENGAL","JH":"JHARKHAND",
          "OR":"ODISHA","CT":"CHHATTISGARH","MP":"MADHYA PRADESH","GJ":"GUJARAT","MH":"MAHARASHTRA",
          "AP":"ANDHRA PRADESH","KA":"KARNATAKA","GA":"GOA","KL":"KERALA","TN":"TAMIL NADU",
           "PY":"PUDUCHERRY","DL":"NCT OF DELHI"}

vacc_state=list(vaccine_state["stateid"])
dos1=list(vaccine_state["dose1"])
dos2=list(vaccine_state["dose2"])
pop_state=list(census["Name"])
pop_total=list(census["TOT_P"])

stateid=[]
dose1ratio=[]
dose2ratio=[]
for i in range(len(vacc_state)):
    if vacc_state[i] not in state_map:
        continue
    state_idx=pop_state.index(state_map[vacc_state[i]])
    state_pop=pop_total[state_idx]
    stateid.append(vacc_state[i])
    dose1ratio.append(int(dos1[i])/int(state_pop))
    dose2ratio.append(int(dos2[i])/int(state_pop))
    
df=pd.DataFrame.from_dict({"stateid":stateid, "vaccinateddose1ratio":dose1ratio, "vaccinateddose2ratio":dose2ratio})
df.sort_values(by="vaccinateddose1ratio",inplace=True)
df.to_csv("vaccinated-dose-ratio-state.csv") #vaccinated-dose-ratio-state.csv


# In[23]:


dose1_tot=0
dose2_tot=0
for i in range(len(vacc_state)):
    dose1_tot+=int(dos1[i])
    dose2_tot+=int(dos2[i])
idx=pop_state.index("India")
total_pop=pop_total[idx]
dos1ratio=dose1_tot/total_pop
dos2ratio=dose2_tot/total_pop

df=pd.DataFrame.from_dict({"id":["overall"], "vaccinateddose1ratio":[dos1ratio], "vaccinateddose2ratio":[dos2ratio]})
df.sort_values(by="vaccinateddose1ratio",inplace=True)
df.to_csv("vaccinated-dose-ratio-overall.csv") #vaccinated-dose-ratio-overall.csv


# In[ ]:




