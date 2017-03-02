# ############################################################
# # Module  : Applicaton Main
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import re
import datetime
import itertools
import numpy as np

from nltk import pos_tag
from copy import deepcopy

import numpy as np

from scripts import * 
from prelude import *

# ############################################################
# '''
# 	PATHS
# '''

# root       = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
# edges      = os.path.join(root,'inputs/small_edges.txt'     )
# iedges     = os.path.join(root,'inputs/intense.txt'         )
# dedges     = os.path.join(root,'inputs/deintense.txt'       )
# test       = os.path.join(root,'inputs/raw/pairwise_judgements.txt')
# all_edges  = os.path.join(root,'inputs/raw/all_edges.txt')


# ############################################################
# '''
# 	TRAINING SET
# '''

# # preprocessing functions
# strip       = lambda ls : (ls[0].strip(), ls[1].strip(), ls[2].strip())
# split_comma = lambda xs : [ strip(x.split(',')) for x in xs if len(x.split(',')) == 3]
# split_tab   = lambda xs : [ x.split('\t') for x in xs]


# '''
# 	Load all edges from PPDB
	
# 	Load parts of edges from ppdb so that 
# 		- known intensity edges `iedges`
# 		- known deintense edges `dedges`
# 		- unknown edges `edges`, note these are useful only 
# 		  to give greater coverage for adverbs not covered by 
# 		  intense and deintense
# '''
# # training set used to determine optimal value of adverbs
# # edges      = split_comma(open(edges,'r' ).read().split('\n'))
# edges      = []
# iedges     = split_comma(open(iedges,'r').read().split('\n'))
# dedges     = split_comma(open(dedges,'r').read().split('\n'))

# ############################################################
# '''
# 	TEST SET
# '''

# '''
# 	load entire testing set annoated by turks	
# 	load entire PPDB graph `all edges`
# '''
# test       = split_tab  (open(test,'r').read().split('\n'))[0:-1]
# test       = [(float(x),float(y),float(t),a1,a2) \
#              for m,x,y,t,_,_,a1,a2 in test if float(m) == 3.0]
# test       = [mark_label(t) for t in test]

# all_edges  = split_comma(open(all_edges,'r' ).read().split('\n'))


# ############################################################
# # Get adverbs, adjectives, and make Data matrix

# advs = list(set(v for _,_,v in edges + iedges + dedges))
# adjs = list(set([a for a,_,_ in edges + iedges + dedges] \
# 	 + [a for _,a,_ in edges + iedges + dedges]))

# data = iedges + dedges + edges

# ############################################################
# # Build A, b, x

# '''
# 	initialize superlatives and their values
# '''
# base_val        = 1.0/4
# superlative_val = 2.0/3
# comparative_val = 1.0/2
# base            = ['warm'   , 'rich'   , 'fair'   ]
# superlatives    = ['warmest', 'richest', 'fairest']
# comparatives    = ['warmer' , 'richer' , 'fairer' ]

# bfixed = dict(zip(base         , [base_val]        * len(base        )))
# cfixed = dict(zip(comparatives , [comparative_val] * len(comparatives)))
# sfixed = dict(zip(superlatives , [superlative_val] * len(superlatives)))
# fixed  = dict(bfixed.items()   + cfixed.items()    + sfixed.items()    )

# '''
# 	Environemental dictionary
# '''
# env = {'adjs' : adjs 		 # all adjectives found in graph
#       ,'advs' : advs         # all adverbs found in graph
#       ,'data' : data         # entire graph

#       ,'base'         : bfixed # all base adjectives with fixed value
#       ,'comparatives' : cfixed # all comparatives and their value
#       ,'superlatives' : sfixed # all superlatives and their value
#       }


# '''
# 	Prep A and b, save to disk
# '''
# A,b,x_lookup = prep_Ab(root,env)

# '''
# 	Read solution from matlab
# '''
# solution = read_solution(root,env,x_lookup)

# '''
# 	Now test `solution` on test data

# 	Find all adjectives in PPDB graph
# 	related to test words
# '''
# cliques = []

# for a1,_,a2 in test:

# 	# find all edges linking to a1
# 	a1_clique = [(a1,y, v) for (x,y,v) in all_edges if a1 == x] \
# 	          + [(x,a1, v) for (x,y,v) in all_edges if a1 == y]

