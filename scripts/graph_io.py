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
	@Use: given path to json file, load graph as
			(adj1, adj2, <adv>)
		  where `<adv> adj1` paraphrases `adj2`
		  and list of vertices

		If path invalid, return empty lists
'''
# from_digraph :: FilePath -> [(String,String, String)]
def load_as_list(path):

	if not os.path.isfile(path):
		return [],[]
	else:

		with open(path, 'r') as f:
			raw_graph  = json.load(f)

		vertices = raw_graph['nodes']
		words  = [v['id'] for v in raw_graph['nodes']]
		graph  = [to_edge(edge, vertices) for edge in raw_graph['links']]

		return graph, words

def to_edge(edge, vertices):
	u = vertices[edge['source']]['id']
	v = vertices[edge['target']]['id']
	e = '<' + edge['adverb'] + '>'
	return (u,v,e)


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
