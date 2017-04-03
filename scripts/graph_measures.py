############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import networkx as nx

from utils   import *
from scripts import *

'''
	@Use  : Given path to graph, and path to log directory
			save edges weighted by counting the 
	        number of vertices going between the vertices

	@Given: path to graph            :: String
	        path to output directory :: String
	        path to log directory    :: String

	@output: dict of weight from:
				u to v, v to u
			or None
			save output to disk
'''
def save_edge_by_edge_count(gr_path, out_path, log_dir):

	writer = Writer(log_dir,1)

	writer.tell('running save_edge_by_edge_count over graph found at \n\t\t'
		       + gr_path)

	edges, words = load_as_list(gr_path)

	writer.tell('constructing all unique edges ...')

	to_tuple     = lambda xs: (xs[0], xs[1])
	unique_edges = set( to_tuple(sorted([u,v])) for u in words for v in words )

	writer.tell('found ' + str(len(unique_edges)) + ' possible unique edges in graph.')

	writer.tell('Computing weights for edges that exist in ppdb graph. This will take a while ...')

	h = open(out_path, 'wb')

	for s,t in list(unique_edges):

		e = edge_by_edge_count(edges,s,t)
	
		if e:
			st = s + '->' + t
			ts = t + '->' + s
			h.write(st + ': ' + str(e[st]) + '\n')
			h.write(ts + ': ' + str(e[ts]) + '\n')

	h.close()
	writer.close()


'''
	@Use  : Given raw ppdb graph as list of edges of form:
				(source, target, <edge>)
			and vertices, output edges weighted by counting the 
	        number of vertices going between the vertices

	        If no edges observed between two verices, then 
	        output None

	@Given: edges of graph         :: [(String,String,String)]
			vertiex in the graph u :: String
			vertiex in the graph v :: String

	@output: dict of weight from:
				u to v, v to u
			or None
'''
def edge_by_edge_count(edges, x, y):

	eps = 1e-5

	x_y = len([(s,t,e) for s,t,e in edges if s == x and t == y])
	y_x = len([(s,t,e) for s,t,e in edges if s == y and t == x])

	if not x_y and not y_x:
		return None

	else:
		tot = float(x_y + y_x) + 2*eps
		return {x +'->' + y: (x_y + eps)/tot, y+ '->'+x : (y_x + eps)/tot}