# 	a2_clique = [(a2,y, v) for (x,y,v) in all_edges if a2 == x] \
# 	          + [(x,a2, v) for (x,y,v) in all_edges if a2 == y]

# 	cliques += a1_clique + a2_clique

# cliques  = set(cliques)
# test_set = [(a,b,v) for a,b,v in cliques if a != b]

# # run test set for which we know v, and don't know a and b
# test_set_small = [(a,b,v) for a,b,v in test_set \
#                   if  v in solution['x']     \
#                   and a not in solution['x'] \
#                   and b not in solution['x'] ]

# '''
# 	Construct A,x,b matrix from test data
# '''
# x_test = list(set(join([a,b] for a,b,_ in test_set_small)))  # vector of adjectives
# b_test = [solution['x'][v] for _,_,v in test_set_small]      # vector of adverbs
# A_test = []

# for a1,a2,v in test_set_small:
# 	row = [0]*len(x_test)
# 	row[x_test.index(a1)] = -1.0
# 	row[x_test.index(a2)] =  1.0
# 	A_test.append(row)

# '''
# 	Save as text file for matlab solver
# '''
# row_str = lambda r : ','.join([str(x) for x in r])
# A_path  = os.path.join(root,'outputs/A-matrix-test.txt')
# f       = open(A_path,'w')
# A_save  = [row_str(r) for r in A_test]

# save_list(f,A_save)
# f.close()

# b_path = os.path.join(root,'outputs/b-vector-test.txt')
# h      = open(b_path,'w')
# bstr   = '\n'.join(str(x) for x in b_test)
# h.write(bstr)
# h.close()
 
# '''
# 	Read matlab solution
# '''
# x_test_sol = open(os.path.join(root,'outputs/x-vector-test.txt'),'r').read().split('\n')[0:-1]
# x_sol      = dict(zip (x_test, [float(n) for n in x_test_sol]))


# '''
# 	Rank based on solution
# '''



# right = dict()
# wrong = dict()
# both  = dict()

# r = 0
# w = 0

# for a1,y,a2 in test:
# 	if a1 in x_test and a2 in x_test:
# 		a1_v = x_sol[a1]
# 		a2_v = x_sol[a2]

# 		if a1_v > a2_v  : y_hat = '<'
# 		elif a1_v < a2_v: y_hat = '>'
# 		else            : y_hat = '=='

# 		d = {a1   : a1_v  \
#            , a2   : a2_v  \
#            ,'gold': y     \
#            ,'algo': y_hat }

# 		if y == y_hat: 
# 			right[(a1,a2)] = d
# 			r += 1.0
# 		else: 
# 			wrong[(a1,a2)] = d
# 			w += 1.0

# 		both[(a1,a2)] = d



# '''
# 	Test on data
# 	so we know intensity of adverbs
# 	solve them for (a1,a2,v) pairs

# 	grab a set of data from training set and 
# 	test for error

# 	(1) inference is done by for each a1,a2 pair:

# 		find all (a1,a2,v)_i and (a2,a1,v)_j triples
# 		and we have system of equations:

# 		a1 + v = a2            (ith data point)
# 		==>
# 		a1 - a2 = v         

# 		x = (x1,x2) 
# 		A = [1_vec, -1_vec]
# 		b = [v_vec]

# 		solve for Ax = b
# 		where x1,x2 \in [-1,1]

# 	(2) we can also do global inference all all
# 	    (ai,aj) pairs by:

# 	    min || Ax - b ||_norm
# 	    s.t. all x_i \in [-1,1]

# 	    Then rank and output solution


# 	(3) Tomorrow: 
# 	      1. implement this idea
# 	      2. find set of examples in the graph
# 	         so that the error on labeled set is
# 	         minimized
# 	      3. Find regularizers until we arrive at 
# 	         same error rate
# '''




# # '''
# # 	check quality of solution on data
# # '''
# # errs = [(a1,a2,v,x[a1],x[v],x[a2],\
# #  	     x[a1] + words[v] - x[a2])    \
# #          for a1,a2,v in data]

# # total_err = sum(n for _,_,_,_,_,_,n in errs)






















