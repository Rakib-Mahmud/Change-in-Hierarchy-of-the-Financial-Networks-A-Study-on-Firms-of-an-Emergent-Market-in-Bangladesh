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

##Identify most central nodes of each MSTs
top_bc = []
top_nodes = []
for mst in msts:
  bc = nx.betweenness_centrality(mst)
  bcs = sorted(bc.items(), key=lambda x: x[1], reverse=True)
  hnode, hbc_val = bcs[0]
  top_bc.append(hbc_val)
  top_nodes.append(names[hnode])
    
