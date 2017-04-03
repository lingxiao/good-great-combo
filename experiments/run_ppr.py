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
gr_path = PATH['assets']['graph']
# digraph = digraph_from_json(PATH['assets']['graph'])

############################################################
'''
	get set of words from ccb and bansal
'''
words = list(set(join(join(ws) for _,ws in ccb.iteritems())
      + join(join(ws) for _,ws in bansal.iteritems())))


############################################################
'''
	first thing to do is construct digraph from multi-digraph 
'''
with open(gr_path, 'r') as f:
	raw_graph  = json.load(f)

'''
	now construct edge from counts

	first construct small graph and make sure pagerank
	runs on it
'''
G = nx.DiGraph()



'''
	@Use  : Given raw ppdb graph, and two vertices
	        output edges weighted by counting the 
	        number of vertices
	@Given: raw ppdb graph         :: Dict
			vertiex in the graph u :: String
			vertiex in the graph v :: String
	@output: tuple of weight from:
				u to v, v to u
'''
def edge_weight_by_edge_count(raw_graph, u, v):
	pass


# G.add_node('limited' )
# G.add_node('suicidal')
# G.add_edge('limited','suicidal', weight=0.9)
# G.add_edge('suicidal','limited', weight=0.1)
# pr = nx.pagerank(G, alpha=0.9)



















