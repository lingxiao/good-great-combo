############################################################
# Module  : Scripts to set up Ax = b
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

import numpy as np

from scripts import * 
from prelude import *


############################################################
# Train 

'''
	@Use: current portion of graph considered `subgraph`
	        known values of adverbs and adjectives `known`
	@Input: - `subgraph` :: [(String,String,String)]
	        - `known`    :: [String]

	@Output: A matrix, b vector, 
		     also saved to common space shared with matlab
'''
def to_Ab(subgraph, known):

	'''
		x-vector lookup
	'''
	x_lookup = list(set(w for w in join([a,b,v] for a,b,v in subgraph) \
	                   if w not in known))

	A = []
	b = [0]*len(subgraph)

	for a1,a2,v in subgraph:
		row       = [0]*len(x_lookup)
		r         = subgraph.index((a1,a2,v))

		# a1 + v = a2  ==> a1 + v - a2 = a1 + v - a2
		if a1 in known and a2 in known and v in known:
			b[r] = known[a1] + known[v] - known[a2]
			row[x_lookup.index(a1)] = 1.0
			row[x_lookup.index(v) ] = 1.0
			row[x_lookup.index(a2)] = -1.0

		# a1 + v = a2  /\ not v ==> v = a2 - a1
		elif a1 in known and a2 in known and v not in known:
			b[r] = known[a2] - known[a1]
			row[x_lookup.index(v)] = 1

		# a1 + v = a2 /\ not a2 ==> a2 = a1 + v
		elif a1 in known and a2 not in known and v in known:
			b[r] = known[a1] + known[v]
			row[x_lookup.index(a2)]	 = 1

		# a1 + v = a2 /\ not a1 ==> a1 = a2 - v
		elif a1 not in known and a2 in known and v in known:
			b[r] = known[a2] - known[v]
			row[x_lookup.index(a1)] = 1

		# a1 + v = a2 /\ not a2 /\ not v ==> a2 - v = a1
		elif a1 in known and a2 not in known and v not in known:
			b[r] = known[a1]
			row[x_lookup.index(a2)] = 1
			row[x_lookup.index(v)]  = -1

		# a1 + v = a2 /\ not a1 /\ not v ==> a1 + v = a2
		elif a1 not in known and a2 in known and v not in known:
			b[r] = known[a2]
			row[x_lookup.index(a1)] = 1
			row[x_lookup.index(v) ] = 1

		# a1 + v = a2 /\ not a1 /\ not a2 ==> a2 - a1 = v
		elif a1 not in known and a2 not in known and v in known:
			b[r] = known[v]
			row[x_lookup.index(a1)] = -1
			row[x_lookup.index(a2)] =  1

		# a1 + v = a2 /\ not a1 /\ not a2 /\ not a1 ==> a1 + v - a2 = 0
		elif a1 not in known and a2 not in known and v not in known:
			row[x_lookup.index(a1)] = 1
			row[x_lookup.index(v) ] = 1
			row[x_lookup.index(a2)] = -1
		else:
			raise NameError("unaccounted case")	

		A.append(row)

	return (A,b,x_lookup)


