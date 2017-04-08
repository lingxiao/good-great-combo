############################################################
# Module  : Run regression on raw pairwise comparisons
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
import json
import pickle
import networkx as nx

from app.config import PATH
from utils   import *
from scripts import *

'''
	Things to test:
		- learning parameters
		- gaussian kernal by hops		
		- consuming various amount of training data
		- word2vec dot products
'''
############################################################
'''
	read test-set
'''
ccb    = read_gold(PATH['assets']['ccb'])
bansal = read_gold(PATH['assets']['bansal'])

'''
	read weighted edge from disk if it exists,
	else compute ppr for every vertex in the graph
'''
gr_path    = PATH['assets']['graph']
vertex_dir = PATH['inputs']['graph-wt-by-edge']	
 
# graph  = load_as_digraph(gr_path, vertex_dir)

############################################################
'''
	Logistic Regression
'''
learning_rate = 0.01
epochs        = 25
batch_size    = 100

# num_px        = 28*28
# num_classes   = 10
# display_step  = 1










