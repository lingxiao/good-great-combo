############################################################
# Module  : Applicaton Main
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import networkx as nx

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
'''
graph = digraph_from_json(PATH['assets']['graph'])

############################################################
'''
	get set of words from ccb and bansal
'''
words = list(set(join(join(ws) for _,ws in ccb.iteritems())
      + join(join(ws) for _,ws in bansal.iteritems())))


'''
	run PPR on subset of words
'''
ws = words[0:5]

G=nx.Graph()
G.add_edges_from([(1,2),(1,3)])
G.add_node("spam")     