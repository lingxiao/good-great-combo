############################################################
# Module  : Applicaton Main
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

graph  = load_as_digraph(gr_path, vertex_dir)

'''
	compute page rank
'''
page_rank = nx.pagerank(graph, alpha= 0.9)








