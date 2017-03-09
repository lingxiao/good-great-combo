############################################################
# Module  : Naive implementation
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import time
import datetime
import operator
import random
import itertools	
from copy import deepcopy
import numpy as np
from pulp    import *

import app
from scripts import *
from prelude import *

num = 8

############################################################
'''
	PATHS
'''
root        = '/home1/l/lingxiao/xiao/good-great-combo'

deploy_in   = os.path.join(root, 'deploy-in' )
deploy_out  = os.path.join(root, 'deploy-out')
ppdb_graph  = os.path.join(root, 'inputs/raw/all_edges.txt'  )
ngram_graph = os.path.join(root, 'inputs/raw/ngram-graph.txt')

words       = os.path.join(deploy_in, 'deploy' + str(num) + '.txt')


'''
	open both graphs
'''
ppdb_graph  = label_adv(split_comma(open(ppdb_graph ,'r' ).read().split('\n')))
ngram_graph = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))
combo_graph = ppdb_graph + ngram_graph

pairs       = [w.split(' ') for w in open(words,'r').read().split('\n') if w.split(' ')][0:-1]

############################################################

def save_score_both(root, name, pairs, graph):

	handl   = open(os.path.join(root, name + '.txt'),'w')
	handl.write('=== ' + name + '\n')
	handl.write('='*20 + '\n')

	score   = dict()
	eps     = float(1e-3)

	for u,v in pairs:
		v_strong  = len([(a,b,c) for a,b,c in graph if a == u and b == v])
		u_strong  = len([(a,b,c) for a,b,c in graph if a == v and b == u])

		if u_strong or v_strong:

			Z = u_strong + v_strong + 2 * eps

			u_ge_v = (u_strong + eps)/Z
			v_ge_u = (v_strong + eps)/Z

			score[u + '>' + v] = u_ge_v
			score[v + '>' + u] = v_ge_u

		else:	

			adj_adv_u = len([a for a,b,c in graph if a == u])
			adj_adv_v = len([a for a,b,c in graph if a == v])

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

############################################################

name = 'deploy' + str(num) 

save_score_both(deploy_out, name, pairs, combo_graph)
