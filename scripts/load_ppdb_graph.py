# ############################################################
# # Module  : process veronica' ppdb graph
# # Date    : March 19th
# # Author  : Xiao Ling
# ############################################################

import os
import datetime

# from ilp_scripts import * 
# from prelude import *

import json
from networkx.readwrite import json_graph

############################################################
'''
	Run top-level script
	@Use: Open veronica's graphs:
			ppdb_graph
			ppdb_graph_and
			ppdb_graph_or

		  and then save them as .txt files *unprocessed*

	ie:
		gr, gr_and, gr_or = load_digraph()
'''
def load_digraph():

	root      = os.getcwd()
	input_dir = os.path.join(root, 'inputs/raw/')

	ppdb_gr     = os.path.join(input_dir, 'ppdb-graph.json')
	ppdb_gr_and = os.path.join(input_dir, 'ppdb-graph-and.json')
	ppdb_gr_or  = os.path.join(input_dir, 'ppdb-graph-or.json')

	print('\n>> loading digraph from: \n'
	+ ppdb_gr     + '\n'
	+ ppdb_gr_and + '\n'
	+ ppdb_gr_or  + '\n')


	'''
		reconstruct all graphs and save all results
	'''
	ppdb_gr     = from_digraph(os.path.join(input_dir, 'ppdb-graph.txt'),
		          from_json(ppdb_gr))

	ppdb_gr_and = from_digraph(os.path.join(input_dir, 'ppdb-graph-and.txt'),
		          from_json(ppdb_gr_and))

	ppdb_gr_or  = from_digraph(os.path.join(input_dir, 'ppdb-graph-or.txt'),
		          from_json(ppdb_gr_or))

	return ppdb_gr, ppdb_gr_and, ppdb_gr_or

############################################################
'''
	@Use: given digraph, output list of triples of form:
			(adj1, adj2, <adv>)
		  where `<adv> adj1` paraphrases `adj2`

		  write results to `out_path`
'''
# from_digraph :: Digraph -> IO [(String,String,String)]
def from_digraph(out_path, digraph):

	print ('\n>> constructing graph to be saved at ' 
		  + out_path + '...')

	words   = set(str(w) for w in digraph.nodes() )
	pwords  = [(u,v) for u in words for v in words]
	graph   = []
	h       = open(out_path, 'w')

	for u,v in pwords:

		advs = digraph.get_edge_data(u,v)

		if advs:
			advs = ['<'+ str(a['adverb']) + '>' for _,a in advs.iteritems()]
			edge = [(u,v,w) for w in advs]
			graph += edge

			for u,v,w in edge:
				xs = u + ',' + v + ',' + w + '\n'
				h.write(xs)
				print ('\n>> writing triple: ' + xs)

	h.write('== END')
	h.close()

	return graph

############################################################
'''
	method to serialize and deserialze graphs
'''
def from_json(path):
    with open(path, 'r') as infile:
        networkx_graph = json_graph.node_link_graph(json.load(infile))
    return networkx_graph

def to_json(networkx_graph):
    return json.dumps(json_graph.node_link_data(self.nx_graph))








