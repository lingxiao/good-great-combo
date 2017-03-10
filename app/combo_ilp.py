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


############################################################
'''
	PATHS
'''
root        = "/Users/lingxiao/Documents/research/code/good-great-combo"
# root        = '/home1/l/lingxiao/xiao/good-great-combo'
gold_ccb    = os.path.join(root, 'inputs/testset-ccb.txt'           )
gold_moh    = os.path.join(root, 'inputs/testset-bansal.txt'        )
gold_all    = os.path.join(root, 'inputs/testset-all-words.txt'     )
graph       = os.path.join(root, 'inputs/raw/all_edges.txt'         )
ngram_graph = os.path.join(root, 'inputs/raw/ngram-graph.txt'       )

############################################################
'''
	open both graphs
'''
ppdb_graph  = label_adv(split_comma(open(graph,'r' ).read().split('\n')))
ngram_graph = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))
combo_graph = ppdb_graph + ngram_graph


'''
	observation: when we get rid of self loops
	the results are worse
'''
# graph     = [(u,w,v) for u,w,v in graph_raw if u != w]

'''
	get list of words in Veronica's graph
'''
graph_words = list(set(join([u,v] for u,v,_ in combo_graph)))

# construct_full_graph(os.path.join(root,'testset'), graph_words, 100000)

'''
	save all pairs of words
'''

'''
	open ccb gold
'''
gold_c = open(gold_ccb,'r').read().split('===')[1:-1]
gold_c = [rs.split('\n') for rs in gold_c if rs.split('\n')]
gold_c = [(rs[0],rs[1:-1]) for rs in gold_c]
gold_ccb = dict([(key,[r.split(', ') for r in val]) for key,val in gold_c])

'''
	open mohit gold
'''
gold_m = open(gold_moh,'r').read().split('===')[1:-1]
gold_m = [rs.split('\n') for rs in gold_m if rs.split('\n')]
gold_m = [(rs[0],rs[1:-1]) for rs in gold_m]
gold_m = [(key,[r.split(', ') for r in val]) for key,val in gold_m]

'''
	open all-gold
'''
gold_all = open(gold_all, 'r').read().split('===')[1:-1]
gold_all = [rs.split('\n') for rs in gold_all if rs.split('\n')]
gold_all = [(rs[0],rs[1:-1]) for rs in gold_all]
gold_all = dict((key,[r.split(', ') for r in val]) for key,val in gold_all)

'''
	filter mohit's gold by adjectives that are in ppdb graph
'''	
gold_moh = dict()

for key, gold in gold_m:

	words          = join(gold)
	words_in_graph = [w for w in words if w in graph_words]

	if len(words) == len(words_in_graph):
		gold_moh[key] = gold


############################################################

def construct_full_graph(root,ts,size):

  pts = [(u,v) for u in ts for v in ts]
  xxs = chunks(pts,size)

  incr = 1
  name = 'testset-'

  for xs in xxs:
    h = open(os.path.join(root,name + str(incr) + '.txt'),'w')
    for u,v in xs:
      h.write('=== foo, bar **\n')
      h.write(u + ', ' + v + '\n')
    h.write('=== END')
    h.close()
    incr += 1


'''
	Get scores for all adjectives

	Our hypothesis is that almost all adverbs are intensifiers,
	so as an upper bound we let all adverbs be intensifiers,
	so adjectives associating with more adverbs are more likely
	to be weaker

'''
def to_score_both(pairs, graph):

	'''
		Score to maximize
	'''
	score = dict()
	eps   = float(1e-3)

	for u,v in pairs:

		v_strong  = len([(a,b,c) for a,b,c in graph if a == u and b == v])
		u_strong  = len([(a,b,c) for a,b,c in graph if a == v and b == u])

		if u_strong or v_strong:

			Z = u_strong + v_strong + 2 * eps
			score[u + '>' + v] = (u_strong + eps)/Z
			score[v + '>' + u] = (v_strong + eps)/Z

		else:	

			adj_adv_u = len([a for a,b,c in graph if a == u])
			adj_adv_v = len([a for a,b,c in graph if a == v])

			Z = adj_adv_u + adj_adv_v + 2*eps

			score[u + '>' + v] = (adj_adv_v + eps)/Z
			score[v + '>' + u] = (adj_adv_u + eps)/Z

	return score


