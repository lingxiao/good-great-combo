############################################################
# Module  : Naive implementation
# Date    : January 28th, 2017
# Author  : Xiao Ling, merle
############################################################

import os

from app import *
from scripts import *
from prelude import *

############################################################
'''
	PATHS
'''
root        = os.getcwd()
deploy_in   = os.path.join(root, 'deploy-in' )
deploy_out  = os.path.join(root, 'deploy-out')
ppdb_graph  = os.path.join(root, 'inputs/raw/all_edges.txt'  )
ngram_graph = os.path.join(root, 'inputs/raw/ngram-graph.txt')


'''
	open both graphs
'''
ppdb_graph  = label_adv(split_comma(open(ppdb_graph ,'r' ).read().split('\n')))
ngram_graph = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))
combo_graph = ppdb_graph + ngram_graph


############################################################

num   = 10
words = os.path.join(deploy_in, 'deploy' + str(num) + '.txt')
pairs = [w.split(' ') for w in open(words,'r').read().split('\n') if w.split(' ')][0:-1]
name  = 'deploy' + str(num) 

save_score_both(deploy_out, name, pairs, combo_graph)


