############################################################
# Module  : Naive implementation
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os
import time
import datetime
import operator
import random
import itertools	
from copy import deepcopy
import numpy as np
from pulp    import *

from app import *
from scripts import *
from prelude import *


############################################################
'''
	PATHS
'''
root        = os.getcwd()
deploy_in   = os.path.join(root, 'deploy-in')
deploy_out  = os.path.join(root, 'deploy-out')
word_all    = os.path.join(root, 'inputs/testset-all-words.txt')

ccb_graph   = os.path.join(root, 'inputs/raw/all_edges.txt'         )
ngram_graph = os.path.join(root, 'inputs/raw/ngram-graph.txt'       )

############################################################
'''
	open both graphs
'''
ppdb_graph  = label_adv(split_comma(open(ccb_graph  ,'r').read().split('\n')))
ngram_graph = label_adv(split_comma(open(ngram_graph,'r').read().split('\n')))
combo_graph = ppdb_graph + ngram_graph

'''
	open all-words for ranking
'''
word_all = open(word_all, 'r').read().split('===')[1:-1]
word_all = [rs.split('\n') for rs in word_all if rs.split('\n')]
word_all = [(rs[0],rs[1:-1]) for rs in word_all]
word_all = dict((key,[r.split(', ') for r in val]) for key,val in word_all)

############################################################
'''
	save probs
'''
words      = join(join(ws for _,ws in word_all.iteritems()))
name       = 'probs-ppdb-graph'
probs      = probs_both(deploy_out, name, words, ppdb_graph)

############################################################

if True:

	gold  = [ws for _,ws in word_all.iteritems()][0]
	results = {'all, words': ilp(probs, gold)}

	out = {'ranking'  : results
           ,'tau'     : 0.0
           ,'|tau|'   : 0.0
           ,'pairwise': 0.0}

	save(out, deploy_out, 'score-both-gold-all-ppdb-graph')

