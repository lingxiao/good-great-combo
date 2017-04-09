############################################################
# Module  : rank using different ppr probs alone
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
from experiments import *

'''
	todo tuesday:
		 - check ppr behave as expcted
		 - deploy ppr scripts
		 - run wt-edge over ppdb + ngram graph
		 - run logistic regression

		 - project difference vectors into some space and separate
		 - project local template of difference vectors to some space and separate
'''

############################################################
'''
	read test-set
'''
ccb    = read_gold(PATH['assets']['ccb'])
bansal = read_gold(PATH['assets']['bansal'])

'''
	paths
'''
gr_path = PATH['assets']['graph']
wt_dir  = PATH['inputs']['edge-weight']
log_dir = PATH['directories']['log']
out_dir = os.path.join(PATH['directories']['results'],'april')
ppr_dir = os.path.join(PATH['directories']['input'],'ppr-by-ppdb')

'''
	path to different kind of edge weights
'''
edge_weight_bradly_terry = os.path.join(wt_dir, 'bradley-terry')
edge_weight_adjacency    = os.path.join(wt_dir, 'neigh'    )

############################################################

'''
	right now: recompute ppr for bradley-terry
	            recompute ppr for neigh
	     		word2vec for all words in graph
	     		ngram for all words

'''

G      = Graph(gr_path, wt_path, ppr_dir)
alphas = [0.9,0.8,0.7,0.5,0.25,0.1,0.01]

alpha = 0.9
gold  = [['good'],['great'], ['excellent']]

words = join(gold)
pairs = [(s,t) for s in words for t in words if s != t]

compares = { (s,t) : G.ppr(s,t,alpha) for s,t in pairs }

# pprs   = run_ppr(ppr_dir, ccb[3], 0.9)











