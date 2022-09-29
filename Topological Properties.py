import pandas as pd
import numpy as np
import igraph as ig
import networkx as nx
import networkx.algorithms.community as nx_comm
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

returns = pd.read_csv('Returns.csv')
idx=0
num_years = 13
msts = []
##Generate MSTs for each year
for k in range(num_years):
    ret = returns.iloc[idx:idx+237, :]
    idx += 237
    corr = ret.corr()
    dis = np.sqrt(2*(1-corr))
    G = nx.from_numpy_matrix(dis.to_numpy())
    mst = nx.minimum_spanning_tree(G)
    msts.append(mst)

##Measure topological properties of the MSTs
diameter = []
avgpth = []
for mst in msts:
  diameter.append(nx.diameter(mst))
  avgpth.append(nx.average_shortest_path_length(mst))
  
##Plot topological properties in graph  
plt.figure(figsize=(10,6))
years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
plt.plot(years, diameter, linewidth=4, marker='o', markersize=13)
plt.ylabel('Diameter', fontsize=15)

plt.figure(figsize=(10,6))
years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020"]
plt.plot(years, avgpth, linewidth=4, marker='o', markersize=13)
plt.ylabel('Average Path Length', fontsize=15)
