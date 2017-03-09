# ############################################################
# # Module  : Applicaton Main
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import numpy as np
import operator

from scripts import * 
from prelude import *

############################################################
'''
	PATHS
'''
root      = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
test      = os.path.join(root,'inputs/raw/pairwise_judgements.txt')
all_edges = os.path.join(root,'inputs/raw/all_edges.txt')

############################################################
'''
	READ TRAINING SET SOLUTION 
'''
solution = read_solution(root,env,x_lookup)
x_sol    = solution['x']
advs     = solution['adverbs']
adjs     = solution['adjectives']
adj_adv  = solution['all']

adverbs = sorted(advs.items(), key=operator.itemgetter(1))

############################################################
'''
	TEST SET:
		- keep only unanimous labeled pairs
'''
def unanimous(x,y,t):
	return x != 0 and y == 0 and t == 0 \
	or     x == 0 and y != 0 and t == 0 \
	or 	   x == 0 and y == 0 and t != 0

all_edges  = split_comma(open(all_edges,'r' ).read().split('\n'))


test_raw   = split_tab  (open(test,'r').read().split('\n'))[0:-1]

test       = [(float(x),float(y),float(t),a1,a2)    \
             for m,x,y,t,_,_,a1,a2 in test_raw       \
             # if float(m) == 2.0]
             if unanimous(float(x),float(y),float(t))]

test       = list(set(mark_label(t) for t in test))

test_set   = {}

for a,y,b in test:
	if (a,b) in test_set:
		test_set[(a,b)].append((a,y,b))
	else:
		test_set[(a,b)] = [(a,y,b)]

'''
	divide test set into repated and non-repeated labels
'''
no_repeat = []
repeated  = {}

for (a,b),d in test_set.iteritems():
	if len(d) > 1: repeated[(a,b)]  = d
	else         : no_repeat.append(d[0])


############################################################
'''
	TEST I: we want to know whether the learned adverbs
	        correctly predict labeled pairs that:
	           - appear in all_edges
	           - related to each other at those adverbs learned
'''
def make_set_set_1(no_repeat, all_edges, x_sol):
	test_set_1 = dict()

	for a,y,b in no_repeat:
		edges = [(a1,a2,v) for a1,a2,v in all_edges \
		        if a == a1 and b == a2 \
		        or a == a2 and b == a1 ]
		edges = [(a1,a2,v) for a1,a2,v in edges if v in x_sol]		       

		test_set_1[(a,b)] = {'gold' : y
		                    ,'edges': edges}

	return test_set_1

test_set_1 = make_set_set_1(no_repeat, all_edges, x_sol)	                 

'''
	Try this heuristic: add all adverbs associated with each one
'''

right = 0
wrong = 0

for (a1,a2),d in test_set_1.iteritems():
	edges      = d['edges']
	a1_adverbs = sum([x_sol[v] for x,_,v in edges if x == a1])
	a2_adverbs = sum([x_sol[v] for x,_,v in edges if x == a2])


	if a1_adverbs > a2_adverbs: yhat = '<'
	else                      : yhat = '>'

	d[a1] = a1_adverbs
	d[a2] = a2_adverbs
	d['algo'] = yhat

	print ('------- ' + y + ', ' + yhat + '\n')
	print ('=== (' + a1 + ', ' + a2 + ') : (' + str(a1_adverbs) + ', ' + str(a2_adverbs) + ')')
	print ('='*20)

	if y == yhat: right += 1.0
	else        : wrong += 1.0


print ('=== Accuracy ', right/(right + wrong))

'''
	Now we need to solve for values of each pair (a,b)
	by construction A_a matrix and b_a vector

	- it seems like we can simply invert the matrix
	  otherwise we can:
	  	(1): save all for matlab use
	  			+ know it works
	  			- lots of code
	  	(2): run cvx_python solver
	  			+ potentially less code
	  			- dont know it works
	  			- havnt used it 

'''
a1,a2 = ('valuable','worthwhile')
d     = test_set_1[(a1,a2)]
edges = test_set_1[(a1,a2)]['edges']

x_vector = [a1,a2]
b_vector = [x_sol[v] for _,_,v in edges]
A_matrix = make_A(x_vector, b_vector,edges)

save_Ab(A_matrix,b_vector
	   ,root
	   ,'pairs/A-' + a1 + '-' + a2
	   ,'pairs/b-' + a1 + '-' + a2)

############################################################
'''
	TEST II: we want to know whether the learned adverbs
	        correctly predict labeled pairs that:
	           - appear in all_edges
	           - related to any other words
'''





############################################################
'''
	Build A matrix, x and b vector

	Now propagate values to rest of graph
	where adverbs are known from 
	base, comparative, superlative triples
'''
# for now run only on adverbs where weights are known
# some_edges = [(a,b,v) for a,b,v in all_edges \
#               if v in x_sol                  \
#               and a != b]

# A_t,b_t,x_t = prep_Ab_test(root, solution, some_edges, True)

# ############################################################

'''
	CHECK ACCURACY

	For now run only on labeled pairs whose 
	adjectives also appear in PPDB graph
'''
def do_test():
	x_test_sol = open(os.path.join(root,'outputs/x-vector-test.txt'),'r').read().split('\n')
	x_test_sol = dict(zip(x_t, [float(n) for n in x_test_sol[0:-1]]))

	some_test = [(a,y,b) for a,y,b in test             \
	            if a in x_test_sol and b in x_test_sol \
	            and y != '==']

	right = 0
	wrong = 0

	for a1,y,a2 in some_test:
		a1_val = x_test_sol[a1]
		a2_val = x_test_sol[a2]

		if a1_val > a2_val:
			yhat  = '<'
		else:
			yhat = '>'

		d = {a1     : a1_val
		    ,a2     : a2_val
		    ,'gold' : y
		    ,'algo' : yhat}

		if y == yhat: right += 1
		else:         wrong += 1

		print ('gold: ', a1 + ' ' + y + ' ' + a2)
		print ('algo: ', a1 + ' ' + yhat + ' ' + a2   )
		print (a1 + ': ', a1_val, a2 + ':', a2_val)
		print ('================================\n')

	print (right, wrong)
	print ('== Accuracy: ', float(right)/(right + wrong))
	return x_test_sol

# d = do_test()



