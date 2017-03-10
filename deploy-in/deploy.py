############################################################
# Module  : pairwise score
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
gold_all    = os.path.join(root, 'inputs/testset-all-words.txt'     )

'''
	open both graphs
'''
ppdb_graph  = label_adv(split_comma(open(ppdb_graph ,'r' ).read().split('\n')))
ngram_graph = label_adv(split_comma(open(ngram_graph,'r' ).read().split('\n')))
combo_graph = ppdb_graph + ngram_graph

'''
	open all-gold
'''
gold_all = open(gold_all, 'r').read().split('===')[1:-1]
gold_all = [rs.split('\n') for rs in gold_all if rs.split('\n')]
gold_all = [(rs[0],rs[1:-1]) for rs in gold_all]
gold_all = dict((key,[r.split(', ') for r in val]) for key,val in gold_all)


############################################################


words = set(join(join(ws for _,ws in gold_all.iteritems())))
pairs = [(u,v) for u in words for v in words if u != v]
name  = 'deploy-all' 

save_score_both(deploy_out, name, pairs, combo_graph)