def save_score_both(root, name, words, graph):

	handl   = open(os.path.join(root, name + '.txt'),'w')
	handl.write('=== ' + name + '\n')
	handl.write('='*20 + '\n')

	pairs   = [(u,v) for u in words for v in words if u != v]

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


def to_score_one_sided(pairs, graph):

	score = dict()
	eps   = 1e-3

	for u,v in pairs:

		adj_adv_u = len([a for a,b,c in graph if a == u])
		adj_adv_v = len([a for a,b,c in graph if a == v])

		Z = adj_adv_u + adj_adv_v + 2*eps

		score[u + '>' + v] = (adj_adv_v + eps)/Z
		score[v + '>' + u] = (adj_adv_u + eps)/Z

	return score

def to_score_two_sided(pairs, graph):
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
def ilp(to_score, gold, graph):

	'''
		construct variables
	'''
	words      = join(gold)
	algo,score = go_ilp(to_score, words, graph)
	
	return {'gold'     : gold
     	    ,'algo'    : algo
	 	    ,'tau'     : tau(gold,algo)
		    ,'pairwise': pairwise_accuracy(gold,algo)
		    ,'raw-score': score}

'''
	run ilp over the list of words wrt the graph
'''
def go_ilp(to_score, words, graph):

	pairs   = [(u,v) for u in words for v in words if u != v]

	triples = [(u,v,w) for u in words for v in words for w in words
	      if u != v and v != w and u != w]

	'''
		Score to maximize
	'''
	score = to_score(pairs,graph)

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

	return (algo, score)


