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

from utils   import *

############################################################
'''
	Iteration 0
'''

def iter0(root, subgraph0, known0):

	pdir = make_dir(os.path.join(root, 'outputs/iter0'))

	A0,b0,x_lookup0 = to_Ab(subgraph0,known0)

	save_Ab(A0, b0,pdir, 'A-matrix','b-vector')

	return {'A'   : A0,
	        'b'   : b0,
	        'x'   : x_lookup0,
	        'path': pdir}

############################################################
'''
	Iteraion 1a
'''

'''
	@Use: known adverbs, unknown adjectives
'''	
def iter_ia(root, prev_iter, graph, piter):

	'''
		read solution from previous iteration and put in dict
		for pretty print
	'''
	x0   = read_x(os.path.join(prev_iter['path'], 'x-vector.txt'), prev_iter['x'])
	advs = sorted(x0.items(), key=operator.itemgetter(1))

	'''
		pick out all pairs in graph where the adverbs v 
		between vertices are known
	'''
	sub_graph = [(a1,a2,v) for a1,a2,v in graph \
	             if v in x0 and a1 != a2]
	
	'''	
		constructing A and b for matlab and save
	'''	             
	A1a,b1a,x_lookup1a = to_Ab(sub_graph,x0)

	pdir = make_dir(os.path.join(root, 'outputs/' + piter))

	save_Ab(A1a,b1a, pdir, 'A-matrix','b-vector')

	return {'A'    : A1a,
	        'b'    : b1a,
	        'x'    : x_lookup1a,
	        'words': advs,
	        'path' : pdir}

'''
	@Use: known adjective, unknown adverb
'''
def iter_ib(root, prev_iter, graph, piter):

	'''
		read solution from previous iteration and put in dict
		for pretty print
	'''
	x0   = read_x(os.path.join(prev_iter['path'], 'x-vector.txt'), prev_iter['x'])
	adjs = sorted(x0.items(), key=operator.itemgetter(1))

	'''
		pick out all pairs in graph where the adverbs v 
		between vertices are known
	'''
	sub_graph = [(a1,a2,v) for a1,a2,v in graph \
				 if a1 != a2 and a1 in x0 and a2 in x0]
	
	'''	
		constructing A and b for matlab and save
	'''	             
	A1b,b1b,x_lookup1b = to_Ab(sub_graph,x0)

	pdir = make_dir(os.path.join(root, 'outputs/' + piter))

	save_Ab(A1b,b1b, pdir, 'A-matrix','b-vector')

	return {'A'    : A1b,
	        'b'    : b1b,
	        'x'    : x_lookup1b,
	        'words': adjs,
	        'path' : pdir}

############################################################
'''
	Utils
'''
def make_dir(pdir):
	if not os.path.isdir(pdir):
		os.makedirs(pdir)
	return pdir
