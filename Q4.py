#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime,timedelta, date

f=open("neighbor-districts-modified.json")
neighb_dist=json.load(f)

cases=pd.read_csv("districts.csv")

dist_list=list(cases["District"])
confirmed=list(cases["Confirmed"])
date=list(cases["Date"])
week_wise1=pd.read_csv("cases-week.csv")
cases1=week_wise1["cases"]
week_wise2={"districtid":[],"timeid":[], "cases":[]}

districtid_val=[]
timeid_val=[]
cases_val=[]

start_dt="2020-03-19"
end_dt="2021-08-11"
start_dt=datetime.strptime(start_dt,"%Y-%m-%d")
end_dt=datetime.strptime(end_dt,"%Y-%m-%d")
date_list={}
date_list[start_dt.strftime("%Y-%m-%d")]=0
for i in range(6,int((end_dt-start_dt).days)+1,7):
    dt=start_dt+timedelta(i)
    date_list[dt.strftime("%Y-%m-%d")]=0
    dt=start_dt+timedelta(i+1)
    if dt.strftime("%Y-%m-%d")=="2021-08-12":
        break
    date_list[dt.strftime("%Y-%m-%d")]=0
    
for i in neighb_dist:
    wkid=0
    dist=i[3:]
    if dist not in dist_list:
        continue
    idx=[j for j in range(len(dist_list)) if dist_list[j]==dist]
    d_list=date_list
    for k in idx:
        if date[k] in d_list:
            d_list[date[k]]=confirmed[k]
    date_cases=[]
    for d in d_list:
        date_cases.append(d_list[d])
    week_cases=[]
    for n in range(0,len(date_cases),2):
        week_cases.append(date_cases[n+1]-date_cases[n])
    for w in week_cases:
        districtid_val.append(i)
        wkid+=1
        timeid_val.append("week"+str(wkid))
        cases_val.append(w)
        
week_wise2["districtid"]=districtid_val
week_wise2["timeid"]=timeid_val
week_wise2["cases"]=cases_val

#merging two week values

week_wise={"districtid":[],"timeid":[], "cases":[]}

districtid_val=[]
timeid_val=[]
cases_val=[]


cases2=week_wise2["cases"]
distid1=week_wise1["districtid"]
distid2=week_wise2["districtid"]

for k in neighb_dist:
    wkid=0
    idx1=[j for j in range(len(distid1)) if distid1[j]==k]
    idx2=[j for j in range(len(distid2)) if distid2[j]==k]
    i1,i2=0,0
    while(i1 < len(idx1) and i2< len(idx2)):
        districtid_val.append(k)
        wkid+=1
        timeid_val.append("week"+str(wkid))
        cases_val.append(cases1[idx1[i1]])
        districtid_val.append(k)
        wkid+=1
        timeid_val.append("week"+str(wkid))
        cases_val.append(cases2[idx2[i2]])
        i1+=1
        i2+=1
    if(i1<len(idx1)):
        districtid_val.append(k)
        wkid+=1
        timeid_val.append("week"+str(wkid))
        cases_val.append(cases1[idx1[i1]])

week_wise["districtid"]=districtid_val
week_wise["timeid"]=timeid_val
week_wise["cases"]=cases_val
        


# In[30]:


month_wise=pd.read_csv("cases-month.csv")

district_peaks={"districtid":[],"wave1-weekid":[], "wave2-weekid":[], "wave1-monthid":[], "wave2-monthid":[]}

week_ids=list(week_wise["timeid"])
mon_ids=list(month_wise["timeid"])
week_cases=list(week_wise["cases"])
mon_cases=list(month_wise["cases"])
distid_val=[]
w1wkid_val=[]
w2wkid_val=[]
w1monid_val=[]
w2monid_val=[]

wkdistid=list(week_wise["districtid"])
mndistid=list(month_wise["districtid"])

for i in neighb_dist:
    w1_wk_cases=0
    w1_wkid='week40'
    w2_wk_cases=0
    w2_wkid='week120'
    w1_mn_cases=0
    w1_mnid='month5'
    w2_mn_cases=0
    w2_mnid='month14'
    if(i not in wkdistid):
        continue
    wkidx=[j for j in range(len(wkdistid)) if wkdistid[j]==i]
    mnidx=[j for j in range(len(mndistid)) if mndistid[j]==i]
    for j in wkidx:
        week_id=week_ids[j]
        if(int(week_id[4:])<82): #wave 1 week id
            if(week_cases[j]>w1_wk_cases):
                w1_wk_cases=week_cases[j]
                w1_wkid=week_ids[j]
        else:                     #wave 2 week id
            if(week_cases[j]>w2_wk_cases):
                w2_wk_cases=week_cases[j] 
                w2_wkid=week_ids[j]
    distid_val.append(i)
    w1wkid_val.append(w1_wkid)
    w2wkid_val.append(w2_wkid)
    
    for j in mnidx:
        mon_id=mon_ids[j]
        if(int(mon_id[5:])<9): #wave 1 month id
            if(mon_cases[j]>w1_mn_cases):
                w1_mn_cases=mon_cases[j]
                w1_mnid=mon_ids[j]
        else:                    #wave 2 month id
            if(mon_cases[j]>w2_mn_cases):
                w2_mn_cases=mon_cases[j]
                w2_mnid=mon_ids[j]
    w1monid_val.append(w1_mnid)
    w2monid_val.append(w2_mnid)

