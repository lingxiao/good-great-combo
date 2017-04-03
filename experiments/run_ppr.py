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
gr_path        = PATH['assets']['graph']
edges, vertices = load_as_list(gr_path)

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

for word in words:
	G.add_node(word)



# G.add_node('limited' )
# G.add_node('suicidal')
# G.add_edge('limited','suicidal', weight=0.9)
# G.add_edge('suicidal','limited', weight=0.1)
# pr = nx.pagerank(G, alpha=0.9)



















