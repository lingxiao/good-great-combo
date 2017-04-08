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



'''
	@Use: assert all ppr probs for all words have been computed
'''
def assert_all_ppr(ppr_dir, gr_path, alpha):
	
	_, words = load_as_list(gr_path)

	bad = []

	for s in words:
		name = s + '-' + str(alpha) + '.pkl'
		path = os.path.join(ppr_dir,name)

		if not os.path.exists(path):
			bad.append(s)

	if bad:
		print('\n>> !!ERROR: missing ' + str(len(bad)) + ' words for ' + str(alpha))
	else:
		print('\n>> found ppr for all words at ' + str(alpha))



alphas = [0.9,0.8,0.7,0.5,0.25,0.1,0.01]

# for a in alphas:
	# personalized_page_rank(gr_path, wt_path, out_dir, log_dir, a)

for a in alphas:
	assert_all_ppr(out_dir, gr_path, a)