district_peaks["districtid"]=distid_val
district_peaks["wave1-weekid"]=w1wkid_val
district_peaks["wave2-weekid"]=w2wkid_val
district_peaks["wave1-monthid"]=w1monid_val
district_peaks["wave2-monthid"]=w2monid_val

df1=pd.DataFrame.from_dict(district_peaks)
df1.to_csv("district-peaks.csv") #district-peaks.csv


# In[40]:


week_wise=pd.DataFrame.from_dict(week_wise)
state_week_wise={"stateid":[],"timeid":[], "cases":[]}

stateid_val=[]
timeid_val=[]
cases_val=[]

dist_id=list(week_wise["districtid"])
week_id=list(week_wise["timeid"])
cases=list(week_wise["cases"])
state_id=[]
for i in neighb_dist:
    ids=i[:2]
    state_id.append(ids)
state_id=np.array(state_id)
state_id=np.unique(state_id)
wkid=0
for i in state_id:
    idx=[j for j in range(len(dist_id)) if (dist_id[j])[:2]==i]
    for j in range(1,148):
        state_cases=0
        week_val="week"+str(j)
        weekidx=week_wise.index[week_wise["timeid"]==week_val].tolist()
        x=set(idx).intersection(weekidx)
        x=list(x)
        for c in x:
            state_cases+=cases[c]
        stateid_val.append(i)
        timeid_val.append(week_val)
        cases_val.append(state_cases)

state_week_wise["stateid"]=stateid_val
state_week_wise["timeid"]=timeid_val
state_week_wise["cases"]=cases_val

state_week_wise=pd.DataFrame.from_dict(state_week_wise)


# In[43]:


state_month_wise={"stateid":[],"timeid":[], "cases":[]}

stateid_val=[]
timeid_val=[]
cases_val=[]

dist_id=list(month_wise["districtid"])
month_id=list(month_wise["timeid"])
cases=list(month_wise["cases"])

mnid=0
for i in state_id:
    idx=[j for j in range(len(dist_id)) if (dist_id[j])[:2]==i]
    for j in range(1,18):
        state_cases=0
        month_val="month"+str(j)
        monidx=month_wise.index[month_wise["timeid"]==month_val].tolist()
        x=set(idx).intersection(monidx)
        x=list(x)
        for c in x:
            state_cases+=cases[c]
        stateid_val.append(i)
        timeid_val.append(month_val)
        cases_val.append(state_cases)

state_month_wise["stateid"]=stateid_val
state_month_wise["timeid"]=timeid_val
state_month_wise["cases"]=cases_val


state_month_wise=pd.DataFrame.from_dict(state_month_wise)


# In[47]:


state_peaks={"stateid":[],"wave1-weekid":[], "wave2-weekid":[], "wave1-monthid":[], "wave2-monthid":[]}

week_ids=list(state_week_wise["timeid"])
mon_ids=list(state_month_wise["timeid"])
week_cases=list(state_week_wise["cases"])
mon_cases=list(state_month_wise["cases"])
stateid_val=[]
w1wkid_val=[]
w2wkid_val=[]
w1monid_val=[]
w2monid_val=[]

wkstateid=list(state_week_wise["stateid"])
mnstateid=list(state_month_wise["stateid"])

for i in state_id:
    w1_wk_cases=0
    w1_wkid='week40'
    w2_wk_cases=0
    w2_wkid='week120'
    w1_mn_cases=0
    w1_mnid='month5'
    w2_mn_cases=0
    w2_mnid='month14'
    if(i not in wkstateid):
        continue
    wkidx=[j for j in range(len(wkstateid)) if wkstateid[j]==i]
    mnidx=[j for j in range(len(mnstateid)) if mnstateid[j]==i]
    for j in wkidx:
        week_id=week_ids[j]
        if(int(week_id[4:])<82): #wave 1 week id
            if(week_cases[j]>w1_wk_cases):
                w1_wk_cases=week_cases[j]
                w1_wkid=week_ids[j]
        else:                     #wave 2 week id
            if(week_cases[j]>w2_wk_cases):
                w2_wk_cases=week_cases[j] 
                w2_wkid=week_ids[j]
    stateid_val.append(i)
    w1wkid_val.append(w1_wkid)
    w2wkid_val.append(w2_wkid)
    
    for j in mnidx:
        mon_id=mon_ids[j]
        if(int(mon_id[5:])<9): #wave 1 month id
            if(mon_cases[j]>w1_mn_cases):
                w1_mn_cases=mon_cases[j]
                w1_mnid=mon_ids[j]
        else:                    #wave 2 month id
            if(mon_cases[j]>w2_mn_cases):
                w2_mn_cases=mon_cases[j]
                w2_mnid=mon_ids[j]
    w1monid_val.append(w1_mnid)
    w2monid_val.append(w2_mnid)

