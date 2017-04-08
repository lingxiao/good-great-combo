############################################################
# Module  : prepare training data for all experiments
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


############################################################
'''
	read test-set
'''
ccb    = read_gold(PATH['assets']['ccb'])
bansal = read_gold(PATH['assets']['bansal'])

'''
	paths
'''
gr_path  = PATH['assets']['graph']
wt_path  = PATH['inputs']['graph-wt-by-edge']
ppr_path = PATH['inputs']['ppr-by-ppdb']
log_dir  = PATH['directories']['input']


############################################################
'''
	construct graph
'''
G = Graph(gr_path, wt_path, ppr_path)







