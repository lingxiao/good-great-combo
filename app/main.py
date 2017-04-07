# ############################################################
# # Module  : Applicaton Main
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import datetime

'''
	top level function to run through entire application
'''
def run_main():

	gr_path = PATH['assets']['graph']
	wt_path = PATH['inputs']['graph-wt-by-edge']
	out_dir = PATH['inputs']['ppr-by-ppdb']
	log_dir = PATH['directories']['log']

	'''
		compute all personalized page_rank
	'''
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.90)
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.80)
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.70)
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.50)
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.25)
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.10)
	personalized_page_rank(gr_path, wt_path, out_dir, log_dir, 0.01)

