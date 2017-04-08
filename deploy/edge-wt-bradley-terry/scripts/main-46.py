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
_root       = os.path.join(PATH['directories']['deploy'], 'edge-wt-bradley-terry')
_edge_dir   = os.path.join(_root, 'edges')
_output_dir = os.path.join(_root, 'outputs')
gr_path     = PATH['assets']['graph']

############################################################

batch = 46

unique_edge_path = os.path.join(_edge_dir, 'edge-' + str(batch) + '.txt')
out_path         = os.path.join(_output_dir, 'edge-' + str(batch) + '.txt')

weight_by_bradly_terry(gr_path, unique_edge_path, out_path)
