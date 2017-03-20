# ############################################################
# # Module  : Constructing all probability
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import datetime

from ilp_scripts import * 
from prelude import *


'''
	@Use: given boolean flag `refresh`, if true:
			check to see if probability lookup table
			have been constructed
			if not then construct all graphs
			else do nothing
		 if not refresh, then construct all probs tables
'''
# to_probs_table :: Bool -> IO ()
def to_probs_table(refresh):
	'''
		Paths
	'''
	root        = os.getcwd()
	input_dir   = os.path.join(root, 'inputs/raw')
	probs_dir   = os.path.join(root, 'inputs/probs')

	old_ppdb_graph  = os.path.join(input_dir, 'all_edges.txt'      )
	ppdb_graph      = os.path.join(input_dir, 'ppdb-graph.txt'     ) 
	ppdb_graph_and  = os.path.join(input_dir, 'ppdb-graph-and.txt' ) 
	ppdb_graph_or   = os.path.join(input_dir, 'ppdb-graph-or.txt'  ) 
	ngram_graph     = os.path.join(input_dir, 'ngram-graph.txt'    )

	print('\n>> openinging all raw graphs from: \n' 
 	+ old_ppdb_graph + '\n'
	+ ppdb_graph     + '\n'
	+ ppdb_graph_and + '\n'
	+ ppdb_graph_or  + '\n'
	+ ngram_graph    + '\n')

	'''
		opening all raw graphs
	'''
	old_ppdb_graph  = split_comma(open(old_ppdb_graph ,'r' ).read().split('\n'))
	ppdb_graph      = split_comma(open(ppdb_graph     ,'r' ).read().split('\n'))
	ppdb_graph_and  = split_comma(open(ppdb_graph_and ,'r' ).read().split('\n'))
	ppdb_graph_or   = split_comma(open(ppdb_graph_or  ,'r' ).read().split('\n'))
	ngram_graph     = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))


	print('\n>> naively combining all ppdb data with ngram data')
	'''
		combine all graphs with ngram graph
	'''
	ngram_ppdb     = ppdb_graph     + ngram_graph
	ngram_ppdb_old = old_ppdb_graph + ngram_graph
	ngram_ppdb_and = ppdb_graph_and + ngram_graph
	ngram_ppdb_or  = ppdb_graph_or  + ngram_graph

	'''
		compute and save probability for both
		if file does not exit already
	'''
	name     = 'probs-ngram-ppdb'
	name_old = 'ngram-ppdb-old'
	name_and = 'probs-ngram-ppdb-and'
	name_or  = 'probs-ngram-ppdb-or'

	path_name, path_old, path_and, path_or = [os.path.join(probs_dir, p + '.txt') for \
	                                p in [name,name_old,name_and,name_or]]

	print('\n>> constructing all probability tables ...')

	if refresh:

		if not os.path.isfile(path_name):
			ngram_ppdb_probs = compute_probs_both(probs_dir, name, ngram_ppdb)

		if not os.path.isfile(path_and):
			ngram_ppdb_and_probs = compute_probs_both(probs_dir, name_and, ngram_ppdb_and)

		if not os.path.isfile(path_or):
			ngram_ppdb_or_probs = compute_probs_both(probs_dir, name_or, ngram_ppdb_or)

		if not os.path.isfile(path_old):
			ngram_ppdb_old = compute_probs_both(probs_dir, name_old, ngram_ppdb_old)

	else:
		print ('\n>> Refresh = False. Rebuilding all graphs and rewriting any existing files ...')
		ngram_ppdb_probs     = compute_probs_both(probs_dir, name, ngram_ppdb)
		ngram_ppdb_and_probs = compute_probs_both(probs_dir, name_and, ngram_ppdb_and)
		ngram_ppdb_or_probs  = compute_probs_both(probs_dir, name_or, ngram_ppdb_or)
		ngram_ppdb_old       = compute_probs_both(probs_dir, name_old, ngram_ppdb_old)


############################################################
'''
	helper functions
'''
def open_probs_table(path):

	to_tuple = lambda xs: (xs[0], float(xs[1]))

	if os.path.isfile(path):

		print ('\n>> found probability table on disk ...' + 
			  '\n>> opening table from ' + path + ' ...')

		raw   = open(path,'r').read().split('\n')[4:-1]
		probs = dict([to_tuple(r.split(': ')) for r in raw])

		return probs
	else:
		print ('\n>> probabilty table not found at path ' + path)

'''
	@Use: given root directory and file name to save,
		  graph graph of form:		  
		  	[('adj1', 'adj2','<adv>'),..]

		  output probability adj_i > adj_k
		  for every i and k

		  save output to root/name.txt
'''
# probs_both :: String
#             -> String
#             -> [(String, String, String)]
#             -> IO (Dict String Float)
def compute_probs_both(root, name, graph):


	print ('\n>> computing probability table for graph ' + name)

	words  = set(join([u,v] for u,v,_ in graph))
	pairs  = [(u,v) for u in words for v in words if u != v]
	words  = set(join(pairs))
	lookup = to_lookup(graph, words)

	handl  = open(os.path.join(root, name + '.txt'),'w')
	handl.write('-'*50 + '\n')
	handl.write(name + '\n')
	handl.write(str(datetime.datetime.now()) + '\n')
	handl.write('-'*50 + '\n')

	probs = dict()
	eps   = float(1e-3)

	print ('\n>> begin computing probs')

	for u,v in pairs:

		u_strong = 0.0
		v_strong = 0.0


		if u not in lookup:
			pass

		elif v in lookup[u]['neigh']:
			v_strong = lookup[u]['neigh'][v]

		if v not in lookup:
			pass

		elif u in lookup[v]['neigh']:
			u_strong = lookup[v]['neigh'][u]

		if u_strong or v_strong:
			Z = u_strong + v_strong + 2 * eps

			u_ge_v = (u_strong + eps)/Z
			v_ge_u = (v_strong + eps)/Z

			probs[u + '>' + v] = u_ge_v
			probs[v + '>' + u] = v_ge_u

		else:
			adj_adv_u = lookup[u]['|neigh|']
			adj_adv_v = lookup[v]['|neigh|']

			Z = adj_adv_u + adj_adv_v + 2*eps

			u_ge_v = (adj_adv_v + eps)/Z
			v_ge_u = (adj_adv_u + eps)/Z

			probs[u + '>' + v] = u_ge_v
			probs[v + '>' + u] = v_ge_u

		handl.write(u + '>' + v + ': ' + str(u_ge_v) + '\n')
		handl.write(v + '>' + u + ': ' + str(v_ge_u) + '\n')
		print ('\n\t>> computed probs for words: ' + u + ', ' + v)
	
	handl.write('== END')		
	handl.close()

	print ('\n>> done computing probs')

	return probs

############################################################
'''
	construct lookup
'''
def to_lookup(graph, words):

	lookup = dict()

	print ('\n>> begin constructing lookup graph')


	for word in words:

		local = [(b,c) for a,b,c in graph if a == word]
		ldict = dict()

		for w,_ in local:
			if w in ldict: ldict[w] += 1
			else: ldict[w] = 1.0

		lookup[word] = {'|neigh|': len(local), 'neigh': ldict}

	print ('\n>> done constructing lookup graph')
	return lookup