'''
	INIT KNOWN ADJECTIVES

	@Input: path/to/intense_edge.txt
	        path/to/deintense_edge.txt
	@output:   keep parts of edges from ppdb where
				- known intensity edges `iedges`
				- known deintense edges `dedges`
		    as a list of triples (adjective, adjective, adverb)

		    list of base, compare and superla adjectives
			with pre-set values		    

'''
def init_adjectives(iedges, dedges):

	iedges     = split_comma(open(iedges,'r').read().split('\n'))
	dedges     = split_comma(open(dedges,'r').read().split('\n'))

	'''
		ad hoc clean noise:
			- remove deintense edges of adverb 'very'
			- remove all intances of (a,a,adverb)
			  since a = a and no adverbs should have value 0
	'''
	adhoc_intense    = ['very', 'much','substantially']
	adhoc_deintense  = ['slightly']

	# edges where adverbs are expected to be 
	# deintensifiers
	dedges = [(a,b,v) for a,b,v in dedges \
	          if v not in adhoc_intense   \
	          and a != b]

	# edges where adverbs are expected to be 
	# intensifiers
	iedges = [(a,b,v) for a,b,v in iedges \
	          if v not in adhoc_deintense \
	          and a != b]

	edges  = label_adv(iedges + dedges)

	'''
		initialize base, comparative, superlatives values
	'''

	base    = [a for a,_,_ in iedges if a[-2:] != 'er'] \
	        + [a for _,a,_ in dedges if a[-2:] != 'er']

	compare = [a for a,_,_ in iedges if a[-2:] == 'er'] \
	        + [a for _,a,_ in iedges if a[-2:] == 'er'] \
	        + [a for a,_,_ in dedges if a[-2:] == 'er'] \
	        + [a for _,a,_ in dedges if a[-2:] == 'er']

	superla = [a for _,a,_ in iedges if a[-3:] == 'est'] \
	        + [a for _,a,_ in dedges if a[-3:] == 'est']

	incr        = 1/4.0
	base_val    = incr
	compare_val = base_val    + incr
	superla_val = compare_val + incr

	base    = set(base)     
	compare = set(compare)
	superla = set(superla)

	base    = dict(zip(base    , [base_val]    * len(base   )))
	compare = dict(zip(compare , [compare_val] * len(compare)))
	superla = dict(zip(superla , [superla_val] * len(superla)))

	fixed   = dict(base.items() + compare.items() + superla.items())

	return (edges, fixed)		


'''
	Given solved adjectives vector x and turks labels labeled
	output x_good where only adjectives that's been correctly
	placed according to labels are output
'''
def filter_adjectives(x, labeled):

	right_adjs   = dict()
	wrong_adjs   = dict()

	for (a1,a2),d in labeled.iteritems():
		if a1 in x and a2 in x:
			(va1,va2) = (x[a1], x[a2])
			if va1 > va2: yhat = '>'
			else        : yhat = '<'

			d = {a1 : va1, a2: va2, 'y': d['y'], 'yhat': yhat}

			if d['y'] == yhat: right_adjs[(a1,a2)] = d
			else:              wrong_adjs[(a1,a2)] = d


	print('=== pairwise accuracy: ', float(len(right_adjs))/(len(right_adjs) + len(wrong_adjs)))

	bad_adjs  = list(set(join([a,b] for a,b in wrong_adjs)))

	x_good = dict()

	for w,d in x.iteritems():
		if w not in bad_adjs: x_good[w] = d

	return x_good

############################################################
'''
	IO
'''

'''
	Given A and b matrix, save to 	
		path/A_name.txt
		path/b_name.txt
'''
def save_Ab(A,b, path, A_name, b_name):
	'''
		Save as text file for matlab solver
	'''

	row_str = lambda r : ','.join([str(x) for x in r])
	A_path  = os.path.join(path, A_name + '.txt')
	f       = open(A_path,'w')
	A_save  = [row_str(r) for r in A]

	save_list(f,A_save)
	f.close()

	b_path = os.path.join(path, b_name + '.txt')
	h      = open(b_path,'w')
	bstr   = '\n'.join(str(x) for x in b)
	h.write(bstr)
	h.close()

	return (A_path, b_path)

def read_x(path,x_lookup):
	x = [float(x) for x in open(path, 'r').read().split('\n')[0:-1]]
	x = dict(zip(x_lookup,x))
	return x


############################################################
'''
	Generic scripts
'''
'''
	TEST SET:
		- keep only unanimous labeled pairs
'''
def unanimous(x,y,t):
	return x != 0 and y == 0 and t == 0 \
	or     x == 0 and y != 0 and t == 0 \
	or 	   x == 0 and y == 0 and t != 0


def mark_label(t):
	[a1_larger, a2_larger, tied, a1,a2] = t
	if a1_larger > a2_larger and a1_larger > tied:
		return (a1, '>', a2)
	elif a2_larger > a1_larger and a2_larger > tied:
		return (a1, '<', a2)
	else:
		return (a1, '==', a2)

'''
	Some words are used as adverbs and adjectives
	we need to syntacitcally differentiate adverbs
'''
def label_adv(edges):
	return [(x,y, '<' + v + '>') for x,y,v in edges]


strip       = lambda ls : (ls[0].strip(), ls[1].strip(), ls[2].strip())
split_comma = lambda xs : [ strip(x.split(',')) for x in xs if len(x.split(',')) == 3]
split_tab   = lambda xs : [ x.split('\t') for x in xs]
