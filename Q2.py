#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import csv

f=open("neighbor-districts-modified.json")

neighb_dist=json.load(f)
edge_list=[]
for i in neighb_dist:
    for j in neighb_dist[i]:
        t=[i,j]
        edge_list.append(t)
np.savetxt("edge-graph.csv", edge_list, delimiter =", ", fmt ='% s') #edge-graph.csv for Q2

