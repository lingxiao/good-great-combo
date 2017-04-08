############################################################
# Module  : compute edge weight where 
#           w(s -> t) =   | s -> t | 
#                       -------------------
#                      	 sum_x  | s -> x|
# 
# Date    : April 2nd, 2017
# Author  : Xiao Ling
############################################################

import os
from utils   import *
from scripts import *
from app.config import PATH

############################################################
'''
	paths
'''
_root       = os.path.join(PATH['directories']['deploy'], 'edge-wt-adjacency')
_edge_dir   = os.path.join(_root, 'edges')
_output_dir = os.path.join(_root, 'outputs')
gr_path     = PATH['assets']['graph']

############################################################

batch = 39

edge_paths       = [os.path.join(_edge_dir,p) for p in os.listdir(_edge_dir)]
unique_edge_path = edge_paths[batch]
out_path         = os.path.join(_output_dir, 'edge-' + str(batch) + '.txt')

weight_by_neigh(gr_path, unique_edge_path, out_path)
