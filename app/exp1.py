############################################################
# Module  : Applicaton Main
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
from copy import deepcopy
from server  import * 
from prelude import *

############################################################
# Paths

name      = 'adj_mat'

root      = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
inputs    = os.path.join(root,'inputs'         )
mat_path  = os.path.join(inputs,'ppdb_data.txt')
cl_path   = os.path.join(inputs,'pairwise_judgements.txt')

adj_mat = load_adjacency_matrix(mat_path)

(strong,weak,neut) = load_training(root,cl_path,mat_path)

############################################################
# update algorithm

'''
	initalize adverbs from training data
	set all adverbs to 0
'''
def init(strong,weak,neut):

	adverbs = []

	for (ai,aj),d in strong.iteritems():
		adverbs.append(d[ai])
		adverbs.append(d[aj])

	for (ai,aj),d in weak.iteritems():
		adverbs.append(d[ai])
		adverbs.append(d[aj])

	for (ai,aj),d in neut.iteritems():
		adverbs.append(d[ai])
		adverbs.append(d[aj])

	keys = set(join(adverbs))

	return dict(zip(keys,[0]*len(keys)))

# increment the v in adverb by eps
def incr(adverb,v,eps):
	if v in adverb:
		if adverb[v] < 0: 
			adverb[v] = adverb[v] + eps
		else:
			adverb[v] = min(1,adverb[v] + eps)
	return adverb

def decr(adverb,v,eps):
	if v in adverb:
		if adverb[v] > 0: 
			adverb[v] = adverb[v] - eps
		else:
			adverb[v] = max(-1,adverb[v] - eps)
	return adverb

'''
	@Use: 

	determine absolute strength of adjective ai
	based on the adverbs that modify it

	if the sum of adverbs that modify ai > 0:
		then ai co-ocur more frequently with
		intensifying adverbs, therefore ai is weak

	if the sum of adverbs that modify ai < 0:
		then ai co-occur more frequently with
		de-intensifying adverbs, therefore ai is strong

	note we reverse the sign

'''
def strength(adverb,ai,d):
	advs = [adverbs[v] for v in d[ai]]
	return -sum(advs)

adverbs   = init(strong,weak,neut)

eps = 1.0/len(adverbs) * 20


# one iteration update adverbs
for (ai,aj),d in strong.iteritems():

	'''
		these adverbs modify ai, since ai > aj
		they are deintensifying adverbs
		we do:  vi <- vi - eps

	'''
	adverb_ai = d[ai]
	for vi in adverb_ai: adverbs = decr(adverbs,vi,eps)

	'''
		these adverbs modify aj, since ai > aj
		they are intensifying adverbs
		we do: vj <- vj + eps
	'''
	adverb_aj = d[aj]
	for vj in adverb_aj: adverbs = incr(adverbs,vj,eps)

for (ai,aj),d in weak.iteritems():

	'''
		these adverbs modify ai, since ai < aj
		they are intensifying adverbs
		we do:  vi <- vi + eps

	'''
	adverb_ai = d[ai]
	for vi in adverb_ai: adverbs = incr(adverbs,vi,eps)

	'''
		these adverbs modify aj, since ai < aj
		they are deintensifying adverbs
		we do: vj <- vj - eps
	'''
	adverb_aj = d[aj]
	for vj in adverb_aj: adverbs = decr(adverbs,vj,eps)

for (ai,aj),d in neut.iteritems():

	'''
		these adverbs modify ai and aj, since ai = aj
		they are neutral adverbs, we move them towards 0
	'''
	adverb_aij = d[ai] + d[aj]
	for vi in adverb_aij: 
		if adverbs[vi] > 0: decr(adverbs,vi,eps)
		if adverbs[vi] < 0: incr(adverbs,vi,eps)

# predict based on adverbs
(ai,aj) = ('obvious', 'visible')
d       = strong[(ai,aj)]

# NOTE: words have polarity!! so > is flipped for certain words





	




'''

	clas  = [(93.2,100),(90.0,100),(90.3,100),(96.2,100),(89.3,100),\
	        (45.1*2,100),(39.3,100),(94.7,100),(95,100)]

	assn = [(85,100),(90.8,100),(99.6,100),(99.5,100),(99,100), \
	       (48*2,100),(48*2,100),(99,100),(98,100)]

	top = sum(a for a,_ in assn)      
	bot = sum(b for _,b in assn)

	avg = top/float(bot)
	m1  = 0.735
	m2  = 0.76   

	mine  = avg * 0.5 + m1*0.25 + m2*0.25
	other = (sum(a for a,_ in clas)/bot) * 0.5 + .85*0.25 + .791*.25


'''




























