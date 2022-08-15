#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
overall_dates=[i for i in range(len(date)) if date[i] == "2021-08-14"]

overall={"districtid":[],"timeid":[], "cases":[],}
districtid_val=[]
timeid_val=[]
cases_val=[]

for i in neighb_dist:
    dist=i[3:]
    if dist not in dist_list:
        continue
    idx=[j for j in range(len(dist_list)) if dist_list[j]==dist]
    count=set(overall_dates).intersection(idx)
    count=list(count)
    k=count[0]
    cases_val.append(confirmed[k])
    districtid_val.append(i)
    timeid_val.append("overall")
    
    
overall["districtid"]=districtid_val
overall["timeid"]=timeid_val
overall["cases"]=cases_val

df=pd.DataFrame.from_dict(overall)

df.to_csv("cases-overall.csv") #cases-overall.csv


# In[2]:


month_wise={"districtid":[],"timeid":[], "cases":[]}
districtid_val=[]
timeid_val=[]
cases_val=[]

for i in neighb_dist:
    yr,mon,day1,day2=2020,'03',15,14
    start=str(yr)+'-'+mon+'-'+str(day1)
    end=str(yr)+'-'+'0'+str(int(mon)+1)+'-'+str(day2)
    dist=i[3:]
    month_cases=[]
    if dist not in dist_list:
        continue
    idx=[j for j in range(len(dist_list)) if dist_list[j]==dist]
    mon_idx=[]
    mon_id=0
    while(start<date[idx[0]]):
        if(end<date[idx[0]]):
            districtid_val.append(i)
            mon_id+=1
            timeid_val.append("month"+str(mon_id))
            cases_val.append(0)
            mon=mon='0'+str(int(mon)+1)
            start=str(yr)+'-'+mon+'-'+str(day1)
            end=str(yr)+'-'+'0'+str(int(mon)+1)+'-'+str(day2)
        else:
            date_idx=cases.index[cases["Date"]==end].tolist()
            x=set(date_idx).intersection(idx)
            x=list(x)
            districtid_val.append(i)
            mon_id+=1
            timeid_val.append("month"+str(mon_id))
            if len(x)==0:
                cases_val.append(0)
            else:
                cases_val.append(confirmed[x[0]])
            mon=mon='0'+str(int(mon)+1)
            start=str(yr)+'-'+mon+'-'+str(day1)
            end=str(yr)+'-'+'0'+str(int(mon)+1)+'-'+str(day2)
    else:
        for k in idx:
            if(end=="2021-09-14"):
                break
            if(date[k]==start):
                mon_idx.append(k)
                if(int(mon)==12):
                    yr=2021
                    mon='01'
                else:
                    if int(mon)>=9:
                        mon=str(int(mon)+1)
                    else:
                        mon='0'+str(int(mon)+1)
                start=str(yr)+'-'+mon+'-'+str(day1)
            elif(date[k]==end):
                mon_idx.append(k)
                if(int(mon)==12):
                    yr=2021
                    end=str(yr)+'-'+'01'+'-'+str(day2)
                else:
                    if int(mon)>=9:
                        end=str(yr)+'-'+str(int(mon)+1)+'-'+str(day2)
                    else:
                        end=str(yr)+'-'+'0'+str(int(mon)+1)+'-'+str(day2)
            elif(k<idx[-1] and date[k]<start and start<date[idx[idx.index(k)+1]]):
                districtid_val.append(i)
                mon_id+=1
                timeid_val.append("month"+str(mon_id))
                date_idx=cases.index[cases["Date"]==end].tolist()
                x=set(date_idx).intersection(idx)
                x=list(x)
                if len(x)==0:
                    cases_val.append(0)
                else:
                    cases_val.append(confirmed[x[0]])
                mon=mon='0'+str(int(mon)+1)
                start=str(yr)+'-'+mon+'-'+str(day1)
                end=str(yr)+'-'+'0'+str(int(mon)+1)+'-'+str(day2)
    for m in range(0,len(mon_idx),2):
        mon_id+=1
        districtid_val.append(i)
        timeid_val.append("month"+str(mon_id))
        cases_val.append(confirmed[mon_idx[m+1]]-confirmed[mon_idx[m]])
            
month_wise["districtid"]=districtid_val
month_wise["timeid"]=timeid_val
month_wise["cases"]=cases_val      
        
df2=pd.DataFrame.from_dict(month_wise)
df2.to_csv("cases-month.csv") #cases-month.csv


# In[3]:


week_wise={"districtid":[],"timeid":[], "cases":[]}

districtid_val=[]
timeid_val=[]
cases_val=[]

start_dt="2020-03-15"
end_dt="2021-08-14"
start_dt=datetime.strptime(start_dt,"%Y-%m-%d")
end_dt=datetime.strptime(end_dt,"%Y-%m-%d")
date_list={}
date_list[start_dt.strftime("%Y-%m-%d")]=0
for i in range(6,int((end_dt-start_dt).days)+1,7):
    dt=start_dt+timedelta(i)
    date_list[dt.strftime("%Y-%m-%d")]=0
    dt=start_dt+timedelta(i+1)
    if dt.strftime("%Y-%m-%d")=="2021-08-15":
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
        
week_wise["districtid"]=districtid_val
week_wise["timeid"]=timeid_val
week_wise["cases"]=cases_val 

df3=pd.DataFrame.from_dict(week_wise)
df3.to_csv("cases-week.csv") #cases-week.csv      


# In[ ]:




