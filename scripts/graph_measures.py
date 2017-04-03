############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import networkx as nx

from scripts import *

'''
	@Use  : Given raw ppdb graph as list of edges of form:
				(source, target, <edge>)
			and vertices, output edges weighted by counting the 
	        number of vertices going between the vertices

	@Given: edges of graph         :: [(String,String,String)]
			vertiex in the graph u :: String
			vertiex in the graph v :: String

	@output: dict of weight from:
				u to v, v to u
'''
def edge_by_edge_count(edges, u, v):
	eps = 1e-5
	u_v = len([(s,t,e) for s,t,e in edges if s == u and t == u]) + eps
	v_u = len([(s,t,e) for s,t,e in edges if s == v and t == u]) + eps
	tot = float(u_v + v_u) + 2*eps
	return {u +'->' + v: u_v/tot, v+ '->'+u : v_u/tot}






