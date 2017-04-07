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
wt_path = PATH['inputs']['graph-wt-by-edge']
log_dir = PATH['directories']['log']
out_dir = os.path.join(PATH['directories']['results'],'april')
ppr_dir = os.path.join(PATH['directories']['input'],'ppr-by-ppdb')


############################################################

edges, words = load_as_list(gr_path)

G_ppdb, _  = load_as_digraph( gr_path, wt_path )


def check(alpha, words):

	bad = []

	for s in words:
		name = s + '-' + str(alpha) + '.pkl'
		path = os.path.join(ppr_dir,name)

		if not os.path.exists(path):
			bad.append(s)

	return bad


personalized_page_rank( gr_path
                      , wt_path
                      , ppr_dir
                      , log_dir
                      , 0.7)
                      # , refresh = True
                      # , debug = False)

# bad  = check(alpha,words)

# for w in bad:

# 	personal = {w : 0 for w in words}
# 	personal[w] = 1.0

# 	ppr = nx.pagerank(G_ppdb, personalization = personal, alpha = alpha)

# 	with open(os.path.join(ppr_dir, w + '-' + str(alpha) + '.pkl'), 'wb') as h:
# 		pickle.dump(ppr, h)



gold = [[w] for w in ['good', 'great', 'excellent']]


'''
	problem right now:
			the nx.pagerank were run w/o actual constant
			change, so they're all wrong
'''
# pprs1 = run_ppr(ppr_dir, gold, 0.9)
# pprs2 = run_ppr(ppr_dir, gold, 0.8)
# pprs3 = run_ppr(ppr_dir, gold, 0.7)
# pprs4 = run_ppr(ppr_dir, gold, 0.5)   # ok
# pprs5 = run_ppr(ppr_dir, gold, 0.25)  # ok
# pprs6 = run_ppr(ppr_dir, gold, 0.1)   # ok

############################################################
'''
	@Use: compute ppr for `gold` set at restart 
	     constant `alpha` using files from
	     `ppr_dir`
'''
def run_ppr(ppr_dir, gold, alpha):

	words = join(gold)
	pprs  = { s : {t : 0 for t in words if t != s} \
	        for s in words}

	for src, tgts in pprs.iteritems():
		ppr_src = ppr_wrt(ppr_dir, src, alpha)
		for t in tgts: tgts[t] = ppr_src[t]

	return pprs

'''
	@Use: load ppr with respect to words s at 
	      alpha from directory ppr_dir
'''
def ppr_wrt(ppr_dir,s,alpha):
	
	name = s + '-' + str(alpha) + '.pkl'
	path = os.path.join(ppr_dir,name)

	if os.path.exists(path):
		return pickle.load(open(path,'rb'))
	else:
		raise NameError('No path found for ' + path)












