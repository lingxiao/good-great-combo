############################################################
# Module  : Naive implementation
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os
from pulp import *

import app
from scripts import *
from prelude import *

############################################################
'''
	@Use: given root directory and file name to save,
		  list of words of form:
		  	['word1', ...]
		  graph graph of form:		  
		  	[('adj1', 'adj2','<adv>'),..]

		  output probability adj_i > adj_k
		  for every i and k

		  save output to root/name.txt
'''
def probs_both(root, name, words, graph):

	pairs  = to_pairs(words)
	words  = set(join(pairs))
	lookup = to_lookup(graph, words)

	handl   = open(os.path.join(root, name + '.txt'),'w')
	handl.write('=== ' + name + '\n')
	handl.write('='*20 + '\n')

	score = dict()
	eps   = float(1e-3)

	print ('\n>> begin computing probs')


	for u,v in pairs:

		u_strong = 0.0
		v_strong = 0.0


		if u not in lookup:
			pass

		elif v in lookup[u]['neigh']:
			v_strong = lookup[u]['neigh'][v]

		if v not in lookup:
			pass

		elif u in lookup[v]['neigh']:
			u_strong = lookup[v]['neigh'][u]

		if u_strong or v_strong:
			Z = u_strong + v_strong + 2 * eps

			u_ge_v = (u_strong + eps)/Z
			v_ge_u = (v_strong + eps)/Z

			score[u + '>' + v] = u_ge_v
			score[v + '>' + u] = v_ge_u

		else:
			adj_adv_u = lookup[u]['|neigh|']
			adj_adv_v = lookup[v]['|neigh|']

			Z = adj_adv_u + adj_adv_v + 2*eps

			u_ge_v = (adj_adv_v + eps)/Z
			v_ge_u = (adj_adv_u + eps)/Z

			score[u + '>' + v] = u_ge_v
			score[v + '>' + u] = v_ge_u

		handl.write(u + '>' + v + ': ' + str(u_ge_v) + '\n')
		handl.write(v + '>' + u + ': ' + str(v_ge_u) + '\n')
	
	handl.write('=== END')		
	handl.close()

	print ('\n>> done computing probs')

	return score

############################################################
'''
	construct lookup
'''
def to_lookup(graph, words):

	lookup = dict()

	print ('\n>> begin constructing lookup graph')


	for word in words:

		local = [(b,c) for a,b,c in graph if a == word]
		ldict = dict()

		for w,_ in local:
			if w in ldict: ldict[w] += 1
			else: ldict[w] = 1.0

		lookup[word] = {'|neigh|': len(local), 'neigh': ldict}

	print ('\n>> done constructing lookup graph')
	return lookup

############################################################
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
def ilp(score, gold):

	'''
		construct variables
	'''
	words  = join(gold)
	algo   = go_ilp(score, words)

	return {'gold'     : gold
     	    ,'algo'    : algo
	 	    ,'tau'     : tau(gold,algo)
		    ,'pairwise': pairwise_accuracy(gold,algo)
		    ,'raw-score': score}

'''
	run ilp over the list of words wrt the graph
'''
def go_ilp(score, words):

	pairs   = to_pairs(words)
	triples = [(u,v,w) for u in words for v in words for w in words
	      if u != v and v != w and u != w]

	print ('\n>> declare LP problem')
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

	print ('\n>> construct objective function')
	'''
		objective function
	'''
	objective = [ score[u+'>'+v]   * variables[u+'='+v]  \
	          for u,v in pairs] \
	        + [ score[v + '>'+  u] * (1 - variables[u+'='+v]) \
	          for u,v in pairs]


	prob += lpSum(objective)  

	print ('\n>> construct constraints')

	# constraints
	for i,j,k in triples:
		prob += (1 - variables[i + '=' + j]) \
		     +  (1 - variables[j + '=' + k]) \
		     >= (1 - variables[i + '=' + k])


	print ('\n>> begin solving ...')
	'''
		output ranking
	'''
	prob.solve()
	print ('\n>> done solving')

	print ('\n>> begin ranking solving')

	algo = prob_to_algo_rank(prob,words)


	return algo

def to_pairs(words):
	return [(u,v) for u in words for v in words if u != v]

















