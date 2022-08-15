#!/usr/bin/env python
# coding: utf-8

# In[12]:


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
vaccine=pd.read_csv("cowin_vaccine_data_districtwise.csv",low_memory=False)
vaccine_state_week=pd.read_csv("state-vaccinated-count-week.csv",low_memory=False)
vaccine_state_overall=pd.read_csv("state-vaccinated-count-overall.csv",low_memory=False)

vacc_state=list(vaccine_state_week["stateid"])
dosecount_week=list(vaccine_state_week["dose1"])
dosecount_overall=list(vaccine_state_overall["dose1"])
stateid_overall=list(vaccine_state_overall["stateid"])
timeid=list(vaccine_state["timeid"])
state=list(census["Name"])
pop_total=list(census["TOT_P"])
days=((datetime.strptime("14/08/2021","%d/%m/%Y"))-(datetime.strptime("15/03/2020","%d/%m/%Y"))).days+1

state_map={"JK":"JAMMU & KASHMIR","HP":"HIMACHAL PRADESH","PB":"PUNJAB","CH":"CHANDIGARH","UT":"UTTARAKHAND","HR":"HARYANA",
           "RJ":"RAJASTHAN","UP":"UTTAR PRADESH","BR":"BIHAR","SK":"SIKKIM","AR":"ARUNACHAL PRADESH","NL":"NAGALAND",
          "MN":"MANIPUR","MZ":"MIZORAM","TR":"TRIPURA","ML":"MEGHALAYA","AS":"ASSAM","WB":"WEST BENGAL","JH":"JHARKHAND",
          "OR":"ODISHA","CT":"CHHATTISGARH","MP":"MADHYA PRADESH","GJ":"GUJARAT","MH":"MAHARASHTRA",
          "AP":"ANDHRA PRADESH","KA":"KARNATAKA","GA":"GOA","KL":"KERALA","TN":"TAMIL NADU",
           "PY":"PUDUCHERRY","DL":"NCT OF DELHI"}

stateid=[]
leftover=[]
rateofvacc=[]
expectdate=[]
for i in state_map:
    idx=state.index(state_map[i])
    state_pop=pop_total[idx]
    state_idx=[j for j in range(len(vacc_state)) if vacc_state[j]==i]
    state_idx=state_idx[-1]
    state_dos_lastweek=dosecount_week[state_idx]
    stateidx_overall=stateid_overall.index(i)
    state_dos_overall=dosecount_overall[stateidx_overall]
    left=int(state_pop)-state_dos_overall
    rate=(state_dos_lastweek//7)+1
    daysrem=(left//rate)+1
    dateexp=datetime.strptime("14/08/2021","%d/%m/%Y")+timedelta(daysrem)
    dateexp=dateexp.strftime("%d/%m/%Y")
    stateid.append(i)
    leftover.append(left)
    rateofvacc.append(rate)
    expectdate.append(dateexp)
    
df=pd.DataFrame.from_dict({"stateid":stateid, "populationleft":leftover, "rateofvaccination":rateofvacc, "date":expectdate})
df.to_csv("complete-vaccination.csv") #complete-vaccination.csv


# In[ ]:




