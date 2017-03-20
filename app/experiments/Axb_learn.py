############################################################
# Module  : Determine value of adverbs that minimize error
#           on data
# Date    : December 22nd
# Author  : Xiao Ling

# 9 tb , 4tb free (spinning disk)

############################################################

import os
import re
import datetime
import operator
import random
import itertools
from copy import deepcopy
import numpy as np
import learn_functions

from scripts import * 
from prelude import *

############################################################
'''
	PATHS
'''
root   = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
iedges = os.path.join(root,'inputs/intense.txt'  )
dedges = os.path.join(root,'inputs/deintense.txt')
train  = os.path.join(root,'inputs/train.txt')
test   = os.path.join(root,'inputs/test.txt')
graph  = os.path.join(root,'inputs/raw/all_edges.txt' )

graph  = label_adv(split_comma(open(graph,'r' ).read().split('\n')))

############################################################
'''
	open training data
'''

train = open(train).read().split('\n')
train = [t.split('\t') for t in train if len(t.split('\t')) == 3]
train = [(u,v,w) for [u,v,w] in train]

test  = open(test).read().split('\n')
test  = [t.split('\t') for t in test if len(t.split('\t')) == 3]
test  = [(u,v,w) for [u,v,w] in test]


############################################################
'''
	Iteration 0
'''


'''
	Eval against training data
'''
def evaluate(pre_iter, train):

	x    = read_x(os.path.join(pre_iter['path'], 'x-vector.txt'), pre_iter['x'])
	adjs = sorted(x.items(), key=operator.itemgetter(1))

	sub_graph = [(u,y,v) for u,y,v in train if u in x and v in x]

	result = dict()
	right  = 0.0
	wrong  = 0.0

	for u,y,v in sub_graph:
		u_val = x[u]
		v_val = x[v]

		if u_val > v_val: yhat = '>'
		else:             yhat = '<'

		result[(u,v)] = {u: u_val, v: v_val, 'gold': y, 'algo': yhat}

		if y == yhat: right += 1
		else:	      wrong += 1

	print ('=== pairwise accuracy: ' + str(right/(right + wrong)))

	return result


############################################################
'''
	Run algorithm
'''

subgraph0, known0 = init_adjectives(iedges, dedges)	

d0   = iter0(root, subgraph0, known0)          # known adj, solve for adv 

d1a  = iter_ia(root, d0, graph, 'iter1a')      # known adv, solve for adj
d1b  = iter_ib(root, d1a, graph, 'iter1b')     # known adj, solve for adv

d2a  = iter_ia(root, d1b, graph, 'iter2a')     # known adv, solve for adj
d2b  = iter_ib(root, d2a, graph, 'iter2b')     # known adj, solve for adv

d3a  = iter_ia(root, d2b, graph, 'iter3a')     # known adv, solve for adj
d3b  = iter_ib(root, d3a, graph, 'iter3b')     # known adj, solve for adv

print ('=== test set 1')
d = evaluate(d1a,train)
e = evaluate(d2a,train)
f = evaluate(d3a,train)

print ('=== test set 2')
a = evaluate(d1a,test)
b = evaluate(d2a,test)
c = evaluate(d3a,test)


f = open(os.path.join(root, 'd1a.txt'),'w')

for (u,v),d in a.iteritems():
	f.write('=== ' + u + ', ' + v + '\n')
	f.write(u + ': ' + str(d[u]) + '\n')
	f.write(v + ': ' + str(d[v]) + '\n')
	f.write('gold: ' + d['gold'] + '\n')
	f.write('algo: ' + d['algo'] + '\n')
f.write('=== END')	



