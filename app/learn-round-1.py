############################################################
# Module  : Determine value of adverbs that minimize error
#           on data
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
import operator
import random
import itertools
from copy import deepcopy
import numpy as np

from scripts import * 
from prelude import *

############################################################
'''
	PATHS
'''
root   = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
iedges = os.path.join(root,'inputs/intense-copy.txt'  )
dedges = os.path.join(root,'inputs/deintense-copy.txt')
graph  = os.path.join(root,'inputs/raw/all_edges.txt' )
graph  = label_adv(split_comma(open(graph,'r' ).read().split('\n')))

round0_root = os.path.join(root,'outputs/iter0')
round1_root = os.path.join(root,'outputs/iter1')

'''
	get labeled pairs
'''
labeled_path  = os.path.join(root,'inputs/raw/pairwise_judgements.txt')
labeled_raw   = split_tab  (open(labeled_path,'r').read().split('\n'))[0:-1]
labeled_raw   = [(float(x),float(y),float(t),a1,a2)    \
                 for m,x,y,t,_,_,a1,a2 in labeled_raw       \
                 if unanimous(float(x),float(y),float(t))]

labeled_ties  = list(set(mark_label(t) for t in labeled_raw))

labeled       = dict()

for a1,y,a2 in labeled_ties:
	if y != '==': labeled[(a1,a2)] = {'y': y}

############################################################
'''
	Get round 0 solutions
'''
adj0 = [x for x in open(os.path.join(round0_root,'soln/adjective.txt')).read().split('\n') if x]
adv0 = [x for x in open(os.path.join(round0_root,'soln/adverb.txt'   )).read().split('\n') if x]

adj0 = dict((u,float(v)) for u,v in [x.split('\t') for x in adj0])
adv0 = dict((u,float(v)) for u,v in [x.split('\t') for x in adv0])

############################################################
'''
	Find adverbs in graph hit by adjectives from round0
'''
subgraph1a = [(a,b,v) for a,b,v in graph           \
             if a in adj0 and b in adj0 and a != b ]

# collect known variables
known1a     = dict(adj0.items() + adv0.items())


known = known1a
subgraph = subgraph1a[0:2]

'''
	x-vector lookup
'''
x_lookup = list(set(w for w in join([a,b,v] for a,b,v in subgraph) \
                   if w not in known))



A = []
b = [0]*len(subgraph)

for a1,a2,v in [subgraph[0]]:
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





