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
wt_path = PATH['inputs']['graph-wt-by-edge']
log_dir = PATH['directories']['log']
out_dir = os.path.join(PATH['directories']['results'],'april')
ppr_dir = os.path.join(PATH['directories']['input'],'ppr-by-ppdb')


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


############################################################

# G_ppdb, words = load_as_digraph( gr_path, wt_path )
# alphas = [0.9,0.8,0.7,0.5,0.25,0.1,0.01]


# alpha  = 0.9
# pprs   = run_ppr(ppr_dir, ccb[3], alpha)











