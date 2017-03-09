############################################################
# Module  : Wrong experiment
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
from random import shuffle
from copy import deepcopy
from server  import * 
from prelude import *
import pytest
import numpy as np

import itertools

############################################################
# assets

root       = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
raw_dir    = os.path.join(root   , 'inputs/raw')
label_dir  = os.path.join(raw_dir, 'pairwise_judgements.txt')
edge_dir   = os.path.join(raw_dir, 'all_edges.txt')


############################################################
# construct oracle and maximum a posteori


'''
	@Use: use oracle to generate test data
	      prediction from oracle
	  	  it is of form (adj1, adj2, compare, [adv])
	 	  where compare \in {<, >, =}
'''	
def oracle_test(oracle_data, label_dir, edge_dir):

	(labels, edges) = load_edge_label(label_dir, edge_dir)

	testing = dict()
	
	for s,w,t,_,_,u,v in labels:
		'''
			map (s,w,t) into '<' or '>' or '='
			and make label y where (u,v) => u < v			
		'''
		po, _ = interpret_score(s,w,t)

		if   po == '<': y = [(u,v)]
		elif po == '>': y = [(v,u)]
		else          : y = [(u,v),(v,u)]        

		'''
			load all adverbs found in document `edges` that modify u
			and similarly for v
			filter out words for which oracle have no data

			for now they're sets
		'''
		# u_advs = set([adv for [a,_,adv] in edges if a == u and adv in oracle_data])
		# v_advs = set([adv for [a,_,adv] in edges if a == v and adv in oracle_data])
		u_advs = [adv for [a,_,adv] in edges if a == u and adv in oracle_data]
		v_advs = [adv for [a,_,adv] in edges if a == v and adv in oracle_data]

		testing[(u,v)] = {'order': po, u: u_advs, v: v_advs, 'label': y}

	return testing

'''
	@Use: each adverb is a three sided die over {I,D,N}
	      determine MAP estimate of parameter from data
	      and output 
	@Input: oracle_data dictionary from function `oracle`

'''
def mle_probs(oracle_data):

	'''
		generate training data from oracle
		it is of form (adverb, label)
	'''
	training = []

	for adv,d in oracle_data.iteritems():
		ts = [(adv,l) for _,_,_,l in d]
		training += ts

	'''
		find MAP probs 
	'''
	eps       = 1e-3
	adv_probs = dict()

	for adv,L in training:
		if adv not in adv_probs:
			adv_probs[adv] = dict(zip(LABEL, [0]*len(LABEL)))
		adv_probs[adv][L] += 1.0

	for adv,d in adv_probs.iteritems():
		bot = sum(d.values()) + 3 * eps
		for L in d:
			d[L] = (d[L] + eps)/bot

	return adv_probs


############################################################
'''
	predict on training data
'''


'''
	@Use: define total ordering on label so that we have:
	      deintense > neutral > intense
	      note this reflects the order on the adjectives
	      they modify
'''
# decide_label :: LABEL -> LABEL -> Bool
def label_gt(LABEL,l1,l2):
	return l1 == LABEL[-1] and l2 != LABEL[-1] \
	or     l1 == LABEL[0]  and l2 == LABEL[1]  

def label_lt(LABEL,l1,l2):
	return not label_gt(LABEL,l1,l2) \
	   and l1 != l2


def is_label(event,L):
	return [e for e in event if e == L]


'''
	Filter events by
	category L has majority
	zip result of each event with 
	its respective advers
'''
def majority(events,advs,L):
	most = len(events[0])/2 + 1
	return [zip(e,advs) for e in events if len(is_label(e,L)) >= most]	                                 

'''
	@Use: like sum(list) but mult(list)
'''
def mult(xs):
	return reduce(lambda x,y : x * y, xs)

'''
	@Use: given a set of events and distribution D,
	      find probability of set of events
	      so if events = {e1, ... en}, we do:
	      Pr(e1 or e2 or ... or en)
'''
def Pr(events,D):
	return sum(mult([D[adv][L] for L,adv in e]) for e in events)

'''
	@Use: given two vector of probabilities (p_netural, p_intese, p_deintense)
	      ouput ordering [(u,v)] interpreted as u < v
	      or [(u,v),(v,u)]       interpreted as u = v
'''
def rank_heu(LABEL,u,v,u_vec,v_vec):

	u_vec = [(u_vec[0], LABEL[0]), (u_vec[1], LABEL[1]), (u_vec[-1], LABEL[-1])]
	v_vec = [(v_vec[0], LABEL[0]), (v_vec[1], LABEL[1]), (v_vec[-1], LABEL[-1])]

	(u_prob,u_label) = max(u_vec, key = lambda (p,a) : p)
	(v_prob,v_label) = max(v_vec, key = lambda (p,a) : p)

	if u_label != v_label:
		if   label_lt(LABEL,u_label,v_label): 
			order = [(u,v)]
		else: 
			order = [(v,u)]
	else:
		if   u_label == LABEL[0]: 
			order = [(u,v),(v,u)]
		elif u_label == LABEL[1]: 
			if u_prob > v_prob: order = [(u,v)]
			else:               order = [(v,u)]
		elif u_label == LABEL[-1]:
			if u_prob > v_prob: order = [(v,u)]
			else:               order = [(u,v)]

	return order

def rank_pair(LABEL,probs,data,u,v):

	'''
		pick out adverbs associated with each word
	'''
	u_adv = data[u]
	v_adv = data[v]

	'''
		generate all possible events of 
		n and m independent rolls of dies for 
		n = number of adverbs for u, and m = number of adverbs for v

		Since this value is intractable as I state it,
		do something else instead

	u_events = list(itertools.product(LABEL, repeat = len(u_adv)))
	v_events = list(itertools.product(LABEL, repeat = len(v_adv)))

	# Pr[ simple majority of u adverbs are intense ]
	u_intense   = Pr(majority(u_events, u_adv, LABEL[1]), probs)
	# Pr[ simple majority of u adverbs are deintense ]
	u_deintense = Pr(majority(u_events, u_adv, LABEL[-1]), probs)
	# Pr[ simple majority of u adverbs are neutral ]
	u_neutral   = Pr(majority(u_events, u_adv, LABEL[0]), probs)
	# Pr[ simple majority of v adverbs are intense ]
	v_intense   = Pr(majority(u_events, v_adv, LABEL[1]), probs)
	# Pr[ simple majority of v adverbs are deintense ]
	v_deintense = Pr(majority(u_events, v_adv, LABEL[-1]), probs)
	# Pr[ simple majority of v adverbs are neutral ]
	v_neutral   = Pr(majority(u_events, v_adv, LABEL[0]), probs)
	'''

	'''
		unanimous consensus heuristic
	'''
	u_intense   = sum([probs[x][LABEL[1]]  for x in u_adv])/len(u_adv)
	u_neutral   = sum([probs[x][LABEL[0]]  for x in u_adv])/len(u_adv)
	u_deintense = sum([probs[x][LABEL[-1]] for x in u_adv])/len(u_adv)

	v_intense   = sum([probs[x][LABEL[1]]  for x in v_adv])/len(v_adv)
	v_neutral   = sum([probs[x][LABEL[0]]  for x in v_adv])/len(v_adv)
	v_deintense = sum([probs[x][LABEL[-1]] for x in v_adv])/len(v_adv)

	u_vec = [u_neutral, u_intense, u_deintense]
	v_vec = [v_neutral, v_intense, v_deintense]

	u_vec = [x/sum(u_vec) for x in u_vec]
	v_vec = [x/sum(v_vec) for x in v_vec]


	return rank_heu(LABEL,u,v,u_vec,v_vec)

def run_test(LABEL, probs, test):

	correct = dict()
	error   = dict()
	no_data = dict()

	for (u,v),d in test.iteritems():
		if d[u] and d[v]:
			y     = d['label']
			yhat  = rank_pair(LABEL,probs,d,u,v)
			if y == yhat or len(y) == 2 and len(yhat) == 2:
				correct[(u,v)] = d
			else:
				error[(u,v)] = d
			# print '== ranking ' + u + ' and ' + v
		else:
			no_data[(u,v)] = d
			# print '== no data for ' + u + ' and ' + v

	bot = len(correct) + len(error)
	top = len(correct)
	err = top/float(bot)
	print 'error: ' + str(err)
	return err

'''
	Problem: not every pair of adjectives have adverbs associated with them
	solutions:
		- note if one of them don't have data but the other one does
		  then we assume the one w/o is neutral, this is maximum entropy
		- we can consider indegree as well, not just outdegree for ppdb data
		- but for actual corpus we don't have this evidence??
'''

# (LABEL,data) = oracle(label_dir,edge_dir)
# probs        = mle_probs    (data)
# test_data    = oracle_test(data,label_dir, edge_dir)

# set of all adverbs
scores = dict.fromkeys([x for x in probs])

for adv in probs:
	D = deepcopy(probs)

	# set it to 1.0 so there's no effect when multiplying
	D[adv] = {LABEL[0]: 1.0, LABEL[1]: 1.0, LABEL[-1]: 1.0}

	err = run_test(LABEL,D,test_data)
	scores[adv] = err













'''	(1) First we need a function that takes two sets of points
		in a 3D convex hull and decides an ordering

	(2) Next we take variance and confidence into account
	    variance gives you a neighborhood around each
	    point in the convex hall

	    confidence gives you a probability that you're 
	    in this neighbor vs some neighbor + eps

	    we want to first find some function :: R^3 -> R

'''























