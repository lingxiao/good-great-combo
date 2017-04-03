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
root        = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
gold_ccb    = os.path.join(root, 'inputs/testset-ccb.txt'           )
gold_moh    = '/Users/lingxiao/Documents/research/code/good-great-ngrams/inputs/testset-bansal.txt'
graph       = os.path.join(root, 'inputs/raw/all_edges.txt'         )
ngram_graph = os.path.join(root, 'inputs/raw/ngram-graph.txt'       )
adj_adv     = os.path.join(root, 'inputs/adjective-adverb-count.txt')


############################################################
'''
	open Veronica's raw graph
	and prune self loops
'''
graph = label_adv(split_comma(open(graph,'r' ).read().split('\n')))

'''
	observation: when we get rid of self loops
	the results are worse
'''
# graph     = [(u,w,v) for u,w,v in graph_raw if u != w]


'''
	get list of words in Veronica's graph
'''
graph_words = list(set(join([u,v] for u,v,_ in graph)))

'''	
	open adjective-adverb-count
'''
adj_adv = [r.split('\t') for r in open(adj_adv,'r').read().split('\n') if len(r.split('\t')) == 2]
adj_adv = dict([(a,float(b)) for a,b in adj_adv])


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
	filter mohit's gold by adjectives that are in ppdb graph
'''	
gold_moh = dict()

for key, gold in gold_m:

	words          = join(gold)
	words_in_graph = [w for w in words if w in graph_words]

	if len(words) == len(words_in_graph):
		gold_moh[key] = gold

'''
	save subset of mohit's cluster that appear in 
	veronica's graph
'''		
f = open(os.path.join(root, 'testset-bansal-in-graph.txt'),'w')

for key, gold in gold_moh.iteritems():
	f.write('=== ' + key + '\n')
	gold = [', '.join(ws) for ws in gold]

	for line in gold:
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
	words   = join(gold)
	algo    = go_ilp(to_score, words, graph)
	
	return {'gold'     : gold
     	    ,'algo'    : algo
	 	    ,'tau'     : tau(gold,algo)
		    ,'pairwise': pairwise_accuracy(gold,algo)
		    ,'raw-score': score}
'''
	given gold, run ilp over 
	subgraph containing all words
'''
def subgraph_ilp(to_score,gold,graph):

	words    = join(gold)
	subgraph = set(join([[u,v] for u,v,w in graph \
	           if u in words or v in words]))

	algo_all = go_ilp(to_score, subgraph, graph)

	algo = []

	for [w] in algo_all:
		if w in words: algo.append([w])

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

	return algo


'''
	Test all three algo on CCB data
'''	
def run_test(gold_standard):

	results_one_sided = dict()
	results_two_sided = dict()
	results_both      = dict()

	for words,gold in gold_standard.iteritems():
		# results_one_sided[words] = subgraph_ilp(to_score_one_sided, gold, graph)
		# results_two_sided[words] = subgraph_ilp(to_score_two_sided, gold, graph)
		results_both     [words] = subgraph_ilp(to_score_both     , gold, graph)

	# tau1      = sum(r['tau']      for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	# abs_tau1  = sum(abs(r['tau']) for _,r in results_one_sided.iteritems())/float(len(results_one_sided))
	# pair1     = sum(r['pairwise'] for _,r in results_one_sided.iteritems())/float(len(results_one_sided))

	# tau2      = sum(r['tau']      for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	# abs_tau2  = sum(abs(r['tau']) for _,r in results_two_sided.iteritems())/float(len(results_two_sided))
	# pair2     = sum(r['pairwise'] for _,r in results_two_sided.iteritems())/float(len(results_two_sided))

	tau3      = sum(r['tau']      for _,r in results_both.iteritems())/float(len(results_both))
	abs_tau3  = sum(abs(r['tau']) for _,r in results_both.iteritems())/float(len(results_both))
	pair3     = sum(r['pairwise'] for _,r in results_both.iteritems())/float(len(results_both))


	# ccb_results1 = {'ranking' : results_one_sided
	#                ,'tau'      : tau1
	#                ,'|tau|'    : abs_tau1
	#                ,'pairwise' : pair1}

	# ccb_results2 = {'ranking' : results_two_sided
	#                ,'tau'      : tau2
	#                ,'|tau|'    : abs_tau2
	#                ,'pairwise' : pair2}

	ccb_results3 = {'ranking' : results_both
	               ,'tau'      : tau3
	               ,'|tau|'    : abs_tau3
	               ,'pairwise' : pair3}


	# return (ccb_results1, ccb_results2, ccb_results3)
	return ccb_results3


############################################################
'''
	Run test
'''


if False:
	results_ccb = run_test(gold_ccb)
	results_moh = run_test(gold_moh)
	# (ccb_results1, ccb_results2, ccb_results3) = run_test(gold_ccb)
	# (moh_results1, moh_results2, moh_results3) = run_test(gold_moh)

	# save(ccb_results1, root, 'ccb-ilp-one-sided')
	# save(ccb_results2, root, 'ccb-ilp-two-sided')
	# save(ccb_results3, root, 'ccb-ilp-both')


	# save(moh_results1, root, 'moh-ppdb-graph-one-sided')
	# save(moh_results2, root, 'moh-ppdb-graph-two-sided')
	# save(moh_results3, root, 'moh-ppdb-graph-both')





############################################################
'''
	Utils
'''

'''
	make graph list into dictionary with format:
		word : [(word_1, edge), (word_2, edge), ..]
'''	

graph = graph[0:100]

def to_graph(graph):

	vertices = set(join([[u,v] for u,v,_ in graph]))
	dgraph   = dict()
	for v in vertices:
		dgraph[v] = [(b,c) for a,b,c in graph if a == v]

	return dgraph

graph = to_graph(graph)


def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest



# gold_moh_subgraph = dict()

# # for key,gold in gold_moh.iteritems():
# key,gold = list(gold_moh.iteritems())[3]
# words    = join(gold)
# subgraph = [(u,v,w) for u,v,w in graph \
#            if u in words or v in words]



'''
	split mohit's gold into Documents of pairs
	to get ngram data
'''
def split_moh_gold(golds):

	proot  = os.path.join(root, 'inputs/moh-graph')

	words  = set(join(join([ws for _, ws in golds.iteritems()])))
	pwords = [(u,v) for u in words for v in words]

	files  = list(chunks(pwords,1000))

	num = 1

	for f in files:
		h = open(os.path.join(proot,'testset-' + str(num) + '.txt'),'w')
		for u,v in f:
			h.write('=== foo, bar **\n')
			h.write(u + '\n' + v + '\n')
		h.write('=== END')		
		h.close()
		num +=1 

















