############################################################
# Module  : Load PPDB graph in variety of formats
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import json
from networkx.readwrite import json_graph

############################################################
'''
	load raw json file as multidigraph
'''

def load_as_multi_digraph(path):
    with open(path, 'r') as infile:
        networkx_graph = json_graph.node_link_graph(json.load(infile))
    return networkx_graph

def multi_digraph_to_json(networkx_graph):
    return json.dumps(json_graph.node_link_data(self.nx_graph))

############################################################
'''
	@Use: given digraph, output list of triples of form:
			(adj1, adj2, <adv>)
		  where `<adv> adj1` paraphrases `adj2`
'''
# from_digraph :: Multdigraph -> [(String,String, String)]
def multi_digraph_to_list(digraph):

	words   = set(str(w) for w in digraph.nodes())
	pwords  = [(u,v) for u in words for v in words]
	graph   = []

	for u,v in pwords:

		advs = digraph.get_edge_data(u,v)

		if advs:
			advs = ['<'+ str(a['adverb']) + '>' for _,a in advs.iteritems()]
			edge = [(u,v,w) for w in advs]
			graph += edge


	return graph
