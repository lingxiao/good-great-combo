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
	get graph
	note this is a multi-digraph

	needs to become digraph by converting edges to weighted edges
'''
gr_path         = PATH['assets']['graph']
edges, vertices = load_as_list(gr_path)
# G               = load_as_digraph(gr_path, edge_by_edge_count, PATH['directories']['log'])

############################################################
'''
	get set of words from ccb and bansal
'''
words = list(set(join(join(ws) for _,ws in ccb.iteritems())
      + join(join(ws) for _,ws in bansal.iteritems())))

############################################################
'''
	compute ppr for every vertex in the graph
'''
save_edge_by_edge_count( PATH['assets']['graph']
	                   , os.path.join(PATH['directories']['input'], 'graph-edge-weight.txt')
	                   , os.path.join(PATH['directories']['log']))








