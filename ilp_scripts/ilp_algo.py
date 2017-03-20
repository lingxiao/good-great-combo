############################################################
# Module  : Final ilp functions
# Date    : March 19th, 2017
# Author  : Xiao Ling
############################################################

import os
import datetime
from pulp import *

from ilp_scripts import * 
from scripts import *
from prelude import *

############################################################

'''
	@Use: Given dictionary mapping keys to clusters
		  rank all clusters
'''
def ilp(probs, golds):

	print('\n>> Running ilp')

	results = dict()
	dim     = float(len(golds))

	for words,gold in golds.iteritems():
		results[words] = ilp_each(probs, gold)

	tau      = sum(r['tau']      for _,r in results.iteritems())/dim
	abs_tau  = sum(abs(r['tau']) for _,r in results.iteritems())/dim
	pair     = sum(r['pairwise'] for _,r in results.iteritems())/dim

	return {'ranking'  : results
	       ,'tau'      : tau
	       ,'|tau|'    : abs_tau
	       ,'pairwise' : pair
	       ,'probs'    : probs}


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
# ilp :: Dict String Float -> [[String]] -> Dict String _
def ilp_each(probs, gold):


	'''
		construct variables
	'''
	words = join(gold)
	algo  = go_ilp(probs, words)

	return {'gold'      : gold
     	    ,'algo'     : algo
	 	    ,'tau'      : tau(gold,algo)
		    ,'pairwise' : pairwise_accuracy(gold,algo)}

'''
	run ilp over the list of words wrt the graph
'''
def go_ilp(probs, words):

	pairs   = to_pairs(words)
	triples = [(u,v,w) for u in words for v in words for w in words
	      if u != v and v != w and u != w]

	'''
		construct solver
	'''
	lpProb =  LpProblem ('='.join(words), LpMaximize)

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
	objective = []

	for u,v in pairs:
		k_uv = u + '>' + v
		k_vu = v + '>' + u

		if k_uv in probs:
			objective.append(probs[k_uv] *  variables[u + '=' + v])
			objective.append(probs[k_vu] * (1 - variables[u + '=' + v]))
		else:
			objective.append(0.5 *  variables[u + '=' + v])
			objective.append(0.5 * (1 - variables[u + '=' + v]))


	lpProb += lpSum(objective)  

	# constraints
	for i,j,k in triples:
		lpProb += (1 - variables[i + '=' + j]) \
		     +  (1 - variables[j + '=' + k]) \
		     >= (1 - variables[i + '=' + k])


	'''
		output ranking
	'''
	lpProb.solve()
	algo = prob_to_algo_rank(lpProb,words)

	return algo

def to_pairs(words):
	return [(u,v) for u in words for v in words if u != v]




'''
  @Use: given milp object, output ranking
        as list of lists

  prob_to_algo_rank :: MILP -> [[String]] -> [[String]]
'''  
def prob_to_algo_rank(prob,words):

  raw = [v.name.split('=') for v in prob.variables() \
        if v.varValue == 1.0]
  raw = [(u.replace('s_',''),v) for [u,v] in raw]
  raw = [(u.replace('_','-'), v.replace('_','-')) for u,v in raw]

  # construct graph :: dictionary for topological sort
  order = dict()        

  for s,w in raw:
    if s in order:
      order[s] += [w]
    else:
      order[s] = [w]

  # complete the sink in the dictonary
  for w in words:
    if w not in order: order[w] = []

  return [[w] for w in toposort(order)]














