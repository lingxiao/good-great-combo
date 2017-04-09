############################################################
# Module  : compute ppr
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
_root          = os.path.join(PATH['directories']['deploy'], 'ppr')
_neigh_out_dir = os.path.join(_root, 'neigh-outputs')
_brad_out_dir  = os.path.join(_root, 'bradley-outputs')

log_dir = PATH['directories']['log']
gr_path = PATH['assets']['graph']

'''
	edge weight path depend on the metric for the edges
'''
wt_dir_neigh   = os.path.join(PATH['directories']['deploy']
	            , 'edge-wt-neigh/outputs')

wt_dir_bradley = os.path.join(PATH['directories']['deploy']
	            , 'edge-wt-bradley-terry/outputs')


alpha = 0.1

personalized_page_rank( gr_path
	                  , wt_dir_neigh
	                  , _neigh_out_dir
	                  , log_dir
	                  , alpha )

personalized_page_rank( gr_path
	                  , wt_dir_bradley
	                  , _brad_out_dir
	                  , log_dir
	                  , alpha )