state_peaks["stateid"]=stateid_val
state_peaks["wave1-weekid"]=w1wkid_val
state_peaks["wave2-weekid"]=w2wkid_val
state_peaks["wave1-monthid"]=w1monid_val
state_peaks["wave2-monthid"]=w2monid_val

df1=pd.DataFrame.from_dict(state_peaks)
df1.to_csv("state-peaks.csv") #state-peaks.csv


# In[49]:


overall_week_wise={"id":[],"timeid":[], "cases":[]}

id_val=[]
timeid_val=[]
cases_val=[]

state_id=list(state_week_wise["stateid"])
week_id=list(state_week_wise["timeid"])
cases=list(state_week_wise["cases"])

for i in range(1,148):
    weekid="week"+str(i)
    overall_cases=0
    idx=state_week_wise.index[state_week_wise["timeid"]==weekid].tolist()
    for j in idx:
        overall_cases+=cases[j]
    id_val.append("overall")
    timeid_val.append(weekid)
    cases_val.append(overall_cases)
    
overall_week_wise["id"]=id_val
overall_week_wise["timeid"]=timeid_val
overall_week_wise["cases"]=cases_val


# In[52]:


overall_month_wise={"id":[],"timeid":[], "cases":[]}

id_val=[]
timeid_val=[]
cases_val=[]

state_id=list(state_month_wise["stateid"])
month_id=list(state_month_wise["timeid"])
cases=list(state_month_wise["cases"])

for i in range(1,18):
    monthid="month"+str(i)
    overall_cases=0
    idx=state_month_wise.index[state_month_wise["timeid"]==monthid].tolist()
    for j in idx:
        overall_cases+=cases[j]
    id_val.append("overall")
    timeid_val.append(monthid)
    cases_val.append(overall_cases)
    
overall_month_wise["id"]=id_val
overall_month_wise["timeid"]=timeid_val
overall_month_wise["cases"]=cases_val


# In[69]:


overall_peaks={"id":[],"wave1-weekid":[], "wave2-weekid":[], "wave1-monthid":[], "wave2-monthid":[]}

week_ids=list(overall_week_wise["timeid"])
mon_ids=list(overall_month_wise["timeid"])
week_cases=list(overall_week_wise["cases"])
mon_cases=list(overall_month_wise["cases"])
id_val=[]
w1wkid_val=[]
w2wkid_val=[]
w1monid_val=[]
w2monid_val=[]

w1_wk_cases=0
w1_wkid='0'
w2_wk_cases=0
w2_wkid='0'
w1_mn_cases=0
w1_mnid='0'
w2_mn_cases=0
w2_mnid='0'

for i in range(len(week_ids)):
    week_id=week_ids[i]
    if(int(week_id[4:])<82): #wave 1 week id
        if(week_cases[i]>w1_wk_cases):
            w1_wk_cases=week_cases[i]
            w1_wkid=week_ids[i]
    else:                     #wave 2 week id
        if(week_cases[i]>w2_wk_cases):
            w2_wk_cases=week_cases[i] 
            w2_wkid=week_ids[i]
        
id_val.append("overall")
w1wkid_val.append(w1_wkid)
w2wkid_val.append(w2_wkid)

for i in range(len(mon_ids)):
    mon_id=mon_ids[i]
    if(int(mon_id[5:])<9): #wave 1 week id
        if(mon_cases[i]>w1_mn_cases):
            w1_mn_cases=mon_cases[i]
            w1_mnid=mon_ids[i]
    else:                     #wave 2 week id
        if(mon_cases[i]>w2_mn_cases):
            w2_mn_cases=mon_cases[i] 
            w2_mnid=mon_ids[i]
            
w1monid_val.append(w1_mnid)
w2monid_val.append(w2_mnid)
    
overall_peaks["id"]=id_val
overall_peaks["wave1-weekid"]=w1wkid_val
overall_peaks["wave2-weekid"]=w2wkid_val
overall_peaks["wave1-monthid"]=w1monid_val
overall_peaks["wave2-monthid"]=w2monid_val

df=pd.DataFrame.from_dict(overall_peaks)
df.to_csv("overall-peaks.csv") #overall-peaks.csv


# In[ ]:




