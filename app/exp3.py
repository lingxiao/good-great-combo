############################################################
# Module  : Non-working heuristic contagion scheme
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
import itertools
import numpy as np

from nltk import pos_tag
from copy import deepcopy

from server  import * 
from prelude import *


############################################################
# assets

root       = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
raw_dir    = os.path.join(root   , 'inputs/raw')
label_dir  = os.path.join(raw_dir, 'pairwise_judgements.txt')
edge_dir   = os.path.join(raw_dir, 'all_edges.txt')



############################################################
'''
	method subroutines
'''

'''
	@Use: Given adjective `adj` and `edges`
	      find all adverbs that modify `adj`
'''
def get_adverbs(adj,edges):
	return [v for [a,_,v] in edges if a == adj]

'''
	@Use: given adverb, find all adjectives that it
	      modifies
'''
def get_adjectives(adv,edges):	
	return [a for [a,_,v] in edges if v == adv]

def lemmatizer(w):
	return [w + 'er', w + 'est']



'''
	pie = {pie1, ... pieN} where each pie_i maps adverb to:
        Pr[ adv = intensifier ]

	pairs = {(a,b),...} where each entry maps (a,b) to 
		Pr[ a < b ]

'''
def init_param(edges):

	adverbs = set(v.strip() for _,_,v in edges)
	pairs_r = [(a,b) for a,b,_ in edges]
	pairs   = []

	for a,b in pairs_r:
		if (b,a) in pairs: pass
		else             : pairs.append((a,b))

	pie   = dict(zip(adverbs, [0.5]*len(adverbs)))
	pairs = dict(zip(pairs, [0.5]*len(pairs)))

	return (pie, pairs)

'''
	find all adjective1, adjective2, adverb triples
	where adj2 is a superlative or comparative of adj1,
	vice versa
'''
def init_lemma_adverbs(edges):

	adjs = set(join([a,b] for a,b,_ in edges))

	'''
		initalize distinguished adverbs
	'''
	d_advs = {'intense': [], 'deintense': []}

	for w in adjs:
		w_er, w_est = lemmatizer(w)

		'''
			set of all advs that strengthens the weaker adjective
		'''	
		v_intense = [[a,b,v] for a,b,v in edges if \
		             a == w and b == w_er  or       \
		             a == w and b == w_est or       \
		             a == w_er and b == w_est       ]

		'''
			set of all advs that weakens the stronger adjective
		'''
		v_deintense = [[a,b,v] for a,b,v in edges if \
		               a == w_er  and b == w  or     \
	      	           a == w_est and b == w  or     \
	    	           a == w_est and b == w_er      ]

		'''
			set of all advs that is neutral
		'''
		v_neut  = [[a,b,v] for a,b,v in edges if \
		           a == w     and b == w     or  \
		           a == w_er  and b == w_er  or  \
		           a == w_est and b == w_est     ]


		d_advs['intense'  ] += v_intense
		d_advs['deintense'] += v_deintense

	return d_advs

'''
	seed pie and pairs with known information
	about comparative and suplerative adjectives
'''
def seed_params(eps, pie,pairs,lemmas):
	intense   = [i for _,_,i in lemmas['intense']]

	for a,b,v in lemmas['intense']:
		pie[v]        = min(1.0, pie[v] + eps)
		if (a,b) in pairs:
			pairs[(a,b)]  = min(1.0, pairs[(a,b)] + eps)
		elif (b,a) in pairs:
			pairs[(b,a)]  = max(0.0, pairs[(b,a)] - eps)

	for a,b,v in lemmas['deintense']:
		if v not in intense:
			pie[v]       = max(0.0, pie[v] - eps)
			if (a,b) in pairs:
				pairs[(a,b)] = max(0.0, pairs[(a,b)] - eps)
			elif (b,a) in pairs:
				pairs[(b,a)]  = min(1.0, pairs[(b,a)] + eps)


	return (pie,pairs)

'''
	update Pr[v = intense] for every adverb in pie

	TODO: the way you're propagating the 
	      belief to adverbs is too cavalier
	      need to find principle reason 
	      for why it's done

	     you need to consider a propagation
	     scheme where labels of adjectives play a role

	     note: you may not have enough samples to map
         	   stuff onto stuff

        solutions:

	        only update 




'''
def update_pie(eps,edges,pie,pairs):
	for (a1,a2),p_12 in pairs.iteritems():
		'''
			if Pr(a1 < a2) > 1/2, then we have:

				{vi} <- all_advs_modifying a1 so it paraphrase a2
				{ Pr(vi = intense) += eps }
				{vj} <- all_advs_modifying a2 so it paraghrase a1
				{ Pr(vi = intense) -= eps }
		'''
		a1_advs = [v for [a,b,v] in edges if a == a1 and b == a2]
		a2_advs = [v for [a,b,v] in edges if a == a2 and b == a1]

		# a1 < a2
		if p_12 > 0.5 + eps:
			for v in a1_advs:  # all adverbs modifying a1 are intensifying
				pie[v] = min(1.0, pie[v] + eps)
			for v in a2_advs: # all adverbs modifying a2 are deinenstifying
				pie[v] = max(0.0, pie[v] - eps)

		# a1 > a2
		if p_12 < 0.5 - eps:
			for v in a1_advs:  # all adverbs modifying a1 are deintensifying
				pie[v] = max(0.0, pie[v] - eps)
			for v in a2_advs: # all adverbs modifying a2 are inenstifying
				pie[v] = min(1.0, pie[v] + eps)

	return pie

'''
	update Pr[a1 < a2] for every pair in pairs
'''
def update_pair(eps, edges, pie, pairs):
	for (a1,a2),p_12 in pairs.iteritems():

		# only get adverbs that are between a1 and a2
		v_a1 = [v for [a,b,v] in edges if a == a1 and b == a2]
		v_a2 = [v for [a,b,v] in edges if a == a2 and b == a1] 

		''' for each v modifying a1:
			if    Pr[v = intense] > 1/2
			then  Pr[a1 < a2] increases
		'''
		for v in v_a1:
			if pie[v] > 0.5 + eps: 
				pairs[(a1,a2)] = min(1.0, pairs[(a1,a2)] + eps) 
			elif pie[v] < 0.5 - eps:
				pairs[(a1,a2)] = max(0.0, pairs[(a1,a2)] - eps)

		''' for each v modifying a2:
			if    Pr[v = intense] > 1/2
			then  Pr[a1 < a2] decreases
		'''
		for v in v_a2:
			if pie[v] > 0.5 + eps: 
				pairs[(a1,a2)] = max(0.0, pairs[(a1,a2)] - eps)
			elif pie[v] < 0.5 - eps:
				pairs[(a1,a2)] = min(1.0, pairs[(a1,a2)] + eps) 

	return pairs

'''
	@Use: given edges step size eps and 
	      number of rounds epoch,
	      iteratively cluster adverbs
	      to {intense, deintense}
	      and pairwise rank adjectives 
'''
def propagate(eps,epoch,edges):

	(pie,pairs) = init_param(edges)
	lemmas      = init_lemma_adverbs(edges)
	(pie,pairs) = seed_params(eps,pie,pairs,lemmas)

	for k in range(0,epoch):
		(pie,pairs) = prop_step(eps,pie,pairs)
	return (pie,pairs)

def prop_step(eps,pie,pairs):
	pie   = update_pie (eps, pie, pairs)
	pairs = update_pair(eps, pie, pairs) 
	return (pie,pairs)

def to_test(labels,edges):

	test       = dict()
	test_pairs = dict()

	for a1s,a2s,tie,_,_,a1,a2 in labels:
		if a1s > a2s  : y = (a2,a1)
		elif a1s < a2s: y = (a1,a2)
		else:           y = False

		if y:
			test[(a1,a2)] = {a1     : get_adverbs(a1,edges)
			                ,a2     : get_adverbs(a2,edges)
			                ,'gold' : y}

			a1_advs = [v for a,b,v in edges if a == a1 and b == a2]
			a2_advs = [v for a,b,v in edges if a == a2 and b == a1]

			if a1_advs or a2_advs:
				test_pairs[(a1,a2)] = {a1    : a1_advs 
				                      ,a2    : a2_advs
				                      ,'gold': y}

	
	return (test, test_pairs)		               

def predict(eps,rho_intense, rho_deintense, test,pie):

	algo = dict()

	for (a1,a2),d in test.iteritems():

		a1_advs = d[a1]
		a2_advs = d[a2]

		'''
			initialize Pr[a1 < a2]
		'''
		p12 = 0.5

		'''
			Every time a1 co-occur with intensifer
			a1 < a2 more likely
		'''
		for v in a1_advs:
			if pie[v] > 0.5 + rho_intense: 
				p12 = min(1.0, p12 + eps)
			if pie[v] < 0.5 - rho_deintense:
				p12 = max(0.0, p12 - eps)

		'''
			Every time a2 co-occur with intensifer
			a1 < a2 less likely
		'''
		for v in a2_advs:
			if pie[v] > 0.5 + rho_intense: 
				p12 = max(0.0, p12 - eps)
			if pie[v] < 0.5 - rho_deintense:
				p12 = min(1.0, p12 + eps)

		if p12 > 0.5: r = (a1,a2)		
		else        : r = (a2,a1)

		algo[(a1,a2)] = {'gold': d['gold']
		                ,'algo': r
		                ,'prob' : ('Pr[' + a1 + '<' + a2 + ']', p12)}

	# correct
	correct = dict()
	wrong   = dict()

	for (a1,a2),d in algo.iteritems():
		if d['gold'] == d['algo']:
			correct[(a1,a2)] = d
		else:
			wrong[(a1,a2)] = d

	pairwise = float(len(correct))/(len(wrong) + len(correct))

	print ('=== pairwise score ' + str(pairwise))

	return (correct, wrong)

############################################################

eps   = 5e-3

labels,edges = load_edge_label(label_dir,edge_dir)
test         = to_test(labels,edges)

(pie,pairs)  = init_param(edges)
lemmas       = init_lemma_adverbs(edges)
# (pie,pairs)  = seed_params(eps,pie,pairs,lemmas)
'''
for k in range(0,3):
	pie   = update_pie (eps, edges, pie, pairs)
	pairs = update_pair(eps, edges, pie, pairs) 
'''

'''
	split test set into three chunks:
		- test-pairs : where we only test labeled data
		  set that appears as paraghrases in PPDB corpus
		     - test if belief propagation capture anything

		- test-greater: labels sets where a1 > a2

		- test-weaker : labels sets where a1 < a2

'''
# (test, test_pairs) = to_test(labels,edges)

'''
	run two experiments:
		- test if belief propgation is justified
		- test if false greater than is more prevelant
		  than false lesser than
'''
rho_intense   = 0.45
rho_deintense = -0.4

# (algo_pairs_right, algo_pairs_wrong) = \
#  predict( eps
#  	    , rho_intense
#  	    , rho_deintense
#  	    , test
#  	    , pie)
'''
	Observe we have no false greaters, only false lessers
	this means either: 
		- our assignment of adverbs to intense is cavalier
		- there aren't enough weaker adverbs to go around?

	note there are 10 times more intensifer than deintensier

	can solve this using regression so that:
		any deintensifying adverb overwhelms all intensifying 


	you have to somehow decouple semantics from frequency?
	but isn't semantics a function of frequency?

	need to work on product of distributions, not sum of distributions
	which is what you're doing by summing

	this fact needs to be used when inducting probabilities 
	across multiple graphs

	for all stuff where there's no pair in PPDB
	start doing breadth first search on graph until 
	you find an edge where both vertices are in PPDB
	then propagate information from there


	in unsupervised setting:
	  you propagate the infromation from authority to citzen
	  in some principled way

	  for every edge:
	  	consider every pair

	  for every pair:
	  	consider every edge

 	  	

	in supervised setting:
		maximized the joint distribution between ordering 
		and adverb parameters

	vertices are adverbs over {-1,+1}		
	and edge are pairs (?) of adjectives?
	directions of pairs indicate (a,b) or (b,a)?
'''

# false_lesser  = dict()    # Pr[ guess a < b | gold a > b]  = 1.0
# false_greater = dict()    # Pr[ guess a > b | gold a < b]  = 0.0

# for a12,d in algo_pairs_wrong.iteritems():
# 	if d['prob'] > 0.5: false_lesser [a12] = d
# 	else              : false_greater[a12] = d


# print ('error : ', float(len(algo_pairs_right))/(len(algo_pairs_wrong) + len(algo_pairs_right)))
# print ('Pr[ guess a < b | gold a > b] :', len(false_lesser) )
# print ('Pr[ guess a > b | gold a < b] :', len(false_greater))









































