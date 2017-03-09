############################################################
# Module  : Naive implementation
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import re
import time
import datetime
import operator
import random
import itertools	
from copy import deepcopy
import numpy as np

from pulp    import *

from prelude import *

############################################################
'''
	PATHS
'''
root    = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
golds   = os.path.join(root, 'inputs/rankings.txt'       )
adj_adv = os.path.join(root, 'adjective-adverb-count.txt')
graph   = os.path.join(root,'inputs/raw/all_edges.txt'   )

############################################################
'''
	open Veronica's raw graph
'''
graph  = label_adv(split_comma(open(graph,'r' ).read().split('\n')))

'''	
	open adjective-adverb-count
'''
adj_adv = [r.split('\t') for r in open(adj_adv,'r').read().split('\n') if len(r.split('\t')) == 2]
adj_adv = dict([(a,float(b)) for a,b in adj_adv])

'''
	open and process Ellie's golds
	format:
		worker id <tab> cluster name <tab> cluster number <tab> ranked list
'''
def to_rank(x):
	xs = x.split('->')
	ys = [x.replace('{','').replace('}','').strip() for x in xs]
	zs = [r.split(',') for r in ys] 
	return fmap(lambda xs : [x.strip() for x in xs], zs)

def to_key(rank):
	return tuple(set(join(rank)))

raw_golds = open(golds).read().split('\n')
raw_golds = [l.split('\t') for l in raw_golds if l.split('\t')][0:-2]

'''
	Split into:
		(1) golds: key  : (a1,a2,...) in alphabetical order
					value: [[[ai],[ak]...],[...],...]
						   list of rankings, each ranking
						   given by a worker
						   each ranking is a list of list of words
						   where words in list_i is less intense
						   than words in list_{i+1}
						   and all words in list_i are tied
'''
golds = dict()

for wid, name, number, rank in raw_golds:

	r = to_rank(rank)
	k = to_key(r)

	if k in golds:
		golds[k].append(r)
	else:
		golds[k] = [r]

'''
	save gold standard
'''	
f = open(os.path.join(root,'ellie-all.txt'), 'w')

for _,gold_list in golds.iteritems():
	for gold in gold_list:
		words = join(gold)
		f.write('=== ' + words[0] + ', ' + words[1] + ' ***\n')
		for ws in gold:
			line = ', '.join(ws)
			f.write(line + '\n')
f.write('=== END')	
f.close()



############################################################
'''
	Get scores for all adjectives

	Our hypothesis is that almost all adverbs are intensifiers,
	so as an upper bound we let all adverbs be intensifiers,
	so adjectives associating with more adverbs are more likely
	to be weaker

'''
def to_score_one_sided(pairs,adj_adv,graph):

	score = dict()
	eps   = 1e-3

	for u,v in pairs:
		Z            = adj_adv[u] + adj_adv[v] + 2*eps

		score[u + '>' + v] = (adj_adv[u] + eps)/Z
		score[v + '>' + u] = (adj_adv[v] + eps)/Z

	return score


############################################################

words = ('positive','encouraging','sweet')
gold  = golds[words][0]
pairs = [(u,v) for u in words for v in words if u != v]
triples = [(u,v,w) for u in words for v in words for w in words
	      if u != v and v != w and u != w]
score = to_score_one_sided(pairs,adj_adv,graph)


'''
	construct solver
'''
prob =  LpProblem ('='.join(words), LpMaximize)


'''
	variables where u-v imples u > v
''' 
variables = dict()

for u,v in pairs:
	uv = u +'='+ v
	variables[uv] = LpVariable('s_' + uv, 0,1, LpInteger)


'''
	objective function
'''
objective = [ score[u+'>'+v]   * variables[u+'='+v]  \
	        for u,v in pairs] \
          + [ score[v + '>'+  u] * (1 - variables[u+'='+v]) \
            for u,v in pairs]


prob += lpSum(objective)  


# constraints
for i,j,k in triples:
	prob += (1 - variables[i + '=' + j]) \
	     +  (1 - variables[j + '=' + k]) \
	     >= (1 - variables[i + '=' + k])


'''
	output ranking
'''
prob.solve()
algo = prob_to_algo_rank(prob,words)























































