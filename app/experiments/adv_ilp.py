############################################################
# Module  : Naive implementation
# Date    : Feburary 13th 2017
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
from prelude import *

############################################################
'''
	PATHS
'''
root    = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
graph   = os.path.join(root,'inputs/raw/all_edges.txt'   )
iedges  = os.path.join(root,'inputs/intense.txt'  )
dedges  = os.path.join(root,'inputs/deintense.txt')

############################################################
'''
	open Veronica's raw graph
'''
graph  = label_adv(split_comma(open(graph,'r' ).read().split('\n')))

############################################################
'''
	Open and process gold CCB standard
'''
gold_m = os.path.join(root, 'inputs/testset-ccb.txt' )
gold_m = open(gold_m,'r').read().split('===')[1:-1]
gold_m = [rs.split('\n') for rs in gold_m if rs.split('\n')]
gold_m = [(rs[0],rs[1:-1]) for rs in gold_m]
golds  = dict([(key,[r.split(', ') for r in val]) for key,val in gold_m])

############################################################
'''
	solve for adverbs by initalizing with known
	base/comparative/superlative adjective triples
'''
subgraph0, known0 = init_adjectives(iedges, dedges)	

d0   = iter0(root, subgraph0, known0)     

d1a  = iter_ia(root, d0 , graph, 'iter1a')
d1b  = iter_ib(root, d1a, graph, 'iter1b')

d2a  = iter_ia(root, d1b, graph, 'iter2a')
d2b  = iter_ib(root, d2a, graph, 'iter2b')

############################################################
'''
	Now compute score using adv values used before
'''
def to_score_two_sided(pairs,adverbs,graph):
	score = dict()
	eps   = 1e-3

	for u,v in pairs:

		v_strongs = [(a,b,c) for a,b,c in graph \
		            if a == u and b == v \
		            and c in advs]
		u_strongs = [(a,b,c) for a,b,c in graph \
		            if a == v and b == u 
		            and c in advs]

		v_strong = sum(adverbs[v] for _,_,v in v_strongs) + eps
		u_strong = sum(adverbs[v] for _,_,v in u_strongs) + eps
		Z        = v_strong + u_strong + 2 * eps
		score[u + '>' + v] = u_strong/Z
		score[v + '>' + u] = v_strong/Z

	return score

def to_score_both(pairs, adverbs, graph):

	score = dict()
	eps   = float(1e-3)

	for u,v in pairs:

		v_strongs = [(a,b,c) for a,b,c in graph \
		            if a == u and b == v \
		            and c in advs]
		u_strongs = [(a,b,c) for a,b,c in graph \
		            if a == v and b == u 
		            and c in advs]

		v_strong = sum(adverbs[v] for _,_,v in v_strongs) 
		u_strong = sum(adverbs[v] for _,_,v in u_strongs)

		if u_strong or v_strong:

			Z = u_strong + v_strong + 2*eps
			score[u + '>' + v] = (u_strong + eps)/Z
			score[v + '>' + u] = (v_strong + eps)/Z

		else:	

			v_strongs = [(a,b,c) for a,b,c in graph if a == u \
						and c in advs]

			u_strongs = [(a,b,c) for a,b,c in graph \
			            if a == v
			            and c in advs]

			v_strong = sum(adverbs[v] for _,_,v in v_strongs) + eps
			u_strong = sum(adverbs[v] for _,_,v in u_strongs) + eps


			Z = u_strong + v_strong + 2*eps

			score[u + '>' + v] = u_strong/Z
			score[v + '>' + u] = v_strong/Z

	return score

def to_score_one_sided(pairs,adverbs,graph):

	score = dict()
	eps   = 1e-3

	for u,v in pairs:

		v_strongs = [(a,b,c) for a,b,c in graph if a == u \
					and c in advs]

		u_strongs = [(a,b,c) for a,b,c in graph \
		            if a == v
		            and c in advs]

		v_strong = sum(adverbs[v] for _,_,v in v_strongs) + eps
		u_strong = sum(adverbs[v] for _,_,v in u_strongs) + eps

		Z = u_strong + v_strong + 2*eps

		score[u + '>' + v] = u_strong/Z
		score[v + '>' + u] = v_strong/Z

	return score

