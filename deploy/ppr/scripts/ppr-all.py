############################################################
# Module  : run ppr at different constants
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

G_ppdb, words  = load_as_digraph( gr_path, wt_path )

personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.90)
personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.80)
personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.70)
personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.50)
personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.25)
personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.10)
personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.01)
