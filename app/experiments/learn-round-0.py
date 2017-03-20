############################################################
# Module  : Determine value of adverbs that minimize error
#           on data
# Date    : December 22nd
# Author  : Xiao Ling
# merle mommy babbaa leora
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
# SCRIPTS

'''
	Initalize
'''
subgraph0, known0 = init_adjectives(iedges, dedges)	

'''
	Iteration 0
'''
def iter0(subgraph0, known0):

	A0,b0,x_lookup0 = to_Ab(subgraph0,known0)
	save_Ab(A0,b0, os.path.join(root,'outputs'), 'A-matrix-0','b-vector-0')

	return (A0,b0,x_lookup0)

'''
	@Use:    Read solution and check error
	@Input : vector of adjectives, dictionary of labeled adjective pairs
	@output: error
'''
def test(x_adj, labeled_set):

	right_adjs   = dict()
	wrong_adjs   = dict()

	for (a1,a2),d in labeled_set.iteritems():

		if a1 in x_adj  and a2 in x_adj:
			(va1,va2) = (x_adj[a1], x_adj[a2])
			if va1 > va2: yhat = '>'
			else        : yhat = '<'

			d = {a1 : va1, a2: va2, 'y': d['y'], 'yhat': yhat}

			if d['y'] == yhat: right_adjs[(a1,a2)] = d
			else:              wrong_adjs[(a1,a2)] = d

	right = float(len(right_adjs))
	wrong = float(len(wrong_adjs))

	if not right and not wrong:
		accu = -1
	else:		
		accu   = right/(right + wrong)
	print ('=== pairwise accuracy: '
	      + str(accu) 
	      + ' on ' 
	      + str(right + wrong) 
	      + ' examples')

	return {'right': right_adjs, 'wrong': wrong_adjs, 'accuracy': accu}


############################################################
'''
	Read solution to x0
'''
A0,b0,x_lookup0 = iter0(subgraph0, known0)

x0   = read_x(os.path.join(root, 'outputs/iter0/soln/x-vector-0.txt'), x_lookup0)
advs = sorted(x0.items(), key=operator.itemgetter(1))

'''
	Feature Engineering in round 1
	- add in one by one

	- these adverbs to solve for value of adjectives for next round

	step 0. see which one has not enough counts
	compile a statistic of how often each adverb appears
	in the graph to get a sense of confidence
'''
adv_counts   = [ (v,len([w for _,_,w in subgraph0 if w == v])) for v,val in advs ]
adv_counts   = sorted(adv_counts, key = lambda t: t[1])
adv_counts_d = dict(adv_counts)

############################################################
'''
	Now use each adverb to predict value of adjectives
	treat each adverb as a weak predictor
	and see if combining them will improve the
	performance of system
'''
addone_path = os.path.join(root, 'outputs/experiments/addone')

adverb_adjective = dict()

for adv,_ in adv_counts:
	x0_i  = {adv : x0[adv]}

	'''
		pick out all pairs in graph where the adverbs v 
		between vertexes are known
	'''
	subgraphi = [(a1,a2,v) for a1,a2,v in graph \
	             if v in x0_i and a1 != a2]

	'''	
		constructing A and b for matlab and save
	'''	
	Ai,bi,x_lookupi = to_Ab(subgraphi,x0_i)
	save_Ab(Ai,bi, addone_path, 'A-matrix-' + adv,'b-vector-' + adv)

	adverb_adjective[adv] = {'|adjectives-pair-0|' : adv_counts_d[adv] \
	                        ,'adjectives-1'        : x_lookupi
	                        ,'value'               : x0[adv]}

############################################################
'''
	Now read solution and check error due to each adverb as a weak predictor
'''
for adv in adverb_adjective:

	x_adv = read_x( os.path.join(addone_path,'soln/' + 'x-vector-' + adv + '.txt')\
		          , adverb_adjective[adv]['adjectives-1'])

	d  = test(x_adv, labeled)
	adverb_adjective[adv]['test']    = d
	adverb_adjective[adv]['|test set|'] = len(d['right']) + len(d['wrong'])


examine = dict()
f = open(os.path.join(root, 'round-0-adverb.txt'), 'w')

for v,d in adverb_adjective.iteritems():
	accu   = d['test']['accuracy']
	adj0   = d['|adjectives-pair-0|']
	adj1   = len(d['adjectives-1'])
	tset   = d['|test set|']

	f.write('=== ' + v + ', ' + str(d['value']) + '\n')	
	f.write('accuracy: '       + str(accu) + '\n')
	f.write('|adjectives-pair-0|: ' + str(adj0) + '\n')
	f.write('|adjectives-1|: ' + str(adj1) + '\n')
	f.write('|test set|: '     + str(tset) + '\n\n')

	examine[v] = {'value': d['value'], 'accuracy': accu, '|adjectives-pair-0|': adj0, '|adjectives-1|': adj1, '|test set|': tset}

'''
	save for examination
'''
f.write('=== END')	
f.close()

############################################################
'''
	sort by accuracy
'''
by_accu = sorted(examine.items(), key = lambda x: x[1]['accuracy'])

'''
	sort by size of test set
'''
by_test = sorted(examine.items(), key = lambda x: x[1]['|test set|'])

'''
	truncate test set heuristically
'''
# confident_by_test_size = [(v,d) for v,d in by_test if d['|test set|'] >= 60]
confident_by_accuracy  = [(v,d) for v,d in by_test if d['accuracy'] > 0.60]

############################################################
'''
	Use this as new x0 and see how they perform together as weak predictors
'''
x0_iter1 = dict((v,d['value']) for v,d in confident_by_accuracy)


'''
	pick out all pairs in graph where the adverbs v 
	between vertexes are known
'''
subgraphi = [(a1,a2,v) for a1,a2,v in graph \
             if v in x0_iter1 and a1 != a2]

'''	
	constructing A and b for matlab and save
'''	
Ai,bi,x_lookupi = to_Ab(subgraphi,x0_iter1)
save_Ab(Ai,bi, os.path.join(root,'outputs/iter0'), 'A-matrix-iter1','b-vector-iter1')

############################################################
'''
	run this in console to determine output of tuning process
'''
def tune():

	x_adj_0 = read_x(os.path.join(root,'outputs/iter0/soln/x-vector-iter1.txt'), x_lookupi)
	d       = test(x_adj_0, labeled)

	'''
		save set to compare against alternative
	'''
	right_sub = random.sample([k for k in d['right']], 5)
	wrong_sub = random.sample([k for k in d['wrong']], 5)

	f = open(os.path.join(root,'testset.txt'), 'w')

	for u,v in right_sub:
		f.write('=== right,right **\n')
		f.write(u + '\n')
		f.write(v + '\n')

	for u,v in wrong_sub:
		f.write('=== wrong,wrong **\n')
		f.write(u + '\n')
		f.write(v + '\n')

	f.write('=== END')	
	f.close()

	return x_adj_0

'''	
	IMPORTANT: Save output for next round
'''
def save_round0():

	# save adjective
	f = open(os.path.join(root,'outputs/iter0/soln/adverb.txt'),'w')

	for adv,v in x0_iter1.iteritems():
		f.write(adv + '\t' + str(v) + '\n')
	f.close()

	# save adverb
	x_adj0 = read_x(os.path.join(root,'outputs/iter0/soln/x-vector-iter1.txt'), x_lookupi)

	h = open(os.path.join(root,'outputs/iter0/soln/adjective.txt'),'w')

	for adj,v in x_adj0.iteritems():
		h.write(adj + '\t' + str(v) + '\n')
	h.close()	

















