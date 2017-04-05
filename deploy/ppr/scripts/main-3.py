############################################################
# Module  : A series of measures on the graph for experiments
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os

from utils   import *
from scripts import *
from app.config import PATH

import networkx as nx

############################################################
'''
	paths
'''
gr_path = PATH['assets']['graph']
wt_path = PATH['inputs']['graph-wt-by-edge']
out_dir = PATH['inputs']['ppr-by-ppdb']
log_dir = PATH['directories']['log']



personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.50)
