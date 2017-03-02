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
from prelude import *

############################################################
'''
	PATHS
'''
root    = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
golds   = os.path.join(root, 'inputs/rankings.txt'       )
adj_adv = os.path.join(root, 'adjective-adverb-count.txt')
graph   = os.path.join(root,'inputs/raw/all_edges.txt'   )
gold_my = os.path.join(root, 'testset-ellie-my-pick.txt' )

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


'''
	open my gold standard pick
'''
gold_m = os.path.join(root, 'testset-ccb.txt' )
gold_m = open(gold_m,'r').read().split('===')[1:-1]
gold_m = [rs.split('\n') for rs in gold_m if rs.split('\n')]
gold_m = [(rs[0],rs[1:-1]) for rs in gold_m]
gold_ccb = dict([(key,[r.split(', ') for r in val]) for key,val in gold_m])

############################################################
'''
	Get scores for all adjectives

	Our hypothesis is that almost all adverbs are intensifiers,
	so as an upper bound we let all adverbs be intensifiers,
	so adjectives associating with more adverbs are more likely
	to be weaker

'''
def to_score_both(pairs, adj_adv, graph):

	'''
		Score to maximize
	'''
	score = dict()
	eps   = float(1e-4)

	for u,v in pairs:

		v_strong  = len([(a,b,c) for a,b,c in graph if a == u and b == v])
		u_strong  = len([(a,b,c) for a,b,c in graph if a == v and b == u])

		if u_strong or v_strong:
			Z = u_strong + v_strong + 2*eps
			score[u + '>' + v] = (u_strong + eps)/Z
			score[v + '>' + u] = (v_strong + eps)/Z
		else:	
			Z = adj_adv[u] + adj_adv[v] + 2*eps

			score[u + '>' + v] = (adj_adv[v] + eps)/Z
			score[v + '>' + u] = (adj_adv[u] + eps)/Z

	return score

def to_score_one_sided(pairs,adj_adv,graph):

	score = dict()
	eps   = 1e-3

	for u,v in pairs:
		Z            = adj_adv[u] + adj_adv[v] + 2*eps

		score[u + '>' + v] = (adj_adv[v] + eps)/Z
		score[v + '>' + u] = (adj_adv[u] + eps)/Z

	return score

def to_score_two_sided(pairs,adj_adv,graph):
	score = dict()
	eps   = 1e-3

	for u,v in pairs:
		v_strongs = [(a,b,c) for a,b,c in graph if a == u and b == v]
		u_strongs = [(a,b,c) for a,b,c in graph if a == v and b == u]
		u_strong  = len(u_strongs) + eps
		v_strong  = len(v_strongs) + eps
		Z         = float(u_strong + v_strong + 2 * eps)
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
def ilp(to_score, gold, adj_adv, graph):

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
	score = to_score(pairs,adj_adv,graph)

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


'''
	Take the subset of gold standard where there's
	unanimous agreement in ranking	
'''
gold_unanimous = dict()
for words,rankings in golds.iteritems():
	rs = [r for r in rankings if len(r) == len(words)]
	if len(rs) == 1: 
		gold_unanimous[words] = rs[0]


f = open(os.path.join(root,'ellie-unanimous.txt'),'w')

for words,ranking in gold_unanimous.iteritems():
	u = words[0]
	v = words[-1]
	f.write('=== '+ u + ', ' + v + ' **\n')
	for [x] in ranking:
		f.write(x + '\n')
f.write('=== END')
f.close()



'''
	Test all three algo on labled with no ties
results_one_sided = dict()
results_two_sided = dict()
results_both      = dict()

for words,ranking in gold_unanimous.iteritems():
	results_one_sided[words] = ilp(to_score_one_sided, ranking, adj_adv, graph)
	results_two_sided[words] = ilp(to_score_two_sided, ranking, adj_adv, graph)
	results_both     [words] = ilp(to_score_both     , ranking, adj_adv, graph)

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


# save(results1, root, 'ilp-one-sided')
# save(results2, root, 'ilp-two-sided')
# save(results3, root, 'ilp-both')


'''