'''
	@Use  : Given graph dictionary and gold, output algo
	@Input: `graph`: a list of all vertices in graph
	         `gold`  : a list of list of form [[a1],[a2,a3],[a4],...]
                       where each word in list_i < list_{i+1} 
	@Ouptut: A dictionary with:
				- gold standard
				- ilp solution
				- pairwise accuracy
				- Kendall's tau
'''
def ilp(to_score, gold, adverbs, graph):

	'''
		construct variables
	'''
	words   = join(gold)
	pairs   = [(u,v) for u in words for v in words if u != v]

	triples = [(u,v,w) for u in words for v in words for w in words
	      if u != v and v != w and u != w]

	'''
		Score to maximize
	'''
	score = to_score(pairs,adverbs,graph)

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
	objective = [ score[u+'>'+v]     *      variables[u+'='+v]  \
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

	return {'gold'     : gold
     	    ,'algo'    : algo
	 	    ,'tau'     : tau(gold,algo)
		    ,'pairwise': pairwise_accuracy(gold,algo)
		    ,'raw-score': score}

############################################################
'''
	Run test with ilp method
'''
def run_test():
	'''
		Test all three algo on CCB data
	'''	
	results_one_sided = dict()
	results_two_sided = dict()
	results_both      = dict()

	for words,ranking in golds.iteritems():
		results_one_sided[words] = ilp(to_score_one_sided, ranking, adverbs, graph)
		results_two_sided[words] = ilp(to_score_two_sided, ranking, adverbs, graph)
		results_both     [words] = ilp(to_score_both     , ranking, adverbs, graph)

	tau1     = sum(r['tau']      for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	abs_tau1 = sum(abs(r['tau']) for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	pair1    = sum(r['pairwise'] for _,r in results_one_sided.iteritems())/float(len(results_one_sided))

	tau2      = sum(r['tau']      for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	abs_tau2  = sum(abs(r['tau']) for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	pair2     = sum(r['pairwise'] for _,r in results_two_sided.iteritems())/float(len(results_two_sided))

	tau3      = sum(r['tau']      for _,r in results_both.iteritems())/float(len(results_both))
	abs_tau3  = sum(abs(r['tau']) for _,r in results_both.iteritems())/float(len(results_both))
	pair3     = sum(r['pairwise'] for _,r in results_both.iteritems())/float(len(results_both))


	results1 = {'ranking'  : results_one_sided
	              ,'tau'      : tau1
	              ,'|tau|'    : abs_tau1
	              ,'pairwise' : pair1}

	results2 = {'ranking'  : results_two_sided
	              ,'tau'      : tau2
	              ,'|tau|'    : abs_tau2
	              ,'pairwise' : pair2}


	results3 = {'ranking'  : results_both
	              ,'tau'      : tau3
	              ,'|tau|'    : abs_tau3
	              ,'pairwise' : pair3}


	print ('=== one sided: tau: '  + str(results1['tau']) + ', |tau|: ' + str(results1['|tau|']) + ', pairwise: ' + str(results1['pairwise']))
	print ('=== two sided: tau: '  + str(results2['tau']) + ', |tau|: ' + str(results2['|tau|']) + ', pairwise: ' + str(results2['pairwise']))
	print ('=== both sided: tau: ' + str(results3['tau']) + ', |tau|: ' + str(results3['|tau|']) + ', pairwise: ' + str(results3['pairwise']))

	return (results1, results2, results3)

############################################################
'''
	naive adjective value ranking
'''

def run_Ab_test(adjectives):

	adj_results = dict()

	for key,gold in golds.iteritems():
		words  = [(w,adjectives[w]) for w in join(gold)]
		words.sort(key = lambda x : x[1])
		algo   = [[w] for w,_ in words]

		d = {'gold'    : gold
	     	,'algo'    : algo
		 	,'tau'     : tau(gold,algo)
			,'pairwise': pairwise_accuracy(gold,algo)
			,'raw-score': dict(words)}

		adj_results[key] = d

	taus     = sum(r['tau']      for _,r in adj_results.iteritems())/len(adj_results)
	abs_taus = sum(abs(r['tau']) for _,r in adj_results.iteritems())/len(adj_results)
	pairs    = sum(r['pairwise'] for _,r in adj_results.iteritems())/len(adj_results)

	results = {'ranking'  : adj_results
	          ,'tau'      : taus
	          ,'|tau|'    : abs_taus
	          ,'pairwise' : pairs}

	return results	          

############################################################
'''
	Run and save results
'''
if False:

	adverbs = dict(d2a['words'])

	results1, results2, results3 = run_test()

	save(results1, root, 'ccb-adv-ilp-one-sided')
	save(results2, root, 'ccb-adv-ilp-two-sided')
	save(results3, root, 'ccb-adv-ilp-both'     )

	f = open(os.path.join(root,'adverbs.txt'),'w')

	for v,n in adverbs.iteritems():
		f.write(v + ': ' + str(n) + '\n')
	f.close()	


if True:
	adjectives = dict(d2b['words'])
	results4   = run_Ab_test(adjectives)
	save(results4, root, 'ccb-least-squares')

	f = open(os.path.join(root,'adjectives.txt'),'w')

	for v,n in adjectives.iteritems():
		f.write(v + ': ' + str(n) + '\n')
	f.close()	













