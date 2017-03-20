# ############################################################
# # Module  : Applicaton Main
# # Date    : December 22nd
# # Author  : Xiao Ling
# ############################################################

import os
import datetime

from ilp_scripts import * 
from prelude import *

############################################################
'''
	Paths
'''
root        = os.getcwd()
test_dir    = os.path.join(root, 'inputs/testset')
probs_dir   = os.path.join(root, 'inputs/probs'  )
output_dir  = os.path.join(root, 'outputs/march' )

cluster_1   = os.path.join(test_dir, 'cluster100.adj-adj.k25.txt' )
cluster_2   = os.path.join(test_dir, 'cluster500.adj-adj.k125.txt')
gold_moh_sm = os.path.join(test_dir, 'testset-bansal-sm.txt'      )
gold_moh    = os.path.join(test_dir, 'testset-bansal.txt'         )
gold_ccb    = os.path.join(test_dir, 'testset-ccb.txt'            )

############################################################
'''
	construct or open probs table
'''
# to_probs_table(refresh=True)

'''
	open clusters
'''
cluster1 = read_gold(cluster_1)
cluster2 = read_gold(cluster_2)

moh      = read_gold(gold_moh)
moh_sm   = read_gold(gold_moh_sm)
ccb      = read_gold(gold_ccb)

############################################################
'''
	run ilp on all clusters from anne

	where you left off: make sure what you have as
	an ilp works on chris's and mohit's data
'''

def run_experiment(output_dir, probs):

	print ('\n>> ranking all clusters ...')
	rmoh      = ilp(probs, moh     )
	rmoh_sm   = ilp(probs, moh_sm  )
	rccb      = ilp(probs, ccb     )
	rcluster1 = ilp(probs, cluster1)
	rcluster2 = ilp(probs, cluster2)

	print ('\n>> saving all clusters ...')

	save_results(rmoh     , output_dir, 'moh'                    )
	save_results(rmoh_sm  , output_dir, 'moh-small'              )
	save_results(rccb     , output_dir, 'ccb'                    )

	save_ranking(rcluster1, output_dir, 'cluster100.adj-adj.k25')
	save_ranking(rcluster2, output_dir, 'cluster500.adj-adj.k125'    )

if True:
	ngram_old_ppdb_probs = open_probs_table(os.path.join(probs_dir, 'probs-ngram-old-ppdb.txt'))
	run_experiment(os.path.join(output_dir, 'ngram-old-ppdb'), ngram_old_ppdb_probs)

if True:
	ngram_ppdb_probs = open_probs_table(os.path.join(probs_dir, 'probs-ngram-ppdb.txt'))
	run_experiment(os.path.join(output_dir, 'ngram-ppdb'), ngram_ppdb_probs    )

if True:
	ngram_ppdb_and_probs = open_probs_table(os.path.join(probs_dir, 'probs-ngram-ppdb-and.txt'))
	run_experiment(os.path.join(output_dir, 'ngram-ppdb-and'), ngram_ppdb_and_probs)

if True:
	ngram_ppdb_or_probs = open_probs_table(os.path.join(probs_dir, 'probs-ngram-ppdb-or.txt'))
	run_experiment(os.path.join(output_dir, 'ngram-ppdb-or'), ngram_ppdb_or_probs )

