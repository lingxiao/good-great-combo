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
output_dir  = os.path.join(root, 'outputs/'      )

cluster_1   = os.path.join(test_dir, 'cluster100.adj-adj.k25.txt' )
cluster_2   = os.path.join(test_dir, 'cluster500.adj-adj.k125.txt')
gold_moh_sm = os.path.join(test_dir, 'testset-bansal-sm.txt'      )
gold_moh    = os.path.join(test_dir, 'testset-bansal.txt'         )
gold_ccb    = os.path.join(test_dir, 'testset-ccb.txt'            )

############################################################
'''
	construct or open probs table
'''
to_probs_table(refresh=True)

ngram_old_ppdb_probs = open_probs_table(os.path.join(probs_dir, 'ngram-old-ppdb.txt'))
ngram_ppdb_probs     = open_probs_table(os.path.join(probs_dir, 'probs-ngram-ppdb.txt'))
ngram_ppdb_and_probs = open_probs_table(os.path.join(probs_dir, 'probs-ngram-ppdb-and.txt'))
ngram_ppdb_or_probs  = open_probs_table(os.path.join(probs_dir, 'probs-ngram-ppdb-or.txt'))

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

def run_experiment(output_dir, stem, graph):

	print ('\n>> ranking all clusters ...')
	rmoh      = ilp(graph, moh     )
	rmoh_sm   = ilp(graph, moh_sm  )
	rccb      = ilp(graph, ccb     )
	rcluster1 = ilp(graph, cluster1)
	rcluster2 = ilp(graph, cluster2)

	print ('\n>> saving all clusters ...')
	save_results(rmoh     , output_dir, stem + 'moh'                    )
	save_results(rmoh_sm  , output_dir, stem + 'moh-small'              )
	save_results(ccb      , output_dir, stem + 'ccb'                    )
	save_results(rcluster1, output_dir, stem + 'cluster100.adj-adj.k25' )
	save_results(rcluster2, output_dir, stem + 'cluster500.adj-adj.k125')

run_experiment(output_dir, 'ngram_old_ppdb'  , ngram_old_ppdb_probs)
run_experiment(output_dir, 'ngram_ppdb'      , ngram_ppdb_probs    )
run_experiment(output_dir, 'ngram_ppdb_and'  , ngram_ppdb_and_probs)
run_experiment(output_dir, 'ngram_ppdb_or'   , ngram_ppdb_or_probs )



