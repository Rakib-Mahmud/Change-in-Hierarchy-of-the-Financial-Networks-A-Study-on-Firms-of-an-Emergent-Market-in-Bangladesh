import pandas as pd
import numpy as np
import igraph as ig
import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt

returns = pd.read_csv('Returns.csv')
idx=0
num_years = 13
centerDeg = np.zeros(num_years)
centerNodes = []
centerNodesID = []
msts = []
cors = []
##Calculate the hub in each year based on max degree
for k in range(num_years):
    ret = returns.iloc[idx:idx+237, :]
    names = ret.columns
    idx += 237
    corr = ret.corr()
    cors.append(corr)
    dis = np.sqrt(2*(1-corr))
    #np.fill_diagonal(corr.values, 0)
    G = nx.from_numpy_matrix(dis.to_numpy())
    mst = nx.minimum_spanning_tree(G)
    msts.append(mst)
    highDeg = sorted(mst.degree, key = lambda x: x[1], reverse=True)[0]
    centerDeg[k] = highDeg[1]
    centerNodes.append(names[highDeg[0]]) 
    centerNodesID.append(highDeg[0])
##Plot the year-wise hubs as a curve    
sn = ['NCCBL', 'TBL', 'SBIL', 'CCL', 'FICL', 'BWEL', 'SBL', 'GSL', 'MICL', 'RICL', 'PBL', 'IFICB', 'PBL']
for a, b in zip(sn, centerNodes):
    print(a+': '+b)
    
fig, ax = plt.subplots(figsize=(10,6))
years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]

ax.plot(years, centerDeg, linewidth=4, marker='o', markersize=13, color='magenta')
plt.ylabel('Largest Degree', fontsize=13)
plt.yticks(np.arange(min(centerDeg), max(centerDeg)+2, 1.0))
for i, txt in enumerate(sn):
    if i==0:
        ax.annotate(txt, (i-0.3, centerDeg[i]+0.15), fontsize=14)
    else:
        ax.annotate(txt, (i, centerDeg[i]+0.15), fontsize=14)    
