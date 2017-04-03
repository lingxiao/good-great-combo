############################################################
# Module  : Applicaton Main
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
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
gr_path = PATH['inputs']['graph-wt-by-edge-cnt']

if os.path.exists(gr_path):
	pass
else:
	save_edge_by_edge_count( PATH['assets']['graph']
		                   , gr_path
	    	               , os.path.join(PATH['directories']['log']))

# '''
# 	read weighted graph
# '''
# gr_path         = PATH['assets']['graph']
# edges, vertices = load_as_list(gr_path)
# G               = load_as_digraph(gr_path, edge_by_edge_count, PATH['directories']['log'])

'''
	now you need to construct a digraph from list of weighted edges
'''




