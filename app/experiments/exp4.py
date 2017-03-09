############################################################
# Module  : Determine value of adverbs that minimize error
#           on data
# Date    : December 22nd
# Author  : Xiao Ling
############################################################

import os
import re
import datetime
import numpy as np

from scripts import * 
from prelude import *

############################################################
'''
	PATHS
'''

root       = "/Users/lingxiao/Documents/research/code/good-great-ppdb"
edges      = os.path.join(root,'inputs/small_edges.txt'     )
iedges     = os.path.join(root,'inputs/intense-copy.txt'         )
dedges     = os.path.join(root,'inputs/deintense-copy.txt'       )
all_edges  = os.path.join(root,'inputs/raw/all_edges.txt')

############################################################
'''
	PREP TRAINING SET

	Load all training edges from PPDB
	
	Load parts of edges from ppdb so that 
		- known intensity edges `iedges`
		- known deintense edges `dedges`
		- unknown edges `uedges`, note these are useful only 
		  to give greater coverage for adverbs not covered by 
		  intense and deintense
'''
all_edges  = split_comma(open(all_edges,'r' ).read().split('\n'))

iedges     = split_comma(open(iedges,'r').read().split('\n'))
dedges     = split_comma(open(dedges,'r').read().split('\n'))
# dedges = []
# uedges     = [(a,b,v) for a,b,v in all_edges     \
              # if (a,b,v) not in (iedges + dedges)]
uedges = []

'''
	ad hoc clean noise:
		- remove deintense edges of adverb 'very'
		- remove all intances of (a,a,adverb)
		  since a = a and no adverbs should have value 0
'''
adhoc_intense    = ['very', 'much']
adhoc_deintense  = ['slightly']
dedges = [(a,b,v) for a,b,v in dedges if v not in adhoc_intense  ]
iedges = [(a,b,v) for a,b,v in iedges if v not in adhoc_deintense]

dedges = [(a,b,v) for a,b,v in dedges if a != b]
iedges = [(a,b,v) for a,b,v in iedges if a != b]
uedges = [(a,b,v) for a,b,v in uedges if a != b]

train_data = iedges + dedges + uedges

'''
	Get adverbs, adjectives, and make Data matrix
'''
advs = list(set(v for _,_,v in  train_data))
adjs = list(set(join([a,b] for a,b,_ in train_data)))


############################################################
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

print ('vals: ', base_val, compare_val, superla_val)

base    = set(base)     
compare = set(compare)
superla = set(superla)

base    = dict(zip(base    , [base_val]    * len(base   )))
compare = dict(zip(compare , [compare_val] * len(compare)))
superla = dict(zip(superla , [superla_val] * len(superla)))

fixed   = dict(base.items() + compare.items() + superla.items())

############################################################
'''
	Build A,b,x matrix for matlab cvx solver

	Things to try:
		- vary values of base, super, compare
		- only set super value or base value or compare value
'''
env = {'adjs' : adjs 		     # all adjectives found in graph
      ,'advs' : advs             # all adverbs found in graph
      ,'data' : train_data       # entire graph
      ,'fixed': fixed            # values of words that are fixed
      }


'''
	Prep A and b, save to disk
'''
A,b,x_lookup = make_Ab_train(root,env,True)


'''
	Experiements to run:

		I.  test data: try only unanimous labeled data
		II. Training data: 
			- more conservative propogation techniques

			    - propagate >> draw sample and test
			      only keep going if the error is w/i
			      some bound

			- regularization 
 
			- l1 norm

'''


'''
	# save base,compare,superla in list
	ws = []

	for k in base:
		ker   = k + 'er'
		kest  = k + 'est'
		ws.append((k,ker,kest))


	f = open(os.path.join(root,'seed.txt'),'w')

	for w,wer,west in ws:
		f.write('=== foo, bar ** \n')
		f.write(w + '\n')
		f.write(wer + '\n')
		f.write(west + '\n')

	f.write('=== END')
	f.close()
'''





























