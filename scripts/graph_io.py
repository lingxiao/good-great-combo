############################################################
# Module  : Load PPDB graph in variety of formats
# Date    : April 3rd, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import json
import networkx as nx
from networkx.readwrite import json_graph

from utils   import *
from scripts import *

############################################################
'''
	@Use: Given path to graph, function that 
		  computs the weight between two vertices, 
		  and directory to log program trace
		  output digraph

	@Input: `gr_path`            :: String
	        `weighted_edge_path` :: String
	        `log_dir`            :: String

	@output: networkx.classes.digraph.Digragh
'''
def load_as_digraph(gr_path, weight_edge_path, log_dir):

	writer = Writer(log_dir,1)
	
	writer.tell('loading graph as digraph from ' + gr_path)

	edges, words = load_as_list(gr_path)

	writer.tell('constructing all unique edges ...')

	to_tuple     = lambda xs: (xs[0], xs[1])
	unique_edges = set( to_tuple(sorted([u,v])) for u in words for v in words )

	G = nx.DiGraph()

	writer.tell('adding all words to graph ...')

	for word in words:
		G.add_node(word)

	writer.tell('adding all edges to graph. This will take a while ...')

	for u,v in unique_edges:
		e = weighted_edge(edges,u,v)
		if e:
			G.add_edge(u, v, weight=e[u + '->' + v])
			G.add_edge(v, u, weight=e[v + '->' + u])

	writer.close()

	return G

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

