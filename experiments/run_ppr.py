############################################################
# Module  : Compute ppr
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import pickle
import networkx as nx
from networkx.readwrite import json_graph

from app.config import PATH
from utils   import *
from scripts import *

'''
	todo tuesday:
		 - run wt-edge over ppdb + ngram graph
		 - run logistic regression
'''

############################################################
'''
	read test-set
'''
ccb    = read_gold(PATH['assets']['ccb'])
bansal = read_gold(PATH['assets']['bansal'])

'''
	read weighted edge from disk if it exists,
	else compute ppr for every vertex in the graph
'''
gr_path    = PATH['assets']['graph']
vertex_dir = PATH['inputs']['graph-wt-by-edge']	
 
# graph  = load_as_digraph(gr_path, vertex_dir)

'''
	compute page rank
'''
# page_rank = nx.pagerank(graph, alpha= 0.9)

'''
	todo: figure out how to compute personalized pagerank
'''
G = nx.DiGraph()

[G.add_node(k) for k in [1,2,3,4]]
G.add_edge(2,1)
G.add_edge(3,1)
G.add_edge(4,1)

# vary iterations
ppr1 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0})
ppr2 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0})











