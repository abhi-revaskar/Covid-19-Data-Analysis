#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from datetime import datetime,timedelta, date
from dateutil.relativedelta import relativedelta

f=open("neighbor-districts-modified.json")
neighb_dist=json.load(f)

vaccine_data=pd.read_csv("cowin_vaccine_data_districtwise.csv")
dist_list=list(vaccine_data["District_Key"])
cols=list(vaccine_data.columns)

district_vaccine_week={"districtid":[], "timeid":[], "dose1":[], "dose2":[]}

distid_val=[]
timeid_val=[]
dos1_val=[]
dos2_val=[]

start_dt="15/03/2020"
end_dt="14/08/2021"
start_dt=datetime.strptime(start_dt,"%d/%m/%Y")
end_dt=datetime.strptime(end_dt,"%d/%m/%Y")
date_list=[]
date_list.append(start_dt.strftime("%d/%m/%Y"))
for i in range(6,int((end_dt-start_dt).days)+1,7):
    dt=start_dt+timedelta(i)
    date_list.append(dt.strftime("%d/%m/%Y"))
    dt=start_dt+timedelta(i+1)
    if dt.strftime("%d/%m/%Y")=="15/08/2021":
        break
    date_list.append(dt.strftime("%d/%m/%Y"))
    
for i in range(1,len(dist_list)):    
    dos1=date_list
    dos2=date_list
    dos1_week=[]
    dos2_week=[]
    row=vaccine_data.iloc[i]
    for j in dos1:
        dos1_dt=j+".3"
        dos2_dt=j+".4"
        if dos1_dt not in cols:
            dos1_week.append(0)
            dos2_week.append(0)
        else:
            dos1_week.append(int(row[dos1_dt]))
            dos2_week.append(int(row[dos2_dt]))

    wkid=0
    for l in range(0,len(dos1_week),2):
        wkid+=1
        distid_val.append(dist_list[i])
        timeid_val.append("week"+str(wkid))
        dos1_val.append(dos1_week[l+1]-dos1_week[l])
        dos2_val.append(dos2_week[l+1]-dos2_week[l])        
        
district_vaccine_week["districtid"]=distid_val
district_vaccine_week["timeid"]=timeid_val
district_vaccine_week["dose1"]=dos1_val
district_vaccine_week["dose2"] = dos2_val

df=pd.DataFrame.from_dict(district_vaccine_week)

all_dist=list(df["districtid"])
final_dist=[]
for i in neighb_dist:
    final_dist.append(i)
for i in range(len(all_dist)):
    if(all_dist[i] not in final_dist):
        df.drop(index=i,inplace=True)

df.to_csv("district-vaccinated-count-week.csv") #district-vaccinated-count-week.csv


# In[2]:


district_vaccine_month={"districtid":[], "timeid":[], "dose1":[], "dose2":[]}

distid_val=[]
timeid_val=[]
dos1_val=[]
dos2_val=[]

start_dt="15/03/2020"
end_dt="14/08/2021"
dt=datetime.strptime(start_dt,"%d/%m/%Y")
start_dt=datetime.strptime(start_dt,"%d/%m/%Y")
end_dt=datetime.strptime(end_dt,"%d/%m/%Y")
date_list=[]
for i in range(0,17):
    if dt.strftime("%d/%m/%Y")>="15/08/2021":
        break
    dt=start_dt+relativedelta(months=i)
    date_list.append(dt.strftime("%d/%m/%Y"))
    dt=start_dt+relativedelta(months=(i+1))+timedelta(-1)
    date_list.append(dt.strftime("%d/%m/%Y"))
    
for i in range(1,len(dist_list)):    
    dos1=date_list
    dos2=date_list
    dos1_mon=[]
    dos2_mon=[]
    row=vaccine_data.iloc[i]
    for j in dos1:
        dos1_dt=j+".3"
        dos2_dt=j+".4"
        if dos1_dt not in cols:
            dos1_mon.append(0)
            dos2_mon.append(0)
        else:
            dos1_mon.append(int(row[dos1_dt]))
            dos2_mon.append(int(row[dos2_dt]))

    mnid=0
    for l in range(0,len(dos1_mon),2):
        mnid+=1
        distid_val.append(dist_list[i])
        timeid_val.append("month"+str(mnid))
        dos1_val.append(dos1_mon[l+1]-dos1_mon[l])
        dos2_val.append(dos2_mon[l+1]-dos2_mon[l])        
        
district_vaccine_month["districtid"]=distid_val
district_vaccine_month["timeid"]=timeid_val
district_vaccine_month["dose1"]=dos1_val
district_vaccine_month["dose2"] = dos2_val

df=pd.DataFrame.from_dict(district_vaccine_month)
all_dist=list(df["districtid"])
for i in range(len(all_dist)):
    if(all_dist[i] not in final_dist):
        df.drop(index=i,inplace=True)
df.to_csv("district-vaccinated-count-month.csv") #district-vaccinated-count-month.csv


# In[3]:


district_vaccine_overall={"districtid":[], "timeid":[], "dose1":[], "dose2":[]}

distid_val=[]
timeid_val=[]
dos1_val=[]
dos2_val=[]

date_list=["14/08/2021"]
    
