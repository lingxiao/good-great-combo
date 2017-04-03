############################################################
# Module  : A series of measures on the graph for experiments
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
droot   = os.path.join(PATH['directories']['deploy'], 'wt-edge')
dedges  = os.path.join(droot, 'edges'  )  
doutput = os.path.join(droot, 'outputs')
gr_path = PATH['assets']['graph']

'''
	@Use: split edges into chunks to compute
	      weight on remote 
'''
batch = 44

save_weighted_edge( gr_path
	              , os.path.join(dedges, 'edge-' + str(batch) + '.txt')
	              , os.path.join(doutput, 'edge-' + str(batch) + '.txt')
	              , edge_by_edge_count)
