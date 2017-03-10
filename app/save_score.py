############################################################
# Module  : Naive implementation
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import app
from scripts import *
from prelude import *

# root        = os.getcwd()
# deploy_in   = os.path.join(root, 'deploy-in' )
# deploy_out  = os.path.join(root, 'deploy-out')
# ppdb_graph  = os.path.join(root, 'inputs/raw/all_edges.txt'  )
# ngram_graph = os.path.join(root, 'inputs/raw/ngram-graph.txt')


# '''
# 	open both graphs
# '''
# ppdb_graph  = label_adv(split_comma(open(ppdb_graph ,'r' ).read().split('\n')))
# ngram_graph = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))
# combo_graph = ppdb_graph + ngram_graph

# pairs       = [w.split(' ') for w in open(words,'r').read().split('\n') if w.split(' ')][0:-1]

# words = set(join(pairs))

############################################################
'''
	construct lookup
'''

def to_lookup(graph, words):

	lookup = dict()

	for word in words:

		local = [(b,c) for a,b,c in graph if a == word]
		ldict = dict()

		print ('<<<' + word)

		for w,_ in local:
			if w in ldict: ldict[w] += 1
			else: ldict[w] = 1.0

		lookup[word] = {'|neigh|': len(local), 'neigh': ldict}

	return lookup


############################################################

def save_score_both(root, name, pairs, graph):

	print ('==== here ====')

	words  = set(join(pairs))
	lookup = to_lookup(graph, words)

	handl   = open(os.path.join(root, name + '.txt'),'w')
	handl.write('=== ' + name + '\n')
	handl.write('='*20 + '\n')

	score = dict()
	eps   = float(1e-3)

	for u,v in pairs:

		u_strong = 0.0
		v_strong = 0.0

		print ('=== ' + u + ', ' + v)

		if u not in lookup:
			pass

		elif v in lookup[u]['neigh']:
			v_strong = lookup[u]['neigh'][v]

		print('>> ' + u + ', ' + v)
		if v not in lookup:
			pass

		elif u in lookup[v]['neigh']:
			u_strong = lookup[v]['neigh'][u]

		if u_strong or v_strong:
			Z = u_strong + v_strong + 2 * eps

			u_ge_v = (u_strong + eps)/Z
			v_ge_u = (v_strong + eps)/Z

			score[u + '>' + v] = u_ge_v
			score[v + '>' + u] = v_ge_u

		else:
			adj_adv_u = lookup[u]['|neigh|']
			adj_adv_v = lookup[v]['|neigh|']

			Z = adj_adv_u + adj_adv_v + 2*eps

			u_ge_v = (adj_adv_v + eps)/Z
			v_ge_u = (adj_adv_u + eps)/Z

			score[u + '>' + v] = u_ge_v
			score[v + '>' + u] = v_ge_u

		handl.write(u + '>' + v + ': ' + str(u_ge_v) + '\n')
		handl.write(v + '>' + u + ': ' + str(v_ge_u) + '\n')
	
	handl.write('=== END')		
	handl.close()

	return score





