'''
	Test all three algo on CCB data
'''	
def run_test():
	results_one_sided = dict()
	results_two_sided = dict()
	results_both      = dict()

	for words,ranking in gold_ccb.iteritems():
		results_one_sided[words] = ilp(to_score_one_sided, ranking, adj_adv, graph)
		results_two_sided[words] = ilp(to_score_two_sided, ranking, adj_adv, graph)
		results_both     [words] = ilp(to_score_both     , ranking, adj_adv, graph)

	tau1     = sum(r['tau']      for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	abs_tau1 = sum(abs(r['tau']) for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	pair1    = sum(r['pairwise'] for _,r in results_one_sided.iteritems())/float(len(results_one_sided))

	tau2      = sum(r['tau']      for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	abs_tau2  = sum(abs(r['tau']) for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	pair2     = sum(r['pairwise'] for _,r in results_two_sided.iteritems())/float(len(results_two_sided))

	tau3      = sum(r['tau']      for _,r in results_both.iteritems())/float(len(results_both))
	abs_tau3  = sum(abs(r['tau']) for _,r in results_both.iteritems())/float(len(results_both))
	pair3     = sum(r['pairwise'] for _,r in results_both.iteritems())/float(len(results_both))


	ccb_results1 = {'ranking'  : results_one_sided
	              ,'tau'      : tau1
	              ,'|tau|'    : abs_tau1
	              ,'pairwise' : pair1}

	ccb_results2 = {'ranking'  : results_two_sided
	              ,'tau'      : tau2
	              ,'|tau|'    : abs_tau2
	              ,'pairwise' : pair2}


	ccb_results3 = {'ranking'  : results_both
	              ,'tau'      : tau3
	              ,'|tau|'    : abs_tau3
	              ,'pairwise' : pair3}


	'''
		save results
	'''
	save(ccb_results1, root, 'ccb-ilp-one-sided')
	save(ccb_results2, root, 'ccb-ilp-two-sided')
	save(ccb_results3, root, 'ccb-ilp-both')



# ''' 
#   Collect all the negative taus
# '''
# one_negative  = [join(d['gold']) for _,d in results_two_sided.iteritems() if d['tau'] < 0]
# two_negative  = [join(d['gold']) for _,d in results_one_sided.iteritems() if d['tau'] < 0]
# both_negative = [join(d['gold']) for _,d in results_both.iteritems()      if d['tau'] < 0]

# one_positive  = [d for _,d in results_two_sided.iteritems() if d['tau'] > 0]
# two_positive  = [d for _,d in results_one_sided.iteritems() if d['tau'] > 0]
# both_positive = [d for _,d in results_both.iteritems()      if d['tau'] > 0]


# one_taus  = [d['tau'] for d in one_positive]
# two_taus  = [d['tau'] for d in two_positive]
# both_taus = [d['tau'] for d in both_positive]

# one_pairs  = [d['pairwise'] for d in one_positive]
# two_pairs  = [d['pairwise'] for d in two_positive]
# both_pairs = [d['pairwise'] for d in both_positive ]

# print ('one-positive taus: ' , sum(one_taus) /len(one_taus ))
# print ('two-positive taus: ' , sum(two_taus) /len(two_taus ))
# print ('both-positive taus: ', sum(both_taus)/len(both_taus))

# print ('one-positive pairs: ' , sum(one_pairs) /len(one_pairs ))
# print ('two-positive pairs: ' , sum(two_pairs) /len(two_pairs ))
# print ('both-positive pairs: ', sum(both_pairs)/len(both_pairs))

# f = open(os.path.join(root, 'one-negative.txt'), 'w')

# for gold in one_negative:
# 	f.write('=== ' + gold[0] + ', ' + gold[-1] + ' ***\n')
# 	for w in gold:
# 		f.write(w + '\n')
# f.write('=== END')
# f.close()

# f = open(os.path.join(root, 'two-negative.txt'), 'w')

# for gold in two_negative:
# 	f.write('=== ' + gold[0] + ', ' + gold[-1] + ' ***\n')
# 	for w in gold:
# 		f.write(w + '\n')
# f.write('=== END')
# f.close()


# f = open(os.path.join(root, 'both-negative.txt'), 'w')

# for gold in both_negative:
# 	f.write('=== ' + gold[0] + ', ' + gold[-1] + ' ***\n')
# 	for w in gold:
# 		f.write(w + '\n')
# f.write('=== END')
# f.close()



