'''
	Test all three algo on CCB data
'''	
def run_test(gold_standard, graph):

	results_one_sided = dict()
	results_two_sided = dict()
	results_both      = dict()

	for words,gold in gold_standard.iteritems():
		results_one_sided[words] = ilp(to_score_one_sided, gold, graph)
		results_two_sided[words] = ilp(to_score_two_sided, gold, graph)
		results_both     [words] = ilp(to_score_both     , gold, graph)

	tau1      = sum(r['tau']      for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	abs_tau1  = sum(abs(r['tau']) for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	pair1     = sum(r['pairwise'] for _,r in results_one_sided.iteritems())/float(len(results_one_sided))

	tau2      = sum(r['tau']      for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	abs_tau2  = sum(abs(r['tau']) for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	pair2     = sum(r['pairwise'] for _,r in results_two_sided.iteritems())/float(len(results_two_sided))

	tau3      = sum(r['tau']      for _,r in results_both.iteritems())/float(len(results_both))
	abs_tau3  = sum(abs(r['tau']) for _,r in results_both.iteritems())/float(len(results_both))
	pair3     = sum(r['pairwise'] for _,r in results_both.iteritems())/float(len(results_both))


	results1 = {'ranking' : results_one_sided
	           ,'tau'      : tau1
	           ,'|tau|'    : abs_tau1
	           ,'pairwise' : pair1}

	results2 = {'ranking' : results_two_sided
	           ,'tau'      : tau2
	           ,'|tau|'    : abs_tau2
	           ,'pairwise' : pair2}

	results3 = {'ranking' : results_both
	           ,'tau'      : tau3
	           ,'|tau|'    : abs_tau3
	           ,'pairwise' : pair3}
	
	return (results1, results2, results3)

def run_each_test(gold_standard, graph, score_function):

	results = dict()

	for words,gold in gold_standard.iteritems():
		results[words] = ilp(score_function, gold, graph)

	tau      = sum(r['tau']      for _,r in results.iteritems())/float(len(results))
	abs_tau  = sum(abs(r['tau']) for _,r in results.iteritems())/float(len(results))
	pair     = sum(r['pairwise'] for _,r in results.iteritems())/float(len(results))


	out = {'ranking'  : results
           ,'tau'     : tau
           ,'|tau|'   : abs_tau
           ,'pairwise': pair}

	return out

############################################################
'''
	compute pairwise score on graph
'''
if False:
	words = join(join(w for _,w in gold_all.iteritems()))
	save_score_both(root,'score-both-gold-all-combo-graph', words, combo_graph)
	save_score_both(root,'score-both-gold-all-ppdb-graph' , words, ppdb_graph)
	save_score_both(root,'score-both-gold-all-ngram-graph', words, ngram_graph)

'''
	run test on entire graph
'''
if False:
	re1 = run_each_test(gold_all, combo_grascore-both-gold-all-combo-graphph, to_score_both)
	save(re1, root, 'all-words-ilp-both-combo-graph'     )

	re2 = run_each_test(gold_all, combo_graph, to_score_two_sided)
	save(re2, root, 'all-words-ilp-pairwise-combo-graph')

	re3 = run_each_test(gold_all, combo_graph, to_score_one_sided)
	save(re3, root, 'all-words-ilp-local-combo-graph')


if False:
	results1, results2, results3 = run_test(gold_all, combo_graph)
	save(results1, root, 'all-words-ilp-one-sided-combo-graph')
	save(results2, root, 'all-words-ilp-two-sided-combo-graph')
	save(results3, root, 'all-words-ilp-both-combo-graph'     )


	results1, results2, results3 = run_test(gold_all, ppdb_graph)
	save(results1, root, 'all-words-ilp-one-sided-ppdb-graph')
	save(results2, root, 'all-words-ilp-two-sided-ppdb-graph')
	save(results3, root, 'all-words-ilp-both-ppdb-graph'     )

	results1, results2, results3 = run_test(gold_all, ngram_graph)
	save(results1, root, 'all-words-ilp-one-sided-ngram-graph')
	save(results2, root, 'all-words-ilp-two-sided-ngram-graph')
	save(results3, root, 'all-words-ilp-both-ngram-graph'     )

'''
	run test on annotated gold
'''
if False:
	if True:
		(results1, results2, results3) = run_test(gold_ccb, combo_graph)
		save(results1, root, 'ccb-ilp-one-sided-combo-graph')
		save(results2, root, 'ccb-ilp-two-sided-combo-graph')
		save(results3, root, 'ccb-ilp-both-combo-graph'     )

	if True:
		(results1, results2, results3) = run_test(gold_moh, combo_graph)
		save(results1, root, 'moh-ilp-one-sided-combo-graph')
		save(results2, root, 'moh-ilp-two-sided-combo-graph')
		save(results3, root, 'moh-ilp-both-combo-graph'     )

	if True:
		(results1, results2, results3) = run_test(gold_ccb, ppdb_graph)
		save(results1, root, 'ccb-ilp-one-sided-ppdb-graph')
		save(results2, root, 'ccb-ilp-two-sided-ppdb-graph')
		save(results3, root, 'ccb-ilp-both-ppdb-graph'     )

	if True:
		(results1, results2, results3) = run_test(gold_moh, ppdb_graph)
		save(results1, root, 'moh-ilp-one-sided-ppdb-graph')
		save(results2, root, 'moh-ilp-two-sided-ppdb-graph')
		save(results3, root, 'moh-ilp-both-ppdb-graph'     )

	if True:
		(results1, results2, results3) = run_test(gold_ccb,ngram_graph)
		save(results1, root, 'ccb-ilp-one-sided-ngram-graph')
		save(results2, root, 'ccb-ilp-two-sided-ngram-graph')
		save(results3, root, 'ccb-ilp-both-ngram-graph'     )

	if True:
		(results1, results2, results3) = run_test(gold_moh,ngram_graph)
		save(results1, root, 'moh-ilp-one-sided-ngram-graph')
		save(results2, root, 'moh-ilp-two-sided-ngram-graph')
		save(results3, root, 'moh-ilp-both-ngram-graph'     )

############################################################
'''
	save any other stuff
'''

'''
	save subset of mohit's cluster that appear in 
	veronica's graph
'''		
if False:
	f = open(os.path.join(root, 'testset-bansal-in-graph.txt'),'w')

	for key, gold in gold_moh.iteritems():
		f.write('=== ' + key + '\n')
		gold = [', '.join(ws) for ws in gold]

		for line in gold:
			f.write(line + '\n')

	f.write('=== END')	
	f.close()


'''	
	divide gold_all into 26 subsections for deployment
'''
if False:
	deploy_path = os.path.join(root, 'deploy')
	name        = 'deploy'

	words  = join(join(ws for _,ws in gold_all.iteritems()))
	pairs  = [(u,v) for u in words for v in words if u != v]
	pairss = chunks(pairs,500000)

	incr   = 1

	for pair in pairss:

		h = open(os.path.join(deploy_path, name + str(incr)) + '.txt','w')

		for u,v in pair:
			h.write(u + ' ' + v + '\n')
		h.write('=== END')
		h.close()
		incr +=1 




