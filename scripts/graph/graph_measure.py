############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import pickle
import networkx as nx

from utils   import *
from scripts import *
from scripts.graph import *

############################################################

'''
	@Use  : compute page rank for all words in graph at 
	        specfied restart constant and save
	@Input: 
		- `gr_path` :: String   path to multi-digraph
		- `wt_path` :: String   path vertex weights
		- `out_dir`	:: String   path to output directory
		- `log_dir` :: String   path to log output
		- `alpha`   :: Float    random walk reset constant
		- `refresh` :: Bool     if true do no recompute ppr if file already exists
		- `debug`   :: Bool     if true only run for three words

	@output: None. Write results to disk

	@Rasies: NameError if output directory does not exists
'''
def personalized_page_rank( gr_path
	                      , wt_path
	                      , out_dir
	                      , log_dir
	                      , alpha
	                      , refresh = True
	                      , debug = False):

	if not os.path.exists(out_dir):
		raise NameError('output directory does not exist at ' + out_dir)

	else:

		salpha   = str(alpha)
		srefresh = 'refresh' if refresh else 'restart'
		writer = Writer(log_dir, 1, debug)

		'''
			Read ppdb graph
		'''
		G_ppdb, words  = load_as_digraph( gr_path, wt_path )

		if debug: ws   = words[0:3]
		else:    ws   = words

		writer.tell('running compute_ppr at constant ' 
			       + salpha 
			       + ' in ' 
			       + srefresh
			       + ' mode') 

		for w in ws:

			out_path = os.path.join(out_dir, w + '-' + salpha + '.pkl')

			if os.path.exists(out_path) and refresh:
				pass
			else:

				personal    = {w : 0 for w in words}
				personal[w] = 1.0

				ppr = nx.pagerank(G_ppdb, personalization = personal, alpha = alpha)

				with open(out_path, 'wb') as h:
					pickle.dump(ppr, h)

		writer.tell('Done')
		writer.close()

############################################################
'''
	@Use  : open graph and compute the weight of 
	        edges between vertices, so that between
	        each vertex there is at most one directed
	        edge. the weight of the edge between s and t
	        is computed by function weighted_edge

	@Given: path to graph                :: String
			path to edges to be computed :: String
	        path to output directory     :: String


	@output: None

'''
def weight_by_bradly_terry(gr_path, edge_path, out_path):
	
	edges, words = load_as_list(gr_path)

	with open(edge_path, 'rb') as h:
		unique_edges = [xs.split(', ') for xs in h.read().split('\n')]

	f = open(out_path, 'wb')

	for s,t in unique_edges:

		e = bradly_terry(edges,s,t)

		if e:
			st = s + '->' + t
			ts = t + '->' + s
			f.write(st + ': ' + str(e[st]) + '\n')
			f.write(ts + ': ' + str(e[ts]) + '\n')

	f.close()


'''
	@Use  : Given raw ppdb graph as list of edges of form:
				(source, target, <edge>)
			and vertices, output edges weighted by counting the 
	        number of vertices going between the vertices

	                   number_of_vertex(s -> t) 
	         ---------------------------------------------------
	         	sum_{x \in neighbor(s)} number_of_vertex(s -> x)

	@NOTE: alpha smoothing parameter ensure that: |neigh(x)| >= alpha

	@Given: path to graph                :: String
			path to edges to be computed :: String
	        path to output directory     :: String

	@output: None
'''
def weight_by_neigh(gr_path, edge_path, out_path):

	G, words = load_as_list(gr_path)

	with open(edge_path, 'rb') as h:
			edges = [xs.split(', ') for xs in h.read().split('\n')]

	f = open(out_path, 'wb')

	for s,t in edges:

		# weight(s -> t)
		neigh_s = [(x,y,z) for x,y,z in G if x == s]
		e_s_t   = [(x,y,z) for x,y,z in neigh_s if y == t]
		w_s_t   = len(e_s_t) / float(len(neigh_s) + 1e-5)

		# weight(t -> s)
		neigh_t = [(x,y,z) for x,y,z in G if x == t]
		e_t_s   = [(x,y,z) for x,y,z in neigh_t if y == s]
		w_t_s   = len(e_t_s) / float(len(neigh_t) + 1e-5)

		st = s + '->' + t
		ts = t + '->' + s
		f.write(st + ': ' + str(w_s_t) + '\n')
		f.write(ts + ': ' + str(w_t_s) + '\n')

	f.close()

############################################################
'''
	edge weight subroutines


	@Use  : Given raw ppdb graph as list of edges of form:
				(source, target, <edge>)
			and vertices, output edges weighted by counting the 
	        number of vertices going between the vertices

	                   number_of_vertex(s -> t) 
	         ---------------------------------------------------
	         number_of_vertex(s -> t) + number_of_vertex(t -> s)

	        If no edges observed between two verices, then 
	        output None

	@Given: edges of graph         :: [(String,String,String)]
			vertiex in the graph u :: String
			vertiex in the graph v :: String

	@output: dict of weight from:
				u to v, v to u
			or None
'''
def bradly_terry(edges, x, y):

	eps = 1e-5

	x_y = len([(s,t,e) for s,t,e in edges if s == x and t == y])
	y_x = len([(s,t,e) for s,t,e in edges if s == y and t == x])

	if not x_y and not y_x:
		return None

	else:
		tot = float(x_y + y_x) + 2*eps
		return {x +'->' + y: (x_y + eps)/tot, y+ '->'+x : (y_x + eps)/tot}

############################################################
'''
	page rank tutorials
'''
def page_rank_unit_test_1():
	'''
		construct graph where 1 is a sink
	'''
	G = nx.DiGraph()

	[G.add_node(k) for k in [1,2,3,4]]
	G.add_edge(2,1)
	G.add_edge(3,1)
	G.add_edge(4,1)

	# vary parameters
	ppr1     = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0})
	ppr1_5   = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 5)
	ppr1_100 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 100)


	ppr2     = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0})
	ppr2_100 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 100)
	ppr2_500 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 500)

	ppr3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0})

	'''
		for ppr, the lower the alpha, the more likely that the random walk will 
		end up where I started given that v1 is a sink
	'''
	ppr3_a1 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.90, max_iter = 500)
	ppr3_a2 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.75)
	ppr3_a3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.50)
	ppr3_a4 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.25)
	ppr3_a5 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.10)
	ppr3_a6 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.01)

def page_rank_unit_test_2():

	'''
		construct graph where 1 is a source
	'''
	G = nx.DiGraph()

	[G.add_node(k) for k in [1,2,3,4]]
	G.add_edge(1,2)
	G.add_edge(1,3)
	G.add_edge(1,4)

	# vary iterations
	ppr1     = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0})
	ppr1_100 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 100)
	ppr1_500 = nx.pagerank(G,personalization={1:1, 2:0, 3:0, 4:0}, max_iter = 500)

	ppr2     = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0})
	ppr2_100 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 100)
	ppr2_500 = nx.pagerank(G,personalization={1:0, 2:1, 3:0, 4:0}, max_iter = 500)

	ppr3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0})

	'''
		the lower the alpha, the more likely that random walk will end up where I started

		so 1 - alpha is the probability of restarting
	'''
	ppr3_a1 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.90, max_iter = 500)
	ppr3_a2 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.75)
	ppr3_a3 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.50)
	ppr3_a4 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.25)
	ppr3_a5 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.10)
	ppr3_a6 = nx.pagerank(G,personalization={1:0, 2:0, 3:1, 4:0}, alpha = 0.01)


