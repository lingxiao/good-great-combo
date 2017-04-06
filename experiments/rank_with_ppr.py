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

gr_path = PATH['assets']['graph']
wt_path = PATH['inputs']['graph-wt-by-edge']
out_dir = PATH['inputs']['ppr-by-ppdb']
log_dir = PATH['directories']['log']











