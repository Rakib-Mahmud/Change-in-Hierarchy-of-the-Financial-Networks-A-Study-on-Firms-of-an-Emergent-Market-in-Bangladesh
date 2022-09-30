import pandas as pd
import numpy as np
import igraph as ig
import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt

#Function to check node-orders based on degree to determine if the path is hierarchical
def isHierarchical(path):
    #If an up-path or down-path exist, the path is hierarchical
    if (all(path[i] <= path[i+1] for i in range(len(path)-1))) or (all(path[i] >= path[i+1] for i in range(len(path)-1))):
        return True
    #If an up-path followed by a down-path exist, the path is hierarchical
    i = 0
    last_idx = len(path)-1
    if i<last_idx and path[i]<=path[i+1]:
        while i<last_idx and path[i]<=path[i+1]:
            i+=1
        if i<last_idx and path[i]>=path[i+1]:
            while i<last_idx and path[i]>=path[i+1]:
                i+=1
    if i == last_idx:
        return True
    
    return False   

#Function to calculate the hierarchy based on the 'hierarchical path' concept
def hierarchy(mst):
    cnt = 0
    degree = dict(mst.degree())
    for i in range(len(mst.nodes)):
        for j in range(i+1, len(mst.nodes)):
            paths = nx.all_simple_paths(mst, source=i, target=j)
            for path in paths:
                deg = [degree[m] for m in path]
                if isHierarchical(deg):
                    cnt += 1
    n = len(mst.nodes)
    F = cnt/((n*(n-1))//2)
    return F

#Main section
returns = pd.read_csv('Returns.csv')
idx=0
num_years = 13
F = np.zeros(num_years)
#Annual Hierarchy calculation
for k in range(num_years):
    ret = returns.iloc[idx:idx+237, :]
    idx += 237
    corr = ret.corr()
    dis = np.sqrt(2*(1-corr))
    #np.fill_diagonal(corr.values, 0)
    G = nx.from_numpy_matrix(dis.to_numpy())
    mst = nx.minimum_spanning_tree(G)
    F[k] = hierarchy(mst)
#Plot the measured hierarchy  
plt.figure(figsize=(10,6))
years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
plt.plot(years, F, linewidth=4, marker='o', markersize=13, color='magenta')
plt.ylabel('F', fontsize=15)  