for i in range(1,len(dist_list)):    
    dos1=date_list
    dos2=date_list
    dos1_mon=[]
    dos2_mon=[]
    row=vaccine_data.iloc[i]
    for j in dos1:
        dos1_dt=j+".3"
        dos2_dt=j+".4"
        if dos1_dt not in cols:
            dos1_mon.append(0)
            dos2_mon.append(0)
        else:
            dos1_mon.append(int(row[dos1_dt]))
            dos2_mon.append(int(row[dos2_dt]))

        distid_val.append(dist_list[i])
        timeid_val.append("overall")
        dos1_val.append(dos1_mon[0])
        dos2_val.append(dos2_mon[0])        
        
district_vaccine_overall["districtid"]=distid_val
district_vaccine_overall["timeid"]=timeid_val
district_vaccine_overall["dose1"]=dos1_val
district_vaccine_overall["dose2"] = dos2_val

df=pd.DataFrame.from_dict(district_vaccine_overall)
all_dist=list(df["districtid"])
for i in range(len(all_dist)):
    if(all_dist[i] not in final_dist):
        df.drop(index=i,inplace=True)
df.to_csv("district-vaccinated-count-overall.csv") #district-vaccinated-count-overall.csv


# In[4]:


stateid=[]
for i in range(1,len(dist_list)):
    temp=dist_list[i]
    if temp not in neighb_dist:
        continue
    a=temp[:2]
    stateid.append(a)
stateid=np.array(stateid)
stateid=np.unique(stateid)

district_vaccine_week=pd.read_csv("district-vaccinated-count-week.csv")

state_vaccine_week={"stateid":[], "timeid":[], "dose1":[], "dose2":[]}
distid=list(district_vaccine_week["districtid"])
weekid=list(district_vaccine_week["timeid"])
distdos1=list(district_vaccine_week["dose1"])
distdos2=list(district_vaccine_week["dose2"])
stateid_val=[]
timeid_val=[]
dos1_val=[]
dos2_val=[]

for i in stateid:
    idx=[j for j in range(len(distid)) if distid[j][:2]==i]
    for wkid in range(1,75):
        weekidx=[j for j in range(len(weekid)) if weekid[j]=="week"+str(wkid)]
        x=set(idx).intersection(weekidx)
        x=list(x)
        dos1=0
        dos2=0
        for j in x:
            dos1+=distdos1[j]
            dos2+=distdos2[j]
        stateid_val.append(i)
        timeid_val.append("week"+str(wkid))
        dos1_val.append(dos1)
        dos2_val.append(dos2)

state_vaccine_week["stateid"]=stateid_val
state_vaccine_week["timeid"]=timeid_val
state_vaccine_week["dose1"]=dos1_val
state_vaccine_week["dose2"] = dos2_val

df=pd.DataFrame.from_dict(state_vaccine_week)
df.to_csv("state-vaccinated-count-week.csv") #state-vaccinated-count-week.csv


# In[5]:


district_vaccine_month=pd.read_csv("district-vaccinated-count-month.csv")

state_vaccine_month={"stateid":[], "timeid":[], "dose1":[], "dose2":[]}
distid=list(district_vaccine_month["districtid"])
monid=list(district_vaccine_month["timeid"])
distdos1=list(district_vaccine_month["dose1"])
distdos2=list(district_vaccine_month["dose2"])
stateid_val=[]
timeid_val=[]
dos1_val=[]
dos2_val=[]

for i in stateid:
    idx=[j for j in range(len(distid)) if distid[j][:2]==i]
    for mnid in range(1,18):
        monidx=[j for j in range(len(monid)) if monid[j]=="month"+str(mnid)]
        x=set(idx).intersection(monidx)
        x=list(x)
        dos1=0
        dos2=0
        for j in x:
            dos1+=distdos1[j]
            dos2+=distdos2[j]
        stateid_val.append(i)
        timeid_val.append("month"+str(mnid))
        dos1_val.append(dos1)
        dos2_val.append(dos2)

state_vaccine_month["stateid"]=stateid_val
state_vaccine_month["timeid"]=timeid_val
state_vaccine_month["dose1"]=dos1_val
state_vaccine_month["dose2"] = dos2_val

df=pd.DataFrame.from_dict(state_vaccine_month)
df.to_csv("state-vaccinated-count-month.csv") #state-vaccinated-count-month.csv


# In[6]:


state_vaccine_month=pd.read_csv("state-vaccinated-count-month.csv")

state_vaccine_overall={"stateid":[], "timeid":[], "dose1":[], "dose2":[]}

stateid_list=list(state_vaccine_month["stateid"])
dos1=list(state_vaccine_month["dose1"])
dos2=list(state_vaccine_month["dose2"])
stateid_val=[]
timeid_val=[]
dos1_val=[]
dos2_val=[]

for i in stateid:
    idx=[j for j in range(len(stateid_list)) if stateid_list[j]==i]
    dos1_overall=0
    dos2_overall=0
    for j in idx:
        dos1_overall+=dos1[j]
        dos2_overall+=dos2[j]
    stateid_val.append(i)
    timeid_val.append("overall")
    dos1_val.append(dos1_overall)
    dos2_val.append(dos2_overall)
    
state_vaccine_overall["stateid"]=stateid_val
state_vaccine_overall["timeid"]=timeid_val
state_vaccine_overall["dose1"]=dos1_val
state_vaccine_overall["dose2"] = dos2_val

df=pd.DataFrame.from_dict(state_vaccine_overall)
df.to_csv("state-vaccinated-count-overall.csv") #state-vaccinated-count-overall.csv


# In[ ]:




