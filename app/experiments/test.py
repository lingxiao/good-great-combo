############################################################
# Module  : Sanity check output of process
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import operator
import numpy as np

from scripts import * 
from prelude import *

############################################################
# Assets
'''
	get labeled pairs
'''
test_path  = os.path.join(root,'inputs/raw/pairwise_judgements.txt')
test_raw   = split_tab  (open(test_path,'r').read().split('\n'))[0:-1]
test_raw   = [(float(x),float(y),float(t),a1,a2)    \
             for m,x,y,t,_,_,a1,a2 in test_raw       \
             if unanimous(float(x),float(y),float(t))]

test_ties  = list(set(mark_label(t) for t in test_raw))

test       = dict()

for a1,y,a2 in test_ties:
	if y != '==': test[(a1,a2)] = {'y': y}

############################################################
'''
	Sanity check output of Iteraion 1b: 60 percent 

	Read in solution from matlab
'''
x1   = read_x(os.path.join(root, 'outputs/x-vector-1.txt'), x_lookup1)


'''
	@Input: Dict Adjective value, Dict (Adj, Adj) {'y': string}
	@Use  : Given current set of solved adjectives so far
	        

'''
def filter_adjectives(adj, labels):

	'''
		get test `intersect` subgraph1
	'''
	test_subgraph1 = dict()

	rightd = dict()
	wrongd = dict()

	right  = 0.0
	wrong  = 0.0

	for (a1,a2),d in labels.iteritems():
		vs = [(x,y,v) for x,y,v in subgraph1 if x == a1 and y == a2]
		if vs:

			y    = d['y']
			v_a1 = adj[a1]
			v_a2 = adj[a2]

			if v_a1 > v_a2: yhat = '>'
			else: 	        yhat = '<'	

			d = {a1: v_a1, a2: v_a2, 'y': y, 'yhat': yhat}

			if y == yhat:
				right += 1
				rightd[(a1,a2)] = d

			else:
				wrong += 1
				wrongd[(a1,a2)] = d

			test_subgraph1[(a1,a2)] = d

	print ('===: ', right/(right + wrong))



############################################################
'''
	Sanity check quality of solution from round0: 100 percent

	Predict outcome using simple addition heuristic
	for base, compare, super adjectivs
		val ai = sum [vi | (ai,_,vi) <- subgraph0 ]

	this makes sense under simple addition

pairs0 = list(set((a1,a2) for a1,a2,_ in subgraph0))
test0  = dict()

for a1,a2 in pairs0:

	a1_advs = sum(x0[v] for x,_,v in subgraph0 if x == a1)
	a2_advs = sum(x0[v] for y,_,v in subgraph0 if y == a2)

	if a1_advs > a2_advs: 
		yhat = a1 + ' < ' + a2
	else:
		yhat = a1 + ' > ' + a2

	test0[(a1,a2)] = {a1: a1_advs, a2: a2_advs , 'yhat': yhat}

'''






